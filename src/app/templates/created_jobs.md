### I created tasks in your yandex calendar

- [x]  🌐 timezone - {{ timezone }}
- [x]  🌤 every day at {{ daily_clock }}
- {% if e_c %}[x]{% else %}[ ]{% endif %}  ⏲ notify 10 minutes before the start of the event
- {% if ch_stat %}[x]{% else %}[ ]{% endif %}  📅 changing status when on conference

##### Added calendars

{% for cal_name in calendars_names %}

- {{ cal_name.label }}
  {% endfor %}
