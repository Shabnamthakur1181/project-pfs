from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, Cart

class HomeView(ListView):
    model = Product
    template_name = 'store/home.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'id'

@method_decorator(login_required, name='dispatch')
class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        
        # Get or create a cart for the user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Get or create the cart item inside that cart
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += 1
            item.save()

        return redirect('view_cart')

@method_decorator(login_required, name='dispatch')
class CartView(View):
    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cart_items.all()

        total_price = 0
        for item in cart_items:
            item.subtotal = item.product.price * item.quantity
            total_price += item.subtotal

        return render(request, 'store/cart.html', {
            'cart_items': cart_items,
            'total_price': total_price
        })



@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        total = sum(item.product.price * item.quantity for item in items)
        return render(request, 'store/checkout.html', {'items': items, 'total': total})

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        address = request.POST['address']

    # Mark the cart as ordered
        cart.ordered = True
        cart.save()

    # Create order and link to updated cart
        Order.objects.create(user=request.user, cart=cart, address=address)

        return redirect('my_orders')  # Redirect to the my_orders page




class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'store/my_orders.html'  # Make sure this HTML exists
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')
    

# class CancelOrderView(View):
#     def post(self, request, order_id):
#         order = get_object_or_404(Order, id=order_id, user=request.user)
#         order.delete()

#         # Optionally clear cart if needed
#         request.session['cart'] = {}  # Clears the cart from the session
#         request.session.modified = True

#         return redirect('my_orders')

class CancelOrderView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)

        if order.cart:
            # Debug: Log cart and items
            print(f"Cancelling Order ID: {order.id}, Cart ID: {order.cart.id}")
            
            # Delete only the cart items linked to this cart
            cart_items = CartItem.objects.filter(cart=order.cart)
            print(f"Cart Items Before Deletion: {cart_items}")
            cart_items.delete()

            remaining = CartItem.objects.filter(cart=order.cart)
            print(f"Cart Items After Deletion: {remaining}")

        # Update the order status to 'Cancelled' but DO NOT delete the order
        order.status = 'Cancelled'
        order.save()

        return redirect('my_orders')
    
# class IncreaseQuantityView(View):
#     def post(self, request, item_id):
#         item = get_object_or_404(CartItem, id=item_id)
#         item.quantity += 1
#         item.save()
#         return redirect('cart')  # change to your cart page name

# class DecreaseQuantityView(View):
#     def post(self, request, item_id):
#         item = get_object_or_404(CartItem, id=item_id)
#         if item.quantity > 1:
#             item.quantity -= 1
#             item.save()
#         else:
#             item.delete()  # Remove item if quantity is 0
#         return redirect('cart')
    
@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def increase_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')

@login_required
def decrease_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')