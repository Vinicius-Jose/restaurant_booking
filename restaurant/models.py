from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, datetime

SUPPLIER = "SUPPLIER"
CUSTOMER = "CUSTOMER"
USER_CHOICES = ((SUPPLIER, "Restaurant Owner"), (CUSTOMER, "Customer"))
TABLE_CHOICES = ((1, 1),)
WAITING = 0
CANCELLED = 1
CONFIRMED = 2
BOOKING_STATUS = (
    (WAITING, "Waiting"),
    (CANCELLED, "Cancelled"),
    (CONFIRMED, "Comfirmed"),
)


# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15)
    type_user = models.CharField(choices=USER_CHOICES, default=CUSTOMER, max_length=8)

    def __str__(self) -> str:
        return self.username


class DayOfWeek(models.Model):
    day_of_week = models.CharField(null=False, blank=False, max_length=10)

    def __str__(self) -> str:
        return self.day_of_week


class Category(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)

    def __str__(self) -> str:
        return self.name


class Restaurant(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="restaurants"
    )
    name = models.CharField(blank=False, null=False, max_length=200)
    booking_time = models.TimeField(blank=False, null=False)
    open_hour = models.TimeField(blank=False, null=False)
    close_hour = models.TimeField(blank=False, null=False)
    logo = models.ImageField(blank=True, null=True, upload_to="images/logo/")
    days_open = models.ManyToManyField(DayOfWeek, related_name="open_restaurants")
    background_image = models.ImageField(
        blank=True, null=True, upload_to="images/background/"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="restaurants_category",
        null=False,
        blank=False,
    )
    average_price_dollars = models.FloatField(blank=False, null=False, default=10)
    address = models.CharField(max_length=200, null=False, blank=False)
    site = models.URLField(null=True, blank=True, max_length=300)
    phone = models.CharField(max_length=15)
    menu = models.ImageField(blank=True, null=True, upload_to="images/menu/")

    def get_booking_times(self):
        booking_times = []
        current_time = self.open_hour
        while self.is_time_in_range(self.open_hour, self.close_hour, current_time):
            booking_times.append(current_time.strftime("%H:%M"))
            delta = timedelta(minutes=15)
            current_time = (
                datetime.combine(datetime.now(), current_time) + delta
            ).time()

        return booking_times

    def is_time_in_range(self, start, end, check_time):
        if start <= end:
            return start <= check_time <= end
        else:
            return check_time >= start or check_time <= end

    def __str__(self) -> str:
        return f"{self.id} {self.owner.email} : {self.name}"


class Table(models.Model):
    number = models.IntegerField(blank=False, null=False)
    seats = models.IntegerField(choices=((4, "4"), (8, "8")), null=False, blank=False)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="tables"
    )

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "number": self.number,
            "seats": self.seats,
            "restaurant": self.restaurant.id,
        }


class Booking(models.Model):
    date_time = models.DateTimeField(blank=False, null=False)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="table_bookings"
    )
    status = models.IntegerField(choices=BOOKING_STATUS, default=WAITING)
