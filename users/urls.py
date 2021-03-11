from django.urls import path, include

from . import views
#from watson.news.views import index

app_name = "users"
urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register")
	#path('news/', include('news.urls'))
]