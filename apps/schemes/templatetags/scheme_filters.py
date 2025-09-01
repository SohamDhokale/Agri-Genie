from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Template filter to get dictionary item by key"""
    return dictionary.get(key)

@register.filter
def status_color(status):
    """Template filter to get color class for application status"""
    status_colors = {
        'pending': 'warning',
        'submitted': 'info',
        'under_review': 'warning',
        'approved': 'success',
        'rejected': 'danger',
        'completed': 'primary'
    }
    return status_colors.get(status, 'secondary')
