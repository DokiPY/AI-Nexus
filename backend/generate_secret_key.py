"""
生成 JWT SECRET_KEY
"""
import secrets

def generate_secret_key():
    """生成一个安全的随机密钥"""
    return secrets.token_urlsafe(32)

if __name__ == "__main__":
    secret_key = generate_secret_key()
    print("=" * 50)
    print("生成的 SECRET_KEY:")
    print("=" * 50)
    print(secret_key)
    print("=" * 50)
    print("\n请将此密钥复制到 .env 文件中的 SECRET_KEY 配置项")
