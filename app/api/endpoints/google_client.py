from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from aiogoogle import Aiogoogle

from app.crud import charity_project_crud
from app.core.google_client import get_service
from app.services.google_client import generate_report
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.api.validators import check_google_api_variables_are_set
from app.core.config import settings


router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_spreadsheet_report(
    aiogoogle_object: Aiogoogle = Depends(get_service),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперпользователей.
    Формирует отчет по закрытым благотворительным проектам.
    """
    await check_google_api_variables_are_set(settings=settings)
    projects = await charity_project_crud.get_projects_by_completion_rate(
        session=session
    )
    try:
        report_link = await generate_report(
            data=projects, aiogoogle_object=aiogoogle_object
        )
        return {'Report link': report_link}
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f'Формирование отчета завершилось с ошибкой: {e}'
        )
