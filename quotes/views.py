from django.shortcuts import render
import random
import time

# Create your views here.
QUOTES = [
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world.",
    "Try not to become a man of success, but rather try to become a man of value.",
    "A person who never made a mistake never tried anything new.",
    "The important thing is not to stop questioning. Curiosity has its own reason for existence.",
]

IMAGES = [
    "https://hips.hearstapps.com/hmg-prod/images/albert-einstein-sticks-out-his-tongue-when-asked-by-news-photo-1681316749.jpg",
    "https://cdn.britannica.com/77/142177-050-4E8010A9/Albert-Einstein-1947.jpg",
    "https://www.nobelprize.org/images/einstein-12923-landscape-medium.jpg",
    "https://invention.si.edu/sites/default/files/styles/story_banner_image/public/blog-guest-bisno-adam-2020-12-08-einstein-1930-library-of-congress-banner-edit.jpg?itok=3BeXRrDn",
    "https://www.thefactsite.com/wp-content/uploads/2017/07/albert-einstein-facts.jpg",
]

def quote(request):
    quote = random.choice(QUOTES)
    image = random.choice(IMAGES)
    context = {
        'quote': quote,
        'image' : image,
        'current_time': time.ctime(),
    }
    template_name = 'quotes/quote.html'
    return render(request, template_name, context)

def show_all(request):
    context = {
        'quotes' : QUOTES,
        'images' : IMAGES,
        'current_time': time.ctime(),
    }
    return render(request, 'quotes/show_all.html', context)

def about(request):
    context = {
        'current_time': time.ctime(),
    }
    return render(request, 'quotes/about.html', context)