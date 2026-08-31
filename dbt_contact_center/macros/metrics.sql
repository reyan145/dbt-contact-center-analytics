{% macro calculate_rate(numerator, denominator, precision=2) %}
    round(safe_divide({{ numerator }}, nullif({{ denominator }}, 0)) * 100, {{ precision }})
{% endmacro %}