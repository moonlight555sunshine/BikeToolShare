from django.urls import path
from tool.views import ToolsView, ToolView, CategoryView

urlpatterns = [
    path('all_tools/', ToolsView.as_view(), name='tools'),
    path('<int:pk>/', ToolView.as_view(), name='tool'),
    path('category/<str:foo>/', CategoryView.as_view(), name='category'),
]