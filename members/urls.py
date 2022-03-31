from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'api/members', views.MemberList, basename='member')

app_name = 'clients'

urlpatterns = [
    path('', include(router.urls,)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('create/', views.register, name='create'),
    path('<int:id>/match', views.match, name='match'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('list', views.clients_list, name='list'),
    path('restapi/members/', views.MemberList.as_view({'get': 'list'}), name='api_members'),
]
urlpatterns += router.urls
