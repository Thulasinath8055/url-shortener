from django.views.generic import TemplateView

class LandingPageView(TemplateView):
    """
    Serves the project's landing page at the root URL (/).

    Uses Django's built-in TemplateView — no custom logic required.
    It simply renders templates/index.html.
    """
    template_name = 'index.html'