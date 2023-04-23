from . import views
from django.urls import path

urlpatterns = [
    path('asymgraph/<_id>/', views.get_asym_data),
    path('groupinfo/', views.get_group_info),
    path('graphvis/', views.get_custom_graphvis),
    path('asym_vis/', views.get_asym_vis),
    path('vis/', views.get_graphvis),
    path('customsym/', views.get_custom_graph_symmetries),
    path('petersen/', views.get_petersen_symmetries)
]
