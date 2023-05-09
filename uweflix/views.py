from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import *
import calendar
from .models import *
from django.http import Http404
from django.utils import timezone
from datetime import datetime as dt
from .forms import *
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group
from django.contrib import messages
import re
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
import requests
from tmdbv3api import TMDb
from tmdbv3api import Movie



def change_account_page(request):
    form = user_Selection_F()
    context = {
        'form':form
    }
    return render(request, 'uweflix/change_account_page.html', context)


def update_accounts_form_page(request):  
    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }

    return render(request, 'uweflix/update_accounts_form_page.html', context)

@user_passes_test(lambda user: user.is_staff)
@login_required 
def add_user(request):
    if request.method == "POST":
        try:
            first_name = request.POST['first_name']
            if not first_name or any(char.isdigit() for char in first_name):
                raise ValueError("Invalid first name")
            last_name = request.POST['last_name']
            if not last_name or any(char.isdigit() for char in last_name):
                raise ValueError("Invalid last name")
            username = request.POST['username']
            if not username:
                raise ValueError("Please enter a valid username")
            email = request.POST['email']
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Invalid email")

            user = User(first_name=first_name, last_name=last_name,
                        username=username, email=email)
            user.save()
            messages.success(request, "User added successfully")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('update_accounts_form_page')
    else:
        pass

    user_list = User.objects.all()
    context = {
        'user_list': user_list
    }
    return render(request, 'uweflix/update_accounts_form_page.html', context)


def delete_user(request, myid):  
    user = User.objects.get(id=myid)
    user.delete()
    messages.info(request, 'USER DELETED SUCCESSFULLY')
    return redirect(update_accounts_form_page)


def edit_user(request, myid):  
    sel_user = User.objects.get(id=myid)
    user_list = User.objects.all()
    context = {
        'sel_user': sel_user,
        'user_list': user_list
    }
    return render(request, 'uweflix/update_accounts_form_page.html', context)


def update_user(request, myid): 
    user = User.objects.get(id=myid)
    user.first_name = request.POST['first_name']
    user.Last_name = request.POST['last_name']
    user.username = request.POST['username']
    user.email = request.POST['email']
    user.save()
    messages.info(request, "THE USER HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('update_accounts_form_page')

def manage_club_account(request): 
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/manage_club_account.html', context)


def manage_club_account(request):  
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/manage_club_account.html', context)


def add_clubs(request): 
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        street_number = request.POST.get('street_number', '').strip()
        street = request.POST.get('street', '').strip()
        city = request.POST.get('city', '').strip()
        post_code = request.POST.get('post_code', '').strip()
        landline_number = request.POST.get('landline_number', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        email = request.POST.get('email', '').strip()

        try:
            
            if not name:
                raise ValueError("Please enter a valid name.")

            if not street_number or not street_number.isdigit():
                raise ValueError("Please enter a valid street number.")

            if not street:
                raise ValueError("Please enter a valid street name.")

            if not city:
                raise ValueError("Please enter a valid city name.")

            if not post_code or not post_code.isalnum():
                raise ValueError("Please enter a valid post code.")

            if landline_number and not landline_number.isdigit():
                raise ValueError("Please enter a valid landline number.")

            if mobile_number and not mobile_number.isdigit():
                raise ValueError("Please enter a valid mobile number.")

            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                raise ValueError("Please enter a valid email.")

            club = Club(name=name, street_number=street_number, street=street, city=city,
                        post_code=post_code, landline_number=landline_number, mobile_number=mobile_number, email=email)
            club.save()
            messages.success(request, "Club added successfully")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('manage_club_account')

    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }
    return render(request, 'uweflix/manage_club_account.html', context)


def delete_clubs(request, myid):  
    clubs = Club.objects.get(id=myid)
    clubs.delete()
    messages.info(request, 'CLUB DELETED SUCCESSFULLY')
    return redirect(manage_club_account)


def edit_clubs(request, myid):
    sel_clubs = Club.objects.get(id=myid)
    club_list = Club.objects.all()
    context = {
        'sel_clubs': sel_clubs,
        'club_list': club_list
    }
    return render(request, 'uweflix/manage_club_account.html', context)


def update_clubs(request, myid):
    clubs = Club.objects.get(id=myid)
    clubs.name = request.POST['name']
    clubs.street_number = request.POST['street_number']
    clubs.street = request.POST['street']
    clubs.city = request.POST['city']
    clubs.post_code = request.POST['post_code']
    clubs.landline_number = request.POST['landline_number']
    clubs.mobile_number = request.POST['mobile_number']
    clubs.email = request.POST['email']
    clubs.save()
    messages.info(request, "THE USER HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('manage_club_account')


def create_account(request):  
    club_list = Club.objects.all()
    context = {
        'club_list': club_list
    }

    return render(request, 'uweflix/create_account.html', context)


def modify_delete_accounts(request): 
    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'account_list': account_list,
        'club_list': club_list

    }

    return render(request, 'uweflix/modify_delete_accounts.html', context)


def create_account(request):
    if request.method == "POST":
        try:
            random_num_generator = request.POST.get(
                'random_num_generator', None)
            if random_num_generator:
                random_num_generator = int(random_num_generator)
            else:
                random_num_generator = random.randint(1000, 9999)
            first_initial = request.POST.get('first_initial', None)
            if not first_initial or any(char.isdigit() for char in first_initial) or len(first_initial) != 1:
                raise ValueError("Invalid first Initial")
            last_name = request.POST.get('last_name', None)
            if not last_name or any(char.isdigit() for char in last_name):
                raise ValueError("Invalid last name")
            club_id = request.POST.get('club', None)
            club = Club.objects.get(id=club_id)
            card_number = request.POST.get('card_number', None)
            expiry_month = request.POST.get('expiry_month', None)
            expiry_year = request.POST.get('expiry_year', None)
            current_year = datetime.now().year
            if not expiry_month.isdigit() or int(expiry_month) > 12:
                raise ValueError("Invalid expiry month")
            if not expiry_year.isdigit() or int(expiry_year) < current_year:
                raise ValueError("Invalid expiry year")

            account = Account(random_num_generator=random_num_generator, first_initial=first_initial, last_name=last_name, club=club,
                              card_number=card_number, expiry_month=expiry_month, expiry_year=expiry_year)
            account.save()
            messages.success(
                request, f"Account added successfully, the unique account number is: {random_num_generator}")
        except ValueError as e:
            messages.error(request, str(e))
            return redirect('create_account')
    else:
        random_num_generator = random.randint(1000, 9999)

    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'account_list': account_list,
        'club_list': club_list,
        'random_num_generator': random_num_generator
    }
    return render(request, 'uweflix/create_account.html', context)


