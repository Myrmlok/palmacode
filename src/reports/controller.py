from typing import Optional
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from src.database.database import session_maker_async
from src.reports.models import Report


class ReportController:

    @classmethod
    async def create_report(
        cls,
        start_time: datetime,
        video_id: int,
        user_id:int
    ) -> Report:
        """Создать отчет"""
        async with session_maker_async() as session:
            try:
                report = Report(
                    start_time=start_time,
                    video_id=video_id,
                    user_id=user_id
                )
                session.add(report)
                await session.commit()
                await session.refresh(report)
                return report
            except IntegrityError:
                await session.rollback()
                raise ValueError("Ошибка при создании отчета")

    @classmethod
    async def update_report(cls, id: int, end_time: datetime) -> Optional[Report]:
        async with session_maker_async() as session:
            report = await ReportController.get_report_by_id(id)
            if not report:
                return None
            report.end_time = end_time
            await session.commit()
            await session.refresh(report)  
            return report
    
    @classmethod
    async def get_report_by_id(cls, report_id: int) -> Optional[Report]:
        """Получить отчет по ID"""
        async with session_maker_async() as session:
            query = select(Report).where(Report.id == report_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

