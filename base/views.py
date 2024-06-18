# from django.shortcuts import render
# from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .consumers import connected_users
from .models import Task, UserProfile, BaseAppInfo, User
from .serializers import TaskSerializer, BaseAppInfoSerializer, UserSerializer, UserProfileSerializer
from .forms import SignUpForm

from django.contrib.auth.decorators import user_passes_test


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = SignUpForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            send_mail_func.delay(
                subject='Welcome to To Do List App',
                message='Thank you for registering at To Do List App!',
                recipient_list=[user.email]
            )
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super().get(*args, **kwargs)


def LogoutUser(request):
    logout(request)

    return redirect('login')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


class ProfileUser(LoginRequiredMixin, TemplateView):
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_profile, created = UserProfile.objects.get_or_create(user=user)

        context['username'] = user.username
        context['email'] = user.email
        context['gender'] = user_profile.gender
        context['birth_date'] = user_profile.birth_date

        return context


class AboutView(TemplateView):
    template_name = 'base/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_info'] = BaseAppInfo.objects.first()
        return context


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)


class BaseAppInfoView(generics.ListAPIView):
    queryset = BaseAppInfo.objects.all()
    serializer_class = BaseAppInfoSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileDetailView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


def lobby(request):
    return render(request, 'base/lobby.html')


def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def online_users(request):
    return render(request, 'base/online_users.html', {'connected_users': connected_users})


from django.http import HttpResponse
from .tasks import send_mail_func


def celeryemailtask(request):
    send_mail_func.delay()
    return HttpResponse('<h1>Email was sent with Celery!!! YAY</h1>')


from django.utils.decorators import method_decorator
from .models import EmailLog


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class EmailLogView(TemplateView):
    template_name = 'base/email_log.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['email_logs'] = EmailLog.objects.all().order_by('-timestamp')
        return context
