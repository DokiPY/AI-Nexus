"""统计数据API路由"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.schemas.response import success_response
from app.services.admin.statistics.statistics_service import StatisticsService

router = APIRouter()


@router.get("/overview", summary="获取统计概览")
async def get_statistics_overview(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取核心统计指标"""
    data = StatisticsService.get_overview(db)
    return success_response(data=data)


@router.get("/trend", summary="获取对话趋势")
async def get_chat_trend(
    days: int = 7,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取最近N天的对话趋势"""
    data = StatisticsService.get_chat_trend(db, days)
    return success_response(data={"trend": data})


@router.get("/workflow-ranking", summary="工作流使用排行")
async def get_workflow_ranking(
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取工作流使用排行榜"""
    data = StatisticsService.get_workflow_ranking(db, limit)
    return success_response(data={"ranking": data})


@router.get("/company-distribution", summary="公司使用分布")
async def get_company_distribution(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取各公司的使用分布"""
    data = StatisticsService.get_company_distribution(db)
    return success_response(data={"distribution": data})


@router.get("/user-activity", summary="公司-员工活跃度排行（按用户消息量）")
async def get_user_activity(
    days: int = 7,
    limit: int = 20,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户活跃度排行"""
    data = StatisticsService.get_company_user_activity(db, days, limit)
    return success_response(data={"activity": data})


@router.get("/response-time-distribution", summary="响应时间分布")
async def get_response_time_distribution(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取响应时间分布统计"""
    data = StatisticsService.get_response_time_distribution(db)
    return success_response(data={"distribution": data})


@router.get("/response-time-by-workflow", summary="工作流响应耗时排行（平均耗时）")
async def get_response_time_by_workflow(
    days: int = 7,
    limit: int = 10,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取各工作流的平均响应时间排行"""
    data = StatisticsService.get_response_time_by_workflow(db, days, limit)
    return success_response(data={"ranking": data})


@router.get("/hourly-heatmap", summary="时段热力图")
async def get_hourly_heatmap(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取按小时统计的使用热力图数据"""
    data = StatisticsService.get_hourly_heatmap(db)
    return success_response(data={"heatmap": data})


@router.get("/recent-chats", summary="最近对话记录")
async def get_recent_chats(
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取最近的对话记录列表"""
    data = StatisticsService.get_recent_chats(db, page, page_size)
    return success_response(data=data)
