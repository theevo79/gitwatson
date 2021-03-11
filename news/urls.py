from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

#from . import views
import news.views
import users.views

app_name = "news"
urlpatterns = [
	path("", news.views.index, name="index1"),
	path("book", news.views.book, name="book"),
	path("allusers", news.views.allusers, name="allusers"),
	path("login", users.views.login_view, name="login"),
	path("logout", users.views.logout_view, name="logout"),
	path("register", users.views.register, name="register")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)