"""公司管理服务层"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.company import Company
from app.models.user import User
from app.schemas.company import CompanyCreate
from app.core.errors.exceptions import NotFoundException, ConflictException


class CompanyService:
    """公司管理服务"""
    
    @staticmethod
    def get_companies(db: Session, page: int = 1, page_size: int = 10) -> dict:
        """
        获取所有公司列表，并统计用户数（支持分页）
        
        Args:
            db: 数据库会话
            page: 页码
            page_size: 每页数量
            
        Returns:
            包含分页信息和公司列表的字典
        """
        # 查询总数
        total = db.query(Company).count()
        
        # 分页查询
        companies = db.query(
            Company,
            func.count(User.id).label('user_count')
        ).outerjoin(User, Company.id == User.company_id)\
         .group_by(Company.id)\
         .offset((page - 1) * page_size)\
         .limit(page_size)\
         .all()
        
        result = []
        for company, user_count in companies:
            company_dict = {
                'id': company.id,
                'name': company.name,
                'domain': company.domain,
                'is_active': company.is_active,
                'created_at': company.created_at.isoformat() if company.created_at else None,
                'updated_at': company.updated_at.isoformat() if company.updated_at else None,
                'user_count': user_count
            }
            result.append(company_dict)
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "companies": result
        }
    
    @staticmethod
    def create_company(db: Session, company_data: CompanyCreate) -> Company:
        """
        创建新公司
        
        Args:
            db: 数据库会话
            company_data: 公司创建数据（名称、域名等）
            
        Returns:
            创建成功的公司对象
            
        Raises:
            ConflictException: 公司名称或域名已存在
        """
        # 检查公司名是否已存在
        existing = db.query(Company).filter(Company.name == company_data.name).first()
        if existing:
            raise ConflictException("公司名称已存在")
        
        # 检查域名是否已存在
        if company_data.domain:
            existing_domain = db.query(Company).filter(Company.domain == company_data.domain).first()
            if existing_domain:
                raise ConflictException("域名已存在")
        
        db_company = Company(**company_data.dict())
        db.add(db_company)
        db.commit()
        db.refresh(db_company)
        
        return db_company
    
    @staticmethod
    def get_company_users(db: Session, company_id: int) -> list:
        """
        获取公司的所有用户
        
        Args:
            db: 数据库会话
            company_id: 公司ID
            
        Returns:
            用户列表
        """
        users = db.query(User).filter(User.company_id == company_id).all()
        
        return [{
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None
        } for user in users]
    
    @staticmethod
    def update_company(db: Session, company_id: int, company_data: CompanyCreate) -> Company:
        """
        更新公司信息
        
        Raises:
            NotFoundException: 公司不存在
            ConflictException: 公司名称或域名已存在
        """
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise NotFoundException("公司不存在")
        
        if company_data.name and company_data.name != company.name:
            existing = db.query(Company).filter(Company.name == company_data.name).first()
            if existing:
                raise ConflictException("公司名称已存在")
            company.name = company_data.name
        
        if company_data.domain and company_data.domain != company.domain:
            existing = db.query(Company).filter(Company.domain == company_data.domain).first()
            if existing:
                raise ConflictException("域名已存在")
            company.domain = company_data.domain
        
        if company_data.is_active is not None:
            company.is_active = company_data.is_active
        
        db.commit()
        db.refresh(company)
        return company
    
    @staticmethod
    def delete_company(db: Session, company_id: int) -> None:
        """
        删除公司
        
        Raises:
            NotFoundException: 公司不存在
        """
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise NotFoundException("公司不存在")
        
        db.delete(company)
        db.commit()
    
    @staticmethod
    def get_company_detail(db: Session, company_id: int) -> Company:
        """
        获取公司详情
        
        Raises:
            NotFoundException: 公司不存在
        """
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise NotFoundException("公司不存在")
        return company
