from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    """Form for using UI to create user"""
    class Meta:
        fields = ('email', 'password1', 'password2', 'name')
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Full Name'
        self.fields['email'].label = 'Email Address'
