from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from aiogoogle import Aiogoogle

from app.crud import charity_project_crud
from app.core.google_client import get_service
from app.services.google_client import (spreadsheets_create,
                                     spreadsheets_update_value,
                                     set_user_permissions)
from app.core.user import current_superuser
from app.core.db import get_async_session

router = APIRouter()


@router.post(
    '/',
    # response_model=list[dict[str, str]],
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_spreadsheet_report(
    aiogoogle_object: Aiogoogle = Depends(get_service),
    session: AsyncSession = Depends(get_async_session)
):
    # TODO Эндпойнт для формирования отчёта в гугл-таблице.
    # В таблице должны быть закрытые проекты, отсортированные
    # по скорости сбора средств — от тех, что закрылись быстрее всего,
    # до тех, что долго собирали нужную сумму.
    # TODO! добавить валидацию - проверять, есть ли в .env нужные данные
    # spreadsheet_id = await spreadsheets_create(aiogoogle_object)
    charity_projects = await charity_project_crud.get_projects_by_completion_rate(
        session=session
    )
    return 'Hello!'
