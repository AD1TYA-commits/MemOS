from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PDFViewSet, task

router = DefaultRouter()
router.register(r'pdfs',PDFViewSet)

urlpatterns = [
    path("",task, name="home"),
    path('api/',include(router.urls)),
]

