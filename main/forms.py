from django.forms import ModelForm
from django.forms import inlineformset_factory

from .models import User, Seller, Ad, Picture


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )


class SellerForm(ModelForm):

    class Meta:
        model = Seller
        fields = ('ITN',)


class AdForm(ModelForm):

    class Meta:
        model = Ad
        fields = '__all__'


ImageFormset = inlineformset_factory(
    Ad,
    Picture,
    fields=('image',)
)
