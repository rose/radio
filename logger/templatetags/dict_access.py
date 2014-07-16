from django import template
register = template.Library()

# django templates don't allow us to access dictionaries using a variable
# d[foo] gives a parse error, d.foo is interpreted as d["foo"].
# So we have to make a custom tag template.  Ralph Minderhoud is a god.
# http://ralphminderhoud.com/posts/variable-as-dictionary-key-in-django-templates/

@register.filter(name='access')
def access(dictionary, key_var):
    return dictionary[key_var]
