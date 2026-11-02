from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order
from django import forms

class CartAddProductForm(forms.Form):
    # Делаем поле необязательным, а значение по умолчанию 1
    quantity = forms.IntegerField(min_value=1, initial=1, required=False)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())

from .models import Order  # добавь это в самый верх файла, если импорта нет

# ... (здесь твой CartAddProductForm) ...

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Иван Иванов'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ivan@mail.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 999 123-45-67'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'г. Москва, ул. Ленина, д. 1'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля красивыми (Bootstrap)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'