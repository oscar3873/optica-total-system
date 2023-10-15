from django.shortcuts import render

# Create your views here.
class PromotionCreateView(TemplateView):
    template_name = 'promotions/promotion_create_form.html'