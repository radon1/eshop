from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    '''Профиль пользователя'''
    CITY = (
        ('1', "Moscow"),
        ("2", "St.Petersburg"),
        ("3", "San-Francisco"),
        ("4", "Boston"),
        ("5", "Prague"),
    )
    COUNTRY = (
        ('1', "Russia"),
        ("2", "Usa"),
        ("3", "Ukraine"),
        ("4", "Belarus"),
    )
    STATES = (
        ('1', 'Washington'),
        ('2', 'Florida'),
        ('3', 'Texas'),
    )
    user = models.OneToOneField(
        User,
        verbose_name='Пользователь',
        related_name= 'user_profile',
        on_delete= models.CASCADE)
    first_name = models.CharField('Имя', max_length=120, default='')
    last_name = models.CharField("Фамилия", max_length=120, default="")
    company_name = models.CharField("Компания", max_length=120, blank=True, default="")
    address = models.CharField('Адресс', max_length=250, default='')
    postcode = models.CharField("Индекс", max_length=120, default="")
    country = models.CharField('Страна', max_length=120, default='', choices=COUNTRY)
    phone = models.IntegerField('Телефон', default=790000000)
    state = models.CharField('Штат', max_length=120, default='California', choices=STATES)
    city = models.CharField('Город', default='Moscow', max_length=50, choices=CITY)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return "Id:{}, {} {}".format(self.id, self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse('profile', kwargs = {'pk': self.user.id})


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля пользователя при регистрации"""
    if created:
        Profile.objects.create(user=instance, id=instance.id)


@receiver
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()