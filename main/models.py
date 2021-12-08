from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from .utils import random_string_generator

User = get_user_model()


class Seller(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
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


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя категории'
    )

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

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        db_index=True,
    )

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

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.name
