from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import ToDoList, ToDoItem
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect


# Create your views here.

class ListListView(ListView):
    model = ToDoList
    template_name = 'mytodos/index.html'


class ItemListView(ListView):
    model = ToDoItem
    template_name = 'mytodos/todo_list.html'

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return context
    
class ListCreate(CreateView):
    model = ToDoList
    fields = ['title']
    
    
class ItemCreate(CreateView):
    model = ToDoItem
    fields = ['todo_list',
              'title',
              'description',
              'due_date']
    
    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        initial_data["todo_list"] = todo_list
        return initial_data
        

    def get_context_data(self, **kwargs):
        context = super(ItemCreate, self).get_context_data(**kwargs)
        todo_list = ToDoList.objects.get(id=self.kwargs["list_id"])
        context["todo_list"] = todo_list
        context["title"] = "Create a new Item"
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    

class ItemUpdate(UpdateView):
    model = ToDoItem
    fields = [
        "todo_list",
        "title",
        "description",
        "due_date"
    ]

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit Item"     
        return context
    
    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])
    
class ListDelete(DeleteView):
    model= ToDoList
    success_url = reverse_lazy('index')

    def get_queryset(self):
        return ToDoList.objects.all()


class ItemDelete(DeleteView):
    model = ToDoItem
    template_name = 'mytodos/items_confirm_delete.html'
    

    def get_success_url(self):
        return reverse_lazy('list', args = [self.kwargs["list_id"]])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context
    