from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:event_id>/', views.book_ticket, name='book_ticket'),
    path('payment/<int:ticket_id>/', views.payment, name='payment'),
    path('my_tickets/', views.my_tickets, name='my_tickets'),
]
