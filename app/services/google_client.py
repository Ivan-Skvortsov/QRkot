from datetime import datetime, timedelta

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.models import CharityProject


DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'


async def spreadsheets_create(aiogoogle_object: Aiogoogle) -> str:
    """Создаёт шаблон гугл-таблицы на гугл-диске севисного аккаунта."""
    spreadsheet_service = await aiogoogle_object.discover(
        api_name='sheets', api_version='v4'
    )
    spreadsheet_body = {
        'properties': {'title': settings.spreadsheet_report_title,
                       'locale': 'ru_RU'},
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
    user_email: str = settings.email
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
    spreadsheet_id: str,
    data: list[CharityProject],
    aiogoogle_object: Aiogoogle
) -> str:
    """Наполняет таблицу с id = spreadsheet_id данными data."""
    spreadsheet_service = await aiogoogle_object.discover(
        api_name='sheets', api_version='v4'
    )
    table_values = [
        ['Отчет от:', datetime.now().strftime(DATETIME_FORMAT)],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание проекта']
    ]
    for project in data:
        project_completion_time = timedelta(
            seconds=float(project.seconds_to_complete)
        )
        table_values.append([
            str(project.name),
            str(project_completion_time),
            str(project.description)
        ])
    table_body = {
        'values': table_values,
        'majorDimension': 'ROWS'
    }
    row_count = len(table_body['values'])
    await aiogoogle_object.as_service_account(
        spreadsheet_service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{row_count}',
            valueInputOption='USER_ENTERED',
            json=table_body
        )
    )
    return spreadsheet_id


async def generate_report(
    data: list[CharityProject], aiogoogle_object: Aiogoogle
) -> str:
    """Формирует отчет и возвращает гиперссылку на него."""
    spreadsheet_id = await spreadsheets_create(aiogoogle_object)
    await spreadsheets_update_value(spreadsheet_id, data, aiogoogle_object)
    await set_user_permissions(spreadsheet_id, aiogoogle_object)
    return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
