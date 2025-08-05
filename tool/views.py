from django.shortcuts import render
from django.views import View

from tool.models import Tool, Category


class HomeView(View):
    def get(self, request):
        latest_tools = Tool.objects.all().order_by('-id')[:4]
        categories = Category.objects.all()
        return render(request, "home.html", {
            'latest_tools': latest_tools,
            'categories': categories,
        })