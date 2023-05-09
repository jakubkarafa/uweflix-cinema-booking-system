from django.urls import path
from uweflix import views
from uweflix.models import *
from .views import *


urlpatterns = [
    path("club_discount/", views.clubdiscount, name="club_discount"),
    path("change_account_page/", views.change_account_page, name="change_account_page"),
    path("update_accounts_form_page/", views.update_accounts_form_page, name="update_accounts_form_page"),
    path('add_user', add_user, name='add_user'),
    path('delete_user/<int:myid>/', delete_user, name='delete_user'),
    path('edit_user/<int:myid>/', edit_user, name='edit_user'),
    path('update_user/<int:myid>/', update_user, name='update_user'),
    path('manage_club_account/', views.manage_club_account, name='manage_club_account'),
    path('add_clubs', add_clubs, name='add_clubs'),
    path('card_payment_form/<str:payment_method>/', views.card_payment_form, name='card_payment_form'),
    path('delete_clubs/<int:myid>/', delete_clubs, name='delete_clubs'),
    path('edit_clubs/<int:myid>/', edit_clubs, name='edit_clubs'),
    path('update_clubs/<int:myid>/', update_clubs, name='update_clubs'),
    
    
    path('modify_delete_accounts/', views.modify_delete_accounts,
         name='modify_delete_accounts'),
    path('create_account/', create_account, name='create_account'),
    path('delete_account/<int:myid>/', delete_account, name='delete_account'),
    path('edit_account/<int:myid>/', edit_account, name='edit_account'),
    path('update_account/<int:myid>/', update_account, name='update_account'),
    path('view_account/', view_account, name='view_account'),

    
    
    
    path("", views.viewings_page, name="home"),
    path("viewings_page/", views.viewings_page, name="viewings_page"),
    path("showings/<int:film>/", views.showings, name="showings_by_film"),
    path("add_new_movie/", views.add_new_movie, name="add_new_movie"),
    path("films_endpoint/", views.films_endpoint, name="films_endpoint"),
    path("specific_film_endpoint/<int:pk>/", views.specific_film_endpoint, name="specific_film_endpoint"),
    path("login/", views.login, name="login"),
    path("topup/", views.topup, name="topup"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.registerPage, name="registerPage"),
    path("payment/<int:showing>/", views.payment, name="payment"),
    path('payment_page_for_representative/<int:showing>/', views.payment_page_for_representative, name='payment_page_for_representative'),
    path("card_payment_form/", views.card_payment_form, name="card_payment_form"),
    path("view_accounts/", views.view_accounts, name="view_accounts"),
    path("daily_transactions/", views.daily_transactions, name="daily_transactions"),
    path("customer_statements/", views.customer_statements, name="customer_statements"),
    path("thanks/", views.thanks, name="thanks"),
    path("user/", views.userpage, name="user-page"),
    path("new_club_add_page/", views.new_club_add_page, name="new_club_add_page"),
    path("clubs_endpoint/", views.clubs_endpoint, name="clubs_endpoint"),
    path("specific_club_endpoint/<int:pk>/", views.specific_club_endpoint, name="specific_club_endpoint"),
    path("adding_new_representative_page/", views.adding_new_representative_page, name="adding_new_representative_page"),
    path("club_rep_home/", views.club_rep_home, name="club_rep_home"),
    path("cinema_manager_home/", views.cinema_manager_home, name="cinema_manager_home"),
    path("student_home/", views.student_home, name="student_home"),
    path("set_payment/", views.set_payment_details, name="set_payment"),
    path("main_home_page/", views.main_home_page, name="main_home_page"),
    path("payment_settle_page/", views.payment_settle_page, name="payment_settle_page"),
    path("review_students/<int:userID>", views.review_students, name="review_students"),
    path("rep_success/", views.rep_success, name="rep_success"),
    path("change_ticket_prices/", views.change_ticket_prices, name="change_ticket_prices"),
    path("view_order_history/", views.view_order_history, name="view_order_history"),
    path("request_cancellation/", views.request_cancellation, name="request_cancellation"),
    path("cancel_payment_aprovement_page/", views.approve_cancellation, name="cancel_payment_aprovement_page"),
    path("screens_endpoint/", views.screens_endpoint, name="screens_endpoint"),
    path("specific_screen_endpoint/<int:pk>/", views.specific_screen_endpoint, name="specific_screen_endpoint"),
    path("New_screen_addition_page/", views.New_screen_addition_page, name="New_screen_addition_page"),
    path("add_new_showing_screen/", views.add_new_showing_screen, name="add_new_showing_screen"),
    path('update_showings_page/<int:showing_id>/', views.update_showings_page, name='update_showings_page'),

    path('movie/<int:movie_id>/', get_movie_details, name='get_movie_details'),
    path('now_playing/', get_now_playing_movies, name='now_playing'),
]
