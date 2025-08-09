from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from tool.forms import ToolForm
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
    def post(self, request):
        searched = request.POST.get('searched')
        search_tools = Tool.objects.filter(name__icontains=searched)
        if not search_tools:
            messages.error(request, 'Nothing was found')
            return redirect('home')
        else:
            return render(request, 'all_tools.html', {
                'tools': search_tools,
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

class AddToolView(View):
    def get(self, request):
        form = ToolForm()
        return render(request, 'form_page.html', {
            'form': form,
            'title': 'New tool',
            'subtitle': 'add your tool',
            'button_text': 'Add',
        })
    def post(self, request):
        if request.user.is_authenticated:
            form = ToolForm(request.POST, request.FILES)
            if form.is_valid():
                tool = form.save(commit=False)
                tool.owner = request.user
                tool.save()
                form.save_m2m()
                messages.success(request, 'Your tool has been added')
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
                return render(request, 'form_page.html', {
                    'form': form,
                    'title': 'New tool',
                    'subtitle': 'add your tool',
                    'button_text': 'Add',
                })
        else:
            messages.error(request, 'You are not logged in')
            return redirect('login')