def delete_account(request, myid):
    account = Account.objects.get(id=myid)
    account.delete()
    messages.info(request, 'ACCOUNT DELETED SUCCESSFULLY')
    return redirect(modify_delete_accounts)


def edit_account(request, myid): 
    sel_account = Account.objects.get(id=myid)
    account_list = Account.objects.all()
    club_list = Club.objects.all()
    context = {
        'sel_account': sel_account,
        'account_list': account_list,
        'club_list': club_list
    }
    return render(request, 'uweflix/modify_delete_accounts.html', context)


def update_account(request, myid): 
    account = Account.objects.get(id=myid)
    account.first_initial = request.POST['first_initial']
    account.last_name = request.POST['last_name']
    club_id = request.POST['club']
    account.club = Club.objects.get(id=club_id)
    account.card_number = request.POST['card_number']
    account.expiry_month = request.POST['expiry_month']
    account.expiry_year = request.POST['expiry_year']
    account.save()
    messages.info(request, "THE ACCOUNT HAS BEEN UPDATED SUCCESSFULLY")
    return redirect('modify_delete_accounts')


def view_account(request):
    return render(request, 'uweflix/modify_delete_accounts.html')

def home(request):
    return render(request, 'uweflix/index.html')
    

def clubdiscount(request):
    context = {}
    form = Club_Discount_Form()
    club_reps = ClubRep.objects.all()

    if request.method == "POST":
        form = Club_Discount_Form(request.POST)
        if form.is_valid():
            club_rep = form.cleaned_data['club_rep']
            discount_value = form.cleaned_data['discountValue']

            club = club_rep.club
            club.discount_rate = discount_value
            club.save()

            messages.success(request, f'Discount of {discount_value}% applied to {club_rep.user.first_name} {club_rep.user.last_name} of {club.name}.')

    context['form'] = form
    context['club_reps'] = club_reps
    return render(request, "uweflix/discount_for_club_page.html", context)


def main_home_page(request):
    transactions = Transaction.objects.filter(date = dt.today())
    transactions = transactions.count()
    context = {
        'transactions': transactions
    }
    return render(request, 'uweflix/main_home_page.html', context)


def club_rep_home(request):
    return render(request, 'uweflix/club_rep_home.html')


def cinema_manager_home(request):
    if request.session['user_group'] == "Cinema Manager":
        context = {}
        restrictions = Screen.objects.first().apply_covid_restrictions
        context = {
            'restrictions_bool' : restrictions
        }
        if request.method == "POST":
            for screen in Screen.objects.all():
                Screen.update_EXisting_Screen(screen.id, not screen.apply_covid_restrictions)
                context = {
                    'restrictions_bool' : not screen.apply_covid_restrictions
                }
            redirect('cinema_manager_home')
        return render(request, 'uweflix/cinema_manager_home.html', context)
    else:
        return redirect('/')

def student_home(request):
    return render(request, 'uweflix/student_home.html')

def viewings_page(request):
    print("User ID in session:", request.session.get('user_id'))
    films = Film.objects.all()
    context = {'films':films}
    return render(request, 'uweflix/viewings_page.html', context)


def showings(request, film):
    print("User ID in session:", request.session.get('user_id'))
    showings = Showing.objects.filter(film=film).order_by('time')
    film = Film.objects.get(pk=film)
    context = {'showings':showings, 'film':film}
    return render(request, 'uweflix/showings.html', context)


@api_view(['GET','POST'])
def films_endpoint(request):
    if request.method == 'GET':
        films = Film.objects.all()
        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = FilmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) 
