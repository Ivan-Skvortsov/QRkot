<div id="top"></div>
<div align="center">
<h1>Проект QRKot</h1>
  <h3>
    Благотворительный фонд поддержки котиков.
    <br />
  </h3>
</div>

## О проекте
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
### Проекты
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
### Пожертвования
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

### Отчет в Google Spreadsheets
В прилождении QRKot существует возможность формирования отчёта в гугл-таблице. В таблицу вносятся закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму. Для использования этого функционала, необходимо подключить к приложению <a href="https://cloud.google.com/iam/docs/service-accounts">сервисный аккаунт Google.</a>

<p align="right">(<a href="#top">наверх</a>)</p>

## Использованные технологии и пакеты
* [FastAPI](https://fastapi.tiangolo.com/)
* [FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.1/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)

<p align="right">(<a href="#top">наверх</a>)</p>

## Необходимый софт
Для развертывания проекта локально, на Вашем комьютере требуется Python вресии 3.9 и выше. <br>
Скачать дистрибутив для Вашей ОС можно на официальном сайте: https://www.python.org/downloads/

## Установка
Склонируйте проект на Ваш компьютер
   ```sh
   git clone https://github.com/Ivan-Skvortsov/cat_charity_fund.git
   ```
Перейдите в папку с проектом
   ```sh
   cd cat_charity_fund
   ```
Активируйте виртуальное окружение
   ```sh
   python3 -m venv venv
   ```
   ```sh
   source venv/bin/activate
   ```
Обновите менеджер пакетов (pip)
   ```sh
   pip3 install --upgrade pip
   ```
Установите необходимые зависимости
   ```sh
   pip3 install -r requirements.txt
   ```
Создайте файл с переменными окружения `.env`
   ```sh
   touch .env
   ```
Наполните файл следующими переменными
   ```sh
   # название проекта
   APP_TITLE=Фонд QRKot
   # описание проекта
   APP_DESCRIPTION=Благотворительный фонд поддержки котиков
   # используемая база данных
   DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
   # секретный ключ
   SECRET=kazhdyuhjk237&!@@!jhksd.f^2/
   # email первого суперпользователя
   FIRST_SUPERUSER_EMAIL=admin@admin.com
   # пароль первого суперпользователя
   FIRST_SUPERUSER_PASSWORD=admin
   
   # информация сервисного аккаунта Google (для использования функционала выгрузки отчета в spreadsheets)
   TYPE=service_account
   PROJECT_ID=some project id
   PRIVATE_KEY_ID=SomePrivatekeyId
   PRIVATE_KEY=some private key
   CLIENT_EMAIL=some client mail
   CLIENT_ID=some client id
   AUTH_URI=https://accounts.google.com/o/oauth2/auth
   TOKEN_URI=https://oauth2.googleapis.com/token
   AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
   CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/some-url
   # почта пользователя, имеюзего доступ к отчет
   EMAIL=your@mail.com
   # заголовок отчета
   SPREADSHEET_REPORT_TITLE=Отчет по закрытым проектам QRkot
   ```
<p align="right">(<a href="#top">наверх</a>)</p>

## Использование
Для запуска проекта выполните команду
```sh
uvicorn app.main:app --reload
```
Если в файле `.env` были указаны переменные `FIRST_SUPERUSER_EMAIL` и `FIRST_SUPERUSER_PASSWORD`, то при первом запуске приложения в базе данных будет создан суперпользователь с приведенными учетным данными. Вы можете воспользоваться этими данными для авторизации.

### Документация API
Документация по проекту доступна на следующих эндпойнтах:
 - `/docs` — документация в формате Swagger;
 - `/redoc` — документация в формате ReDoc.
<p align="right">(<a href="#top">наверх</a>)</p>

## Об авторе
Автор проекта: Иван Скворцов<br/><br />
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Ivan-Skvortsov/)
[![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:pprofcheg@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Profcheg)
<p align="right">(<a href="#top">наверх</a>)</p>
