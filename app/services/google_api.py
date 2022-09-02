from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings


DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


async def spreadsheets_create(aiogoogle_object: Aiogoogle) -> str:
    """Создаёт шаблон гугл-таблицы на гугл-диске севисного аккаунта."""
    spreadsheet_service = await aiogoogle_object.discover(
        api_name='sheets', api_version='v4'
    )
    spreadsheet_body = {
        'properties': {"title": settings.spreadsheet_report_title,
                       "locale": 'ru_RU'},
        'sheets': [{'properties': {'sheetId': 0,
                                   'title': 'Отчет'}}]
    }
    response = await aiogoogle_object.as_service_account(
        spreadsheet_service.spreadsheets.create(json=spreadsheet_body)
    )
    return response.get('spreadsheetId')


async def set_user_permissions(
    spreadsheet_id: str,
    aiogoogle_object: Aiogoogle,
    user_email: str = settings.spreadsheet_user_email
) -> None:
    """
    Разрешает доступ к файлу с id = spreadsheet_id на гугл-диске
    сервисного аккаунта пользователю user_email.
    """
    drive_service = await aiogoogle_object.discover(
        api_name='drive', api_version='v3'
    )
    permissions_body = {
        'role': 'writer',
        'type': 'user',
        'emailAddress': user_email,
    }
    await aiogoogle_object.as_service_account(
        drive_service.permissions.create(
            json=permissions_body,
            fileId=spreadsheet_id,
            sendNotificationEmail=False
        )
    )


async def spreadsheets_update_value(
    spreadsheet_id: str, data: list, aiogoogle_object: Aiogoogle
) -> str:
    """Наполняет таблицу с id = spreadsheet_id данными data."""
    spreadsheet_service = await aiogoogle_object.discover(
        api_name='sheets', api_version='v4'
    )
    table_values = [
        ['Топ проектов по скорости закрытия'],
        ['Дата и время формирования отчета', datetime.now().strftime(DATETIME_FORMAT)],
        ['Название проекта', 'Время сбора', 'Описание проекта']
    ]
    for i in range(25):
        table_values.append([f'Название_{i}', i, f'Описание №{i}'])
    table_body = {
        'values': table_values,
        'majorDimension': 'ROWS'
    }
    await aiogoogle_object.as_service_account(
        spreadsheet_service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=table_body
        )
    )
    return spreadsheet_id


async def style_spreadsheets_report():
    # TODO наводим красоту
    ...
