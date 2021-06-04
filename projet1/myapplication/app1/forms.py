from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import *

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, required=True, error_messages={
        "required": "Please enter your username"
    })
    password = forms.CharField(widget=forms.PasswordInput, required=True, error_messages={
        "required": "Please enter your password"
    })


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")

        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class PartieModelForm(ModelForm):
    titre = forms.CharField(max_length=20, error_messages={'required': 'Veuillez entrer un titre '})
    budget = forms.IntegerField()

    class Meta:
        model = Partie
        fields = ['titre']
        exclude = ['nbchap', 'debit', 'credit', 'solde', 'budget']



    def clean(self):
        titre = self.cleaned_data.get("titre")
        budget = self.cleaned_data.get("budget")

        if titre == '':
            raise forms.ValidationError('title is required')

        if budget == '':
            raise forms.ValidationError('budget is required')

        return self.cleaned_data


    def clean_titre(self):
        titre = self.cleaned_data.get('titre')

        parties = Partie.objects.all()

        for partie in parties:
            if str(titre) == str(partie.titre):
                raise forms.ValidationError("Title already exists")

        return titre


class PartieUpdateForm(ModelForm):
    class Meta:
        model = Partie
        fields = '__all__'
        exclude = ['nbchap', 'debit', 'credit', 'solde']


class ChapitreModelForm(ModelForm):
    titre = forms.CharField(max_length=20, error_messages={
        'required': 'Please enter a title'
    })

    budget = forms.IntegerField(error_messages={
        'required': 'Please enter a budget'
    })

    partie = forms.ModelChoiceField(error_messages={
        "required": 'Please select a partie',
        'invalid': 'Enter a valid field'
    }, queryset=Partie.objects.all())

    class Meta:
        model = Chapitre
        fields = '__all__'
        exclude = ['nbart', 'debit', 'credit', 'solde']

class ChapitreUpdateForm(ModelForm):
    class Meta:
        model = Chapitre
        fields = '__all__'
        exclude = ['nbchap', 'debit', 'credit', 'solde', 'nbart']

class ArticleModelForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = ['debit', 'credit', 'solde']
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'nbchap': forms.NumberInput(attrs={'class': 'form-control'})
        }


class ArticleUpdateForm(ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        exclude = [ 'debit', 'credit', 'solde']
