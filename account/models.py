from django.db import models
from django.core.validators import MinLengthValidator,MaxLengthValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

cont = [
    ('cairo','cairo'),
    ('alex','alex'),
    ('aswan','aswan'),
    ('giza','giza'),
    ('sohage','sohage'),
    ('assuit','assuit'),
    ('6october','6october'),
    ('10ramadan','10ramadan'),
    ('qena','qena'),
    ('luxor','luxor'),
    ('menia','menia'),
    ('sena','sena'),
    ('sharqia','sharqia'),
    ('iesmalia','iesmalia'),
    ('tanta','tanta'),
    ('matrouh','matrouh'),
    ('dahab','dahab'),
]


class Account(models.Model):
    firstname = models.CharField(max_length=20, null=False, blank=False)
    lastname = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, max_length=50, blank=False)
    password = models.CharField(max_length=20, null=False, validators=[
        MinLengthValidator(8, 'the field must contain at least 8 characters')
    ], blank=False)
    confirm_password = models.CharField(max_length=20, null=False, validators=[
        MinLengthValidator(8, 'the field must contain at least 8 characters')
    ], blank=False)
    mobile_phone = models.CharField(null=False, blank=False, max_length=11)
    image = models.ImageField(upload_to='accounts', null=False, blank=False)
    is_active = models.BooleanField(default=False)
    token = models.CharField(null=True,max_length=200)

    def __str__(self):
        return self.firstname + " " + self.lastname


class Profile(models.Model):
    name = models.OneToOneField('Account',  on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    facebook = models.CharField(null=True, max_length=100)
    country = models.CharField(choices=cont, max_length=50, null=True)

    def __str__(self):
        return format(self.name.lastname)

#
# def create_profile(sender,**kwargs):
#     if kwargs['created']:
#         Profile.objects.create(name=kwargs['instance'])
#
# post_save.connect(create_profile,sender=Account)