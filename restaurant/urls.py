from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user", views.user, name="user"),
    path("restaurant", views.restaurant, name="restaurant"),
    path("restaurant/<int:restaurant_id>", views.restaurant, name="restaurant"),
    path(
        "restaurant/<int:restaurant_id>/update",
        views.update_restaurant,
        name="update_restaurant",
    ),
    path("tables/<int:restaurant_id>", views.tables, name="tables"),
    path("booking", views.booking, name="booking"),
    path("booking/<int:restaurant_id>", views.booking, name="booking"),
    path("bookings/<int:status>", views.booking, name="bookings"),
    path("bookings/<int:restaurant_id>/<int:status>", views.booking, name="bookings"),
]
