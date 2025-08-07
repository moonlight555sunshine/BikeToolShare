from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from tool.models import Tool, Category


class HomeView(View):
    def get(self, request):
        available_tools = Tool.objects.filter(is_available=True)
        latest_tools = available_tools.order_by('-id')[:4]
        categories = Category.objects.all()
        return render(request, "home.html", {
            'title': 'Choose necessary tool',
            'subtitle': 'or share with other',
            'latest_tools': latest_tools,
            'categories': categories,
        })

class ToolsView(View):
    def get(self, request):
        tools = Tool.objects.filter(is_available=True)
        return render(request, 'all_tools.html', {
            'tools': tools,
            'title': 'Choose necessary tool',
            'subtitle': 'or share with other',
        })

class ToolView(View):
    def get(self, request, pk):
        tool = Tool.objects.get(id=pk)
        categories = tool.category.all()
        user_profile = tool.owner.profile
        return render(request, 'tool.html', {
            'tool': tool,
            'title': 'Choose necessary tool',
            'subtitle': 'or share with other',
            'user_profile': user_profile,
            'categories': categories,
        })

class CategoryView(View):
    def get(self, request, foo):
        foo = foo.replace('-', ' ')
        try:
            category = Category.objects.get(name__iexact=foo)
            tools = category.tools.all()
            return render(request, 'all_tools.html', {
                'tools': tools,
                'title': category.name,
                'subtitle': 'choose necessary tool',
            })
        except:
            messages.error(request, 'Category does not exist.')
            return redirect('home')