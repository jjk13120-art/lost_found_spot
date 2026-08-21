from django.views.generic import TemplateView

class FAQView(TemplateView):
    template_name = 'pages/faq.html'
