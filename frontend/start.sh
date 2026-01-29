WHITE='\033[1;37m'
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
LG='\033[0;37m'
NC='\033[0m'

build_args() {
  if [ ! -z "${AWS_REGION+x}" ]; then
    ARGS+=(--region $AWS_REGION)
  fi
  if [ ! -z "${AWS_ACCESS_KEY+x}" ]; then
    ARGS+=(--aws-access-key-id $AWS_ACCESS_KEY)
  fi
  if [ ! -z "${AWS_SECRET_KEY+x}" ]; then
    ARGS+=(--aws-secret-access-key $AWS_SECRET_KEY)
  fi
  if [ ! -z "${AWS_SESSION_TOKEN+x}" ]; then
    ARGS+=(--aws-session-token $AWS_SESSION_TOKEN)
  fi
  if [ ! -z "${AWS_DRS_ENDPOINT+x}" ]; then
    if [ ! -z "${AWS_DRS_ENDPOINT}" ]; then
      ARGS+=(--endpoint $AWS_DRS_ENDPOINT)
    else
      ARGS+=(--default-endpoint)
    fi
  fi
  if [ ! -z "${RECOVERY_INSTANCE_ID+x}" ]; then
    ARGS+=(--recovery-instance-id $RECOVERY_INSTANCE_ID)
  fi
  if [ ! -z "${DEVICE_MAPPING+x}" ]; then
    ARGS+=(--device-mapping $DEVICE_MAPPING)
  fi
  if [ ! -z "${NO_PROMPT+x}" ]; then
    ARGS+=(--no-prompt)
  fi
}

is_ipv4() {
    local ip=$1
    python -c "
import sys
import socket

ip = sys.argv[1]

try:
    socket.inet_pton(socket.AF_INET, ip)
    sys.exit(0)
except socket.error:
    sys.exit(1)
" "$ip"
}

is_ipv6() {
    local ip=$1
    python -c "
import sys
import socket

ip = sys.argv[1]

try:
    socket.inet_pton(socket.AF_INET6, ip)
    sys.exit(0)
except socket.error:
    sys.exit(1)
" "$ip"
}

try_to_download() {
  local url="$1"

  # Check if URL parameter is provided
  if [ -z "$url" ]; then
    echo "Usage: check_url <url>" >&2
    return 1
  fi

  TEMP_FILE=$(mktemp)
  TEMP_FILE_STDERR=$(mktemp)

  trap 'rm -f "$TEMP_FILE" "$TEMP_FILE_STDERR"' EXIT

  echo "wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 --tries=1 -O \"$TEMP_FILE\" \"$url\" " >> /tmp/links

  wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 --tries=1 -O "$TEMP_FILE" "$url" &> ${TEMP_FILE_STDERR}
  if [ $? -eq 0 ]; then
    return 0
  fi
  cat "$TEMP_FILE_STDERR"
  return 1
}

can_download_file() {
  try_to_download $MANIFEST_HASH_URL
  if [ $? -eq 0 ]; then
    return 0
  fi
  try_to_download $MANIFEST_DUALSTACK_HASH_URL
  if [ $? -eq 0 ]; then
    return 0
  fi
  return 1
}

check_hashes() {
  if [ $(sha512sum /home/ec2-user/failback_assets.tar.gz | awk {'print $1'}) != $(cat /home/ec2-user/failback_assets.tar.gz.sha512) ]; then
    echo -e "${RED}Failed to validate Failback Client executable, wrong sha512 hash!${NC}"
    exit 1
  fi
}

check_if_DHCP_worked() {
  if can_download_file; then
    return 0
  else
    return 1
  fi
}

