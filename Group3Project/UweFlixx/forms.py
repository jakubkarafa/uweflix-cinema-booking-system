from django import forms
from datetime import datetime
from uweflix.models import *
from django.utils.safestring import mark_safe
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import time
import calendar
from datetime import date
from django import forms
import calendar




class Club_Discount_Form(forms.Form):
    club_rep = forms.ModelChoiceField(
        queryset=ClubRep.objects.all(),
        label="Select Club Rep"
    )
    discount_val = forms.IntegerField(label="Discount Value")

class Club_Reprensative_Search_Form(forms.Form):
    time_range_choices = (
        (None, "Select a statement:"),
        ("Month", "Monthly Statement"),
        ("Year", "Annual Statement")
    )
    club_rep_choices = tuple(
        (club_rep.club_rep_num, club_rep) for club_rep in ClubRep.objects.all()
    )
    club_rep_choice = forms.ChoiceField(choices=club_rep_choices)
    time_range_choice = forms.ChoiceField(choices=time_range_choices)

class User_Form_Creation_customized(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(User_Form_Creation_customized, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

class User_Form_Change_Customize(UserChangeForm):
    class Meta:
        model = User
        fields = ('username','email', 'first_name', 'last_name')

class Club_Representation_Registrate_form(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput())
    class Meta:
        model = ClubRep
        fields = ('club', 'club_rep_num', 'dob')

class Customer_Register_Form(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('dob',)

class pick_date(forms.Form):
    date = forms.DateField(required=False)

class select_date_form(forms.Form):
    startDate = forms.DateField(required=True)
    endDate = forms.DateField(required=False)

class user_Selection_F(forms.Form):
    user_choices = tuple((user, user) for user in User.objects.all())
    user = forms.ChoiceField(choices=user_choices)
    

class access_to_club_form(forms.Form):
    club = forms.ChoiceField(choices=((None, "Select a club:"),) + tuple((club.id, club.name) for club in Club.objects.all()))
    card_number = forms.DecimalField(max_digits=16, decimal_places=0)
    expiry_month = forms.ChoiceField(choices=((i, f"{i:02d}") for i in range(1, 13)))
    expiry_year = forms.ChoiceField(choices=((i, str(i)) for i in range(date.today().year, date.today().year + 15)))

    def clean(self):
        cleaned_data = super().clean()
        club = cleaned_data.get('club')
        card_number = cleaned_data.get('card_number')
        expiry_month = cleaned_data.get('expiry_month')
        expiry_year = cleaned_data.get('expiry_year')

        if not club:
            self.add_error('club', "Club is required.")

        if len(str(int(card_number))) < 16:
            self.add_error('card_number', "Card number is less than 16 digits.")

        expiry_date = date(int(expiry_year), int(expiry_month), calendar.monthrange(int(expiry_year), int(expiry_month))[1])
        if expiry_date < date.today():
            self.add_error('expiry_date', "The expiry date entered has already passed.")

        return cleaned_data

class payment_Ticket_form(forms.Form):
    adult_tickets = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], required=False, initial=0)
    student_tickets = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], required=False, initial=0)
    child_tickets = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(0)], required=False, initial=0)
    total_cost = forms.FloatField(label="Total Cost: ", disabled=True, required=False)
    payment_options = forms.ChoiceField(choices=[
        (None, 'Select an option:'),
        ('nopay', 'Customer: Pay with Card'),
        ('credit', 'Student: Pay with Credit'),
    ])

    def clean(self):
        cleaned_data = super().clean()
        adult_tickets = cleaned_data.get('adult_tickets')
        student_tickets = cleaned_data.get('student_tickets')
        child_tickets = cleaned_data.get('child_tickets')

        if adult_tickets == 0 and student_tickets == 0 and child_tickets == 0:
            self.add_error(None, "You must purchase at least one ticket type.")

        return cleaned_data

class represent_Ticket_payment_form(forms.Form):
    rep_student_tickets = forms.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(10)], required=False, initial=0)
    total_cost = forms.FloatField(label="Total Cost: ", disabled=True, required=False)
    payment_options = forms.ChoiceField(choices=[
        (None, 'Select an option:'),
        ('cCredit', 'Club Reps: Pay with Credit'),
        ('tTab', 'Club Reps: Add to monthly bill'),
    ])

    def clean(self):
        cleaned_data = super().clean()
        student_tickets = cleaned_data.get('student_tickets')

        if student_tickets == 0:
            self.add_error(None, "You must purchase at least one ticket type.")

        return cleaned_data


class user_Selection_F(forms.Form):
    user_choices = tuple((user, user) for user in User.objects.all())
    user = forms.ChoiceField(choices=user_choices)



class Club_addition_form(forms.ModelForm):
    class Meta:
        model = Club
        fields = "__all__"
        exclude = "card_number", "card_expiry_date", "discount_rate"

class Club_representative_add_form(forms.ModelForm):
    class Meta:
        model = ClubRep
        fields = "__all__"
        exclude = "user", "credit", "club_rep_num"

class Club_Representative_User_creation_Form(User_Form_Creation_customized):
    class Meta:
        model = User
        fields = ('first_name', 'last_name',)

class Payment_card_phone(forms.Form):
    month_choices = tuple((i + 1, f"{i + 1:02d}") for i in range(12))
    year_choices = tuple((date.today().year + i, date.today().year + i) for i in range(15))

    card_number = forms.DecimalField(max_digits=16, decimal_places=0)
    expiry_month = forms.ChoiceField(choices=month_choices)
    expiry_year = forms.ChoiceField(choices=year_choices)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.today = date.today()

    def clean(self):
        cleaned_data = super().clean()
        card_number = cleaned_data.get('card_number')
        expiry_month = cleaned_data.get('expiry_month')
        expiry_year = cleaned_data.get('expiry_year')

        if len(str(int(card_number))) < 16:
            self.add_error('card_number', "Card number is less than 16 digits.")

        expiry_date = date(int(expiry_year), int(expiry_month), calendar.monthrange(int(expiry_year), int(expiry_month))[1])
        if expiry_date < self.today:  # Access the instance variable
            self.add_error(None, "The expiry date entered has already passed.")
            return cleaned_data


class Price_changing_page(forms.ModelForm):
   class Meta:
        model = Prices
        fields = "__all__"

class Addition_of_Showings_page(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)
    
class Editing_showing_page(forms.ModelForm):
    class Meta:
        model = Showing
        fields = "__all__"
        exclude = ('remaining_tickets',)

class Film_delete_page(forms.Form):
    film_choices = tuple((film.id, film.title) for film in Film.objects.all())
    film = forms.ChoiceField(choices=((None, "Select a film:"),) + film_choices)

class Screen_add_form(forms.ModelForm):
    age_rating_choices = ()
    class Meta:
        model = Screen
        fields = "__all__"

class Screen_Edit_Page(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ('capacity', 'apply_covid_restrictions')
        widgets = {
        'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Screen capacity'}),
        'apply_covid_restrictions': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }


class Film_editing_form(forms.ModelForm):
    class Meta:
        model = Film
        fields = ('title', 'genre', 'year', 'description', 'poster')

    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    genre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    poster = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
