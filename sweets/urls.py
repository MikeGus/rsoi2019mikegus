from django.urls import path
from .views import ListSweetView, SweetView


urlpatterns = [
    path('sweets/', ListSweetView.as_view(), name="sweets"),
    path('sweets/<int:pk>/', SweetView.as_view(), name="sweet")
]
