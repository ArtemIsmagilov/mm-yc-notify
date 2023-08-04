# Mattermost - Yandex Calendar Интеграция

![header](imgs/header.PNG)

## Содержание

- [Задача](#задача)
- [Проблема](#проблема)
- [Решение](#решение)
- [Описание](#описание)
- [Предварительные требования](#предварительные-требования)
- [Дерево команд](#дерево-команд)
- [Команды](#команды)
- [Получить токен](#получить-токен)
- [Запуск](#запуск)
- [Как работает](#как-работает)
- [Полезные ссылки](#полезные-ссылки)
- [Вопрос-ответ](#вопрос-ответ)
- [Проблемы Яндекс Календаря](#проблемы-яндекс-календаря)
- [Будущие доработки](#будущие-доработки)
- [Благодарности](#благодарности)

## Задача

> 📝 В Яндекс Календаре назначаются встречи. Нужно как по ссылке
> [YandexCalendar(plugin)](https://github.com/LugaMuga/mattermost-yandex-calendar-plugin) <br>
> - Присылать утром список встреч на день.
> - Информировать за 10 минут до встречи, показывать ссылку на яндекс-телемост у встречи.
> - Сообщать об отменённых встречах, переносах встреч, добавленных встречах.
> - Сообщать о действиях участников встреч со мной (не подтвердили встречу, отказались от встречи и так далее).
> - Автоматически проставлять статус `📆 На втсрече`, когда на встрече.

## Проблема

> Плагин местами не работает, не правильный календарь

## Решение

- Переработка плагина (Go) https://github.com/LugaMuga/mattermost-yandex-calendar-plugin на Python
- Добавление необходимого функционала
- Исправление ошибок

## Описание

- Программа представлена в виде интеграции сервиса mattermost и яндекс календаря по протоколу CalDAV,
  а именно, ___вытягивание конференций___ из сервера.
- Доступны запросы на получение списка конференций с атрибутами в различные промежутки времени.
- Аутентификация по логину яндекса и токену яндекс приложения.
- Настройка часового пояса.
- Ежедневное уведомление в заданное время по часовому поясу пользователя.
- Уведомление о предстоящей конференции за 10 минут до начала.
- Установка статуса "📆 In a meeting" во время конференции.
- Проверка активности аккаунта.
- Проверка активности планировщика.
- Возможность удалить/обновить установленные параметры в интеграции

## Предварительные требования

- Docker Engine 24.0.5
- Python 3.11.4

## Дерево команд

    /yandex_calendar
    .
    ├── calendars
    │         ├── current
    │         ├── from_to
    │         ├── get_a_month
    │         ├── get_a_week
    │         └── today
    ├── checks
    │         ├── check_account
    │         └── check_scheduler
    ├── connections
    │         ├── connect
    │         ├── disconnect
    │         └── update
    ├── info
    └── notifications
        ├── create
        ├── delete
        └── update

## Команды

* yandex_calendar [root all commands in integration app]
    - connections [module authentication client]
        + connect [*connection* to yandex calendar, need required ***login***, ***token yandex app***,
          ***timezone*** - form command]
        + disconnect [*disconnection* account from integration - execute command]
        + update [*update* ***login***, ***token***, ***timezone*** - form command ]

    - calendars [module Yandex Calendar API for client]
        + get_a_week [get conferences *for the week* by user timezone, execute command]
        + get_a_month [get conferences *for the month* by user timezone, execute command]
        + current [get conferences on *current* day by user timezone, need `dd.mm.YYYY` - form command]
        + from_to [get conferences *from* date `dd.mm.YYYY` *to* date `dd.mm.YYYY` by user timezone,
          need start date and end date in format `dd.mm.YYYY` - form command]
        + today [get conferences for *today* by user timezone, execute command]

    - notifications [module scheduler with notifications]
        + create [create jobs with notifications every day or/and every next conference before in 10 minutes,
          need select calendar with exists conferences, select time 00:00->23:45 with interval 15 minutes(required),
          click `Notification` for every next conferences notifications(optional), click `Status` for change status
          when in a meeting]
        + update [clear user jobs(scheduler) and create all by command `create` again]
        + delete [clear user jobs(scheduler)]

    - checks [module checking info about active user]
        + check_account [*check exist user* in integration]
        + check_scheduler [*check exist notifications* for user in integration ]

    - info [help information about commands app, execute command]

## Получить токен

1. Перейти на сайт [Яндекс ID](https://id.yandex.ru/)
2. Войти или зарегистрироваться
3. Перейти в `Безопасность`
4. В самом низу `Пароли приложений`
5. Нажмите на `Календарь CalDAV` и создайте пароль
6. Для интеграции потребуется логин яндекс аккаунта и созданный ранее пароль

Или можно почитать первый шаг из https://yandex.ru/support/calendar/common/sync/sync-desktop.html

## Запуск

- Клонируем репозиторий
    ```shell
    git clone https://github.com/ArtemIsmagilov/mm-yc-notify && cd mm-yc-notify/
    ```
- Активируем виртуальное окружение
    ```shell
    python3 -m venv venv && source venv/bin/activate
    ```
- Копируем файл с переменными окружения и редактируем в зависимости от ваших общих конфигураций
    ```shell
    cp .example.env .env
    ```
- Настраиваем переменные `wsgi/settings.py`

- Настраиваем переменные `gunicorn.conf.py`

- Настраиваем `microservice/docker-compose.yml`

- Запускаем докер контейнер mattermost
    ```bash
    cd ./mm/
    sudo docker compose up
    ```

- Запускаем докер контейнер приложения
    ```bash
    сd ../microservice
    sudo docker compose up
    ```

- Устанавливаем бота в mattermost, а именно - пишем команду в любом диалоговом окне
    ```
    /app install http http://192.168.31.57:8065/manifest.json
    ```

- Теперь необходимо добавить бота в команду
  https://www.ibm.com/docs/en/z-chatops/latest?topic=platform-inviting-created-bot-your-mattermost-team

- Создать токен, предоставить права

- В файле `.env` добавить токен для приложения `MM_APP_TOKEN=example`

- Перезапустить докер контейнер
    ```bash
    sudo docker compose -f ./microservice/docker-compose.yml down
    sudo docker compose -f ./microservice/docker-compose.yml up
    ```
- При разработке, удобно запустить отдельно postgres и app
    + app
      ```bash
      cd ../
      bash run_app.sh
      ```
    + postgres
      ```bash
      cd /psql
      sudo docker compose up
      ```

## Как работает

- /yandex-calendar checks check_account
  ![checks_account](imgs/checks_account.PNG)

- /yandex-calendar connections connect
  ![connect](imgs/connect.PNG)

- /yandex-calendar calendars current [--date]
  ![current](imgs/current.PNG)

- /yandex-calendar connections disconnect
  ![disconnect](imgs/disconnect.PNG)

- /yandex-calendar calendars get_a_month <br>
  Снизу будут высвечиваться ошибки клиента и разработчика, в данном случае пользователь __не авторизовался__,
  но пытается получить список конференций за месяц.
  ![error](imgs/error.PNG)

- /yandex-calendar calendars from_to
  ![from_to](imgs/from_to.PNG)

- /yandex-calendar calendars get_a_month <br>
  В модуле `calendars` список конференция в различных интервалах будет в следующей форме
  ![get_a_month](imgs/get_a_month.PNG)

- /yandex-calendar info
  ![info](imgs/info.PNG)

- /yandex-calendar notifications create/update <br>
  Вы можете создать только один планировщик. С помощью `update` можно обновить планировщик,
  задать другие параметры для уведомлений
  ![notifications_create](imgs/notifications_create.PNG)

- /yandex-calendar notifications delete <br>
  Попытка удалить несуществующий планировщик
  ![notifications_delete](imgs/notifications_delete.PNG)

## Полезные ссылки

- Scheduling All Kinds of Recurring Jobs with Python - https://martinheinz.dev/blog/39
- 7 способов выполнения запланированных заданий с помощью Python - https://evogeek.ru/articles/250819/
- Работа с токенами на Flask - https://kirill-sklyarenko.ru/lenta/flask-api-json-web-token-1
- Кодирование секретных ключей -
  https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
- Настройка работников и потоков в gunicorn - https://stackoverflow.com/questions/38425620/gunicorn-workers-and-threads
- Mattermost Yandex Calendar Plugin (CALDav) - https://github.com/LugaMuga/mattermost-yandex-calendar-plugin
- Команды Postgresql - https://www.postgresqltutorial.com/postgresql-administration/psql-commands/
- Команды SQL - https://www.w3schools.com/sql/default.asp

## Вопрос-ответ

- Почему не шифруешь токены?

    + Изначально шифровал с помощью библиотеки cryptography по секретному через объект Fernet.
      В процессе разработки выяснил, что ни Redmine, ни Mattermost не шифруют токены. Хотя пароли хешируют - это мы
      одобряем.
      В интернете большая полемика по тому, как правильно шифровать личную информацию. Я склонился к тому, что
      нужно придерживаться политика самого сайта, где рядом создаётся интеграция. Если шифруют, то нужно тоже шифровать
      и обратно.

    + Давайте посмотрим в как токен храниться в нашей БД.
        * вы должны уже были авторизоваться в интеграции через маттермост(добавить логин, токен, часовой пояс).
        ```bash
        sudo docker exec -it microservice-db-1 bash
        ```
      Вы перешли в оболочку контейнера БД, смотрим содержимое БД
        ```bash
        su postgres
        ```
        ```bash
        psql
        ```
        ```bash
        \dt
        ```
                        List of relations
           Schema |       Name       | Type  |  Owner   
          --------+------------------+-------+----------
           public | apscheduler_jobs | table | postgres
           public | user_account     | table | postgres
          (2 rows)

        ```bash
        SELECT * FROM user_account;
        ```

           id |          user_id           |      login       |      token       |   timezone    
          ----+----------------------------+------------------+------------------+---------------
            1 | hak3jkeh67y4dd1h6q8r16gqrr | artemismagilov03 | bcxekezavhqfxaqy | Europe/Samara
          (1 row)

    + Токен у нас не зашифрован(мы ничего и не делали для этого), предыдущий метод долгий, лучше просто добавить в
      докер контейнер маттермоста adminer и посмотреть в вебе.
      ![mm](imgs/mm.PNG)

    + В маттермост тоже не зашифрован, такая же ситуация и в редмайне.

    + Почему не шифруем? Если, буквально в двух словах, то REST API токены позволяем использовать совсем малую часть
      функционала приложений. Пароли захешированы, уже хорошо. Если унесут БД все токены можно сразу же поменять.

    + https://docs.mattermost.com/developer/personal-access-tokens.html

## Проблемы Яндекс Календаря

- Отсутствие какой-либо документации, RESTAPI, туториала, инструментария от яндекса для работы с Яндекс Календарём в
  удобном формате JSON, XML. Google хорошо задокументировал работу с google календарём на python
  https://developers.google.com/calendar/api/quickstart/python?hl=ru
- Выборка текущих конференций происходит по часовому поясу клиента, если вы поменяли часовой пояс, то старые
  конференции не меняют часовой пояс, только на сайте визуально. Поэтому нужно настроить часовой пояс один раз при
  коннекте к интеграции.
- Не доступны запросы на занятость (тег freebusy, статус 504).

## Будущие доработки

- добавить русский язык
- добавить уведомление об изменения в календаре либо единожды через команду, либо через планировщик, который через
  интервал времени анализирует изменения и отправляет уведомление если они есть.

## Благодарности

- Проекту https://github.com/lugamuga/mattermost-yandex-calendar-plugin,
  демонстрирует работу с яндекс календарём, есть документация
  https://pkg.go.dev/github.com/lugamuga/mattermost-yandex-calendar-plugin
- Проекту https://github.com/python-caldav/caldav , очень простые интерфейс-запросы на сервер, вся тяжелейшая работа
  под капотом пакета. Отличная документация, но есть ещё над чем поработать(фильтрация по параметрам). Документация -
  https://caldav.readthedocs.io/en/latest/
- Проекту https://github.com/agronholm/apscheduler . Отличный инструмент для планирования нетривиальных задач,
  триггеров, настройка планировщика и БД. Документация - https://pypi.org/project/APScheduler/
