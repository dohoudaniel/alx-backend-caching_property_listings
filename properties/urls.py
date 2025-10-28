from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path("properties/", views.property_list, name="property-list"),
]

