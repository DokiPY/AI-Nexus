"""
生成客户友好的 HTML 测试报告
"""

import json
from datetime import datetime
from pathlib import Path


def generate_html_report():
    """生成漂亮的 HTML 测试报告"""
    
    # 读取 pytest JSON 报告
    report_path = Path(__file__).parent.parent / "output" / "report.json"
    if not report_path.exists():
        print("❌ 找不到 report.json，请先运行测试")
        return
    
    with open(report_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 测试用例映射
    test_mapping = {
        # 健康检查
        "test_01_health.py::TestHealthCheck::test_root_endpoint": {
            "module": "系统健康检查",
            "api": "GET /",
            "scenario": "正常场景",
            "description": "访问根路径，验证系统是否正常运行",
            "expected": "返回 200，包含系统信息"
        },
        "test_01_health.py::TestHealthCheck::test_health_endpoint": {
            "module": "系统健康检查",
            "api": "GET /health",
            "scenario": "正常场景",
            "description": "访问健康检查接口",
            "expected": "返回 200，状态为 healthy"
        },
        
        # 认证接口
        "test_02_auth.py::TestAuthentication::test_login_success": {
            "module": "用户认证",
            "api": "POST /api/v1/auth/login",
            "scenario": "正常场景",
            "description": "使用正确的用户名和密码登录",
            "expected": "返回 200，包含用户信息和 Cookie"
        },
        "test_02_auth.py::TestAuthentication::test_login_wrong_password": {
            "module": "用户认证",
            "api": "POST /api/v1/auth/login",
            "scenario": "异常场景",
            "description": "使用错误的密码登录",
            "expected": "返回 401，提示账号或密码错误"
        },
        "test_02_auth.py::TestAuthentication::test_login_user_not_found": {
            "module": "用户认证",
            "api": "POST /api/v1/auth/login",
            "scenario": "异常场景",
            "description": "使用不存在的用户名登录",
            "expected": "返回 401，提示账号或密码错误"
        },
        "test_02_auth.py::TestAuthentication::test_login_missing_fields": {
            "module": "用户认证",
            "api": "POST /api/v1/auth/login",
            "scenario": "异常场景",
            "description": "缺少必填字段（用户名或密码）",
            "expected": "返回 422，参数验证失败"
        },
        "test_02_auth.py::TestAuthentication::test_get_current_user": {
            "module": "用户认证",
            "api": "GET /api/v1/auth/me",
            "scenario": "正常场景",
            "description": "已登录用户获取自己的信息",
            "expected": "返回 200，包含用户详细信息"
        },
        "test_02_auth.py::TestAuthentication::test_get_current_user_unauthorized": {
            "module": "用户认证",
            "api": "GET /api/v1/auth/me",
            "scenario": "异常场景",
            "description": "未登录用户尝试获取信息",
            "expected": "返回 401，提示未认证"
        },
        "test_02_auth.py::TestAuthentication::test_logout": {
            "module": "用户认证",
            "api": "POST /api/v1/auth/logout",
            "scenario": "正常场景",
            "description": "用户登出系统",
            "expected": "返回 200，清除 Cookie"
        },
        
        # 用户管理
        "test_03_users.py::TestUserManagement::test_get_users_list": {
            "module": "用户管理",
            "api": "GET /api/v1/admin/users",
            "scenario": "正常场景",
            "description": "管理员获取用户列表（分页）",
            "expected": "返回 200，包含用户列表和分页信息"
        },
        "test_03_users.py::TestUserManagement::test_get_users_with_search": {
            "module": "用户管理",
            "api": "GET /api/v1/admin/users?search=lucky",
            "scenario": "正常场景",
            "description": "管理员搜索用户（按用户名/邮箱）",
            "expected": "返回 200，包含匹配的用户"
        },
        "test_03_users.py::TestUserManagement::test_create_user_success": {
            "module": "用户管理",
            "api": "POST /api/v1/admin/users",
            "scenario": "正常场景",
            "description": "管理员创建新用户",
            "expected": "返回 201，包含新用户 ID"
        },
        "test_03_users.py::TestUserManagement::test_create_user_duplicate_username": {
            "module": "用户管理",
            "api": "POST /api/v1/admin/users",
            "scenario": "异常场景",
            "description": "创建用户时使用已存在的用户名",
            "expected": "返回 409，提示用户名已存在"
        },
        "test_03_users.py::TestUserManagement::test_create_user_invalid_email": {
            "module": "用户管理",
            "api": "POST /api/v1/admin/users",
            "scenario": "异常场景",
            "description": "创建用户时使用无效的邮箱格式",
            "expected": "返回 422，参数验证失败"
        },
        "test_03_users.py::TestUserManagement::test_get_user_by_id": {
            "module": "用户管理",
            "api": "GET /api/v1/admin/users/{user_id}",
            "scenario": "正常场景",
            "description": "管理员获取指定用户的详细信息",
            "expected": "返回 200，包含用户详情"
        },
        "test_03_users.py::TestUserManagement::test_get_user_not_found": {
            "module": "用户管理",
            "api": "GET /api/v1/admin/users/{user_id}",
            "scenario": "异常场景",
            "description": "获取不存在的用户",
            "expected": "返回 404，提示用户不存在"
        },
        "test_03_users.py::TestUserManagement::test_update_user": {
            "module": "用户管理",
            "api": "PUT /api/v1/admin/users/{user_id}",
            "scenario": "正常场景",
            "description": "管理员更新用户信息",
            "expected": "返回 200，包含更新后的用户信息"
        },
        "test_03_users.py::TestUserManagement::test_delete_user_not_found": {
            "module": "用户管理",
            "api": "DELETE /api/v1/admin/users/{user_id}",
            "scenario": "异常场景",
            "description": "删除不存在的用户",
            "expected": "返回 404，提示用户不存在"
        },
        
        # 公司管理
        "test_04_companies.py::TestCompanyManagement::test_get_companies_list": {
            "module": "公司管理",
            "api": "GET /api/v1/admin/companies",
            "scenario": "正常场景",
            "description": "管理员获取公司列表（分页）",
            "expected": "返回 200，包含公司列表和分页信息"
        },
        "test_04_companies.py::TestCompanyManagement::test_create_company_success": {
            "module": "公司管理",
            "api": "POST /api/v1/admin/companies",
            "scenario": "正常场景",
            "description": "管理员创建新公司",
            "expected": "返回 201，包含新公司 ID"
        },
        "test_04_companies.py::TestCompanyManagement::test_get_company_by_id": {
            "module": "公司管理",
            "api": "GET /api/v1/admin/companies/{company_id}",
            "scenario": "正常场景",
            "description": "管理员获取指定公司的详细信息",
            "expected": "返回 200，包含公司详情"
        },
        "test_04_companies.py::TestCompanyManagement::test_get_company_not_found": {
            "module": "公司管理",
            "api": "GET /api/v1/admin/companies/{company_id}",
            "scenario": "异常场景",
            "description": "获取不存在的公司",
            "expected": "返回 404，提示公司不存在"
        },
        
        # 工作流管理
        "test_05_workflows.py::TestWorkflowManagement::test_get_user_workflows": {
            "module": "工作流管理",
            "api": "GET /api/v1/user/workflows",
            "scenario": "正常场景",
            "description": "用户获取自己有权限的工作流列表",
            "expected": "返回 200，包含工作流列表"
        },
        "test_05_workflows.py::TestWorkflowManagement::test_get_workflow_categories": {
            "module": "工作流管理",
            "api": "GET /api/v1/user/workflows/categories",
            "scenario": "正常场景",
            "description": "用户获取工作流分类列表",
            "expected": "返回 200，包含分类信息"
        },
        "test_05_workflows.py::TestWorkflowManagement::test_get_admin_workflows": {
            "module": "工作流管理",
            "api": "GET /api/v1/admin/workflows",
            "scenario": "正常场景",
            "description": "管理员获取所有工作流列表",
            "expected": "返回 200，包含所有工作流"
        },
    }
    
    # 统计信息
    total = data['summary']['total']
    passed = data['summary'].get('passed', 0)
    failed = data['summary'].get('failed', 0)
    duration = data['duration']
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    # 按模块分组
    modules = {}
    for test in data['tests']:
        nodeid = test['nodeid']
        outcome = test['outcome']
        duration_test = test.get('call', {}).get('duration', 0)
        
        test_id = nodeid.replace('tests/', '').replace('api_test/', '')
        
        if test_id in test_mapping:
            info = test_mapping[test_id]
            module = info['module']
            
            if module not in modules:
                modules[module] = {
                    'tests': [],
                    'passed': 0,
                    'failed': 0
                }
            
            modules[module]['tests'].append({
                'api': info['api'],
                'scenario': info['scenario'],
                'description': info['description'],
                'expected': info['expected'],
                'outcome': outcome,
                'duration': duration_test
            })
            
            if outcome == 'passed':
                modules[module]['passed'] += 1
            else:
                modules[module]['failed'] += 1
    
    # 生成 HTML（使用科技深蓝配色）
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Nexus API 测试报告</title>
    <style>
        :root {{
            /* 配色方案：科技深蓝 */
            --bg-main: #0f172a;
            --bg-card: #1e293b;
            --accent: #38bdf8;
            --success: #22c55e;
            --fail: #ef4444;
            --warning: #f59e0b;
            --text-bright: #f1f5f9;
            --text-dim: #94a3b8;
            --border: rgba(255, 255, 255, 0.05);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-bright);
            padding: 30px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1300px;
            margin: 0 auto;
        }}
        
        .header {{
            padding: 40px 0;
            text-align: left;
            border-bottom: 1px solid var(--border);
            margin-bottom: 30px;
        }}
        
        .header h1 {{
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(to right, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -1px;
        }}
        
        .header .subtitle {{
            color: var(--text-dim);
            font-size: 14px;
            margin-top: 8px;
            font-family: 'JetBrains Mono', monospace;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }}
        
        .summary-card {{
            background: var(--bg-card);
            padding: 24px;
            border-radius: 16px;
            border: 1px solid var(--border);
            transition: transform 0.2s;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(56, 189, 248, 0.3);
        }}
        
        .summary-card .label {{
            font-size: 12px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
            display: block;
        }}
        
        .summary-card .value {{
            font-size: 36px;
            font-weight: 700;
            font-family: 'JetBrains Mono', sans-serif;
        }}
        
        .summary-card.passed .value {{ color: var(--success); }}
        .summary-card.failed .value {{ color: var(--fail); }}
        .summary-card.rate .value {{ color: var(--accent); }}
        .summary-card.time .value {{ color: var(--warning); }}
        
        .module {{
            background: var(--bg-card);
            border-radius: 16px;
            margin-bottom: 30px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        
        .module-header {{
            padding: 20px 24px;
            background: rgba(255, 255, 255, 0.02);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border);
        }}
        
        .module-header h2 {{
            font-size: 18px;
            font-weight: 600;
            color: var(--accent);
        }}
        
        .module-header .badge {{
            font-size: 12px;
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent);
            padding: 4px 12px;
            border-radius: 20px;
        }}
        
        .test-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .test-table th {{
            text-align: left;
            padding: 14px 24px;
            font-size: 12px;
            color: var(--text-dim);
            text-transform: uppercase;
            background: rgba(0, 0, 0, 0.1);
        }}
        
        .test-table td {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--border);
            font-size: 14px;
        }}
        
        .test-table tbody tr:hover {{
            background: rgba(255, 255, 255, 0.01);
        }}
        
        .api-badge {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent);
            background: rgba(56, 189, 248, 0.1);
            padding: 4px 8px;
            border-radius: 4px;
        }}
        
        .scenario-badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .scenario-badge.normal {{ 
            background: rgba(34, 197, 94, 0.1); 
            color: var(--success); 
        }}
        
        .scenario-badge.error {{ 
            background: rgba(239, 68, 68, 0.1); 
            color: var(--fail); 
        }}
        
        .status-badge {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }}
        
        .status-badge.passed {{
            background: rgba(34, 197, 94, 0.1);
            color: var(--success);
        }}
        
        .status-badge.failed {{
            background: rgba(239, 68, 68, 0.1);
            color: var(--fail);
        }}
        
        .duration {{
            color: var(--text-dim);
            font-family: tabular-nums, sans-serif;
            font-weight: 500;
        }}
        
        .footer {{
            margin-top: 50px;
            padding: 40px 0;
            border-top: 1px solid var(--border);
            color: var(--text-dim);
            font-size: 13px;
        }}
        
        .footer-item {{
            margin-bottom: 12px;
        }}
        
        .footer-item strong {{ 
            color: var(--text-bright); 
            margin-right: 8px;
        }}
        
        @media (max-width: 768px) {{
            body {{ padding: 15px; }}
            .header h1 {{ font-size: 24px; }}
            .summary {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI-Nexus API 测试报告</h1>
            <div class="subtitle">✨ 自动化测试流水线 • {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</div>
        </div>
        
        <div class="summary">
            <div class="summary-card passed">
                <span class="label">Passed Tests</span>
                <div class="value">{passed}</div>
            </div>
            <div class="summary-card failed">
                <span class="label">Failed Tests</span>
                <div class="value">{failed}</div>
            </div>
            <div class="summary-card rate">
                <span class="label">Success Rate</span>
                <div class="value">{pass_rate:.0f}%</div>
            </div>
            <div class="summary-card time">
                <span class="label">Total Time</span>
                <div class="value">{duration:.2f}s</div>
            </div>
        </div>
"""
    
    # 生成每个模块的测试表格
    for module_name, module_data in modules.items():
        total_tests = len(module_data['tests'])
        passed_tests = module_data['passed']
        failed_tests = module_data['failed']
        
        status_icon = "✅" if failed_tests == 0 else "⚠️"
        
        html += f"""
        <div class="module">
            <div class="module-header">
                <h2>{status_icon} {module_name}</h2>
                <div class="badge">{passed_tests} / {total_tests} Passed</div>
            </div>
            
            <table class="test-table">
                <thead>
                    <tr>
                        <th style="width: 20%">接口路径</th>
                        <th style="width: 12%">场景</th>
                        <th style="width: 35%">测试重点</th>
                        <th style="width: 25%">预期结果</th>
                        <th style="width: 10%">状态</th>
                        <th style="width: 8%">耗时</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for test in module_data['tests']:
            scenario_class = "normal" if test['scenario'] == "正常场景" else "error"
            status_class = "passed" if test['outcome'] == 'passed' else "failed"
            status_text = "PASSED" if test['outcome'] == 'passed' else "FAILED"
            
            html += f"""
                    <tr>
                        <td><span class="api-badge">{test['api']}</span></td>
                        <td><span class="scenario-badge {scenario_class}">{test['scenario']}</span></td>
                        <td>{test['description']}</td>
                        <td>{test['expected']}</td>
                        <td><span class="status-badge {status_class}">{status_text}</span></td>
                        <td><span class="duration">{test['duration']:.3f}s</span></td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
"""
    
    html += f"""
        <div class="footer">
            <div class="footer-item"><strong>测试账号:</strong> lucky / 123456 (Administrator)</div>
            <div class="footer-item"><strong>测试环境:</strong> Windows 10 | Python 3.11.9 | FastAPI</div>
            <div class="footer-item"><strong>响应规范:</strong> Unified JSON {{success, code, data}}</div>
            <div class="footer-item" style="margin-top: 20px; opacity: 0.5; text-align: center;">© 2026 AI-Nexus Intelligence Center</div>
        </div>
    </div>
</body>
</html>
"""
    
    # 写入文件
    output_path = Path(__file__).parent.parent / "output" / "CLIENT_REPORT.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 客户友好 HTML 报告已生成: {output_path}")
    
    return output_path


if __name__ == "__main__":
    generate_html_report()
