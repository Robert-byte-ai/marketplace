from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import random_string_generator, check_inn


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='common_users'))


class BaseModel(models.Model):
    """
    Базовая абстрактная модель, в которой определенно общее поле name
    """
    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Seller(models.Model):
    """
        Модель продавца, имеет поля:
        user(связь с юзером один к одному),
        ITN(ИНН продавца, строковое поле с ограничением по размеру),
        avatar(аватар продавца, файловое поле, проверяющее, что загруженный
        объект является допустимым изображением),
        phone(телефон продавца, строковое поле с ограничением по размеру),
        count_ads(функция, подсчитывающая количество объявлений продавца)
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    ITN = models.CharField(
        max_length=200,
        db_index=True,
        unique=True,
        default=11111,
        verbose_name='ИНН',
        validators=[check_inn],
    )

    avatar = models.ImageField(
        upload_to='images/avatars',
        default=f'images/avatars/{user}default.jpg',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=18,
        db_index=True,
        unique=True,
        null=True,
        blank=True,
        verbose_name='Номер телефона'
    )

    @property
    def count_ads(self):
        count = Ad.objects.filter(seller__user=self.user).count()
        if count:
            return count
        return 0

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'

    def __str__(self):
        return '{}'.format(self.user)


class Category(BaseModel):
    """
        Модель категории, наследуюется от базовой модели, имеет поля:
        slug(самозаполняемый слаг категории),
    """
    slug = models.SlugField(
        max_length=50,
        unique=True,
        null=True,
        verbose_name='Slug категории',
        db_index=True
    )

    def unique_slug_generator(self, instance, new_slug=None):
        if new_slug is not None:
            slug = new_slug
        else:
            slug = slugify(instance.name)

        Category = instance.__class__
        qs_exists = Category.objects.filter(slug=slug).exists()
        if qs_exists:
            new_slug = "{slug}-{randstr}".format(
                slug=slug,
                randstr=random_string_generator(length=4)
            )
            return self.unique_slug_generator(instance, new_slug=new_slug)
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.unique_slug_generator(self)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Tag(BaseModel):
    """
        Модель тега, наследуюется от базовой модели
    """

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'тег'
        verbose_name_plural = 'теги'


class Ad(BaseModel):
    """
        Модель объявления, наследуется от базовой содели, имеет поля:
        category(связь с моделью Category один ко многим),
        seller(связь с моделью Seller один ко многим),
        pub_date(Дата публикации объявления, дата и время,
        представленные в Python экземпляром datetime.datetime),
        edited_date(дата редактирования объявления, см. pub_date),
        tags(связь с моделью Tag многие ко многим),
        price(цена объявления, целое положительное число),
        is_archive(являеется ли объявление архивированным, буллево значение)
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='ads',
        verbose_name='Категория'
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name='Продавец'
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    edited_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата редактирования'
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='ads',
        verbose_name='Теги',
    )

    price = models.PositiveIntegerField(
        default=0,
        verbose_name='Цена',
    )

    is_archive = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class ManagerArchive(models.Manager):
    """
    Определение архивных моделей
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_archive=True)


class ArchiveAds(Ad):
    """
    Модель архивного объявления
    """
    objects = ManagerArchive()

    class Meta:
        proxy = True
        verbose_name = 'Архивное объявление'
        verbose_name_plural = 'Архивные объявления'


class Picture(models.Model):
    """
        Модель изображения, имеет поля:
        ad(объявление, связь с моделью Ad один к многим),
        image(изображение объявления, файловое поле, проверяющее, что загруженный
        объект является допустимым изображением),
    """
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='pictures',
        verbose_name='Объявление'
    )

    image = models.ImageField(
        upload_to='images/ads',
        default='images/ads/default.jpg',
        verbose_name='Картинка'
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Subscription(models.Model):
    """
        Модель подписки, имеет поля:
        user(связь с юзером один к одному),
    """
    user = models.ManyToManyField(
        User,
        related_name='subscriptions',
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class SMSLog(models.Model):
    """
        Модель СМС отправленного на телефон
        продавца для потверждения телефона, имеет поля:
        seller(продавец номер которого изменен, связь с моделю Seller один к одному),
        code(код потверждения, отправленный на номер продавца, ограниченное строковое поле),
        confirmed(подтвержден ли номер, буллево значение),
        response(ответ от провайдера, строковое поле)
    """
    seller = models.OneToOneField(
        Seller,
        on_delete=models.CASCADE,
        verbose_name='Продавец'
    )

    code = models.CharField(
        max_length=4,
        db_index=True,
        verbose_name='Код'
    )

    confirmed = models.BooleanField(
        default=False,
        verbose_name='Подтвержден номер или нет,'
    )

    response = models.TextField(
        verbose_name='Ответ от провайдера'
    )
