#
from django.urls import path
# Views basadas en clases
from .views import HomePageView, TestPDFView

app_name = 'core_app'

urlpatterns = [
    path('', 
        HomePageView.as_view(), 
        name='home'
    ),


    #TEST PDF
    path('pdf/', 
        TestPDFView.as_view(), 
        name='gen_pdf'
    ),
] 