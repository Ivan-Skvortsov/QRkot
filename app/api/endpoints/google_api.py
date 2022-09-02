from fastapi import APIRouter, Depends
from aiogoogle import Aiogoogle

from app.core.google_api import get_service
from app.services.google_api import (spreadsheets_create,
                                     spreadsheets_update_value,
                                     set_user_permissions)
from app.core.user import current_superuser

router = APIRouter()


@router.post(
    '/',
    response_model=str,
    dependencies=[Depends(current_superuser)]
)
async def get_spreadsheet_report(aiogoogle_object: Aiogoogle = Depends(get_service)):
    # TODO Эндпойнт для формирования отчёта в гугл-таблице.
    # В таблице должны быть закрытые проекты, отсортированные
    # по скорости сбора средств — от тех, что закрылись быстрее всего,
    # до тех, что долго собирали нужную сумму.
    # TODO! добавить валидацию - проверять, есть ли в .env нужные данные
    spreadsheet_id = await spreadsheets_create(aiogoogle_object)
    await set_user_permissions(spreadsheet_id=spreadsheet_id, aiogoogle_object=aiogoogle_object)
    await spreadsheets_update_value(spreadsheet_id=spreadsheet_id, data=0, aiogoogle_object=aiogoogle_object)
    return spreadsheet_id
