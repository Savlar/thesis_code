from . import views
from django.urls import path

urlpatterns = [
    path('asymgraph/<_id>/', views.get_asym_data),
    path('groupinfo/', views.get_group_info),
    path('graphvis/', views.get_custom_graphvis),
    path('customsym/', views.get_custom_graph_symmetries)
]
