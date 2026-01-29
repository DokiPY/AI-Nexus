from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import func, case

from app.models.user import User
from app.models.workflow import ChatLog, Workflow
from app.models.company import Company


class StatisticsService:
    """数据统计服务"""
    
    @staticmethod
    def get_overview(db: Session) -> dict:
        """获取核心指标"""
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        
        total_messages = db.query(func.count(ChatLog.id)).filter(
            ChatLog.role == "user",
            ChatLog.is_deleted == False
        ).scalar() or 0
        
        active_users = db.query(func.count(func.distinct(ChatLog.user_id))).filter(
            ChatLog.is_deleted == False
        ).scalar() or 0
        
        avg_response_time = db.query(func.avg(ChatLog.response_time_ms)).filter(
            ChatLog.role == "ai",
            ChatLog.response_time_ms.isnot(None),
            ChatLog.is_deleted == False
        ).scalar() or 0
        
        today_messages = db.query(func.count(ChatLog.id)).filter(
            ChatLog.role == "user",
            ChatLog.created_at >= today_start,
            ChatLog.is_deleted == False
        ).scalar() or 0
        
        return {
            "total_messages": total_messages,
            "active_users": active_users,
            "avg_response_time": round(avg_response_time, 2),
            "today_messages": today_messages
        }
    
    @staticmethod
    def get_chat_trend(db: Session, days: int = 7) -> list:
        """获取对话趋势"""
        now = datetime.utcnow()
        start_date = now - timedelta(days=days)
        
        results = db.query(
            func.date(ChatLog.created_at).label('date'),
            func.count(case((ChatLog.role == 'user', 1))).label('user_count'),
            func.count(case((ChatLog.role == 'ai', 1))).label('ai_count')
        ).filter(
            ChatLog.created_at >= start_date,
            ChatLog.is_deleted == False
        ).group_by(func.date(ChatLog.created_at)).order_by(func.date(ChatLog.created_at)).all()
        
        return [{
            "date": r.date.isoformat(),
            "user_messages": r.user_count,
            "ai_messages": r.ai_count
        } for r in results]
    
    @staticmethod
    def get_workflow_ranking(db: Session, limit: int = 10) -> list:
        """工作流使用排行"""
        results = db.query(
            Workflow.id,
            Workflow.name,
            Workflow.icon,
            func.count(ChatLog.id).label('usage_count')
        ).join(ChatLog, ChatLog.workflow_id == Workflow.id).filter(
            ChatLog.is_deleted == False
        ).group_by(Workflow.id, Workflow.name, Workflow.icon).order_by(
            func.count(ChatLog.id).desc()
        ).limit(limit).all()
        
        return [{
            "workflow_id": r.id,
            "workflow_name": r.name,
            "icon": r.icon,
            "usage_count": r.usage_count
        } for r in results]
    
    @staticmethod
    def get_company_distribution(db: Session) -> list:
        """公司使用分布"""
        results = db.query(
            Company.name,
            func.count(ChatLog.id).label('message_count')
        ).join(User, User.company_id == Company.id).join(
            ChatLog, ChatLog.user_id == User.id
        ).filter(
            ChatLog.is_deleted == False
        ).group_by(Company.name).order_by(
            func.count(ChatLog.id).desc()
        ).all()
        
        return [{
            "company_name": r.name,
            "message_count": r.message_count
        } for r in results]

    @staticmethod
    def get_company_user_activity(db: Session, days: int = 7, limit: int = 20) -> list:
        """公司-员工活跃度（按用户消息量排行）"""
        now = datetime.utcnow()
        start_date = now - timedelta(days=days)

        results = db.query(
            Company.id.label("company_id"),
            Company.name.label("company_name"),
            User.id.label("user_id"),
            User.username.label("username"),
            func.count(ChatLog.id).label("message_count"),
            func.max(ChatLog.created_at).label("last_active_at"),
        ).join(
            User, User.company_id == Company.id
        ).join(
            ChatLog, ChatLog.user_id == User.id
        ).filter(
            ChatLog.role == "user",
            ChatLog.created_at >= start_date,
            ChatLog.is_deleted == False
        ).group_by(
            Company.id, Company.name, User.id, User.username
        ).order_by(
            func.count(ChatLog.id).desc()
        ).limit(limit).all()

        return [{
            "company_id": r.company_id,
            "company_name": r.company_name,
            "user_id": str(r.user_id),
            "username": r.username,
            "message_count": r.message_count,
            "last_active_at": r.last_active_at.isoformat() if r.last_active_at else None,
        } for r in results]
    
    @staticmethod
    def get_response_time_distribution(db: Session) -> list:
        """响应时间分布"""
        results = db.query(
            case(
                (ChatLog.response_time_ms < 1000, '<1s'),
                (ChatLog.response_time_ms < 3000, '1-3s'),
                (ChatLog.response_time_ms < 5000, '3-5s'),
                else_='>5s'
            ).label('range'),
            func.count(ChatLog.id).label('count')
        ).filter(
            ChatLog.role == 'ai',
            ChatLog.response_time_ms.isnot(None),
            ChatLog.is_deleted == False
        ).group_by('range').all()
        
        return [{
            "range": r.range,
            "count": r.count
        } for r in results]

    @staticmethod
    def get_response_time_by_workflow(db: Session, days: int = 7, limit: int = 10) -> list:
        """工作流响应耗时排行（基于 AI 回复的 response_time_ms）"""
        now = datetime.utcnow()
        start_date = now - timedelta(days=days)

        results = db.query(
            Workflow.id.label("workflow_id"),
            Workflow.name.label("workflow_name"),
            func.count(ChatLog.id).label("count"),
            func.avg(ChatLog.response_time_ms).label("avg_response_time_ms"),
            func.max(ChatLog.response_time_ms).label("max_response_time_ms"),
        ).join(
            ChatLog, ChatLog.workflow_id == Workflow.id
        ).filter(
            ChatLog.role == "ai",
            ChatLog.response_time_ms.isnot(None),
            ChatLog.created_at >= start_date,
            ChatLog.is_deleted == False
        ).group_by(
            Workflow.id, Workflow.name
        ).order_by(
            func.avg(ChatLog.response_time_ms).desc()
        ).limit(limit).all()

        return [{
            "workflow_id": r.workflow_id,
            "workflow_name": r.workflow_name,
            "count": r.count,
            "avg_response_time_ms": round(float(r.avg_response_time_ms or 0), 2),
            "max_response_time_ms": int(r.max_response_time_ms or 0),
        } for r in results]
    
    @staticmethod
    def get_hourly_heatmap(db: Session) -> list:
        """时段热力图"""
        results = db.query(
            func.extract('dow', ChatLog.created_at).label('day_of_week'),
            func.extract('hour', ChatLog.created_at).label('hour'),
            func.count(ChatLog.id).label('count')
        ).filter(
            ChatLog.is_deleted == False
        ).group_by('day_of_week', 'hour').all()
        
        return [{
            "day": int(r.day_of_week),
            "hour": int(r.hour),
            "count": r.count
        } for r in results]
    
    @staticmethod
    def get_recent_chats(db: Session, page: int = 1, page_size: int = 20) -> dict:
        """最近对话记录"""
        offset = (page - 1) * page_size
        
        results = db.query(
            ChatLog.id,
            ChatLog.role,
            ChatLog.message,
            ChatLog.response_time_ms,
            ChatLog.created_at,
            User.username,
            Company.name.label('company_name'),
            Workflow.name.label('workflow_name')
        ).join(User, User.id == ChatLog.user_id).join(
            Company, Company.id == User.company_id
        ).join(Workflow, Workflow.id == ChatLog.workflow_id).filter(
            ChatLog.is_deleted == False
        ).order_by(ChatLog.created_at.desc()).limit(page_size).offset(offset).all()
        
        total = db.query(func.count(ChatLog.id)).filter(ChatLog.is_deleted == False).scalar()
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "records": [{
                "id": r.id,
                "role": r.role,
                "message": r.message[:100] + "..." if len(r.message) > 100 else r.message,
                "response_time_ms": r.response_time_ms,
                "created_at": r.created_at.isoformat(),
                "username": r.username,
                "company_name": r.company_name,
                "workflow_name": r.workflow_name
            } for r in results]
        }
