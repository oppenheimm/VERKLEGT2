# property/urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "property"

urlpatterns = [
    path("", views.property_list, name="list"),
    path("create/", views.property_create, name="create"),
    path("<int:id>/", views.property_detail, name="detail"),
    path("<int:id>/delete/", views.property_delete, name="delete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
