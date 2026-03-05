"""
测试运行器
运行所有测试并生成报告
"""

import subprocess
import sys
from pathlib import Path


def main():
    """运行测试并生成报告"""
    backend_dir = Path(__file__).parent.parent
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    report_json = output_dir / "report.json"

    # 使用当前 Python 解释器运行 pytest
    pytest_args = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        f"--json-report",
        f"--json-report-file={report_json}",
    ]

    print("=" * 60)
    print("🚀 开始运行 API 自动化测试")
    print("=" * 60)

    result = subprocess.run(pytest_args, cwd=str(backend_dir))

    print()
    print("=" * 60)

    # 生成 HTML 报告
    if report_json.exists():
        print("📊 正在生成 HTML 测试报告...")
        try:
            # 将 tests 目录加入 sys.path 以支持导入
            tests_dir = str(Path(__file__).parent)
            if tests_dir not in sys.path:
                sys.path.insert(0, tests_dir)
            from utils.generate_html_report import generate_html_report
            generate_html_report()
        except Exception as e:
            print(f"⚠️ HTML 报告生成失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ 未找到 JSON 报告，跳过 HTML 报告生成")

    print("=" * 60)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
