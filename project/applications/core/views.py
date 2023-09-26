from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, View
from django.contrib.sessions.models import Session


#TEST PDF
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import FileResponse


# Create your views here.

class HomePageView(LoginRequiredMixin , TemplateView):
    template_name = "core/home_page.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        print(Session.objects.all())
        return super().get_context_data(**kwargs)

class TestPDFView(View):
    def get(self, request):
        # Crear un objeto BytesIO para almacenar el PDF
        buffer = BytesIO()
        
        # Crear un objeto canvas para dibujar en el PDF
        p = canvas.Canvas(buffer)
        
        # Configurar el título y fuente
        p.setFont("Courier", 28)
        p.setFillColorRGB(0.14, 0.59, 0.74)
        p.drawString(60, 750, "Videojuegos")
        
        # Configurar la fuente para el contenido del PDF
        p.setFont("Helvetica", 16)
        p.setFillColorRGB(0, 0, 0)
        
        # Agregar contenido al PDF aquí
        
        # Guardar la página actual y finalizar el PDF
        p.showPage()
        p.save()
        
        # Obtener el contenido del buffer y cerrarlo
        pdf = buffer.getvalue()
        buffer.close()
        
        # Configurar la respuesta HTTP para mostrar el PDF en el navegador
        response = FileResponse(BytesIO(pdf), content_type="application/pdf")
        
        return response