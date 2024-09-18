from django import forms
from restaurant.models import User, Restaurant


def ajust_form_classes(visible_fields: list[forms.BoundField]) -> None:
    for visible in visible_fields:
        visible.field.widget.attrs["class"] = "form-control col-50 mb-2 "
        if isinstance(visible.field, forms.TypedChoiceField) or isinstance(
            visible.field, forms.ModelChoiceField
        ):
            visible.field.widget.attrs["class"] = "form-select "


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "email",
            "phone_number",
            "type_user",
            "first_name",
            "last_name",
            "password",
        ]
        labels = {"type_user": "You are"}
        widgets = {
            "password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        ajust_form_classes(self.visible_fields())


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            "id",
            "owner",
            "name",
            "address",
            "site",
            "phone",
            "booking_time",
            "open_hour",
            "close_hour",
            "logo",
            "background_image",
            "category",
            "menu",
            "average_price_dollars",
        ]
        labels = {
            "category": "Category of your restaurant ",
            "average_price_dollars": "Average price of plates in dollars:",
        }
        widgets = {
            "booking_time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "open_hour": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "close_hour": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
            "owner": forms.HiddenInput(),
        }

    def __init__(self, user_id: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["owner"].initial = user_id
        self.fields["owner"].disabled = True
        ajust_form_classes(self.visible_fields())
