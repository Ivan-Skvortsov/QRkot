from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import charity_project_crud
from app.models import CharityProject
from app.schemas import CharityProjectUpdateSchema


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Проверяет, существует ли проект в базе."""
    charity_project = await charity_project_crud.read_single(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с указанным id не существует!'
        )
    return charity_project


async def check_charity_project_name_duplilcate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """Проверяет, существует ли в базе проект с указанным именем."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_before_delete(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """
    Првоеряет, существут ли проект в базе и были ли  в него
    инвестированы средства.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('В проект были внесены средства, не подлежит удалению!')
        )
    return charity_project


async def check_charity_project_before_update(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdateSchema,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверяте возможность редактирования проекта:
        - проект должен существовать в базе;
        - новое имя не должно дублировать существюущие в базе;
        - проект не должен быть закрыт;
        - нельзя установить сумму проекта меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=charity_project_id, session=session
    )
    if charity_project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    full_amount_update_value = charity_project_in.full_amount
    if (full_amount_update_value and
       charity_project.invested_amount > full_amount_update_value):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Нельзя установить требуемую cумму меньше уже вложенной'
        )
    name_update_value = charity_project_in.name
    await check_charity_project_name_duplilcate(
        charity_project_name=name_update_value, session=session
    )
    return charity_project
