from email import charset
from pyexpat import model
from tokenize import String
from xml.dom.minidom import CharacterData
from django.db import models
from django.contrib.auth.models import *
from datetime import datetime as dt
import datetime
import random


from django.forms import ValidationError

class User(AbstractUser):
    pass

class Customer(models.Model):  # Student accounts
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField('Date Of Birth')
    credit = models.FloatField(default=0.00)

class Transaction(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, default=None, on_delete=models.SET_DEFAULT)
    date = models.DateField()
    cost = models.FloatField()
    is_settled = models.BooleanField()
    request_to_cancel = models.BooleanField(default=False)
    
    @staticmethod
    def load_new_transactions(transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            return transaction
        except:
            print("No transaction exists")
            
    @classmethod
    def create_new_transaction(cls, cust, cost, is_paid):
        try:
            transaction = cls.objects.create(customer=cust, date=dt.today(), cost=cost, is_settled=is_paid)
            return transaction
        except:
            print("Transaction could not be made.")

    @staticmethod
    def update_existing_transaction(id, **transaction_data):
        try:
            update_fields = {}
            for key, value in transaction_data.items():
                if key in ['customer', 'date', 'cost', 'is_settled']:
                    update_fields[key] = value

            Transaction.objects.filter(pk=id).update(**update_fields)
            return Transaction.objects.get(id=id)
        except:
            print("Error.")

    @staticmethod
    def delete_existing_transaction(id):
        try:
            transaction = Transaction.objects.get(id=id)
            transaction.delete()
        except:
            print("This transaction does not exist, or had an issue being deleted.")



from django.db import models

class Film(models.Model):
    AGE_RATING_CHOICES = [
        ('U', 'U'),
        ('PG', 'PG'),
        ('12', '12'),
        ('12A', '12A'),
        ('15', '15'),
        ('18', '18'),
    ]

    title = models.CharField(max_length=100)
    age_rating = models.CharField(max_length=3, choices=AGE_RATING_CHOICES)
    duration = models.CharField(max_length=3)  # Store duration in minutes only (e.g. 120)
    trailer_desc = models.CharField(max_length=500)
    image = models.ImageField(default="placeholder.png")

    @classmethod
    def create_new_film(cls, title, age_rating, duration, trailer_desc):
        try:
            film = cls.objects.create(title=title, age_rating=age_rating, duration=duration, trailer_desc=trailer_desc)
            return film
        except:
            print("Film could not be added")

    @classmethod
    def read_created_film(cls, id):
        try:
            film = cls.objects.get(id=id)
            return film
        except:
            print("Film could not be found")

    @classmethod
    def delete_existing_film(cls, id):
        try:
            film = cls.objects.get(id=id)
            if not Showing.objects.exists(film=film):
                film.delete()
            else:
                print("The selected Item has showings going on, therefore it cannot be deleted")
        except:
            print("Could not be deleted")

    @classmethod
    def update_existing_film(cls, id, *field_to_edit):
        try:
            for field in field_to_edit:
                if isinstance(field, str):
                    cls.objects.filter(id=id).update(title=field)
                elif isinstance(field, int):
                    cls.objects.filter(id=id).update(age_rating=field)
            return cls.objects.get(id=id)
        except:
            print("Film could not be updated")

    def __str__(self):
        return self.title


from django.db import models

class Screen(models.Model):
    capacity = models.IntegerField()
    apply_covid_restrictions = models.BooleanField(null=True)

    def __str__(self):
        return "Screen " + str(self.id)

    @classmethod
    def create_new_Screen(cls, seats, covid_restrictions):
        try:
            screen = cls.objects.create(capacity=seats, apply_covid_restrictions=covid_restrictions)
            return screen
        except:
            print("Screen cannot be created, perhaps you are missing some parameters?")

    @classmethod
    def read_existing_screen(cls, id):
        try:
            screen = cls.objects.get(id=id)
            return screen
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")

    @classmethod
    def update_EXisting_Screen(cls, id, field_to_edit):
        try:
            if isinstance(field_to_edit, bool):
                cls.objects.filter(id=id).update(apply_covid_restrictions=field_to_edit)
            elif isinstance(field_to_edit, (int, float)):
                cls.objects.filter(id=id).update(capacity=field_to_edit)
            return cls.objects.get(id=id)
        except Exception as e:
            print("Screen cannot be found, perhaps you have entered an invalid field type?")
            print(e)

    @classmethod
    def delete_existing_screen(cls, id):
        try:
            screen = cls.objects.get(id=id)
            screen.delete()
        except:
            print("Screen cannot be found, perhaps you have entered an incorrect id?")



class Showing(models.Model):
    screen = models.ForeignKey(Screen, default=1, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    time = models.DateTimeField()
    remaining_tickets = models.IntegerField(default=150)

    @classmethod
    def newShowing(cls, screen, film, time):
        try:
            showing = cls.objects.create(screen=screen, film=film, time=time, remaining_tickets=screen.capacity)
            if screen.apply_covid_restrictions:
                showing.remaining_tickets = showing.remaining_tickets // 2
                showing.save()
            return showing
        except:
            print("Cannot create this new showing!")

    @classmethod
    def find_existing_showing(cls, id):
        try:
            showing = cls.objects.get(id=id)
            return showing
        except:
            print("No such showing available!.")

    @classmethod
    def modify_existing_showing(cls, id, *showing_data):
        try:
            for data_item in showing_data:
                if isinstance(data_item, Screen):
                    cls.objects.filter(pk=id).update(screen=data_item)
                elif isinstance(data_item, Film):
                    cls.objects.filter(pk=id).update(film=data_item)
                elif isinstance(data_item, float):
                    cls.objects.filter(pk=id).update(time=data_item)
                elif isinstance(data_item, int):
                    cls.objects.filter(pk=id).update(remaining_tickets=data_item)
                elif isinstance(data_item, bool):
                    cls.objects.filter(pk=id).update(apply_covid_restrictions=False)
                else:
                    print(f"Data item {data_item} does not meet the requirements.." +
                          "\n Cannot update this.")
            return cls.objects.get(id=id)
        except:
            print("error")

    @classmethod
    def remove_existing_showing(cls, id):
        try:
            showing = cls.objects.get(id=id)
            showing.delete()
        except:
            print("Showing is deleted, Bye!.")



class Ticket(models.Model):
    transaction = models.ForeignKey(Transaction, default=1, on_delete=models.SET_DEFAULT)
    showing = models.ForeignKey(Showing, default=1, on_delete=models.SET_DEFAULT)
    ticket_type = models.CharField(max_length=7)

    @classmethod
    def create_ticket(cls, trans, show, ticket_type):
        try:
            ticket = cls.objects.create(transaction=trans, showing=show, ticket_type=ticket_type)
            return ticket
        except:
            print("Error, wrong parameter!")

    @classmethod
    def find_ticket(cls, id):
        try:
            ticket = cls.objects.get(id=id)
            return ticket
        except:
            print("Ticket cannot be found, perhaps you have entered an incorrect id?")

    @classmethod
    def modify_ticket(cls, id, *fields_to_edit):
        try:
            for field in fields_to_edit:
                if isinstance(field, Transaction):
                    cls.objects.filter(id=id).update(transaction=field)
                elif isinstance(field, Showing):
                    cls.objects.filter(id=id).update(showing=field)
                elif isinstance(field, str):
                    cls.objects.filter(id=id).update(ticket_type=field)
            return cls.objects.get(id=id)
        except:
            print("Cannot update, wrong field type!")

    @classmethod
    def delete_ticket(cls, id):
        try:
            ticket = cls.objects.get(id=id)
            ticket.delete()
        except:
            print("Ticket cannot be found, perhaps you have entered an invalid id?")



class Club(models.Model):
    name = models.CharField(max_length=65)
    street_number = models.IntegerField()
    street = models.CharField(max_length=66)
    city = models.CharField(max_length=43)
    post_code = models.CharField(max_length=10)
    landline_number = models.CharField(max_length=13)
    mobile_number = models.CharField(max_length=13)
    email = models.EmailField(max_length=1333)
    card_number = models.IntegerField(blank=True, null=True)
    card_expiry_date = models.DateField(blank=True, null=True)
    discount_rate = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    @classmethod
    def create_new_club_exe(cls, club_name, address_street_num, address_street, address_city, address_postcode, contact_landline, contact_mobile, contact_email):
        try:
            club = cls.objects.create(name=club_name, street_number=address_street_num, street=address_street, city=address_city, post_code=address_postcode, landline_number=contact_landline, mobile_number=contact_mobile, email=contact_email)
            return club
        except:
            print("Cannot Create ClUb!")

    @classmethod
    def load_r_existing_club(cls, id):
        try:
            club = cls.objects.get(id=id)
            return club
        except:
            print("This club does not exists! Try again!")

    @classmethod
    def update_existing_club(cls, id, **club_data):
        try:
            update_fields = {}
            for key, value in club_data.items():
                if key in ['name', 'card_number', 'card_expiry_date', 'discount_rate']:
                    update_fields[key] = value

            cls.objects.filter(pk=id).update(**update_fields)
            return cls.objects.get(id=id)
        except:
            print("Error ")

    @classmethod
    def delete_existing_club(cls, id):
        try:
            club = cls.objects.get(id=id)
            club.delete()
        except:
            print("Can't delete something that doesn't exists :)")



class ClubRep(Customer):
    club = models.ForeignKey(Club, null=True, on_delete=models.CASCADE)
    club_rep_num = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.club_rep_num} - {self.user.first_name} {self.user.last_name}"

class Prices(models.Model):
    adult = models.FloatField(default=0.0)
    student = models.FloatField(default=0.0)
    child = models.FloatField(default=0.0)

    @classmethod
    def update_tickets_price(cls, adult, student, child):
        cls.objects.create(adult=adult, student=student, child=child)

    @classmethod
    def load_Existing_price(cls):
        current_prices = cls.objects.last()
        return current_prices.adult, current_prices.student, current_prices.child

class Account(models.Model):
    random_num_generator = models.IntegerField(blank=True, null=True)
    first_initial = models.CharField(max_length=1, default='')
    last_name = models.CharField(max_length=35)
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    expiry_year = models.IntegerField(default=timezone.now().year)
    expiry_month = models.CharField(max_length=2, default='')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def New_ACcount_saved(self, *args, **kwargs):
        if not self.random_num_generator:
            self.random_num_generator = random.randint(0000, 9999)
        super().save(*args, **kwargs)