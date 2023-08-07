# Today's conferences

### Calendar name: {{ calendar_name }}

{% for c in conferences %}
{% if c.dtstart %}*  Start: {{ c.dtstart }}{% endif %}  
{% if c.dtend %}* End: {{ c.dtend }}{% endif %}
{% if c.summary %}* Summary: {{ c.summary }}{% endif %}
{% if c.created %}* Created: {{ c.created }}{% endif %} 
{% if c.last_modified %}* Last modified: {{ c.last_modified }}{% endif %}
{% if c.description %}* Description: {{ c.description }}{% endif %} 
{% if c.url_event %}* Event: {{ c.url_event }}{% endif %}
{% if c.categories %}* Categories: {{ c.categories }}{% endif %} 
{% if c.x_telemost_conference %}* Telemost conference: {{ c.x_telemost_conference }}{% endif %} 
{% if c.organizer %}* Organizer: {{ c.organizer }}{% endif %}
{% if c.attendee %}
* attendees:
{% for attendee in c.attendee %}  * attendee:
{% for k, v in attendee.items() %}    * {{ k|e }} {{ v|e }}
{% endfor %}
{% endfor %}{% endif %} 
{% if c.location %}* location: {{ c.location }}{% endif %}
__________
{% endfor %}
