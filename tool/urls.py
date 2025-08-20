from django.urls import path
from tool.views import ToolsView, ToolView, CategoryView, AddToolView, UserToolsView

urlpatterns = [
    path('all-tools/', ToolsView.as_view(), name='tools'),
    path('<int:pk>/', ToolView.as_view(), name='tool'),
    path('category/<str:foo>/', CategoryView.as_view(), name='category'),
    path('add-tool/', AddToolView.as_view(), name='add-tool'),
    path('user-tools/', UserToolsView.as_view(), name='my-tools'),
    path('user-tools/<int:pk>/', UserToolsView.as_view(), name='tool-action'),
]