def specific_film_endpoint(request, pk): 
    try: 
        film = Film.objects.get(pk=pk) 
    except film.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = FilmSerializer(film) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = FilmSerializer(film, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        film.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


def add_new_movie(request):
    form = Film_delete_page()
    context = {"form": form}
    if request.method == "POST":
        messages.set_level(request, messages.ERROR) 
        ages = {"U", "PG", "12", "12A", "15", "18"}
        title = request.POST.get('title')
        age_rating = request.POST.get('age_rating')
        duration = request.POST.get('duration')
        trailer_desc = request.POST.get('trailer_desc')
        if duration is not None and duration.isdigit():
            if(age_rating in ages):
                film = Film()
                film.title = title
                film.age_rating = age_rating
                film.duration = duration
                film.trailer_desc = trailer_desc
                try:
                    image = request.FILES.get('image')
                    film.image = image
                except:
                    pass
                messages.success(request, 'Film added successfully!')
                film.save()        
            else:
                messages.error(request, 'Invalid Age Rating')
        else:
            messages.error(request, 'Duration is not a valid number')
        if 'delete_film' in request.POST: 
            form = Film_delete_page(request.POST)
            if form.is_valid():
                film_id = form.cleaned_data.get('film')
                if film_id is not None:
                    try:
                        film = Film.objects.get(id=film_id)
                        film.delete()
                        messages.success(request, 'Film deleted successfully!')
                    except Film.DoesNotExist:
                        messages.error(request, 'Film does not exist')
                else:
                    messages.error(request, 'Invalid Film ID')
        if 'edit_film' in request.POST:
            ages = {"U", "PG", "12", "12A", "15", "18"}
            title = request.POST.get("edit_title")
            age_rating = request.POST.get("edit_age_rating")
            duration = request.POST.get("edit_duration")
            trailer_desc = request.POST.get("edit_trailer_desc")
            film_id = request.POST.get("film")
            try:
                film = Film.objects.get(id=film_id)
                if duration is not None and duration.isdigit():
                    if age_rating in ages:
                        film.title = title
                        film.age_rating = age_rating
                        film.duration = duration
                        film.trailer_desc = trailer_desc
                        try:
                            image = request.FILES.get('edit_image')
                            film.image = image
                        except:
                            pass
                        film.save()
                        messages.success(request, 'Film updated successfully!')
                    else:
                        messages.error(request, 'Invalid Age Rating')
                else:
                    messages.error(request, 'Duration is not a valid number')
            except Film.DoesNotExist:
                messages.error(request, 'Film does not exist')
    return render(request, 'uweflix/add_new_movie.html', context)


def edit_film(request):
    form = Film_editing_form()
    context = {"form": form}
    if request.method == "POST":
        ages = {"U", "PG", "12", "12A", "15", "18"}
        title = request.POST.get("title")
        age_rating = request.POST.get("age_rating")
        duration = request.POST.get("duration")
        trailer_desc = request.POST.get("trailer_desc")
        film = None
        if duration is not None and duration.isdigit():
            if age_rating in ages:
                try:
                    film = Film.objects.get(title=title)
                    film.age_rating = age_rating
                    film.duration = duration
                    film.trailer_desc = trailer_desc
                    try:
                        image = request.FILES.get("image")
                        film.image = image
                    except:
                        pass
                    film.save()
                except Film.DoesNotExist:
                    print("Film does not exist")
            else:
                print("Invalid Age Rating")
        else:
            print("Duration is not a valid number")
        if film:
            form = Film_editing_form(instance=film)
    context["form"] = form
    return render(request, "uweflix/add_new_movie.html", context)


@api_view(['GET','POST'])
def screens_endpoint(request):
    if request.method == 'GET':
        screens = Screen.objects.all()
        serializer = ScreenSerializer(screens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ScreenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) 
def specific_screen_endpoint(request, pk): 
    try: 
        screen = Screen.objects.get(pk=pk) 
    except screen.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = ScreenSerializer(screen) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = ScreenSerializer(screen, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        screen.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


def New_screen_addition_page(request):
    context = {}
    form = Screen_add_form()
    selected_screen = None
    form1 = Screen_Edit_Page()
    screens = Screen.objects.all()
    options = [screen.id for screen in screens]
    if screens:
        context['screens'] = screens
        context['options'] = options
    if request.method == "POST":
        form = Screen_add_form(request.POST)
        if form.is_valid():
            capacity = form.cleaned_data['capacity']
            covid_restrictions = form.cleaned_data['apply_covid_restrictions']
            screen = Screen(capacity=capacity, apply_covid_restrictions=covid_restrictions)
            screen.save()
            return redirect('New_screen_addition_page')
            
        if 'edit_screen' in request.POST:
            capacity = request.POST.get('capacity')
            covid_restrictions = request.POST.get('apply_covid_restrictions')
            try:
                selected_screen = Screen.objects.get(id=screen_id)
                if capacity is not None and capacity.isdigit():
                    screen_id = Screen.objects.get(id=id)
                    screen_id.capacity = capacity
                    screen_id.apply_covid_restrictions = covid_restrictions
                selected_screen = Screen.objects.get(id=screen_id)
                form1 = Screen_Edit_Page(request.POST, instance=selected_screen)
            except Screen.DoesNotExist:
                    print("Screen does not exist")
            if screen_id:
                form = Film_editing_form(instance=screen_id)

    context['form'] = form
    context['form1'] = form1
    context['selected_screen'] = selected_screen
    return render(request, 'uweflix/New_screen_addition_page.html', context)


@api_view(['GET','POST']) 
def showings_endpoint(request):
    if request.method == 'GET':
        showings = Showing.objects.all()
        serializer = ShowingSerializer(showings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ShowingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def add_new_showing_screen(request):
    context = {}
    form = Addition_of_Showings_page
    showings = Showing.objects.all()
    options = [showing.id for showing in showings]
    if showings:
        context['options'] = options
    if request.method == "POST":
        form = Addition_of_Showings_page(request.POST)
        if form.is_valid():
            screen = form.cleaned_data['screen']
            film = form.cleaned_data['film']
            time = form.cleaned_data['time']
            Showing.newShowing(screen,film,time)
            messages.success(request, f"Successfully added: Showing *{film}* Screen *{screen}* at *{time}*")
    context['form'] = form
    return render(request, 'uweflix/add_new_showing_screen.html', context)

def update_showings_page(request, showing_id):
    form = Editing_showing_page()
    context = {"form":form}
    showing = get_object_or_404(Showing, id=showing_id)
    if 'update_showings_page' in request.POST:
        screen = request.POST.get("Screen")
        film = request.POST.get("Film")
        time = request.POST.get("Time")
        try:
            showing = Film.objects.get(id=showing_id)
            if time is not None:
                showing.screen = screen
                showing.film = film
                showing.time = time       
                if form.is_valid():
                    form.save()
                showing.save()
                messages.success(request, f"Successfully updated: Showing *{film}* Screen *{screen}* at *{time}*")
            else:
                messages.error(request, 'Invalid time')
        except Showing.DoesNotExist:
                messages.error(request, "Showing doesn't exists")
    context['form'] = form
    return render(request, 'uweflix/update_showings_page.html', context)
def registerPage(request):
    form = User_Form_Creation_customized()
    customer_form = Customer_Register_Form()
    context = {
        'form': form,
        'customer_form': customer_form
    }
    if request.method == 'POST':
        form = User_Form_Creation_customized(request.POST)
        customer_form = Customer_Register_Form(request.POST)
        
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords doesn't match")
        else:
            if form.is_valid():
                if customer_form.is_valid():
                    dob = customer_form.cleaned_data['dob']
                    user=form.save()
                    user.is_active = False
                    user.save()
                    student = Customer.objects.create(user=user, dob=dob)
                    group = Group.objects.get(name='Student')
                    group.user_set.add(user)
                    context['confirm'] = "Your request has been received."
                    return render(request, 'uweflix/register.html', context)
    return render(request, 'uweflix/register.html', context)



def login(request):
    if request.method == 'POST':
        un = request.POST['username'] 
        pw = request.POST['password'] 
        user = authenticate(username=un, password=pw)
        if user is not None:
            request.session['user_name'] = user.username
            request.session['user_id'] = user.id
            messages.success(request, "Welcome!")
            if user.groups.filter(name='Student').exists():
                request.session['user_group'] = "Student"
                request.session['credit'] = Customer.objects.get(user=user.id).credit
                return redirect ('student_home')
            elif user.groups.filter(name='Club Rep').exists():
                request.session['user_group'] = "Club Rep"
                request.session['credit'] = ClubRep.objects.get(user=user).credit
                return redirect ('club_rep_home')
            elif user.groups.filter(name='Account Manager').exists():
                request.session['user_group'] = "Account Manager"
                return redirect ('main_home_page')
            elif user.groups.filter(name='Cinema Manager').exists():
                request.session['user_group'] = "Cinema Manager"
                return redirect ('cinema_manager_home')
            
        else:
            messages.error(request, "Bad Credentials")
    return render(request, "uweflix/login.html")

def logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
        del request.session['user_group']
        del request.session['credit']
    except KeyError:
        pass
    finally:
        return redirect("/login/")

def userpage(request):
    context = {}
    return render(request, 'uweflix/user.html', context)




def payment(request, showing):

    if 'user_id' in request.session:
        if request.session['user_group'] == "Club Rep":
            return redirect('payment_page_for_representative', showing=showing)

    adult,student,child=Prices.load_Existing_price()

    showing = Showing.objects.get(id=showing)
    form = payment_Ticket_form()
    context = {
        "showing": showing,
        "form": form,
        "adult_price": adult,
        "student_price": student,
        "child_price": child
    }

    if request.method == 'POST':
        form = payment_Ticket_form(request.POST)
        print("Form is not valid")
        if form.is_valid():
            print("Form is valid")
            total_cost_data = form["total_cost"].data
            print("Total cost data:", total_cost_data)
            try:
                total_cost = float(total_cost_data)
            except ValueError:
                total_cost = 0.0



            adult_tickets = int(form["adult_tickets"].data)
            student_tickets = int(form["student_tickets"].data)
            child_tickets_data = form["child_tickets"].data
            child_tickets = int(child_tickets_data) if child_tickets_data is not None else 0

            total_tickets = adult_tickets + student_tickets + child_tickets
            payment_option = form.cleaned_data.get("payment_options")
            print("Payment option data:", payment_option)
            if showing.remaining_tickets < total_tickets: 
                print("Not enough tickets remaining to make this booking.")
                return render(request, "uweflix/error.html")
            else:
                if 'user_id' in request.session:  
                    user_type = request.session['user_group']
                    if (user_type == "Student"):
                        #Club reps and students
                        user = Customer.objects.get(user=request.session['user_id'])
                        print("User credit: ", user.credit)
                        print("Total cost: ", total_cost)
                        print("Payment option: ", payment_option)

                        if payment_option == 'credit' and float(user.credit) >= float(total_cost):
                            user.credit -= total_cost
                            print("Processing credit payment")
                            request.session['credit'] = user.credit
                            print("Processing credit payment")
                            user.save()
                            print("User saved")
                            paying = True

                        elif payment_option == 'nopay' and float(user.credit) >= float(total_cost):
                            return redirect(f'/card_payment_form/?user={user.id}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                        else:
                            print("DEBUG: Error condition triggered")
                            context = {'error': "Credit error: You do not have sufficient credit to make this order, please add funds and try again."}
                            return render(request, "uweflix/error.html", context)
                    else:
                        context = {'error': "Account based error: Your account type is not permitted to purchase tickets. Please change accounts and try again."}
                        return render(request, "uweflix/error.html", context)
                elif payment_option == "nopay":  
                    return redirect(f'/card_payment_form/?user={0}&cost={total_cost}&adult={adult_tickets}&student={student_tickets}&child={child_tickets}&showing={showing.id}')
                else:
                    context = {'error': "You may only make purchases via credit card.."}
                    return render(request, "uweflix/error.html", context)
                new_transaction = Transaction.create_new_transaction(user, total_cost, paying)
                print("New transaction created")
                for i in range(adult_tickets):
                    Ticket.create_ticket(new_transaction, showing, "adult")
                for i in range(student_tickets):
                    Ticket.create_ticket(new_transaction, showing, "student")
                for i in range(child_tickets):
                    Ticket.create_ticket(new_transaction, showing, "child")

                showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
                print("Remaining tickets updated")
                showing.save()
                print("Showing saved")
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
                if showing.screen.apply_covid_restrictions:
                    request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
                print("Session data updated")
                return redirect('/thanks')
        else:
            return render(request, 'uweflix/payment.html', context={'form':form, "showing": showing})
        print("Method is not POST")
    return render(request, 'uweflix/payment.html', context)


def card_payment_form(request):
    form = Payment_card_phone()
    context = {
        'user': request.GET.get('user'),
        'cost': request.GET.get('cost'),
        'adult': request.GET.get('adult'),
        'student': request.GET.get('student'),
        'child': request.GET.get('child'),
        'showing': request.GET.get('showing'),
        'form': form
    }

    if request.method == "POST":
        form = Payment_card_phone(request.POST)
        if form.is_valid():
            id = int(context['user'])
            user = None
            if id == 0:
                pass
            else:
                user = Customer.objects.get(id=context['user'])
            total_cost = float(context['cost'])
            adult_tickets = int(context['adult'])
            child_tickets = int(context['child'])
            student_tickets = int(context['student'])
            showing = Showing.objects.get(pk=int(context['showing']))
            new_transaction = Transaction.objects.create(customer=user, cost=total_cost, is_settled=True, date=datetime.date.today())
            for i in range(adult_tickets):
                Ticket.objects.create(transaction=new_transaction, showing=showing, ticket_type="adult")
            for i in range(student_tickets):
                Ticket.create_ticket(new_transaction, showing, "student")
            for i in range(child_tickets):
                Ticket.create_ticket(new_transaction, showing, "child")
            showing.remaining_tickets -= (adult_tickets + student_tickets + child_tickets)
            showing.save()
            request.session['screen'] = showing.screen.id
            request.session['transaction'] = new_transaction.id
            request.session['film'] = showing.film.title
            request.session['age_rating'] = showing.film.age_rating
            request.session['date'] = showing.time.strftime("%d/%m/%y")
            request.session['time'] = showing.time.strftime("%H:%M")
            request.session['successful_purchase'] = True
            request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
            if showing.screen.apply_covid_restrictions:
                request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
            return redirect('/thanks')
        else:
            return render(request, "uweflix/card_payment_form.html", {'form': form})

    return render(request, "uweflix/card_payment_form.html", context)


def payment_page_for_representative(request, showing):
    showing = Showing.objects.get(id=showing)
    form = represent_Ticket_payment_form()
    rep = ClubRep.objects.get(user_id=request.session["user_id"])
    discountRate = rep.club.discount_rate
    adult,student,child=Prices.load_Existing_price()
    context = {
        "showing": showing,
        "form": form,
        "discount_rate": discountRate,
        "student_price" : student
    }
    if request.method == 'POST':
        form = represent_Ticket_payment_form(request.POST)
        if form.is_valid():
            print("Valid")
            total_cost_data = form["total_cost"].data
            try:
                total_cost = float(total_cost_data)
            except ValueError:
                total_cost = 0.0
            student_tickets = int(form["rep_student_tickets"].data)
            total_tickets = student_tickets
            payment_option = form.cleaned_data.get("payment_options")
            print("Payment option data:", payment_option)
            if showing.remaining_tickets < total_tickets: 
                print("Not enough tickets remaining to make this booking.")
                return render(request, "uweflix/error.html")
            else:
                user_type = request.session['user_group']
                user = Customer.objects.get(user=request.session['user_id'])
                print("User credit: ", user.credit)
                print("Total cost: ", total_cost)
                print("Payment option: ", payment_option)
                print("DEBUG: payment_option:", payment_option)
                if payment_option == 'cCredit' and float(user.credit) >= float(total_cost):
                    user.credit -= total_cost
                    print("Processing credit payment")
                    request.session['credit'] = user.credit
                    print("Processing credit payment")
                    user.save()
                    paying = True
                elif user_type == "Club Rep" and payment_option == "tTab":
                    print("Payment option: ", payment_option)
                    paying = False
                else:
                    print("DEBUG: user credit:", user.credit, "total cost:", total_cost) 
                    context = {'error': "Credit error: You do not have sufficient credit to make this order, please add funds and try again."}
                    return render(request, "uweflix/error.html", context)
                new_transaction = Transaction.create_new_transaction(user, total_cost, paying)
                for i in range(student_tickets):
                    ticket = Ticket(transaction=new_transaction, showing=showing, ticket_type="student")
                    ticket.save()
                showing.remaining_tickets -= student_tickets
                showing.save()
                request.session['screen'] = showing.screen.id
                request.session['transaction'] = new_transaction.id
                request.session['film'] = showing.film.title
                request.session['age_rating'] = showing.film.age_rating
                request.session['date'] = showing.time.strftime("%d/%m/%y")
                request.session['time'] = showing.time.strftime("%H:%M")
                request.session['successful_purchase'] = True
                request.session['covid_restrictions'] = showing.screen.apply_covid_restrictions
                if showing.screen.apply_covid_restrictions:
                    request.session['allocated_seat'] = showing.screen.capacity - showing.remaining_tickets
                return redirect('/thanks')
        else:
            print("invalid")
            return render(request, 'uweflix/payment_page_for_representative.html', context={'form':form, "showing": showing})
    return render(request, 'uweflix/payment_page_for_representative.html', context)


def thanks(request):
    if 'successful_purchase' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_purchase']
    return render(request, "uweflix/thanks.html")


def error(request):
    return render(request, "uweflix/error.html")


def topup(request):
    if 'user_group' in request.session:
        if request.session['user_group'] == "Club Rep":
            userObject = ClubRep
        elif request.session['user_group'] == "Student":
            userObject = Customer
        else:
            return redirect('home') 
        if request.method == 'POST':
            topUpValue = request.POST.get("topUpValue")
            loggedInRep = userObject.objects.get(user = request.session['user_id'])
            loggedInRep.credit = loggedInRep.credit + round(float(topUpValue), 2)
            request.session['credit'] = loggedInRep.credit
            loggedInRep.save()
        return render(request, "uweflix/topup.html")
    else:
        return redirect('home')


def view_accounts(request):
    return render(request, "uweflix/view_accounts.html")


def daily_transactions(request):
    form = pick_date()
    titleText = "Please select a day to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        form = pick_date(request.POST)
        if form.is_valid():
            selectedDate = dt.today()
            if "search" in request.POST:
                selectedDate = form.cleaned_data['date']
            elif "today" in request.POST:
                selectedDate = dt.today()
            transaction_list = Transaction.objects.filter(date = selectedDate)
            if not transaction_list:
                titleText = f"There were no transactions made on {str(selectedDate)}"
                context = {
                    'form': form,
                    'title_text': titleText
                }
            else:
                context = {
                    'selected_date': selectedDate,
                    'transaction_list': transaction_list,
                    'form': form
                }
        return render(request, "uweflix/daily_transactions.html", context)
    else:
        return render(request, "uweflix/daily_transactions.html", context)


def customer_statements(request):
    form = Club_Reprensative_Search_Form()
    context = {'form': form}
    if request.method == "POST":
        form = Club_Reprensative_Search_Form(request.POST)
        if form.is_valid():
            clubrep = ClubRep.objects.get(
                club_rep_num=form.cleaned_data['clubrep_choice']
            )
            trange = form.cleaned_data['timerange_choice']
            if trange == 'Month':
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year=dt.now().year,
                    date__month=dt.now().month,

                )
            elif trange == "Year":
                transaction_list = Transaction.objects.filter(
                    customer=clubrep,
                    date__year=dt.now().year,
                )
            context = {
                'club_rep_num': clubrep.club_rep_num,
                'club_name': clubrep.club.name,  
                'transaction_list': transaction_list,
                'form': form,

            }
        return render(request, 'uweflix/customer_statements.html', context)
    else:
        return render(request, 'uweflix/customer_statements.html', context)


def payment_settle_page(request):
    context = {}
    if request.session["user_group"] == "Club Rep":
        club_rep = ClubRep.objects.get(user_id=request.session["user_id"])
        transaction_list = Transaction.objects.filter(
                customer=club_rep,
                date__year = dt.now().year,
                date__month = dt.now().month,
                is_settled = False
            )
        context = {
            'transactions': transaction_list,
            'club_rep': club_rep.club_rep_num
            }
        if request.method == "POST":
            for transaction in transaction_list:
                transaction.is_settled = True
                transaction.save()
                return redirect('payment_settle_page')   
        return render(request, 'uweflix/payment_settle_page.html', context)
    else:
        return redirect('home')


def set_payment_details(request):
    form = access_to_club_form()
    context = {'form': form}
    if request.method == "POST":
        form = access_to_club_form(request.POST)
        if form.is_valid():
            club_id = form.cleaned_data['club']
            club_obj = Club.objects.get(id=club_id)
            club_obj.card_number = form.cleaned_data['card_number']
            month = form.cleaned_data['expiry_month']
            year = form.cleaned_data['expiry_year']
            formatted_date = f"{year}-{month}-{calendar.monthrange(int(year), int(month))[1]}"
            club_obj.card_expiry_date = formatted_date
            club_obj.save()
            club_name = club_obj.name
            card_number = form.cleaned_data['card_number']
            expiry_month = form.cleaned_data['expiry_month']
            expiry_year = form.cleaned_data['expiry_year']
            success_message = True
            context.update({'success_message': success_message,
                            'club_name': club_name,
                            'card_number': card_number,
                            'expiry_month': expiry_month,
                            'expiry_year': expiry_year})
        else:
            context = {'form': form}
    return render(request, "uweflix/set_payment.html", context)


@api_view(['GET','POST'])
def clubs_endpoint(request):
    if request.method == 'GET':
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = ClubSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE']) 
def specific_club_endpoint(request, pk): 
    try: 
        club = Club.objects.get(pk=pk) 
    except club.DoesNotExist: 
        return Response(status=status.HTTP_404_NOT_FOUND) 
    if request.method == 'GET': 
        serializer = ClubSerializer(club) 
        return Response(serializer.data) 
    elif request.method == 'PUT': 
        serializer = ClubSerializer(club, data=request.data) 
        if serializer.is_valid(): 
            serializer.save() 
            return Response(serializer.data) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    elif request.method == 'DELETE': 
        club.delete() 
        return Response(status=status.HTTP_204_NO_CONTENT)


def new_club_add_page(request):
    context = {}
    form = Club_addition_form()
    if request.method == "POST":
        form = Club_addition_form(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            clubName = form.cleaned_data['name']
            clubStreetNumber = form.cleaned_data['street_number']
            clubStreet = form.cleaned_data['street']
            clubCity = form.cleaned_data['city']
            clubPostcode = form.cleaned_data['post_code']
            clubLandlineNumber = form.cleaned_data['landline_number']
            clubMobileNumber = form.cleaned_data['mobile_number']
            clubEmail = form.cleaned_data['email']
            Club.create_new_club_exe(clubName, clubStreetNumber, clubStreet, clubCity, clubPostcode, clubLandlineNumber, clubMobileNumber, clubEmail)
            messages.success(request, "Club successfully registered.")
            return redirect('/cinema_manager_home')

    context['form'] = form
    return render(request, "Uweflix/new_club_add_page.html", context)


def adding_new_representative_page(request):
    context = {}
    userForm = Club_Representative_User_creation_Form()
    form = Club_representative_add_form()
    if request.method == "POST":
        userForm = Club_Representative_User_creation_Form(request.POST)
        form = Club_representative_add_form(request.POST)
        if userForm.is_valid():
            if form.is_valid():
                user = userForm.save(commit=False)
                dob = form.cleaned_data['dob']
                club = form.cleaned_data['club']
                clubRepNum = 1
                if ClubRep.objects.exists():
                    clubRepNum = int(ClubRep.objects.all().last().club_rep_num) + 1
                crUsername = ("%04d" % (clubRepNum,))
                user.username = crUsername
                user.save()
                newCr = ClubRep.objects.create(user=user, club=club, dob=dob, club_rep_num=clubRepNum)
                userGroup = Group.objects.get(name="Club Rep")
                user.groups.add(userGroup)
                request.session['new_cr'] = newCr.club_rep_num
                request.session['new_club'] = newCr.club.name
                request.session['successful_creation'] = True
                return redirect("/rep_success")
    context['form'] = form
    context['userform'] = userForm
    return render(request, "uweflix/adding_new_representative_page.html", context)


def rep_success(request):
    if 'successful_creation' not in request.session:
        raise Http404("Forbidden access to this page.")
    del request.session['successful_creation']
    return render(request, "uweflix/rep_success.html")


def review_students(request, userID):
    print(userID)
    students = User.objects.filter(is_active=False)
    studentChoice = students.first()
    if userID == 0 and studentChoice is not None:
        return redirect('review_students', userID=studentChoice.id)
    if userID != 0:
        studentChoice = User.objects.get(id = userID)
    context = {
        'students' : students,
        'chosenStudent' : studentChoice,
        'urlID' : userID
    }
    if (request.method == "POST"):
        name = request.POST.get('name')
        if name == "changeStudent":
            studentID = request.POST['ReviewStudentForm']
            studentChoice = User.objects.get(id = studentID)
            return redirect('review_students', userID=studentChoice.id)
        else:
            if name == "acceptStudent":
                User.objects.filter(id=userID).update(is_active=True)
            elif name == "denyStudent":
                studentChoice.delete()
            students = User.objects.filter(is_active=False)
            studentChoice = students.first()
            return redirect('review_students', userID=0)
    return render(request, "UweFlix/review_students.html", context)


def view_order_history(request):
    form = select_date_form()
    titleText = "Please select a date range to view transactions for:"
    context = {
        'form': form,
        'title_text': titleText}
    if request.method == "POST":
        user = None
        if request.session["user_group"] == "Club Rep":
            user = ClubRep.objects.get(user_id=request.session["user_id"])
        elif request.session["user_group"] == "Student":
            user = Customer.objects.get(user=request.session["user_id"])
        if user is not None:
            form = select_date_form(request.POST)
            if form.is_valid():
                startDate = form.cleaned_data['startDate']
                endDate = form.cleaned_data['endDate']
                transaction_list = Transaction.objects.filter(customer=user, date__range = (startDate, endDate))
                if not transaction_list:
                    titleText = f"There were no transactions made in your date range"
                    context = {
                        'form': form,
                        'title_text': titleText
                    }
                else:
                    context = {
                        'start_date': startDate,
                        'end_date': endDate,
                        'transaction_list': transaction_list,
                        'form': form
                    }
                form = select_date_form()
            return render(request, "UweFlix/view_order_history.html", context)
        else:
            form = select_date_form()
            titleText = "Please select a date range to view transactions for:"
            context = {
                'form': form,
                'title_text': titleText}
            return render(request, "UweFlix/view_order_history.html", context)
    else:
        return render(request, "UweFlix/view_order_history.html", context)


def change_ticket_prices(request):
    form = Price_changing_page()
    context = {
        'form':form
    }
    if request.method=="POST":
        form = Price_changing_page (request.POST)
        if form.is_valid():
            Prices.update_tickets_price(form.cleaned_data['adult'],form.cleaned_data['student'], form.cleaned_data['child'])
            adult,student,child=Prices.load_Existing_price()
            messages.success(request, f"New ticket prices: \nAdult = £{adult}\nStudent = £{student}\nChild = £{child}")
    return render(request, "uweflix/change_ticket_prices.html", context)


def request_cancellation(request):
    now = timezone.now()
    user = None
    showingsToCancel = []
    adultTickets = []
    childTickets = []
    studentTickets = []
    if request.session["user_group"] == "Club Rep":
        user = ClubRep.objects.get(user_id=request.session["user_id"])
    elif request.session["user_group"] == "Student":
        user = Customer.objects.get(user=request.session["user_id"])
    if user is not None:
        transaction_list = Transaction.objects.filter(customer=user, request_to_cancel=False)
        for purchase in transaction_list:
            allTickets = Ticket.objects.filter(transaction=purchase)
            ticket = allTickets.first()
            if ticket is not None:
                showingTime = ticket.showing.time
                if showingTime > now:
                    showingsToCancel.append(ticket)
                    adultTickets.append(len(allTickets.filter(ticket_type="adult")))
                    childTickets.append(len(allTickets.filter(ticket_type="child")))
                    studentTickets.append(len(allTickets.filter(ticket_type="student")))
    zippedList = zip(showingsToCancel, adultTickets, childTickets, studentTickets)
    context = {
        'zipped': zippedList
    }
    if request.method == "POST":
        requestedTransaction = Transaction.objects.filter(id=request.POST.get('transaction_number'))
        requestedTransaction.update(request_to_cancel=True)
        return redirect('request_cancellation') 
    return render(request, "uweflix/request_cancellation.html", context)


def approve_cancellation(request):
    now = timezone.now()
    user = None
    showingsToCancel = []
    adultTickets = []
    childTickets = []
    studentTickets = []
    transaction_list = Transaction.objects.filter(request_to_cancel=True)
    for purchase in transaction_list:
        allTickets = Ticket.objects.filter(transaction=purchase)
        ticket = allTickets.first()
        if ticket is not None:
            showingTime = ticket.showing.time
            if showingTime > now:
                showingsToCancel.append(ticket)
                adultTickets.append(len(allTickets.filter(ticket_type="adult")))
                childTickets.append(len(allTickets.filter(ticket_type="child")))
                studentTickets.append(len(allTickets.filter(ticket_type="student")))
    zippedList = zip(showingsToCancel, adultTickets, childTickets, studentTickets)
    context = {
        'zipped': zippedList
    }
    if request.method == "POST":
        requestedTransaction = Transaction.load_new_transactions(request.POST.get('transaction_number'))
        ticketList = Ticket.objects.filter(transaction=requestedTransaction.id)
        totalTickets = ticketList.count()
        transactionCost = requestedTransaction.cost
        if requestedTransaction.customer is not None:
            customer = Customer.objects.get(id=requestedTransaction.customer.id)
            if requestedTransaction.is_settled == True:
                customer.credit += transactionCost
                customer.save()
        showing = ticketList.first().showing
        showing.remaining_tickets += totalTickets
        showing.save()
        Transaction.delete_existing_transaction(requestedTransaction.id)
        return redirect('cancel_payment_aprovement_page') 
    return render(request, "uweflix/cancel_payment_aprovement_page.html", context)

def get_movie_details(request, movie_id):
    api_key = '17973a416c598e011053e2fb0ded89c5'
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        movie_data = response.json()
        return JsonResponse(movie_data)
    else:
        return JsonResponse({"error": "Unable to fetch data"}, status=400)
    
def get_now_playing_movies(request):
    api_key = '17973a416c598e011053e2fb0ded89c5'
    url = f'https://api.themoviedb.org/3/movie/now_playing?api_key={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        movies_data = response.json()
        return render(request, 'uweflix/now_playing.html', {'movies': movies_data['results']})
    else:
        return render(request, 'uweflix/error.html', {'message': 'Unable to fetch data'})
    
def manage_movies(request):
    api = tmdb.TMDb()
    api.api_key = '17973a416c598e011053e2fb0ded89c5'
    popular = tmdb.Movies()
    now_playing = popular.now_playing()["results"]

    context = {"now_playing_movies": now_playing}

    return render(request, "uweflix/manage_movies.html", context)