from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('offer/<int:offer_id>/finalize/<str:step>/', views.finalize_offer, name='finalize_offer'),
]