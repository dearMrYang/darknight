from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = 'userauth'
urlpatterns = [
       path('login/', csrf_exempt(views.Login.as_view()), name='login'),
       path('logout/', views.logout_view, name='logout'),
]
