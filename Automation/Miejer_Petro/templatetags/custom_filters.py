# xyz/templatetags/custom_filters.py
from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_timestamp(value):
    """Formats a timestamp from 'YYYY-MM-DD HH:MM:SS,sss' to 'YYYYMMDDHHMMSSsss'."""
    return value.replace("-", "").replace(":", "").replace(" ", "").replace(",", "")


@register.filter
def calculate_time_diff(current_timestamp, next_timestamp):
    print(current_timestamp, next_timestamp)
    if current_timestamp and next_timestamp:
        # Replace comma with a dot for milliseconds
        try:
            current_time = datetime.strptime(current_timestamp, '%Y-%m-%d %H:%M:%S.%f')  # Adjusted format
            next_time = datetime.strptime(next_timestamp, '%Y-%m-%d %H:%M:%S.%f')
            # Calculate the difference
            return (next_time - current_time).total_seconds()  # Returns seconds
        except ValueError:
            return None  # Handle parsing errors
    return None

@register.filter
def get_item(lst, index):
    print(lst, index)
    try:
        return lst[index]
    except IndexError:
        return None