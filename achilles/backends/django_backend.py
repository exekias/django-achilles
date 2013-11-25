from django.conf import settings
from django.template import Context
from django.template.loader import get_template


class DjangoBackend(object):

    def action_modules(self):
        """
        Return a list of modules that could be holding action libraries
        """
        return [app + '.actions' for app in settings.INSTALLED_APPS]

    def block_modules(self):
        """
        Return a list of modules that could be holding block libraries
        """
        return [app + '.blocks' for app in settings.INSTALLED_APPS]

    def render_template(self, template_name, context):
        """
        Render a template from the given name and context
        """
        t = get_template(template_name)
        return t.render(context)

    def template_context(self):
        """
        Return an empty template context. This object will be passed
        to the render_template method.

        It should provide an update method to fill it with additional
        context data from a dict
        """
        return Context()
