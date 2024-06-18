from django.urls import path, re_path
from . import views
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDelete, CustomLoginView, LogoutUser, RegisterPage
from .views import TaskListView, ProfileUser, AboutView, BaseAppInfoView, UserListView, UserProfileDetailView, \
    EmailLogView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="To Do List API",
        default_version='v1',
        description="Документация для To Do List API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@todolist.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutUser, name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', TaskDelete.as_view(), name='task-delete'),
    path('profile/', ProfileUser.as_view(), name='profile'),
    path('about/', AboutView.as_view(), name='about'),
    path('lobby/', views.lobby, name='lobby'),
    path('online-users/', views.online_users, name='online_users'),
    path('email-log/', EmailLogView.as_view(), name='email_log'),
    path('api-serial/', TaskListView.as_view(), name='serial'),
    path('api-aboutapp/', BaseAppInfoView.as_view(), name='aboutapp'),
    path('api-userlist/', UserListView.as_view(), name='userlist'),
    path('api-userprofile/', UserProfileDetailView.as_view(), name='userprofile'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
