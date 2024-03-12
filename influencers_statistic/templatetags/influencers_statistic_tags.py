from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def sort_link(label, sort_by_param, current_sort_by, current_order):
    # Функция, которая генерирует ссылку для сортировки и возвращает ее как безопасную строку HTML

    url = f"?sort_by={sort_by_param}&order={'desc' if current_order == 'asc' else 'asc'}"
    if current_sort_by == sort_by_param:
        if current_order == 'asc':
            icon = '<i class="fas fa-caret-up"></i>'
        else:
            icon = '<i class="fas fa-caret-down"></i>'
    else:
        icon = '<i class="fa-solid fa-sort"></i>'
    return mark_safe(f'<a href="{url}" style="color: inherit;">{label} {icon}</a>')
