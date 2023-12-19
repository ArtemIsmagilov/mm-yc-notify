{% block content %}{% endblock %}
{% for calendar_name, conferences in represents %}

## calendar name: {{ calendar_name | string }}

{% for c in conferences %}
__№{{ loop.index }}__

{% if c.timezone %}* Timezone: {{ c.timezone }}{% endif %}
{% if c.dtstart %}*  Start: {{ c.dtstart }}{% endif %}  
{% if c.dtend %}* End: {{ c.dtend }}{% endif %}
{% if c.summary %}* Summary: {{ c.summary }}{% endif %}
{% if c.created %}* Created: {{ c.created }}{% endif %} 
{% if c.last_modified %}* Last modified: {{ c.last_modified }}{% endif %}
{% if c.description %}* Description: {{ c.description }}{% endif %} 
{% if c.url_event %}* Event: {{ c.url_event }}{% endif %}
{% if c.categories %}* Categories: {{ c.categories }}{% endif %} 
{% if c.x_telemost_conference %}* Telemost conference: {{ c.x_telemost_conference }}{% endif %} 
{% if c.organizer %}
* Organizer:
{% for k, v in c.organizer.items() %}   * {{ k|e }} {{ v|e }}
{% endfor %}{% endif %}
{% if c.attendee %}
* attendees:
{% for a in c.attendee %}  
  * attendee:
{% for k, v in a.items() %}    * {{ k|e }} {{ v|e }}
{% endfor %} {% endfor %}{% endif %} 
{% if c.location %}* Location: {{ c.location }}{% endif %}
{% if c.recurrence_id %}* Recurrence_id: {{ c.recurrence_id }}{% endif %}
__________
{% else %}No conference.{% endfor %}{% endfor %}