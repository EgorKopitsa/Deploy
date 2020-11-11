from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from Application.models import (
    Category,
    Cart,
    Customer,
    Top,
    Button,
    Shoes,
    Order
)


class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG_PRODUCT_MODEL = {
        'top': Top,
        'button': Button,
        'shoes': Shoes
    }

    def get_context_data(self, **kwargs):
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG_PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context


class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:  # создание покупателя, в случае если он не создан
                customer = Customer.objects.create(
                    user=request.user
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
            orders = Order.objects.filter(customer=customer)
        else:
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            orders = []
        self.cart = cart
        self.orders = orders
        return super().dispatch(request, *args, **kwargs)

