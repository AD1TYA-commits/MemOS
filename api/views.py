from django.shortcuts import render
from rest_framework import viewsets
from .models import PDF
from .serializers import PDFSerializer
from ingestion.tasks import process_pdf

def task(request):
    uploaded = False
    if request.method == "POST":
        uploaded_pdf = request.FILES["pdf"]
        pdf = PDF.objects.create(file=uploaded_pdf)
        process_pdf.delay(pdf.id)
        uploaded = True
    return render(request, "api/index.html", {"uploaded":uploaded})

class PDFViewSet(viewsets.ModelViewSet):
    queryset = PDF.objects.all()
    serializer_class = PDFSerializer