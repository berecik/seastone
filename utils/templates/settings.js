{% for name,value in settings_dir.items %}
    {{name|safe}} = {{value|safe}};
{% endfor %}