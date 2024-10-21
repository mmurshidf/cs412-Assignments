from django.shortcuts import render, redirect
import random
import time

# Create your views here.
def main(request):
    return render(request, 'restaurant/main.html')

def order(request):
    daily_specials = [
        {'name': 'Salmon Sushi', 'price': 16},
        {'name': 'Tuna Sushi', 'price': 17},
        {'name': 'Eel Sushi', 'price': 18},
        {'name': 'Vegetarian Sushi', 'price': 14}
    ]
    daily_special = random.choice(daily_specials)
    
    context = {
        'daily_special_name': daily_special['name'],
        'daily_special_price': daily_special['price']
    }
    
    return render(request, 'restaurant/order.html', context)

import random
from datetime import datetime, timedelta

def confirmation(request):
    if request.method == 'POST':
        ordered_items = request.POST.getlist('items')
        extras = request.POST.getlist('extras')
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        special_instructions = request.POST.get('special_instructions', '')

        # Define prices for items, including the daily special
        item_prices = {
            'Chicken/Lamb_over_rice': 10,
            'Chicken_Curry': 12,
            'Kachi_Byriani': 10,
            'Sushi': 15,
            'Salmon Sushi': 16,
            'Tuna Sushi': 17,
            'Eel Sushi': 18,
            'Vegetarian Sushi': 14,
        }
        
        # Prices for extras
        extra_prices = {
            'Roll': 3,
            'Extra_Soy_Sauce': 1,
            'Wasabi': 1
        }

        # Calculate total for items
        total = sum(item_prices[item] for item in ordered_items if item in item_prices)

        # Add extras to the total
        total += sum(extra_prices[extra] for extra in extras if extra in extra_prices)

        # Calculate ready time 
        ready_time_minutes = random.randint(30, 60)
        ready_time = (datetime.now() + timedelta(minutes=ready_time_minutes)).strftime("%I:%M %p")

        context = {
            'ordered_items': ordered_items,
            'extras': extras,
            'special_instructions': special_instructions,
            'name': name,
            'phone': phone,
            'email': email,
            'total': total,
            'ready_time': ready_time
        }

        return render(request, 'restaurant/confirmation.html', context)
    return redirect('order')