collect_asset_info() {
  while [ -z $ASSETS_INFO ]; do
    while [ -z $AWS_REGION ]; do
      echo -e "${WHITE}Enter AWS region to fail back from: ${NC}"
      read -r AWS_REGION
    done
    ASSETS_ENCODED="eyJpbnN0YWxsZXJfYWNjb3VudF9hcC1zb3V0aC0xIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9hcC1zb3V0aC0xIjogIjA4ODgxOTU0NDUxNyIsICJhcC1zb3V0aC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1hcC1zb3V0aC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1hcC1zb3V0aC0xIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfYXAtbm9ydGhlYXN0LTIiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2FwLW5vcnRoZWFzdC0yIjogIjA4ODgxOTU0NDUxNyIsICJhcC1ub3J0aGVhc3QtMiI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktYXAtbm9ydGhlYXN0LTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWFwLW5vcnRoZWFzdC0yIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfYXAtZWFzdC0xIjogIjMzMzQ1OTYyODYzMCIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9hcC1lYXN0LTEiOiAiMzMzNDU5NjI4NjMwIiwgImFwLWVhc3QtMSI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktYXAtZWFzdC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1hcC1lYXN0LTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9ldS13ZXN0LTIiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2V1LXdlc3QtMiI6ICIwODg4MTk1NDQ1MTciLCAiZXUtd2VzdC0yIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1ldS13ZXN0LTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWV1LXdlc3QtMiIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2FwLW5vcnRoZWFzdC0zIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9hcC1ub3J0aGVhc3QtMyI6ICIwODg4MTk1NDQ1MTciLCAiYXAtbm9ydGhlYXN0LTMiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWFwLW5vcnRoZWFzdC0zIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1hcC1ub3J0aGVhc3QtMyIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X3VzLXdlc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAiaW50ZXJuYWxfaW5zdGFsbGVyX2FjY291bnRfdXMtd2VzdC0xIjogIjA4ODgxOTU0NDUxNyIsICJ1cy13ZXN0LTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LXVzLXdlc3QtMSIsICJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1oYXNoZXMtdXMtd2VzdC0xIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfY2EtY2VudHJhbC0xIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9jYS1jZW50cmFsLTEiOiAiMDg4ODE5NTQ0NTE3IiwgImNhLWNlbnRyYWwtMSI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktY2EtY2VudHJhbC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1jYS1jZW50cmFsLTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9zYS1lYXN0LTEiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X3NhLWVhc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAic2EtZWFzdC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1zYS1lYXN0LTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLXNhLWVhc3QtMSIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2V1LW5vcnRoLTEiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2V1LW5vcnRoLTEiOiAiMDg4ODE5NTQ0NTE3IiwgImV1LW5vcnRoLTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWV1LW5vcnRoLTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWV1LW5vcnRoLTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9hcC1zb3V0aGVhc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAiaW50ZXJuYWxfaW5zdGFsbGVyX2FjY291bnRfYXAtc291dGhlYXN0LTEiOiAiMDg4ODE5NTQ0NTE3IiwgImFwLXNvdXRoZWFzdC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1hcC1zb3V0aGVhc3QtMSIsICJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1oYXNoZXMtYXAtc291dGhlYXN0LTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF91cy1lYXN0LTIiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X3VzLWVhc3QtMiI6ICIwODg4MTk1NDQ1MTciLCAidXMtZWFzdC0yIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS11cy1lYXN0LTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLXVzLWVhc3QtMiIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2V1LXdlc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAiaW50ZXJuYWxfaW5zdGFsbGVyX2FjY291bnRfZXUtd2VzdC0xIjogIjA4ODgxOTU0NDUxNyIsICJldS13ZXN0LTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWV1LXdlc3QtMSIsICJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1oYXNoZXMtZXUtd2VzdC0xIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfYXAtc291dGhlYXN0LTIiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2FwLXNvdXRoZWFzdC0yIjogIjA4ODgxOTU0NDUxNyIsICJhcC1zb3V0aGVhc3QtMiI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktYXAtc291dGhlYXN0LTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWFwLXNvdXRoZWFzdC0yIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfYXAtc291dGhlYXN0LTMiOiAiMTQ5OTAyMDY2Nzg5IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2FwLXNvdXRoZWFzdC0zIjogIjE0OTkwMjA2Njc4OSIsICJhcC1zb3V0aGVhc3QtMyI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktYXAtc291dGhlYXN0LTMiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWFwLXNvdXRoZWFzdC0zIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfdXMtd2VzdC0yIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF91cy13ZXN0LTIiOiAiMDg4ODE5NTQ0NTE3IiwgInVzLXdlc3QtMiI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktdXMtd2VzdC0yIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy11cy13ZXN0LTIiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9ldS1jZW50cmFsLTEiOiAiMDg4ODE5NTQ0NTE3IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2V1LWNlbnRyYWwtMSI6ICIwODg4MTk1NDQ1MTciLCAiZXUtY2VudHJhbC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1ldS1jZW50cmFsLTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWV1LWNlbnRyYWwtMSIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2FwLW5vcnRoZWFzdC0xIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9hcC1ub3J0aGVhc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAiYXAtbm9ydGhlYXN0LTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWFwLW5vcnRoZWFzdC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1hcC1ub3J0aGVhc3QtMSIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X3VzLWVhc3QtMSI6ICIwODg4MTk1NDQ1MTciLCAiaW50ZXJuYWxfaW5zdGFsbGVyX2FjY291bnRfdXMtZWFzdC0xIjogIjA4ODgxOTU0NDUxNyIsICJ1cy1lYXN0LTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LXVzLWVhc3QtMSIsICJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1oYXNoZXMtdXMtZWFzdC0xIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfZXUtd2VzdC0zIjogIjA4ODgxOTU0NDUxNyIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9ldS13ZXN0LTMiOiAiMDg4ODE5NTQ0NTE3IiwgImV1LXdlc3QtMyI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktZXUtd2VzdC0zIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1ldS13ZXN0LTMiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9ldS1zb3V0aC0xIjogIjc0NDg5MzczOTA2MCIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9ldS1zb3V0aC0xIjogIjc0NDg5MzczOTA2MCIsICJldS1zb3V0aC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1ldS1zb3V0aC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1ldS1zb3V0aC0xIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfbWUtc291dGgtMSI6ICI3NzIyOTQwNjk0NjIiLCAiaW50ZXJuYWxfaW5zdGFsbGVyX2FjY291bnRfbWUtc291dGgtMSI6ICI3NzIyOTQwNjk0NjIiLCAibWUtc291dGgtMSI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktbWUtc291dGgtMSIsICJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1oYXNoZXMtbWUtc291dGgtMSIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2FmLXNvdXRoLTEiOiAiMTcwODk5NTU5NzQ4IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2FmLXNvdXRoLTEiOiAiMTcwODk5NTU5NzQ4IiwgImFmLXNvdXRoLTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWFmLXNvdXRoLTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWFmLXNvdXRoLTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9ldS1jZW50cmFsLTIiOiAiODY0OTIyNDcwMjY4IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2V1LWNlbnRyYWwtMiI6ICI4NjQ5MjI0NzAyNjgiLCAiZXUtY2VudHJhbC0yIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1ldS1jZW50cmFsLTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWV1LWNlbnRyYWwtMiIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X2V1LXNvdXRoLTIiOiAiMzEyMjA0MjQyMzg4IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2V1LXNvdXRoLTIiOiAiMzEyMjA0MjQyMzg4IiwgImV1LXNvdXRoLTIiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWV1LXNvdXRoLTIiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWV1LXNvdXRoLTIiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9hcC1zb3V0aC0yIjogIjUzNTA5MTU4ODA4OSIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9hcC1zb3V0aC0yIjogIjUzNTA5MTU4ODA4OSIsICJhcC1zb3V0aC0yIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1hcC1zb3V0aC0yIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1hcC1zb3V0aC0yIiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfYXAtc291dGhlYXN0LTQiOiAiMDEzNjQ3ODM4NTUyIiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X2FwLXNvdXRoZWFzdC00IjogIjAxMzY0NzgzODU1MiIsICJhcC1zb3V0aGVhc3QtNCI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktYXAtc291dGhlYXN0LTQiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLWFwLXNvdXRoZWFzdC00IiwgImxhdGVzdCJdLCAiaW5zdGFsbGVyX2FjY291bnRfaWwtY2VudHJhbC0xIjogIjA1MDU3Mzc5MDg2NSIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF9pbC1jZW50cmFsLTEiOiAiMDUwNTczNzkwODY1IiwgImlsLWNlbnRyYWwtMSI6IFsiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaWwtY2VudHJhbC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy1pbC1jZW50cmFsLTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF9tZS1jZW50cmFsLTEiOiAiNTA0MTQ0NTA2MTg4IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X21lLWNlbnRyYWwtMSI6ICI1MDQxNDQ1MDYxODgiLCAibWUtY2VudHJhbC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS1tZS1jZW50cmFsLTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLW1lLWNlbnRyYWwtMSIsICJsYXRlc3QiXSwgImluc3RhbGxlcl9hY2NvdW50X3VzLWdvdi13ZXN0LTEiOiAiMjk2MjM5MTAwMjM5IiwgImludGVybmFsX2luc3RhbGxlcl9hY2NvdW50X3VzLWdvdi13ZXN0LTEiOiAiMjk2MjM5MTAwMjM5IiwgInVzLWdvdi13ZXN0LTEiOiBbImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LXVzLWdvdi13ZXN0LTEiLCAiYXdzLWVsYXN0aWMtZGlzYXN0ZXItcmVjb3ZlcnktaGFzaGVzLXVzLWdvdi13ZXN0LTEiLCAibGF0ZXN0Il0sICJpbnN0YWxsZXJfYWNjb3VudF91cy1nb3YtZWFzdC0xIjogIjI5NjIzOTEwMDIzOSIsICJpbnRlcm5hbF9pbnN0YWxsZXJfYWNjb3VudF91cy1nb3YtZWFzdC0xIjogIjI5NjIzOTEwMDIzOSIsICJ1cy1nb3YtZWFzdC0xIjogWyJhd3MtZWxhc3RpYy1kaXNhc3Rlci1yZWNvdmVyeS11cy1nb3YtZWFzdC0xIiwgImF3cy1lbGFzdGljLWRpc2FzdGVyLXJlY292ZXJ5LWhhc2hlcy11cy1nb3YtZWFzdC0xIiwgImxhdGVzdCJdfQ=="
    INSTALLER_ACCOUNT=$(python -c "import sys, json, base64; installer_account =  json.loads(base64.b64decode('$ASSETS_ENCODED').decode())['installer_account_'+'$AWS_REGION']; print(installer_account)")
    ASSETS_INFO=$(python -c "import sys, json, base64; reg_data = json.loads(base64.b64decode('$ASSETS_ENCODED').decode())['$AWS_REGION']; print(reg_data[0] + ',' + reg_data[1] + ',' + reg_data[2])")
    if [ $? -ne 0 ]; then
      echo -e "${RED}Bad or unsupported region, please retry${NC}"
      ASSETS_INFO=""
      AWS_REGION=""
    fi
  done

  IFS=, read ASSETS_BUCKET HASHES_BUCKET KEY_PREF <<< $ASSETS_INFO
  if [ $? -ne 0 ]; then
    echo -e "${RED}Internal error parsing assets s3 info${NC}"
    exit 1
  fi

  MANIFEST_URL="https://"${ASSETS_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/manifest.json"
  MANIFEST_HASH_URL="https://"${HASHES_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/manifest.json.sha512"
  MANIFEST_DUALSTACK_URL="https://"${ASSETS_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/manifest.json"
  MANIFEST_DUALSTACK_HASH_URL="https://"${HASHES_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/manifest.json.sha512"
}

flush_ips() {
  sudo ifconfig "${tmpif}" "0.0.0.0"
  sudo ip -6 addr flush dev "${tmpif}"
}

get_ip() {
  # try to get_ip via dhclient (dhcp) once
  sudo dhclient -1
  sudo dhclient -6 -1
}

download_manifest() {
  # There is a chance that we may be downloading the manifest and hash files during their update, which is not an atomic operation.
  # Therefore, we need to wait until the files are updated.
  timeout=60
  start_time=$(date +%s)

  while true; do
    TEMP_FILE=$(mktemp)
    wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 -O $TEMP_FILE "$MANIFEST_URL"
    MANIFEST_HASH_CALC=$(sha512sum $TEMP_FILE | awk '{{print $1}}')
    MANIFEST=$(<"$TEMP_FILE")
    rm $TEMP_FILE
    MANIFEST_HASH=$(wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 -O - "$MANIFEST_HASH_URL")

    [[ $MANIFEST_HASH_CALC == $MANIFEST_HASH ]] && break

    TEMP_FILE=$(mktemp)
    wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 -O $TEMP_FILE "$MANIFEST_DUALSTACK_URL"
    MANIFEST_HASH_CALC=$(sha512sum $TEMP_FILE | awk '{{print $1}}')
    MANIFEST=$(<"$TEMP_FILE")
    rm $TEMP_FILE
    MANIFEST_HASH=$(wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 -O - "$MANIFEST_DUALSTACK_HASH_URL")

    [[ $MANIFEST_HASH_CALC == $MANIFEST_HASH ]] && break


    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))

    [ $elapsed_time -ge $timeout ] && { echo -e "${RED}ERROR: Manifest download timed out.${NC}"; exit 1; }
    sleep 5
  done

  ASSETS_VERSION=$(python -c "import json; installer_version = json.loads('''$MANIFEST''')['installerVersion']; print(installer_version)")

  [[ -z $ASSETS_VERSION ]] && { echo -e "${RED}ERROR: Failed to retrieve assets version.${NC}"; exit 1; }

  ASSETS_KEY_PREF=$(python -c "path_parts = '''$KEY_PREF'''.split('/'); path_parts[-1] = '''$ASSETS_VERSION'''; print('/'.join(path_parts))")

  ASSETS_URL="https://"${ASSETS_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${ASSETS_KEY_PREF}"/failback_assets/failback_assets.tar.gz"
  HASH_URL="https://"${HASHES_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${ASSETS_KEY_PREF}"/failback_assets/failback_assets.tar.gz.sha512"
  ASSETS_DUALSTACK_URL="https://"${ASSETS_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${ASSETS_KEY_PREF}"/failback_assets/failback_assets.tar.gz"
  HASH_DUALSTACK_URL="https://"${HASHES_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${ASSETS_KEY_PREF}"/failback_assets/failback_assets.tar.gz.sha512"
}

setup_ipv4() {
  local interface=$1
  local ip_addr=$2
  local netmask=$3
  local gateway=$4

  if ! sudo ifconfig "${interface}" "${ip_addr}" netmask "${netmask}"; then
    echo "Error: Failed to set IP address for ${interface}."
    return 1
  fi

  if ! sudo route add default gw "${gateway}" "${interface}"; then
    echo "Error: Failed to set default gateway for ${interface}."
    return 1
  fi

  sleep 5
  echo "Successfully configured IP address and gateway for ${interface}."
}


setup_ipv6() {
  local interface=$1
  local ipv6_addr=$2
  local netmask=$3
  local gateway=$4

  echo "Flushing existing IPv6 addresses on $interface..."
  sudo ip -6 addr flush dev "$interface"
  sleep 5

  echo "Adding IPv6 address ${ipv6_addr}/${netmask} to $interface..."
  if ! sudo ip -6 addr add "${ipv6_addr}/${netmask}" dev "$interface"; then
    echo "Error: Failed to set IPv6 address for ${interface}."
    return 1
  fi
  sleep 5

  echo "Deleting existing default IPv6 routes on $interface..."
  sudo ip -6 route del default dev "$interface" 2>/dev/null || true
  sleep 5

  echo "Adding default IPv6 gateway ${gateway}..."
  if ! sudo ip -6 route add default via "$gateway" dev "$interface"; then
    echo "Error: Failed to set default IPv6 gateway for ${interface}."
    return 1
  fi

  echo "IPv6 address and gateway configured successfully on $interface."
  ip -6 addr show dev "$interface"
  ip -6 route show dev "$interface"
  sleep 5
}


setup_ips() {
  local interface=$1
  local ip_addr=$2
  local netmask=$3
  local gateway=$4

  if is_ipv4 "${ip_addr}"; then
    echo "IP Setup: requested ip (${ip_addr}) is classified as IPv4 "
    setup_ipv4 "${interface}" "${ip_addr}" "${netmask}" "${gateway}"
    return 0
  elif is_ipv6 "${ip_addr}"; then
    echo "IP Setup: requested ip (${ip_addr}) is classified as IPv6 "
    setup_ipv6 "${interface}" "${ip_addr}" "${netmask}" "${gateway}"
    return 0
  fi
  echo "IP Setup: requested ip (${ip_addr}) type couldn't be classified IPv4/IPv6. Will try to interpret it as IPv4"
  setup_ipv4 "${interface}" "${ip_addr}" "${netmask}" "${gateway}"
  return 0
}


configure_network() {
  echo "Skipping network configuration..."
  # # EXPECT TO GET VALUES FOR IPADDR, NETMASK, GATEWAY, DNS and PROXY (DNS and PROXY could be blank)
  # if [ -z "${DNS}" ]; then
  #   DNS=127.0.1.1  # default LiveCD DNS configuration
  #   DNSv6=::1
  #   echo -e "nameserver ${DNS}\nnameserver ${DNSv6}" | sudo tee /etc/resolv.conf &> /dev/null
  # else
  #   echo "nameserver ${DNS}" | sudo tee /etc/resolv.conf &> /dev/null
  # fi

  # if [ -n "${PROXY}" ]; then
  #   echo https_proxy="${PROXY}" | sudo tee -a /etc/environment &> /dev/null
  #   export https_proxy="${PROXY}"
  #   echo Defaults env_keep = "https_proxy" | sudo tee -a /etc/sudoers &> /dev/null
  # fi

  # if [ -n "${IPADDR}" ]; then
  #   sudo systemctl stop network &> /dev/null
  #   for tmpif in $(ls /sys/class/net)
  #   do
  #     if [ "${tmpif}" != 'lo' ] ; then
  #       echo trying "${tmpif}"
  #       setup_ips "${tmpif}" "${IPADDR}" "${NETMASK}" "${GATEWAY}"
  #       configure_s3_endpoint
  #       if can_download_file; then
  #         break;
  #       fi
  #       flush_ips
  #     fi
  #   done
  # else
  #   get_ip
  #   configure_s3_endpoint
  # fi
}

configure_s3_endpoint() {
  if [ -n "$S3_ENDPOINT_HOST" ]; then
    S3_ENDPOINT_IP=$(dig +short ${S3_ENDPOINT_HOST} | head -n1)

    if [ -n "$S3_ENDPOINT_IP" ]; then
      TEMP_FILE=\`mktemp\`
      echo "address=/s3."${AWS_REGION}".amazonaws.com/"${S3_ENDPOINT_IP}"" > $TEMP_FILE
      sudo chown root:root $TEMP_FILE
      sudo chmod 644 $TEMP_FILE
      sudo mv $TEMP_FILE /etc/dnsmasq.d/s3_endpoint

      TEMP_FILE=\`mktemp\`
      echo "nameserver 127.0.0.1" > $TEMP_FILE
      echo "nameserver ::1" >> $TEMP_FILE
      grep -v -E "127.0.0.1|::1" /etc/resolv.conf >> $TEMP_FILE
      sudo chown root:root $TEMP_FILE
      sudo chmod 644 $TEMP_FILE
      sudo mv $TEMP_FILE /etc/resolv.conf

      sudo systemctl restart dnsmasq

      echo -e "${GREEN}Custom s3 VPC endpoint configured${NC}"
    fi
  fi
}

prompt_for_network() {
  echo -n -e "${WHITE}Enter Static IP address ${LG}(leave empty for DHCP): ${NC}"
  read -r IPADDR
  if [ -n "${IPADDR}" ]; then
    sudo systemctl stop network &> /dev/null
    echo -n -e "${WHITE}Enter Subnet Mask: ${NC}"
    read -r NETMASK
    echo -n -e "${WHITE}Enter Default Gateway: ${NC}"
    read -r GATEWAY
  else
    sudo systemctl restart network &> /dev/null
  fi
  echo -n -e "${WHITE}Enter DNS Server IP ${LG}(leave empty if not relevant): ${NC}"
  read -r DNS
  echo -n -e "${WHITE}Enter Web Proxy ${LG}(leave empty if not relevant): ${NC}"
  read -r PROXY
}

input_s3_endpoint() {
  if [ -z ${S3_ENDPOINT+x} ]; then
    echo  -e "${WHITE}Enter a custom s3 endpoint ${LG}(leave empty if not relevant): ${NC}"
    read -r S3_ENDPOINT_HOST
  else
    S3_ENDPOINT_HOST="$S3_ENDPOINT"
  fi
}

retrieve_one_asset() {
  wget --header x-amz-expected-bucket-owner:${INSTALLER_ACCOUNT} --quiet --timeout=20 --tries=1 $1 -O /home/ec2-user/$2
  if [ $? -ne 0 ]; then
    return 1
  fi
}

retrieve_assets_legacy_url() {
  retrieve_one_asset $ASSETS_URL failback_assets.tar.gz
  retrieve_one_asset $HASH_URL failback_assets.tar.gz.sha512
}

retrieve_assets_dualstack() {
  retrieve_one_asset $ASSETS_DUALSTACK_URL failback_assets.tar.gz
  retrieve_one_asset $HASH_DUALSTACK_URL failback_assets.tar.gz.sha512
}

retrieve_assets() {
  retrieve_assets_legacy_url || (rm failback_assets.tar.gz || true && rm failback_assets.tar.gz.sha512 || true && retrieve_assets_dualstack)
  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download Failback Client assets${NC}"
    return 1
  fi
}

retrieve_failback_iso_legacy_url() {
  retrieve_one_asset $LIVECD_HASH_URL failback_client_latest.sha512
  retrieve_one_asset $LIVECD_VERSION_HASH_URL failback_client_version.sha512
}

retrieve_failback_iso_dualstack_url() {
  retrieve_one_asset $LIVECD_HASH_DUALSTACK_URL failback_client_latest.sha512
  retrieve_one_asset $LIVECD_VERSION_HASH_DUALSTACK_URL failback_client_version.sha512
}

retrieve_failback_iso() {
  retrieve_failback_iso_legacy_url || (rm failback_client_latest.sha512 || true && rm failback_client_version.sha512 || true && retrieve_failback_iso_dualstack_url)
  if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download latest Failback Client hashes${NC}"
    return 1
  fi
}

check_for_new_live_cd() {
  LIVECD_URL="https://"${ASSETS_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/failback_livecd/aws-failback-livecd-64bit.iso"
  LIVECD_HASH_URL="https://"${HASHES_BUCKET}".s3."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/failback_livecd/aws-failback-livecd-64bit.iso.sha512"
  LIVECD_VERSION_HASH_URL=$(echo $LIVECD_HASH_URL | sed s/latest/2c526b0e7180fe5419da2625e26b4141ddab1cae/)
  LIVECD_DUALSTACK_URL="https://"${ASSETS_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/failback_livecd/aws-failback-livecd-64bit.iso"
  LIVECD_HASH_DUALSTACK_URL="https://"${HASHES_BUCKET}".s3.dualstack."${AWS_REGION}".amazonaws.com/"${KEY_PREF}"/failback_livecd/aws-failback-livecd-64bit.iso.sha512"
  LIVECD_VERSION_HASH_DUALSTACK_URL=$(echo $LIVECD_HASH_DUALSTACK_URL | sed s/latest/2c526b0e7180fe5419da2625e26b4141ddab1cae/)

  retrieve_failback_iso

  diff -q /home/ec2-user/failback_client_latest.sha512 /home/ec2-user/failback_client_version.sha512
  if [ $? -ne 0 ]; then
    echo -e "${RED}WARNING: A newer version of the Failback Client ISO has been released here: ${LIVECD_URL} or ${LIVECD_DUALSTACK_URL}, please download and use the newest version"
    read -p "Press Enter to continue..."
  fi
}

start_replicator() {
  retrieve_assets
  check_hashes
  echo -e "${BLUE}Running Failback Client executable...${NC}"
  cd /home/ec2-user
  tar -xzf ./failback_assets.tar.gz
  chmod +x /home/ec2-user/jre/bin/*
  chmod +x /home/ec2-user/failback_entry
  ARGS=()
  build_args
  sudo /home/ec2-user/failback_entry "${ARGS[@]}"
  failback_exit_code=$?
  if [ $failback_exit_code -eq 0 ]; then
    livecd_device=$(blkid --label DRSFAILBACK)
    sudo eject -m $livecd_device
    sudo shutdown -r now
  elif [ $failback_exit_code -eq 1 ]; then
    echo -e "${RED}Unexpected error during failback, please see ${GREEN}failback.log.  ${NC}"
  fi
}

wait_for_dhcp_worked() {
  local ntries=10  # 10 times * 3 seconds = total 30 seconds of waiting for DHCP
  while true; do
    if [ $ntries = 0 ]; then
      return 1
    else
      sleep 3
      (( ntries-- ));
      # shellcheck disable=SC2009
      if ps -A | grep -q dhclient; then
        sleep 1
        if check_if_DHCP_worked; then
          return 0;
        fi
      fi
    fi
  done
}

MEM=$(grep MemTotal /proc/meminfo | awk '/[0-9]/ {print $2}')
if [ "$MEM" -lt "3800000" ]; then
    echo "Running the failback requires at least 4GiB of RAM"
    exit 1
fi

collect_asset_info

# 注释掉网络配置检查和循环，直接跳过
input_s3_endpoint
# if [ "$CONFIG_NETWORK" == 1 ]; then
#   # we are manually configuring network. Check all relevant values exist
#   if [ -n "$IPADDR" ] && [ -n "$NETMASK" ] && [ -n "$GATEWAY" ] && [ -n "$DNS" ]; then
#     input_s3_endpoint
#     configure_network
#   else
#     # values are missing, and we are using CONFIG_NETWORK, so display error and exit
#     echo -e "${RED}ERROR: Needed data is missing in order to set up the network. Please check your network configuration ${NC}"
#     exit 1
#   fi
# else
#   if ! check_if_DHCP_worked; then
#     if  wait_for_dhcp_worked; then
#       sleep 1
#     else
#       while ! can_download_file; do
#         prompt_for_network
#         input_s3_endpoint
#         configure_network
#         sleep 1
#       done
#     fi
#   fi
# fi

download_manifest
check_for_new_live_cd
start_replicator
