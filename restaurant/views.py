from datetime import datetime, timedelta
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone
from django.db.models import OuterRef, Subquery, Q, Count


from restaurant.forms import RestaurantForm, UserForm
from restaurant.models import (
    SUPPLIER,
    CUSTOMER,
    DayOfWeek,
    Restaurant,
    Table,
    Booking,
    WAITING,
    BOOKING_STATUS,
)
from copy import deepcopy

import json


# Create your views here.
@login_required
def index(request: HttpRequest):
    url = reverse("restaurant")
    if request.user.type_user == SUPPLIER:
        query_params = "?list=True"
        return redirect(f"{url}{query_params}")
    popular_restaurants = Restaurant.objects.annotate(
        num_bookings=Count("tables__table_bookings")
    ).order_by("-num_bookings")[:10]
    return render(
        request,
        "restaurant/restaurant_list.html",
        {
            "restaurant_list": popular_restaurants,
            "title": "Popular Restaurants",
        },
    )


def login_view(request: HttpRequest):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        type_user = request.POST.get("type_user", "")
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            if user.type_user == type_user:
                login(request, user)
                return redirect("index")

        return render(
            request,
            "restaurant/login.html",
            {"message_" + type_user.lower(): "Invalid username and/or password."},
        )

    return render(request, "restaurant/login.html")


@login_required
def logout_view(request: HttpRequest):
    logout(request)
    return redirect("login")


def register(request: HttpRequest):
    content = {"form": UserForm(), "message": ""}
    page = "restaurant/register.html"
    if request.method == "POST":
        data = deepcopy(request.POST)
        if data.get("confirm_password") == data.get("password"):
            data["username"] = data["email"]
            del data["confirm_password"]
            try:
                user = UserForm(data=data)
                if request.user.is_authenticated:
                    user = UserForm(data=data, instance=request.user)
                if not user.errors:
                    user = user.save(commit=True)
                    user.username = user.email
                    user.set_password(user.password)
                    user.save()
                else:
                    content["message"] = user.errors
                    return render(request, page, content)
            except IntegrityError as e:
                content["message"] = "Email already in use."
                return render(request, page, content)

            login(request, user)
            return redirect("index")

        else:
            content["message"] = "Passwords must match."
            return render(request, page, content)

    return render(request, page, content)


@login_required
def restaurant(request: HttpRequest, restaurant_id: int = 0):
    if request.method == "POST":
        restaurant = RestaurantForm(request.user.id, request.POST, request.FILES)
        if not restaurant.errors:
            restaurant: Restaurant = restaurant.save(commit=True)
            save_days_of_work(request, restaurant)
            restaurant.save()
            return redirect(f"tables/{restaurant.id}")
    elif request.method == "GET":
        if restaurant_id:
            restaurant = get_object_or_404(Restaurant, id=restaurant_id)
            return render(
                request,
                "restaurant/restaurant.html",
                {
                    "restaurant": restaurant,
                    "booking_times": restaurant.get_booking_times(),
                    "min_date": datetime.now().strftime("%Y-%m-%d"),
                },
            )
        elif request.user.type_user == SUPPLIER and not (
            request.GET.get("list") or ("search" in request.GET.keys())
        ):
            return render(
                request,
                "restaurant/new_restaurant.html",
                {
                    "form": RestaurantForm(request.user.id),
                    "days_of_week": DayOfWeek.objects.all(),
                    "days_of_work": [],
                },
            )
        search_text = request.GET.get("search", "")
        restaurant_list = []
        title = ""
        if "search" in request.GET.keys():
            restaurant_list = Restaurant.objects.filter(
                Q(name__icontains=(search_text))
                | Q(category__name__icontains=(search_text))
            )
            title = (
                f"Your search '{search_text}': " if restaurant_list else "Nothing found"
            )
        elif "list" in request.GET.keys():
            restaurant_list = Restaurant.objects.filter(owner=request.user)
            title = "Yours restaurant(s)"
        return render(
            request,
            "restaurant/restaurant_list.html",
            {
                "restaurant_list": restaurant_list,
                "title": title,
            },
        )

    return redirect("index")


def save_days_of_work(request: HttpRequest, restaurant: Restaurant):
    restaurant.days_open.clear()
    for i in range(1, 8):
        if request.POST.get(f"day_{i}"):
            restaurant.days_open.add(DayOfWeek.objects.get(id=i))


@login_required
def tables(request: HttpRequest, restaurant_id: int):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if restaurant.owner != request.user:
        return redirect("index")
    if request.method == "POST":
        data = json.loads(request.body)
        for table in data.get("tables"):
            table["restaurant"] = restaurant
            Table.objects.create(**table)
        return JsonResponse(
            {"message": "tables saved"},
            status=201,
        )
    elif request.method == "PUT":
        data = json.loads(request.body)
        for table in data.get("tables"):
            table_id = table.get("id")
            if table_id:
                table_model = Table.objects.filter(id=table.get("id"))
                table_model = table_model.update(**table)
            else:
                table["restaurant"] = restaurant
                Table.objects.create(**table)
        return JsonResponse(
            {"message": "tables updated"},
            status=201,
        )
    elif request.method == "DELETE":
        data = json.loads(request.body)
        table_model = Table.objects.filter(id=data.get("id"))
        table_model.delete()
        return JsonResponse(
            {"message": "table deleted"},
            status=201,
        )
    elif request.method == "GET":
        if len(restaurant.tables.all()) == 0:
            return render(
                request, "restaurant/tables.html", {"restaurant_id": restaurant_id}
            )
        else:
            table_list = restaurant.tables.all().order_by("number")
            return render(
                request,
                "restaurant/update_table.html",
                {
                    "restaurant_id": restaurant_id,
                    "table_list": table_list,
                    "total_seats": len(table_list),
                },
            )


