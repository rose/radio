from django import template
register = template.Library()

# timedelta prints itself with a leading 0 for hours, we're dealing with
# lengths nearly always less than an hour and don't want the extra zeros

@register.simple_tag(name='td_format')
def access(td):
    if (td.days > 0):
        out = "{d} days " % td.days 
    else:
        out = ""
    if (td.seconds > 3600):
        return "{:s}{:d}:{:02d}:{:02d}".format(out, td.seconds / 3600, int((td.seconds % 3600) / 60), int(td.seconds % 60))
    else:
        return "{:s}{:d}:{:02d}".format(out, td.seconds // 60, td.seconds % 60) 

