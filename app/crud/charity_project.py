from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import BaseCRUD
from app.models.charity_project import CharityProject


class CRUDCharityProject(BaseCRUD):

    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ):
        charity_project = await session.scalar(
            select(CharityProject).where(
                CharityProject.name == charity_project_name
            )
        )
        return charity_project

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ):
        seconds_to_complete = (
            (func.julianday(CharityProject.close_date) -
             func.julianday(CharityProject.create_date)) * 24 * 60 * 60)
        stmt = (
            select([
                CharityProject.name,
                CharityProject.description,
                seconds_to_complete.label('seconds_to_complete')
            ]).where(CharityProject.fully_invested)
              .order_by('seconds_to_complete')
        )
        charity_projects = await session.execute(stmt)
        return charity_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
