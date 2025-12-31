from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Product, Favorite, CartItem, Category, Profile
from .forms import ProfileForm

def product_list(request):

    categories = Category.objects.all()


    query = request.GET.get('search')
    category_id = request.GET.get('category')


    products_list = Product.objects.all().order_by('name')


    if query:
        products_list = products_list.filter(name__icontains=query)
    if category_id:
        products_list = products_list.filter(category_id=category_id)


    paginator = Paginator(products_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'list.html', {
        'products': page_obj,
        'categories': categories,
        'current_category': category_id
    })

@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    fav, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        fav.delete()

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.name} to cart!")
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))

@login_required
def cart_detail(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {
        'items': items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()
    if cart_item:
        cart_item.delete()
        messages.success(request, f"Removed {product.name} from cart!")
    else:
        messages.warning(request, "Item not found in cart.")
    return redirect('cart_detail')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
    else:
        messages.warning(request, "Your cart is empty.")
    return redirect('product_list')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    favorites = Favorite.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {
        'favorites': favorites,
        'form': form,
        'profile': profile
    })
