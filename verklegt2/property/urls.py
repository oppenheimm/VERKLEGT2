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
    path('<int:pk>/toggle-sold/', views.toggle_property_sold, name='toggle_property_sold'),
    path('<int:id>/edit/', views.edit_property, name='edit'),
    path('<int:property_id>/make-offer/', views.make_offer, name='make_offer'),
    path('offer/<int:offer_id>/accept/', views.accept_offer, name='accept_offer'),
    path('offer/<int:offer_id>/decline/', views.decline_offer, name='decline_offer'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
