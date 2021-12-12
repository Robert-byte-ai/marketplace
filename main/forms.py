from django.forms import ModelForm

from .models import User, Seller


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class SellerForm(ModelForm):

    class Meta:
        model = Seller
        fields = ('ITN',)
