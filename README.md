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
- [Тесты](#тесты)
- [Интеграция в производственной среде](#интеграция-в-производственной-среде)
- [Как работает](#как-работает)
- [Алгоритм уведомлений](#алгоритм-уведомлений)
- [Диаграммы](#диаграммы)
- [Пробуем новую архитектуру](#пробуем-новую-архитектуру)
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
> - Автоматически проставлять статус `📆 На встрече`, когда на встрече.

## Проблема

> Плагин [YandexCalendar(plugin)](https://github.com/LugaMuga/mattermost-yandex-calendar-plugin) местами не работает

## Решение

- Переработка плагина (Go) https://github.com/LugaMuga/mattermost-yandex-calendar-plugin на Python
- Добавление необходимого функционала
- Исправление ошибок

## Описание

- [x] Программа представлена в виде интеграции сервиса mattermost и яндекс календаря по протоколу CalDAV,
  а именно, ___вытягивание конференций___ из сервера.
- [x]  Доступны запросы на получение списка конференций с атрибутами в различные промежутки времени.
- [x]  Аутентификация по логину яндекса и токену яндекс приложения.
- [x]  Настройка часового пояса.
- [x]  Ежедневное уведомление в заданное время по часовому поясу пользователя.
- [x]  Уведомление о предстоящей конференции за 10 минут до начала.
- [x]  Установка статуса "📆 In a meeting" во время конференции. Если изначальный статус длительнее или в
  режиме `не стирать`,
  то происходит возврат вашего статуса после конференции. Напрмер: 🏠 "Working from home". Status `Don't clear` ->
  📆 `In a meeting`. Status `18:30` -> 🏠 "Working from home". Status `Don't clear`.
- [x]  Проверка активности аккаунта.
- [x]  Проверка активности планировщика.
- [x]  Возможность удалить/обновить установленные параметры в интеграции
- [x]  Уведомление об изменении/добавлении/удалении конференций, наличие всех доступных атрибутов участников конференции
- [x]  Интеграция с несколькими яндекс календарями по выбору

## Предварительные требования

- Docker Engine 24.0.5
- Python 3.12

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
    │         ├── update
    │         └── profile
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
        + profile [*show* info about me(user  attributes) - execute command]

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
    + postgres
      ```bash
      cd /psql
      sudo docker compose up
      ```

    + app
      ```bash
      cd ../
      flask init-db
      bash run-app.bash
      ```

## Тесты

- предварительно у вас должен быть запущен mattermost, psql контейнеры, у бота должны быть токен и права.
- очищаем БД в `src/`
  ```bash
  sudo quart init-db -c
  ```
- запускаем тесты в папке `src`
  ```bash
  coverage run -m pytest --cache-clear
  ```
  ```bash
  coverage report -m
  ```
  ```text
    Name                                                Stmts   Miss  Cover   Missing
    ---------------------------------------------------------------------------------
    src/app/__init__.py                                    49      3    94%   36, 40, 44
    src/app/app_handlers.py                                14      0   100%
    src/app/async_wraps/async_wrap_caldav.py               27      3    89%   11, 18-19
    src/app/bots/bot_commands.py                           34      4    88%   11, 32, 49, 54
    src/app/calendars/caldav_api.py                        97     14    86%   66-88, 173
    src/app/calendars/caldav_filters.py                    10      6    40%   6-10, 14, 18
    src/app/calendars/caldav_funcs.py                      15      2    87%   20-22
    src/app/calendars/caldav_searchers.py                  21      5    76%   33-37
    src/app/calendars/calendar_app.py                      15      0   100%
    src/app/calendars/calendar_backgrounds.py              25      8    68%   18-24, 28-29
    src/app/calendars/calendar_views.py                    10      1    90%   11
    src/app/calendars/conference.py                        96     33    66%   47, 76, 85, 91, 95-100, 104-109, 113, 117, 121, 129-134, 138-148, 152, 156-163
    src/app/checks/check_app.py                             9      0   100%
    src/app/checks/check_my_account.py                     13      0   100%
    src/app/checks/check_my_scheduler.py                   14      0   100%
    src/app/connections/connection_app.py                  24      3    88%   20, 25, 35
    src/app/connections/connection_backgrounds.py          40      8    80%   24, 40, 43-50, 65, 86
    src/app/connections/connection_handlers.py             62      7    89%   49-52, 68, 138-141
    src/app/constants.py                                    3      0   100%
    src/app/converters.py                                  79     46    42%   19-20, 30, 34-36, 40-41, 46-48, 55-70, 77-88, 92-97, 101, 111-114, 118, 126, 130
    src/app/decorators/account_decorators.py               65      3    95%   77-79
    src/app/dict_responses.py                              48      7    85%   49, 106, 120, 127, 148, 155, 162
    src/app/notifications/notification_app.py              24      0   100%
    src/app/notifications/notification_backgrounds.py      46      3    93%   44-46, 84
    src/app/notifications/notification_handlers.py         99      4    96%   37, 112, 174, 251
    src/app/notifications/notification_views.py            23      7    70%   20, 37-40, 53-56
    src/app/notifications/tasks.py                        212    102    52%   35-36, 42-43, 49-50, 56-57, 63-64, 100, 116, 135-183, 198, 223-278, 286, 292, 299, 336-435, 441-455
    src/app/notifications/worker.py                        14      0   100%
    src/app/schemas.py                                     30      0   100%
    src/app/sql_app/crud.py                                87      9    90%   149, 173-183, 194, 244, 261-272, 276
    src/app/sql_app/database.py                             8      0   100%
    src/app/sql_app/db_CLI.py                              21     10    52%   15-20, 24-25, 29-31
    src/app/sql_app/models.py                               5      0   100%
    src/app/validators.py                                   8      2    75%   8-9
    src/settings.py                                        35      0   100%
    src/tests/__init__.py                                   0      0   100%
    src/tests/additional_funcs.py                          33      2    94%   67-68
    src/tests/conftest.py                                  51      4    92%   28, 50, 54, 81
    src/tests/test_app.py                                 633      2    99%   1226-1227
    ---------------------------------------------------------------------------------
    TOTAL                                                2099    298    86%
  ```
  Подробная информация в html
  ```bash
  coverage html
  ```
  Помимо тестов также требуется соблюдение PEP8
  ```bash
  flake8 src/
  ```

## Интеграция в производственной среде

- получить сертификаты для зашифрованного трафика https://certbot.eff.org/
- развернуть докер контейнер маттермоста с HTTPS https://docs.mattermost.com/install/install-docker.html
- в `wsgi/gunicorn.conf.py` меняем протокол на https, хост и порт на локальные `127.0.0.1:5000 `, добавляем сертификаты
  и указываем пути к ним. Настраиваем количество работников и потоков. В зависимости от
  вашей кофигурации, меняем переменные в `.env`
- добавляем nginx конфигурацию для проксирования запросов к интеграции на локальный хост и порт
  ```bash
  sudo nano /etc/nginx/sites-enabled/app_nginx
  ```
  ```
  # in /etc/nginx/sites-enabled
  # reverse proxy app
  # http
    
  #server {
  #    listen 10081;
  #    listen [::]:10081;
  #    location / {
  #        include proxy_params;
  #        proxy_pass http://127.0.0.1:5000/;
  #    }
  #}
    
  # https
  server {
      listen 10441 ssl; # managed by Certbot
      listen [::]:10441 ssl;
      ssl_certificate /etc/letsencrypt/live/CHANGE/fullchain.pem; # managed by Certbot
      ssl_certificate_key /etc/letsencrypt/live/CHANGE/privkey.pem; # managed by Certbot
      include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
      ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
      server_name CHANGE; # managed by Certbot
    
      location / {
          include proxy_params;
          proxy_pass https://127.0.0.1:5000/;
      }
  }
  ```
  ```bash
  sudo systemctl reload nginx
  ```
- После добавления интеграции не забудьте создать токен, предоставить права и добавить в `src/.env`
- Перезапустить докер контейнер.

## Как работает

- /yandex-calendar checks check_account
  ![checks_account](imgs/checks_account.PNG)

- /yandex-calendar connections connect
  ![connect](imgs/connect.PNG)

- /yandex-calendar connections profile
  ![profile](imgs/profile.PNG)

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
  В модуле `calendars` список конференций в различных интервалах будет в следующей форме
  ![get_a_month](imgs/get_a_month.PNG)

- /yandex-calendar info
  ![info](imgs/info.PNG)

- /yandex-calendar notifications create/update <br>
  Вы можете создать только один планировщик. С помощью `update` можно обновить планировщик,
  задать другие параметры для уведомлений
  ![notifications_create](imgs/notifications_create.PNG)

  Ответное сообщение о созданном планировщике
  ![notification_created](imgs/notifications_created.PNG)

- /yandex-calendar notifications delete <br>
  Попытка удалить несуществующий планировщик
  ![notifications_delete](imgs/notifications_delete.PNG)

- Уведомление (за 10 минут до конференции)/(ежедневное обо всех сегодня конференциях)
  ![notify](imgs/upcoming_conference.PNG)

## Алгоритм уведомлений

1. В переменной окружения следует прописать в стиле cron частоту запроса от каждого пользователя,
   который подключить планировщик, к яндекс-серверу<br>
   Примеры https://crontab.guru/examples.html

2. Внимание! Администратору следует тонко настроить время повторения пинга сервера.
   Если запросы слишком регулярные, то приложение будет излишне перегружено, если же редкие, то для сотрудников с
   очень частыми конференциями информация от уведомлений будет не актуальна.

3. Вы получаете уведомление об удалённых/изменённых/добавленных конференций на яндекс-сервере.

4. При тестировании следует поменять несколько параметров, а именно:
    1. поменять в коде функцию уведомление за 1 минуту(поменять 10 на 1)
    2. поменять функцию, которая проверяет существование конференции `в пределах от 15 минут и более` на `в переделах от
       времени сейчас и более`.
    3. поменять параметры создания задач на пинг сервера яндекс календаря с cron стилистики на параметр секунды,
       например пинг каждые 10 секунд, в продакшене этого не стоит делать. Также добавить параметр случайности.
       `jitter ` - исполнение задач в случайное время в заданном порядке секунд
       https://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html#module-apscheduler.triggers.cron .
       Это обеспечивает стабильность при сильных нагрузках в час пик.

5. Как работает:
    1. Отслеживаются приложением все конференции и при совершении над ними операция приходят уведомления
    2. Приложение уведомляет вас о предстоящей конференции за 10 минут до начал при условии, что конференция была
       добавлена не раньше 15 минут. Почему? Потому что нужно гарантированно отправлять уведомления о событиях которые
       не
       были удалены за 10 минут до сообщения. 5 минут буфер.
    3. Смена статус осуществляется в момент начала конференции и закачивается в момент окончания конференции. Если,
       ваш статус длительнее по времени статуса конференции или стоит в режиме(постоянно), то приложение вернут ваш
       статус.
    4. Блок `notifications` состоит из подпунктов:
        - уведомление ежедневные в конкретное время
        - уведомление обо всех операция связанных с вашими конференциями, синхронизация через лонг-пуллинг,
          зависит от настройки администратора
        - уведомление за 10 минут до начала предстоящей конференции
    5. Примеры:
        - добавленная конференция ![was_added](imgs/was_added.PNG)
        - измененная конференция ![was_updated](imgs/was_updated.PNG)
        - удалённая конференция ![was_deleted](imgs/was_deleted.PNG)

6. Предостережение
    - Если клиент при создании интеграции вводите валидный логин, токен, потом пользуетесь приложением, затем меняете
      в яндекс календаре логин или токен,
      то интеграция сразу удаляет ваши данные из приложения как невалидного пользователя. Следует либо ничего не менять,
      либо в приложении удалять/обновлять данные через команды приложения.
    - Если вы выбираете некоторые календари, а потом удаляете в яндекс календаре, ваш изначальный выбор уведомлений
      с синхронизированными конференциями удаляется как не валидные данные, опять же - обновляйте/удаляте ваши изменения
      через
      команды приложения.
    - Конференции, которые были добавлены раньше 15 минут не будут обрабатываться приложением для обновления статуса и
      сообщения о предстоящем событии, так как невозможно уведомить о предстоящей конференции за 10 минут если вы
      создали
      конференцию за 1, 3, 5 и так далее до 15 минут. 5 минут добавлены как буфер.
    - библиотека apscheduler не корректно работает с несколькими процессами, поэтому в настройках gunicorn не следует 
      запускать более 1 процесса. Существуют обходные пути, которые позволяют работать с несколькими потоками в apscheduler.
        
      > #### https://apscheduler.readthedocs.io/en/latest/faq.html#how-do-i-share-a-single-job-store-among-one-or-more-worker-processes
      > APScheduler does not currently have any interprocess synchronization and signalling scheme that would enable 
      > the scheduler to be notified when a job has been added, modified or removed from a job store.
      > 
      > Workaround: Run the scheduler in a dedicated process and connect to it via some sort of remote access mechanism 
      > like RPyC, gRPC or an HTTP server. The source repository contains an example of a 
      > RPyC based service that is accessed by a client.

## Диаграммы

- __Пинг сервера__ <br>![diagram](imgs/diagram.svg)
- __БД__ <br>![DB](imgs/db_schema.PNG)
- __apscheduler_job__ <br>![tb1](imgs/tb_apscheduler_job.PNG)
- __user_account__ <br>![tb2](imgs/tb_user_account.PNG)
- __yandex_calendar__ <br>![tb3](imgs/tb_yandex_calendar.PNG)
- yandex_conference <br>![tb4](imgs/tb_yandex_conference.PNG)

## Пробуем новую архитектуру

* Повысили эффективность и производительность кода сделав его асинхронным(asyncio, Quart).
* Добавили брокер сообщений rabbitmq через который очень быстро и надёжно передаются сообщения. (Раньше просто БД)
* Внедрили библиотеку фоновых задач Dramatiq(Для наших задач самое то)
* Есть идея хранить данные синхронизированных календарей и конференций в Redis так как обмен данными очень быстрый,
но структура данных не совсем ключь-значние(пока думаем)
* Требуется нагрузочное и mock тестирование
* Можно удалить middleware Prometheus в dramatiq(в 2 версии автор собирается убрать из коробки)

1. rabbitmq
    Добавляем переменные окружения в .env
    ```bash
    sudo docker compose up -d
    ```
2. worker dramatiq
    ```bash
    dramatiq app.notifications.tasks
    ```
3. events scheduler
    ```bash
    python -m app.notifications.task0_scheduler
    ```
4. web server
   ```bash
   bash run-server.bash
   ```
5. После проверки корректности работы всех компонентов добавляем логирование
6. Запускаем докер файл
   ```bash
   cd src/microsevice/ && sudo docker compose up -d
   ```
   Cмотрим статистику
   ```bash
   sudo docker stats 
   ```
   Смотрим логи
   ```bash
   sudo docker compose logs > output.txt
   ```
7. Можно добавить миграцию БД 
   - https://alembic.sqlalchemy.org/en/latest/tutorial.html
   - https://alembic.sqlalchemy.org/en/latest/autogenerate.html
   - https://github.com/sqlalchemy/alembic/issues/805
   - в `/src`
     ```bash
     alembic init -t async alembic
     ```
   - в файле `alembic.ini` меняем url на действительный<br>
     sqlalchemy.url = ~~driver://user:pass@localhost/dbname~~
   - в файле `env.py` меняем target_metadata
     ```text
     from app.sql_app.models import metadata_obj
     target_metadata = metadata_obj
     # target_metadata = None
     ```
   - при изменениях делаем автогенерацию скрипта миграции
     ```bash
     alembic revision --autogenerate -m "Added account table"
     ```
   - запускаем миграцию
     ```bash
     alembic upgrade head
     ```
   - получить информацию
     ```bash
     alembic history --verbose
     ```

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
- Mattermost troubleshooting - https://docs.mattermost.com/install/troubleshooting.html
- Installing
  packages - https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
- RFC2445(iCalendar) - https://www.ietf.org/rfc/rfc2445.txt
- RFC4791(CALDAV) - https://www.ietf.org/rfc/rfc4791.txt
- Python iCalendar - https://github.com/collective/icalendar
- Python CalDAV - https://github.com/python-caldav/caldav
- Add column psql with foreign
  key - https://stackoverflow.com/questions/17645609/add-new-column-with-foreign-key-constraint-in-one-command
- What is a reasonable code coverage % for unit tests (and
  why)? - https://stackoverflow.com/questions/90002/what-is-a-reasonable-code-coverage-for-unit-tests-and-why
- sync/thread/async https://ru.stackoverflow.com/questions/1159101/python-thread-multiprocessing-asyncio
- rebbitmq docker-compose https://habr.com/ru/companies/slurm/articles/704208/
- periodic task https://docs.celeryq.dev/en/latest/userguide/periodic-tasks.html#using-custom-scheduler-classes
- prefork vs eventlet https://stackoverflow.com/questions/29952907/celery-eventlet-pool-does-not-improve-execution-speed-of-asynchronous-web-requ
- Asynchronous yield from https://peps.python.org/pep-0525/#asynchronous-yield-from
- SQLAlchemy Transactions https://docs.sqlalchemy.org/en/20/core/connections.html#begin-once 
- Flower --broker_api https://github.com/mher/flower/issues/1036
- rabbitmq (unacked,ready) https://stackoverflow.com/questions/31915773/rabbitmq-what-are-ready-and-unacked-types-of-messages
- rabbitmq docker environs https://www.rabbitmq.com/configure.html#supported-environment-variables
- asyncpg interface error https://stackoverflow.com/questions/66444620/asyncpg-cannot-perform-operation-another-operation-is-in-progress
- best naming endpoints in restful https://blog.dreamfactory.com/best-practices-for-naming-rest-api-endpoints/
- pgadmin https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html
- Recurrence events in CalDAV https://icalendar.org/iCalendar-RFC-5545/3-8-4-4-recurrence-id.html
- cancel asyncio.to_thread Task https://stackoverflow.com/questions/71416383/python-asyncio-cancelling-a-to-thread-task-wont-stop-the-thread
- asyncpg transaction error https://stackoverflow.com/questions/74313692/fastapi-asyncpg-sqlalchemy-cannot-use-connection-transaction-in-a-manual

## Вопрос-ответ

- Почему не шифруешь токены?

    + Изначально шифровал с помощью библиотеки cryptography через объект Fernet.
      В процессе разработки выяснил, что ни Redmine, ни Mattermost не шифруют токены. Хотя пароли хэшируют - это мы
      одобряем.
      В интернете большая полемика по тому, как правильно шифровать личную информацию. Я склонился к тому, что
      нужно придерживаться политика самого сайта, где рядом создаётся интеграция. Если шифруют, то нужно тоже шифровать
      и наоборот.

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
           Schema |       Name        | Type  |  Owner   
          --------+-------------------+-------+----------
           public | user_account      | table | postgres
           public | yandex_calendar   | table | postgres
           public | yandex_conference | table | postgres
          (3 rows)

        ```bash
        SELECT id, token FROM user_account;
        ```

           id |      token         
          ----+----------------------------
            1 | hak3jkeh67y4dd1h6q8r16gqrr 
          (1 row)

    + Токен у нас не зашифрован(мы ничего и не делали для этого), предыдущий метод долгий, лучше просто добавить в
      докер контейнер маттермоста adminer и посмотреть в вебе.
      ![mm](imgs/mm.PNG)

    + В маттермост тоже не зашифрован, такая же ситуация и в редмайне.

    + Почему не шифруем? Если, буквально в двух словах, то REST API токены позволяем использовать совсем малую часть
      функционала приложений. Пароли захешированы, уже хорошо. Если унесут БД все токены можно сразу же поменять.

    + https://docs.mattermost.com/developer/personal-access-tokens.html

- Что мы тестируем?

    + Тесты проверяют правильность работы клиентской части - разделы
        1. */calendars*
        2. */checks*
        3. */connections*
        4. */notifications*
        5. */jobs*
    
## Проблемы Яндекс Календаря

- Отсутствие какой-либо документации, RESTAPI, туториала, инструментария от яндекса для работы с Яндекс-Календарём в
  удобном формате JSON, XML. Google хорошо задокументировал работу с google календарём на python
  https://developers.google.com/calendar/api/quickstart/python?hl=ru
- Выборка текущих конференций происходит по часовому поясу клиента, если вы поменяли часовой пояс, то старые
  конференции не меняют часовой пояс, только на сайте визуально. Поэтому нужно настроить часовой пояс один раз при
  создании клиента интеграции в маттермост.
- Не доступны запросы на занятость (тег freebusy, статус 504).
- Если в яндекс-календаре создаю календари с одинаковым именем, то при добавлении в форму, маттермост удаляет эти
  дубликаты.
  Это и логично, как нам их отличить, если одинаковые имена. Можно сделать выбор по id, но это не самые комфортный
  интерфейс для пользователя.
- Произвольные обновления событий без участия клиента, что требует дополнительной корректировки синхронизации событий.
  Скорее всего, сервер обновляет свойства событий не относящиеся к атрибутам вытягиваемой конференции. Для правильной
  синхронизации потребовалась перепроверка на идентичность новых событий-конференций по sync_token с
  событиями-конфренециями
  в БД.
- Не корректное хранение данных о событии. Здесь имеется ввиду, что при поиске событий через метод `calendar.search`
  возвращаются не отсортированные и лишние события. Я создал issue для автора библиотеки `caldav` 
  https://github.com/python-caldav/caldav/issues/351 . Тут не понятно, то ли это проблема Яндекс Календаря(не правильно
  сохраняет timezone) то ли библиотеки `caldav`

## Будущие доработки

- добавить русский язык
- оптимизировать алгоритм обновлений конференций через CalDAV сервер
- покрыть код тестами
- выявить уязвимости
- желательна переработка кода

## Благодарности

- Проекту https://github.com/lugamuga/mattermost-yandex-calendar-plugin,
  демонстрирует работу с яндекс календарём, есть документация
  https://pkg.go.dev/github.com/lugamuga/mattermost-yandex-calendar-plugin
- Проекту https://github.com/python-caldav/caldav , очень простые интерфейс-запросы на сервер, вся тяжелейшая работа
  под капотом пакета. Отличная документация, но есть ещё над чем поработать(фильтрация по параметрам). Документация -
  https://caldav.readthedocs.io/en/latest/
- Проекту https://github.com/agronholm/apscheduler . Отличный инструмент для планирования нетривиальных задач,
  триггеров, настройка планировщика и БД. Документация - https://pypi.org/project/APScheduler/
- Проекту [mattermostautodriver](https://github.com/embl-bio-it/python-mattermost-autodriver), форк от заброшенного
  проекта [mattermostdriver](https://github.com/Vaelor/python-mattermost-driver) . На данный момент поддерживается,
  соответствует последним изменения и дополнениям [Mattermost API Reference (4.0.0)](https://api.mattermost.com/).
  Документация https://embl-bio-it.github.io/python-mattermost-autodriver/ . Есть возможность автоматически обновить
  конечные точки
  Mattermost API в пакете
  драйвера https://github.com/embl-bio-it/python-mattermost-autodriver#updating-openapi-specification
  Драйвер не упоминается на сайте Mattermost, однако имеет все шансы быть официальным. Требуется дальнейшая доработка
- Василию, очень интересный проект
- Анастасии, помощь в разработке и тестировании приложения
