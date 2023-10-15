from django.views.generic import TemplateView



# Create your views here.
class PromotionCreateView(TemplateView):
    template_name = 'promotions/promotions_page.html'