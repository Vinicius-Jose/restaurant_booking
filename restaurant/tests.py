from django.test import TestCase
from restaurant.models import User, Booking, DayOfWeek, Table, Restaurant, Category
import restaurant.models as models
from datetime import time, datetime, timedelta
from django.db.models import OuterRef, Subquery
from django.utils import timezone
from django.core.files import File
from pathlib import Path

# Create your tests here.

BOOKING_DATE = datetime(year=2024, month=8, day=6, hour=21)
BOOKING_DATE = timezone.make_aware(BOOKING_DATE, timezone.get_current_timezone())
IMAGE_PATH = ""


class BookingTest(TestCase):

    def setUp(self) -> None:
        owner = User.objects.create(username="Owner", type_user=models.SUPPLIER)
        client = User.objects.create(username="Client", type_user=models.CUSTOMER)

        sunday = DayOfWeek.objects.create(day_of_week="Sunday")
        monday = DayOfWeek.objects.create(day_of_week="Monday")
        tuesday = DayOfWeek.objects.create(day_of_week="Tuesday")
        wednesday = DayOfWeek.objects.create(day_of_week="Wednesday")
        thursday = DayOfWeek.objects.create(day_of_week="Thursday")
        friday = DayOfWeek.objects.create(day_of_week="Friday")
        saturday = DayOfWeek.objects.create(day_of_week="Saturday")

        category = Category.objects.create(name="Test")

        restaurant = Restaurant.objects.create(
            owner=owner,
            booking_time=time(hour=1),
            open_hour=time(hour=20),
            close_hour=time(hour=23),
            name="Test Restaurant",
            category=category,
        )
        restaurant.days_open.set([monday, tuesday, wednesday, thursday, friday])
        table_1 = Table.objects.create(number=1, seats=2, restaurant=restaurant)
        table_2 = Table.objects.create(number=2, seats=4, restaurant=restaurant)
        table_3 = Table.objects.create(number=3, seats=6, restaurant=restaurant)
        table_4 = Table.objects.create(number=4, seats=8, restaurant=restaurant)

        Booking.objects.create(
            date_time=BOOKING_DATE,
            client=client,
            table=table_1,
        )
        return super().setUp()

    def test_searching_restaurant_bookings(self):
        restaurant = Restaurant.objects.get(pk=1)
        bookings = Booking.objects.filter(table__restaurant=restaurant)
        self.assertEqual(len(bookings), 1)

    def test_searching_restaurant_bookings_on_date(self):
        restaurant = Restaurant.objects.get(pk=1)
        open_date_time = datetime(
            year=2024,
            month=8,
            day=6,
            hour=restaurant.open_hour.hour,
            minute=restaurant.open_hour.minute,
        )
        open_date_time = timezone.make_aware(
            open_date_time, timezone.get_current_timezone()
        )
        close_date_time = datetime(
            year=2024,
            month=8,
            day=6,
            hour=restaurant.close_hour.hour,
            minute=restaurant.close_hour.minute,
        )
        close_date_time = timezone.make_aware(
            close_date_time, timezone.get_current_timezone()
        )
        bookings = Booking.objects.filter(
            date_time__range=[open_date_time, close_date_time],
            table__restaurant=restaurant,
        )
        self.assertEqual(len(bookings), 1)

    def test_searching_tables_without_bookings_datetime_range(self):
        restaurant = Restaurant.objects.get(pk=1)
        booking_time = timedelta(
            hours=restaurant.booking_time.hour,
            minutes=restaurant.booking_time.minute - 1,
        )
        initial_datetime = BOOKING_DATE - booking_time
        final_datetime = BOOKING_DATE + booking_time
        tables_with_booking = Booking.objects.filter(
            table=OuterRef("pk"), date_time__range=[initial_datetime, final_datetime]
        )
        tables_without_booking = Table.objects.filter(restaurant=restaurant).exclude(
            id__in=Subquery(tables_with_booking.values("table"))
        )
        self.assertEqual(tables_without_booking[0].id, 2)
        self.assertNotIn(Table.objects.get(pk=1), tables_without_booking)

    def test_check_table_is_available_at_booking_time(self):
        restaurant = Restaurant.objects.get(pk=1)
        booking_date = datetime(year=2024, month=8, day=6, hour=22)
        booking_date = timezone.make_aware(
            booking_date, timezone.get_current_timezone()
        )
        booking_time = timedelta(
            hours=restaurant.booking_time.hour,
            minutes=restaurant.booking_time.minute - 1,
        )

        initial_datetime = booking_date - booking_time
        final_datetime = booking_date + booking_time
        tables_with_booking = Booking.objects.filter(
            table=OuterRef("pk"), date_time__range=[initial_datetime, final_datetime]
        )
        tables_without_booking = Table.objects.filter(restaurant=restaurant).exclude(
            id__in=Subquery(tables_with_booking.values("table"))
        )
        self.assertIn(Table.objects.get(pk=1), tables_without_booking)

    def test_adding_logo_and_background_image(self):
        restaurant = Restaurant.objects.get(pk=1)
        path = Path(IMAGE_PATH)
        with open(path, "rb") as file:
            image = File(file, name=path.name)
            restaurant.logo = image
            restaurant.backgroud_image = image
            restaurant.save()
        self.assertIsNotNone(restaurant.logo)

    def test_search_restaurants_open(self):
        date = datetime(year=2024, month=8, day=10, hour=22, minute=10)
        day_of_week = DayOfWeek.objects.get(day_of_week=date.strftime("%A"))
        list_restaurant = day_of_week.open_restaurants.all()
        self.assertFalse(list_restaurant)
