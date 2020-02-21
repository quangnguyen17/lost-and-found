from django.urls import path
from . import views

urlpatterns = [
    # /
    path('', views.index),
    # /home/
    path('home', views.home),
    path('home/add', views.add),
    path('home/logout', views.log_out),
    # /home/
    path('home/<str:keyword>', views.custom_home),
    # /actions
    path('add_item', views.add_item),
    path('found_item/<int:item_id>', views.found_item),
    path('unfound_item/<int:item_id>', views.unfound_item),
    path('remove_item/<int:item_id>', views.remove_item),
]
