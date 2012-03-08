from django.db.models import get_model
from django import template
register = template.Library()

# homepage introduction
# templates/phytosanitary/resource_archive.html
# templates/phytosanitary/includes/homeintro.html
from project.phytosanitary.models import Resource
def homeintro(context): # need 'context' in here otherwise get 'list index out of range' error
    resource = Resource.objects.filter(title__exact='Homepage')
    # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    user = context['request'].user
    return {'resource': resource, 'user': user}

register.inclusion_tag('phytosanitary/includes/homeintro.html', takes_context=True)(homeintro) # needed to add 'takes_context=True' argument so that the user variable would get passed into the context


def do_latest_content(parser, token):
    bits = token.split_contents()
    if len(bits) != 5:
        raise template.TemplateSyntaxError("'get_latest_content' tag takes exactly four arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to 'get_latest_content' must be an 'application name'.'model name' string")
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError("'get_latest_content' tag got an invalid model: %s" % bits[1])
    return LatestContentNode(model, bits[2], bits[4])

class LatestContentNode(template.Node):
    def __init__(self, model, num, varname):
        self.model = model
        self.num = int(num)
        self.varname = varname
        
    def render(self, context):
        manager = self.model._default_manager
        if self.model.__name__ == 'Resource':
            manager = self.model.live
        context[self.varname] = manager.all()[:self.num]
        return ''


register.tag('get_latest_content', do_latest_content)