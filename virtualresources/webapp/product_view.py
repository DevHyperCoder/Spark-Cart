from django.shortcuts import render, redirect
from .forms import CreateProductForm, CreateRatingForm
from .models import Product, Ratings, UserProfile
from django.contrib.auth.decorators import login_required

# Helper method to check if the user has enough money in his account
def enough_money_in_user(user: UserProfile, amt: int):
    money = user.money
    if (money >= amt):
        return True

    return False

# Method to find out the avg. rating of a product
def get_avg_rating(product_id :Product):
    try:
        product = Product.objects.get(id = product_id)
        ratings = Ratings.objects.filter(product = product)
        lenght = Ratings.objects.filter(product = product).count()
        avg_rating = 0
        sum_rating = 0
        for rating in ratings:
            sum_rating += rating.rating_num
        avg_rating = sum_rating/lenght

        return avg_rating
    except Ratings.DoesNotExist:
        print(f"Can not find rating for product with id = {product_id} ")
    except Product.DoesNotExist:
        print(f"Can not find product with id = {product_id} ")

    return 0


# Buy a product
# Shows the page where checkout page with the confirmation and stuff
@login_required(login_url="/signin")
def buy_product(request):
    product_id = request.GET.get("id")
    product: Product = None
    ratings: Ratings = None
    try:
        product = Product.objects.get(id=product_id)
        ratings = Ratings.objects.filter(product=product)
    except Product.DoesNotExist:
        print(f"Could not find a product with id = {product_id}")
    except Ratings.DoesNotExist:
        print(f"No reviews for product with id {product_id}")

    if request.POST:

        # Same user
        if request.user.id == product.seller.id:
            return render(request, "buy.html", {"product": product, "same_user": "asdf"})

        if enough_money_in_user(request.user, product.price):

            # Deduct from the user
            user: UserProfile = request.user
            old_bal_user = user.money
            new_bal_user = old_bal_user - product.price
            user.money = new_bal_user
            user.save()

            # Add the money to the seller
            seller = product.seller
            old_bal_seller = seller.money
            new_bal_seller = old_bal_seller+product.price
            seller.money = new_bal_seller
            seller.save()

            # TODO Remove from cart list if exists

            return redirect(f"/checkout?id={product_id}")
        else:
            return render(request, "buy.html", {"product": product, "not_enough_error": "asdf"})

    return render(request, "buy.html", {'product': product, 'ratings': ratings, 'rating_form': CreateRatingForm()})


@login_required(login_url='/signin')
def rate_product(request):
    prod_id = request.GET.get("id")
    product = None
    ratingForm = CreateRatingForm(request.POST or None)
    user = request.user

    try:
        product:Product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        print(f"Could not find {prod_id}")

    # Add the rating
    if ratingForm.is_valid() and product != None:
        rating: Ratings = ratingForm.save(commit=False)
        rating.user = user
        rating.product = product
        rating.save()

        # Update the avg rating
        product.avg_rating = get_avg_rating(product_id=prod_id)
        product.save()
        
    return redirect(f'/buy?id={prod_id}')


@login_required(login_url='/signin')
def checkout(request):
    prod_id = request.GET.get("id")
    product = None
    try:
        product = Product.objects.get(id=prod_id)
    except Product.DoesNotExist:
        print(f"Could not find {prod_id}")

    return render(request, "checkout.html", {'product': product})

# Explore Products


def explore_product(request):
    
    return render(request,
                  "explore.html",
                  {'products': Product.objects.all()})

# Sell a product
# Make it login required


@login_required(login_url="/signin")
def sell_product(request):
    product_creation_form = CreateProductForm(request.POST or None)
    if request.method == "POST":
        print("POSTED")
        if product_creation_form.is_valid():
            # product_creation_form
            print("form is valid")
            product: Product = product_creation_form.save(commit=False)
            product.seller = request.user
            product.save()

    return render(
        request,
        "sell.html",
        {'form': product_creation_form}
    )

import random 

@login_required(login_url='signin/')
def gift_card(request):
    if request.POST:
        user:UserProfile = request.user
        gift_card_money = random.randint(0,1000)

        user.money += gift_card_money
        user.save()

        return render(request,'gift-card.html',{'money':gift_card_money})
    
    return render(request,'gift-card.html')