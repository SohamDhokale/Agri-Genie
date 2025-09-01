from django import template
from django.template.defaultfilters import stringfilter
from ..translations import get_translation

register = template.Library()

@register.filter
@stringfilter
def t(key, language='en'):
    """Template filter to get translation for a key"""
    return get_translation(key, language)

@register.simple_tag(takes_context=True)
def translate(context, key):
    """Template tag to get translation for a key using current language"""
    language = context.get('site_lang', 'en')
    return get_translation(key, language)
