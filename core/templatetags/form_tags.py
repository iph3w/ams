from django import template
from django.forms import CheckboxInput, fields, HiddenInput

register = template.Library()


@register.filter
def is_checkbox(field: fields) -> bool:
    """
    checks whether field is CheckboxInput or not
    """
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter
def is_hidden(field: fields) -> bool:
    """
    checks whether field is CheckboxInput or not
    """
    return field.field.widget.__class__.__name__ == HiddenInput().__class__.__name__


@register.filter()
def inject_class(field, css_class):
    """
    injects css class to field
    """
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), css_class))
    })
