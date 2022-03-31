from django.db import models
from django.utils import timezone
from geopy.distance import geodesic
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse
from django_resized import ResizedImageField


class Gender(models.Model):
    name = models.CharField(max_length=64, verbose_name='Пол')
    slug = models.SlugField(max_length=64, db_index=True, unique=True, verbose_name='Уникальная строка')
    is_active = models.BooleanField(default=True, verbose_name='Актуальность')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now, verbose_name='Дата создания записи')
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Дата ред-ия записи')

    class Meta:
        ordering = ('-created', '-name')
        verbose_name = 'Пол участника'
        verbose_name_plural = 'Пол участников'

    def __str__(self):
        return '%s' % self.name


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Участник')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия участника')
    first_name = models.CharField(max_length=200, verbose_name='Имя участника')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default='18.020448',
                                    verbose_name='Долгота')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default='-76.794728',
                                   verbose_name='Широта')
    gender = models.ForeignKey(Gender, null=True, on_delete=models.CASCADE, verbose_name='Пол участника')
    photo = ResizedImageField(size=[520, 650], null=True, crop=['middle', 'center'], force_format='PNG',
                              upload_to='members_photos/%Y/%m/%d/', verbose_name='Фотография участника')
    is_active = models.BooleanField(default=False, verbose_name='Актуальность участника')
    created = models.DateTimeField(blank=True, null=True, default=timezone.now,
                                   verbose_name='Дата регистрации участника')
    updated = models.DateTimeField(blank=True, null=True, auto_now=True, verbose_name='Дата ред-ия записи')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return 'Профиль учаcтника %s %s' % (self.first_name, self.last_name)

    def min_photo(self):
        if self.photo:
            return mark_safe(u'<a href="{0}" target="_blank"><img src="{0}" width="50"/></a>'.format(self.photo.url))
        else:
            return 'Фотографии нет'

    min_photo.short_description = 'Фотография'
    min_photo.allow_tags = True

    def get_longitude_latitude(self):
        return '(%s, %s)' % (self.longitude, self.latitude)

    get_longitude_latitude.short_description = 'Долгота, широта'

    def get_absolute_url(self):
        return reverse('clients:match', args=[self.id])
