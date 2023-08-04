{% for c, e  in represents %}
### calendar name: {{ c }}
{% for a in e %}
{% if a.dtstart %}*  Start: {{ a.dtstart }}{% endif %}  
{% if a.dtend %}* End: {{ a.dtstart }}{% endif %}
{% if a.summary %}* Summary: {{ a.summary }}{% endif %}
{% if a.created %}* Created: {{ a.created }}{% endif %} 
{% if a.last_modified %}* Last modified: {{ a.last_modified }}{% endif %}
{% if a.description %}* Description: {{ a.description }}{% endif %} 
{% if a.url_event %}* Event: {{ a.url_event }}{% endif %}
{% if a.categories %}* Categories: {{ a.categories }}{% endif %} 
{% if a.x_telemost_conference %}* Telemost conference: {{ a.x_telemost_conference }}{% endif %} 
{% if a.organizer %}* Organizer: {{ a.organizer }}{% endif %}
{% if a.attendee %}
* attendees:
{% for attendee in a.attendee %}  * attendee:
{% for k, v in attendee.items() %}    * {{ k|e }} {{ v|e }}
{% endfor %}
{% endfor %}{% endif %} 
{% if a.location %}* location: {{ a.location }}{% endif %}
__________
{% endfor %}
{% endfor %}


