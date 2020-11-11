from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseServerError
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render
from django.views.generic import DetailView, View, CreateView

from Application.forms import OrderForm, AuthUserForm, RegisterUserForm
from Application.mixins import *
from Application.models import *
from Application.utils import recalc_cart


def custom_handler404(request, exception):
    return HttpResponseNotFound('Запрашиваемый запрос не найден, или его вообще не существует!')


def custom_handler500(request):
    return HttpResponseServerError('Ошибка на нашей стороне')


class IndexView(CartMixin, View):

    def get(self, request, *args, **kwargs):

        categories = Category.objects.get_categories_for_left_sidebar()

        carousels = Carousel.objects.all()
        products = LatestProducts.objects.get_products_for_main_page(
            'top', 'button', 'shoes'
        )
        context = {
            'categories': categories,
            'products': products,
            'cart': self.cart,
            'orders': self.orders,
            'carousels': carousels,
        }
        return render(request, 'index.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):  # определяет информацию о товаре из категории

    CT_MODEL_MODEL_CLASS = {
        'top': Top,
        'button': Button,
        'shoes': Shoes,
    }

    def dispatch(self, request, *args, **kwargs):  # определяем, что за модель
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        context['orders'] = self.orders
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        context['orders'] = self.orders
        return context


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        products = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=products.id
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен!")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        products = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=products.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален!")
        return HttpResponseRedirect('/cart/')


class ChangeQTYANDSIZEView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        products = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=products.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        size = str(request.POST.get('size'))
        cart_product.size = size
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Параметры товара успешно измены!")
        return HttpResponseRedirect('/cart/')


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        dimensions = self.cart.products.all()
        size_count = CartProduct.objects.filter(size="").count()
        context = {
            'cart': self.cart,
            'categories': categories,
            'orders': self.orders,
            'dimensions': dimensions,
            'size_count': size_count,

        }

        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form,
            'orders': self.orders
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        cart = Cart.objects.last()
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = request.user.first_name
            new_order.last_name = request.user.last_name
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.comment = form.cleaned_data['comment']
            new_order.delivery_price = cart.final_price
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO, 'Заказ оформлен, осталось лишь оплатить!')
            return HttpResponseRedirect(f'/payment/{new_order.id}')
        return HttpResponseRedirect('/checkout/')


class InfoView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories,
            'orders': self.orders
        }
        return render(request, 'information.html', context)


class OrdersView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        deliveries = Delivery.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories,
            'orders': self.orders,
            'deliveries': deliveries
        }
        return render(request, 'orders.html', context)


class MyLoginView(LoginView):

    redirect_authenticated_user = True
    template_name = 'login.html'
    form_class = AuthUserForm


class RegisterUserView(CreateView):

    model = User
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = '/login'


class PaymentView(CartMixin, View):

    def get(self, request, order_id, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        order = Order.objects.get(id=order_id)
        cart_arrange = order.cart
        delivery = Delivery.objects.get(where=order.delivery)
        context = {
            'categories': categories,
            'order': order,   # данные по заказу
            'orders': self.orders,  # кол-во заказов и данные по заказчику
            'cart_arrange': cart_arrange,
            'cart': self.cart,  # кол-во товара в корзине
            'delivery': delivery
        }

        return render(request, 'payment.html', context)


class BrandView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()

        context = {
            'cart': self.cart,
            'categories': categories,
            'orders': self.orders
        }
        return render(request, 'brand.html', context)





