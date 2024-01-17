from django.db import models
from service.constant import STARS
from account.models import UserAccount

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 50)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.name
    
class Service(models.Model):
    service_name = models.CharField(max_length = 100)
    description = models.TextField()
    price = models.DecimalField(max_digits=12,decimal_places=2)
    image = models.ImageField(upload_to = 'service/images/')
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def average_rating(self):
        if self.reviews.exists():
            total_ratings = sum(review.rating for review in self.reviews.all())
            average_rating = total_ratings / self.reviews.count()
            return round(average_rating, 2)
        else:
            return None

    def __str__(self):
        return self.service_name
    
class Review(models.Model):
    customer_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    rating = models.IntegerField(choices = STARS, default = 5)
    service = models.ForeignKey(Service, on_delete= models.CASCADE, related_name = 'reviews')
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.customer_name
    

class Cart(models.Model):
    service = models.ForeignKey(Service, on_delete = models.CASCADE)
    customer = models.ForeignKey(UserAccount, on_delete = models.CASCADE)
    is_order_confirm = models.BooleanField(default=False)

    def __str__(self):
        return self.service.service_name