
from django.db import models
from django.db.models import Min, Max, Sum, Avg

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'category', default = 'category/default-image.jpg')
    discreption = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title

    def product_category_count(self):
        products_cat = Product.objects.filter(category=self).count()
        return products_cat 

    
    def min_prices_product(self):
        min_product = Product.objects.filter(category=self).order_by("price").first()
        return min_product

class Brand(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'brand')
    discreption = models.TextField(blank=True)

    def product_brand_count(self):
        products_brand = Product.objects.filter(brand=self).count()
        return products_brand

    def __str__(self) -> str:
        return self.title

class Banner_list(models.Model):
    title = models.CharField(max_length=200)
    bg_image = models.ImageField(upload_to = 'banner_list/bg_image')
    product_image = models.ImageField(upload_to = 'banner_list/product_image')

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.FloatField(default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    discreption = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title

    def images(self):
        image = Image.objects.get(product=self)
        return image  

    def discount_price(self):
        price = self.price
        discount = Discount.objects.get(product = self)
        chegirma = price * (100 - discount.discount) / 100
        return chegirma

    def discount(self):
        discount = Discount.objects.get(product = self)
        return discount.discount
        
    def information_wealth(self):
        information = Informations.objects.get(product = self) 
        return information.wealth

class Discount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount = models.IntegerField(default=0)
    start_date_discount = models.DateTimeField(auto_now_add=True)
    end_date_discount = models.DateTimeField(auto_created=False)

    def __str__(self):
        return f"{self.product.title} && {self.discount}%"

    
    
    

class Filter(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    start_price = models.PositiveIntegerField(default=0)
    end_price = models.PositiveIntegerField(default=0)

class Image(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'product_image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Informations(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wealth = models.CharField(max_length=200)
    size = models.CharField(max_length=200, blank=True)
    discreption = models.TextField()

    def __str__(self):
        return self.discreption[:15]

class Widsh_List(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{{self.owner}}"

class User_type(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class Post(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'post')
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} {self.text[:50]}"
    
class Cart(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    order = models.BooleanField(blank=False)

    def __str__(self):
        return self.owner.username

class Cart_item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, blank=True, null=True)
    count = models.IntegerField(default=0)
    total = models.FloatField(default=0)
    order_time = models.DateTimeField(null=True)
    
    def __str__(self):
        return self.product.title

class Advertisem(models.Model):
    image = models.ImageField(upload_to = 'advertisem')
    title = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Profile(models.Model):
    telephone = models.CharField(max_length = 200)
    zip_code = models.PositiveIntegerField()

    def __str__(self):
        return self.order

class Comment(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField()
 
    def __str__(self):
        return f"{self.owner} {self.body[:20]}"

class Like(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    like = models.BooleanField(blank=False)
     
    def __str__(self):
        return self.product

class Contact(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return f"{self.owner} {self.subject}"
        
    


    


        
    
    
    