"""
初始化管理员账户脚本
"""
import psycopg2
from getpass import getpass
from app.core.security import get_password_hash
from app.core.config import settings

def init_admin():
    print("=" * 50)
    print("AI Agent Platform - 管理员账户初始化")
    print("=" * 50)
    
    # 获取管理员信息
    company_name = input("\n请输入公司名称: ").strip()
    if not company_name:
        print("❌ 公司名称不能为空")
        return
    
    username = input("请输入管理员用户名: ").strip()
    if not username:
        print("❌ 用户名不能为空")
        return
    
    email = input("请输入管理员邮箱: ").strip()
    if not email:
        print("❌ 邮箱不能为空")
        return
    
    password = getpass("请输入管理员密码: ")
    if len(password) < 6:
        print("❌ 密码长度至少6位")
        return
    
    password_confirm = getpass("请再次输入密码: ")
    if password != password_confirm:
        print("❌ 两次密码不一致")
        return
    
    try:
        # 连接数据库
        conn = psycopg2.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD,
            database=settings.DB_NAME
        )
        cursor = conn.cursor()
        
        # 检查公司是否存在
        cursor.execute("SELECT id FROM companies WHERE name = %s", (company_name,))
        company = cursor.fetchone()
        
        if company:
            company_id = company[0]
            print(f"\n✓ 使用现有公司: {company_name} (ID: {company_id})")
        else:
            # 创建公司
            cursor.execute(
                "INSERT INTO companies (name) VALUES (%s) RETURNING id",
                (company_name,)
            )
            company_id = cursor.fetchone()[0]
            print(f"\n✓ 创建公司: {company_name} (ID: {company_id})")
        
        # 检查用户是否存在
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            print(f"❌ 用户名或邮箱已存在")
            cursor.close()
            conn.close()
            return
        
        # 创建管理员用户
        password_hash = get_password_hash(password)
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, company_id, role, is_active)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
            """,
            (username, email, password_hash, company_id, 'admin', True)
        )
        user_id = cursor.fetchone()[0]
        
        conn.commit()
        
        print(f"✓ 创建管理员用户: {username} (ID: {user_id})")
        print("\n" + "=" * 50)
        print("✅ 管理员账户创建成功！")
        print("=" * 50)
        print(f"\n登录信息:")
        print(f"  用户名: {username}")
        print(f"  邮箱: {email}")
        print(f"  公司: {company_name}")
        print(f"  角色: 管理员")
        print("\n请使用以上信息登录系统")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")

if __name__ == "__main__":
    init_admin()

