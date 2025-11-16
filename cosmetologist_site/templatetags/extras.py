from typing import Optional, Iterable, Dict, Any

from django import template


register = template.Library()


@register.filter
def split(value: str, delimiter: str) -> list[str]:
    """Разбивает строку по разделителю"""
    return value.split(delimiter)


@register.simple_tag(takes_context=True)
def querystring(
    context: Dict[str, Any],
    exclude: Optional[Iterable[str] | str] = None,
    **kwargs: Any,
) -> str:
    """
    Собирает querystring на основе текущих request.GET, с возможностью:
      - исключить параметры (exclude="page,sort")
      - переопределить/добавить параметры через именованные аргументы (page=2)
      - удалить параметр, если его значение None (page=None)
    Пример: {% querystring exclude="page" page=3 %}
    """
    request = context.get("request")
    if not request:
        return ""
    params = request.GET.copy()

    if exclude:
        if isinstance(exclude, str):
            exclude_keys = [k.strip() for k in exclude.split(",") if k.strip()]
        else:
            exclude_keys = list(exclude)
        for key in exclude_keys:
            params.pop(key, None)

    for key, value in kwargs.items():
        if value is None:
            params.pop(key, None)
        else:
            params[key] = value

    return params.urlencode()
