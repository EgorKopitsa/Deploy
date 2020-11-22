from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse


User = get_user_model()


def get_models_for_count(*model_names):  # считает кол-во товара для категории
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):  # создает ссылки на опеределенный товар
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:  # собирает из всех моделей товар

    @staticmethod
    def get_products_for_main_page(*args):
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.filter(available=True)
            products.extend(model_products)
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Товар': 'top__count',
        'Низ': 'button__count',
        'Обувь': 'shoes__count'
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        product = get_models_for_count('top', 'button', 'shoes')
        qs = list(self.get_queryset().annotate(*product))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории', db_index=True)
    slug = models.SlugField(max_length=255, verbose_name='Индентификатор', unique=True)
    objects = CategoryManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Идентификатор')
    material = models.CharField(max_length=255, verbose_name='Материал', default='')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2)
    available = models.BooleanField(default=False, verbose_name='Наличие')
    dimensions = models.CharField(max_length=255, verbose_name='Размеры (через один пробел, без запятых)', blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class Top(Product):

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class ImageTop(models.Model):

    top = models.ForeignKey(Top, default=None, on_delete=models.CASCADE, related_name='images')
    images = models.FileField(upload_to='images/', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.top.title


class Button(Product):

    class Meta:
        verbose_name = 'Низ'
        verbose_name_plural = 'Низ'

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Shoes(Product):

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', null=True, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, verbose_name='Категория', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name='Товар')
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Кол-во')
    size = models.CharField(max_length=50, verbose_name='Размер', default='')
    final_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая цена')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    def __str__(self):
        return "Продукт: {}".format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=10, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Промежуточная корзина'
        verbose_name_plural = 'Промежуточная корзина'

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_SENT = 'Отправлен'
    STATUS_PAID = 'Оплачен'
    STATUS_IN_PROCESSING = 'В обработке'
    STATUS_NOT_PAID = 'Не оплачен'

    DELIVERY_RUSSIA = 'Россия'
    DELIVERY_OTHER_COUNTRIES = 'Другие страны'
    DELIVERY_PICKUP_FROM_MOSCOW = 'Самовывоз из Москвы'

    STATUS_CHOICES = (
        (STATUS_SENT, 'Отправлен'),
        (STATUS_PAID, 'Оплачен'),
        (STATUS_IN_PROCESSING, 'В обработке'),
        (STATUS_NOT_PAID, 'Не оплачен'),
    )

    DELIVERY_CHOICES = (
        (DELIVERY_RUSSIA, 'Россия'),
        (DELIVERY_OTHER_COUNTRIES, 'Другие страны'),
        (DELIVERY_PICKUP_FROM_MOSCOW, 'Самовывоз из Москвы')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель (Заказчик)', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя (Получатель)')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия (Получатель)')
    phone = models.CharField(max_length=20, verbose_name='Телефон (Заказчика)')
    email = models.CharField(max_length=50, verbose_name='Email', default='')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    index = models.CharField(max_length=255, verbose_name='Индекс', default='')
    address = models.CharField(max_length=1024, verbose_name='Адрес', default='')
    status = models.CharField(max_length=100, verbose_name='Статус заказа', choices=STATUS_CHOICES, default=STATUS_IN_PROCESSING)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    delivery_price = models.DecimalField(max_digits=10, default=0, decimal_places=2)
    delivery = models.CharField(max_length=100, verbose_name='Доставка', choices=DELIVERY_CHOICES, default=DELIVERY_RUSSIA)
    track_number = models.CharField(max_length=255, verbose_name='Трек номер', default='', null=True, blank=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)


class Carousel(models.Model):

    images = models.ImageField(verbose_name='Изображение (1110х360)')

    class Meta:
        verbose_name = 'Карусель'
        verbose_name_plural = 'Карусель'


class Delivery(models.Model):

    DELIVERY_RUSSIA = 'Россия'
    DELIVERY_OTHER_COUNTRIES = 'Другие страны'
    DELIVERY_PICKUP_FROM_MOSCOW = 'Самовывоз из Москвы'

    DELIVERY_CHOICES = (
        (DELIVERY_RUSSIA, 'Россия'),
        (DELIVERY_OTHER_COUNTRIES, 'Другие страны'),
        (DELIVERY_PICKUP_FROM_MOSCOW, 'Самовывоз из Москвы')
    )

    where = models.CharField(max_length=100, verbose_name='Куда', choices=DELIVERY_CHOICES, default=DELIVERY_RUSSIA)
    price = models.DecimalField(max_digits=10, default=0, decimal_places=2)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'



