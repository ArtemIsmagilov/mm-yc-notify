### In calendar *{{ calendar_name }}* conference was `{{ loaded }}`.

{% if loaded == 'deleted' %}
#### 🗑️
{% elif loaded == 'added' %}
#### 🆕
{% elif loaded == 'updated' %}
#### 🔂
{% endif %}

{% if was_table %}

{{ was_table }}

{% endif %}

{% if now_table and loaded == 'updated' %}
# ⬇
{{ now_table }}

{% elif now_table %}

{{ now_table }}

{% endif %}
