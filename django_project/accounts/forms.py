from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
      class Meta:
            model = CustomUser
            # fields = UserCreationForm.Meta.fields  + ("age",)
            fields = (                                                      # for see and fill all the details during signup
                        "username",
                        "email",
                        "age",
                  )
            
class CustomUserChangeForm(UserChangeForm):
      class Meta:
            model = CustomUser
            # fields = UserChangeForm.Meta.fields
            
            fields = (                                                     # for see and fill all the details during signup
                        "username",
                        "email",
                        "age",
                  )