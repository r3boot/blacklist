from django import template
register = template.Library()

class SetVariable(template.Node):
    def __init__(self, varname, value, is_string=False):
        self.varname = varname
        self.value = value
        self.is_string = is_string

    def render(self,context):
        if self.is_string or not context[self.value]:
            context[self.varname] = self.value
        else:
            context[self.varname] = context[self.value]
        return ''

def setvar(parser, token):
    """
    Set value to variable. If value is object or variable 
    copy pointer of that object/variable to new variable.
    
        {% setvar variable value %}
    
    Set string to variable.
        {% setvar variable "new string" %}        
    """
    
    from re import split
    bits = split(r'\s+', token.contents, 2)
    if bits[2][:1] in '"\'' and bits[2][-1:] in '"\'':
        return SetVariable(bits[1], bits[2][1:-1], True)
    
    return SetVariable(bits[1], bits[2])
register.tag('setvar', setvar)
