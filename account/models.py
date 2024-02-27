from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserAccount(AbstractUser):
    address = models.TextField()
    balance = models.DecimalField( max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    image = models.ImageField(upload_to='account/images/')


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Admin(models.Model):
    user = models.OneToOneField(UserAccount, on_delete = models.CASCADE)
    is_admin = models.BooleanField(default = False)

    def __str__(self) -> str:
        return self.user.first_name