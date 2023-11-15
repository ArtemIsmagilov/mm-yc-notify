# Hi, @{{ mm_username }}.

## Info about App

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