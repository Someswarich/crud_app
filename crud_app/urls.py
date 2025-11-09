from django.urls import path
from . import views
urlpatterns=[
    path("product_details/",view=views.product_details),

]