@login_required
def booking(request: HttpRequest, restaurant_id: int = 0, status: str = None):
    restaurant = None
    if restaurant_id:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == "GET":
        return do_get_request_booking(request, restaurant, status)
    if request.method == "POST":
        date_booking = request.POST.get("date")
        time_booking = request.POST.get("btnradio")
        id_table = request.POST.get("btnradio2")
        table = Table.objects.get(id=id_table)
        date_booking = datetime.strptime(
            date_booking + "-" + time_booking, "%Y-%m-%d-%H:%M"
        )
        date_booking = set_timezone(date_booking)
        Booking.objects.create(date_time=date_booking, client=request.user, table=table)
        return redirect(f"/bookings/{WAITING}")
    if request.method == "PUT":
        data = json.loads(request.body)
        status = data.get("status")
        booking_id = data.get("booking")
        booking = get_object_or_404(Booking, id=booking_id)
        if (
            request.user == booking.client
            or request.user == booking.table.restaurant.owner
        ):
            booking.status = status
            booking.save()
            return JsonResponse({"message": "Update sucessfull"}, status=201)


def get_tables_without_booking(
    restaurant: Restaurant, date_booking: str
) -> list[Table]:
    initial_datetime = datetime.strptime(date_booking, "%Y-%m-%d-%H:%M")
    day_of_week = initial_datetime.strftime("%A")
    day_of_week = DayOfWeek.objects.get(day_of_week=day_of_week)
    tables_without_booking = []
    if day_of_week in restaurant.days_open.all():
        booking_time = timedelta(
            hours=restaurant.booking_time.hour,
            minutes=restaurant.booking_time.minute - 1,
        )
        final_datetime = initial_datetime + booking_time
        initial_datetime = initial_datetime - booking_time
        initial_datetime = set_timezone(initial_datetime)
        final_datetime = set_timezone(final_datetime)
        tables_with_booking = Booking.objects.filter(
            table=OuterRef("pk"),
            date_time__range=[initial_datetime, final_datetime],
            status=WAITING,
        )
        tables_without_booking = Table.objects.filter(restaurant=restaurant).exclude(
            id__in=Subquery(tables_with_booking.values("table"))
        )
    return tables_without_booking


def set_timezone(date: datetime):
    return timezone.make_aware(date, timezone.get_current_timezone())


def get_bookings(
    initial_date: datetime,
    final_date: datetime,
    restaurant: Restaurant,
    status: str = None,
) -> list[Booking]:
    initial_date = set_timezone(initial_date)
    final_date = set_timezone(final_date)
    if status in [0, 1, 2]:
        return Booking.objects.filter(
            date_time__range=[initial_date, final_date],
            table__restaurant=restaurant,
            status=status,
        )
    return Booking.objects.filter(
        date_time__range=[initial_date, final_date],
        table__restaurant=restaurant,
    )


def do_get_request_booking(
    request: HttpRequest, restaurant: Restaurant = None, status: int = None
):
    date_booking = request.GET.get("date")
    if request.user.type_user == CUSTOMER:
        if restaurant:
            tables = get_tables_without_booking(restaurant, date_booking)
            bookings_available = [table.serialize() for table in tables]
            return JsonResponse({"tables": bookings_available}, status=201)
        elif status in [0, 1, 2]:
            bookings = Booking.objects.filter(status=status, client=request.user)
            return render(
                request,
                "restaurant/bookings.html",
                {
                    "bookings": bookings,
                    "target_booking": request.user.first_name,
                    "status": BOOKING_STATUS[status][1].lower(),
                },
            )
    elif request.user == restaurant.owner:
        if date_booking:
            date_fmt = datetime.strptime(date_booking, "%Y-%m-%d")
        else:
            date_fmt = datetime.now()
        initial_datetime = datetime.combine(date_fmt, restaurant.open_hour)
        final_datetime = datetime.combine(date_fmt, restaurant.close_hour)
        return render(
            request,
            "restaurant/bookings.html",
            {
                "bookings": get_bookings(
                    initial_datetime, final_datetime, restaurant, status
                ),
                "restaurant": restaurant,
                "date": date_fmt.strftime("%Y-%m-%d"),
                "min_date": datetime.now().strftime("%Y-%m-%d"),
                "target_booking": restaurant.name,
                "status": BOOKING_STATUS[status][1].lower(),
            },
        )


@login_required
def update_restaurant(request: HttpRequest, restaurant_id: int):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)

    if request.method == "GET":
        restaurant_form = RestaurantForm(request.user.id, instance=restaurant)
        return render(
            request,
            "restaurant/new_restaurant.html",
            {
                "form": restaurant_form,
                "days_of_week": DayOfWeek.objects.all(),
                "restaurant_id": restaurant.id,
                "days_of_work": [day.id for day in restaurant.days_open.all()],
            },
        )
    elif request.method == "POST":
        restaurant_form = RestaurantForm(
            request.user.id, request.POST, request.FILES, instance=restaurant
        )
        restaurant_form.save(commit=True)
        save_days_of_work(request, restaurant)
        url = reverse(f"restaurant")
        return redirect(f"{url}/{restaurant.id}")


@login_required
def user(request: HttpRequest):
    content = {"form": UserForm(instance=request.user), "message": ""}
    page = "restaurant/register.html"
    return render(request, page, content)
