from django.views.generic.base import TemplateView

class Home(TemplateView):
    template_name = "home.html"
