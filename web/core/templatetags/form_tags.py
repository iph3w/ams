import uuid
from django import template
from django.forms import CheckboxInput, fields, HiddenInput, Select, SelectMultiple

register = template.Library()


@register.filter
def is_checkbox(field: fields) -> bool:
    """
    checks whether field is CheckboxInput or not
    """
    return field.field.widget.__class__.__name__ == CheckboxInput().__class__.__name__


@register.filter
def is_select(field: fields) -> bool:
    """
    checks whether field is Select or not
    """
    return field.field.widget.__class__.__name__ in (
        Select().__class__.__name__,
        SelectMultiple().__class__.__name__
    )


@register.filter
def is_hidden(field: fields) -> bool:
    """
    checks whether field is CheckboxInput or not
    """
    return field.field.widget.__class__.__name__ == HiddenInput().__class__.__name__


@register.filter
def inject_class(field, css_class):
    """
    injects css class to field
    """
    if field.errors:
        css_class += " is-invalid "
    return field.as_widget(attrs={
        "class": " ".join((field.css_classes(), css_class))
    })


@register.inclusion_tag(
    "bootstrap/floating_field.html",
    takes_context=False
)
def floating_field(field):
    css_class = "form-control"
    if field.field.widget.__class__.__name__ in (
        Select().__class__.__name__,
        SelectMultiple().__class__.__name__
    ):
        css_class = "form-select"
    if field.errors:
        css_class += " is-invalid"
    return {
        'field': field,
        'widget': field.as_widget(attrs={
            "class": " ".join((field.css_classes(), css_class)),
            "placeholder": field.name
        })
    }


@register.inclusion_tag(
    "bootstrap/field.html",
    takes_context=False
)
def field(field):
    css_class = "form-control"
    if field.field.widget.__class__.__name__ in (
        Select().__class__.__name__,
        SelectMultiple().__class__.__name__
    ):
        css_class = "form-select"
    if field.errors:
        css_class += " is-invalid"
    return {
        'field': field,
        'widget': field.as_widget(attrs={
            "class": " ".join((field.css_classes(), css_class))
        })
    }


@register.inclusion_tag(
    "bootstrap/submit_button.html",
    takes_context=False
)
def submit_button(title: str, css_class: str = ""):
    return {
        'title': title,
        'css_class': css_class
    }


@register.inclusion_tag(
    "bootstrap/form_errors.html",
    takes_context=False
)
def form_errors(form):
    return {
        'form': form,
    }


@register.inclusion_tag(
    "bootstrap/modal.html",
    takes_context=True
)
def modal(context, title, modal_template, button_type=None, modal_button=None, fullscreen=False, is_static=False, modal_size=None):
    return {
        'id': 'modal_' + str(uuid.uuid4()).replace('-', '_'),
        'title': title,
        'type': button_type if button_type is not None else "primary",
        'template': modal_template,
        'modal_button': modal_button,
        'form': context['form'],
        'fullscreen': True if fullscreen is True or fullscreen == 1 else False,
        'is_static': True if is_static is True or is_static == 1 else False,
        'model_size': modal_size if modal_size is None or modal_size in ('modal-sm', 'modal-lg', 'modal-xl') else ""
    }


@register.inclusion_tag(
    "bootstrap/progress.html",
    takes_context=False
)
def progress(value, css_class=None, min_value=0, max_value=100, element_id=f"progress_{uuid.uuid4()}"):
    _css_class = css_class
    if _css_class is None:
        _css_class = 'bg-success' if value == max_value else 'bg-secondary'

    if value > max_value:
        _css_class = "bg-warning"
    value = max_value

    return {
        'id': element_id,
        'css_class': _css_class,
        'value': value,
        'min_value': min_value,
        'max_value': max_value,
        'width': (value / (max_value - min_value)) * 100
    }


@register.inclusion_tag(
    "bootstrap/breadcrumb.html",
    takes_context=False
)
def breadcrumb(title, subtitle=None):
    return {
        'title': title,
        'subtitle': subtitle
    }