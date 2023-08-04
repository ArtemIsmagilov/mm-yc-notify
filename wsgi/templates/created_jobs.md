### @{{ mm_username }}, I created tasks in your yandex calendar ***{{ calendar_name }}***

{% if errors %}##### {{ errors }} {% endif %}

- [x]  🌐 timezone - {{ timezone }}
- [x]  ⏲ every day at {{ daily_clock }}
- {% if notification_before_10_min %}[x]{% else %}[ ]{% endif %}  🗞 notify 10 minutes before the start of the event
- {% if status %}[x]{% else %}[ ]{% endif %}  📅 changing status when on conference
