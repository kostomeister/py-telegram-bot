from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db_handler.models import Reports


async def create_report(
    db: AsyncSession,
    user_id: int,
    location: str,
    checklist: str,
    comment: str = "Все чисто",
    photo_url: str = None,
):
    report = Reports(
        user_id=user_id,
        location=location,
        checklist=checklist,
        comment=comment,
        photo_url=photo_url,
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def get_existing_reports(db: AsyncSession, user_id: int, location: str):
    result = await db.execute(
        select(Reports).filter(Reports.user_id == user_id, Reports.location == location)
    )
    reports = result.scalars().all()
    comments = [report.comment for report in reports]

    return comments
