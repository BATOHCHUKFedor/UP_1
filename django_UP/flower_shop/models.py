from django.db import models

MAX_LENGTH = 255

class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name # Вернётся только название.
    
    class Meta: # Как таблица будет отображаться в административной панели
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Collection(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')

    def __str__(self):
        return self.name 
    
    class Meta: 
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class Supplier(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    contact_person = models.CharField(max_length=MAX_LENGTH, null=True, blank=True, verbose_name='Контактное лицо')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(null=True, blank=True, verbose_name='Email')
    address = models.TextField(null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Flowers(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name='Наименование')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    height_cm = models.PositiveIntegerField(default=40, verbose_name='Высота, см')
    color = models.CharField(max_length=MAX_LENGTH, null=True, blank=True, verbose_name='Цвет')
    photo = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Изображение')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления на сайт")
    is_exists = models.BooleanField(default=True, verbose_name='Доступность к заказу')

    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Категория')
    collection = models.ManyToManyField(Collection, verbose_name='Коллекция')
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Поставщик')

    def __str__(self):
        return f"{self.name} ({self.price} руб.)"
    
    class Meta:
        verbose_name = 'Цветы'
        verbose_name_plural = 'Цветы'


class Order(models.Model):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (NEW, 'Новый'),
        (IN_PROGRESS, 'В работе'),
        (DELIVERED, 'Доставлен'),
        (CANCELED, 'Отменён'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=NEW, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость')
    delivery_address = models.TextField(verbose_name='Адрес доставки')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к заказу')

    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='Заказ')
    flower = models.ForeignKey(Flowers, on_delete=models.PROTECT, verbose_name='Цветок')

    def __str__(self):
        return f"{self.flower.name} x {self.quantity}"

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Оценка')
    text = models.TextField(verbose_name='Текст отзыва')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    flower = models.ForeignKey(Flowers, on_delete=models.CASCADE, related_name='reviews', verbose_name='Цветок')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f"Отзыв на {self.flower.name} от {self.user.username}"

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Промокод')
    discount_percent = models.PositiveSmallIntegerField(verbose_name='Процент скидки')
    valid_from = models.DateTimeField(verbose_name='Действует с')
    valid_to = models.DateTimeField(verbose_name='Действует по')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f"{self.code} ({self.discount_percent}%)"

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'