from django.contrib import admin
from restaurant.models import Category, DayOfWeek, User, Restaurant, Table, Booking

# Register your models here.


admin.site.register(User)
admin.site.register(DayOfWeek)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Table)
admin.site.register(Booking)
