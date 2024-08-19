from django.shortcuts import render, redirect
from .models import Event, Ticket
from .forms import TicketBookingForm
from django.contrib.auth.decorators import login_required
import stripe

stripe.api_key = 'your-stripe-secret-key'

def index(request):
    events = Event.objects.all()
    dic={
        "events":events
        
    }
    return render(request, 'index.html', dic)

@login_required
def book_ticket(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        form = TicketBookingForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.event = event
            ticket.save()
            return redirect('payment', ticket_id=ticket.id)
    else:
        form = TicketBookingForm(initial={'event': event})
    return render(request, 'book_ticket.html', {'form': form, 'event': event})

@login_required
def payment(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == 'POST':
        try:
            # Assuming ticket has a price field to determine amount
            charge = stripe.Charge.create(
                amount=int(ticket.event.price * 100),  # Convert dollars to cents
                currency='usd',
                description=f'Ticket for {ticket.event.title}',
                source=request.POST['stripeToken']
            )
            ticket.payment_status = True
            ticket.save()
            return redirect('my_tickets')
        except stripe.error.StripeError as e:
            # Handle error (e.g., log the error, show an error message)
            print(f"Stripe error: {e}")
            return render(request, 'payment.html', {'ticket': ticket, 'error': str(e)})
    return render(request, 'payment.html', {'ticket': ticket})

@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'my_tickets.html', {'tickets': tickets})
