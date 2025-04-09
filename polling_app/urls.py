from django.contrib import admin
from django.urls import path, include
from polls.views import home  # 👈 import the view
from polls.views import home, create_poll

urlpatterns = [
    path('', home, name='home'),
    path('create/', create_poll, name='create'),
    path('admin/', admin.site.urls),
    path('api/', include('polls.urls')),
]
