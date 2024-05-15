from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import os 
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField
import random 
from django.utils.timezone import now
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from cloudinary_storage.storage import VideoMediaCloudinaryStorage
from cloudinary_storage.validators import validate_video 

USER_TYPE = (("HOD", "HOD"), ( "Staff", "Staff"), ("Student", "Student"))
GENDER = [("M", "Male"), ("F", "Female")]
from django.db.models.signals import post_save
from django.dispatch import receiver
PROGRAM = (("All", "All"), ("BL", "BL"),("BE", "BE"),("BP", "BP"), ("BCS", "BCS"))
AUDIENCE_CHOICES = [
    ("WebDesign", "WebDesign"),
    ("GraphicsDesign", "GraphicsDesign"),
    ("UI/UX", "UI/UX"),
    ("StoreKeeping", "StoreKeeping"),
    ("DigitalExplorer", "DigitalExplorer"),
    ("WebDevelopment", "WebDevelopment"),
    ("Coding", "Coding"),
    ("TradingTitans", "TradingTitans"),
    ("PhotoshopProdigy", "PhotoshopProdigy"),
    ("CulinaryCanvas", "CulinaryCanvas"),
    ("SocialMediaMaverick", "SocialMediaMaverick"),
    ("FitProInstructor", "FitProInstructor"),
    ("NumberCruncher", "NumberCruncher"),
    ("WeddingWizard", "WeddingWizard"),
    ("WordPress Wiz", "WordPress Wiz"),
    ("Influence Igniter", "Influence Igniter"),
    ("Stocks Savvy", "Stocks Savvy"),
    ("E-commerce Expertise", "E-commerce Expertise"),
    ("Digital Explorer", "Digital Explorer"),
]


PROGRAM = (("All", "All"),
            ("BL", "BL"),
            ("BE", "BE"),
            ("BP", "BP"), 
            ("BCS", "BCS"))



def school_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename
    filename = f'{instance.email}.{ext}'
    # Return the file path
    return os.path.join('uploads', 'cred1', filename)

def school_file_path2(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename
    filename = f'{instance.email}.{ext}'
    # Return the file path
    return os.path.join('uploads', 'cred2', filename)

def school_file_path3(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename
    filename = f'{instance.email}.{ext}'
    # Return the file path
    return os.path.join('uploads', 'cred3', filename)

def course_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename
    filename = f'{instance._id}.{ext}'
    # Return the file path
    return os.path.join('uploads', 'course', filename)

def coupon_file_path(instance, filename):
    # Get the file extension
    ext = filename.split('.')[-1]
    # Generate a new filename
    filename = f'{instance._id}.{ext}'
    # Return the file path
    return os.path.join('uploads', 'coupon', filename)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('isWebAdmin', True)        
        return self.create_user(email, password, **extra_fields)
    


class Course(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    Instructor = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    courseduration = models.CharField(max_length=255, blank=True, null=True)
    streamingtime = models.CharField(max_length=255, blank=True, null=True)
    startingday = models.CharField(max_length=255, blank=True, null=True)
    endingday = models.CharField(max_length=255, blank=True, null=True)
    image =  models.ImageField(upload_to='post/image', blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

'''
{ "MerchantRequestID":"1c5b-4ba8-815c-ac45c57a3db0284908",
  "CheckoutRequestID":"ws_CO_03052024110555066740408496",
    "ResponseCode": "0",
      "ResponseDescription":"Success. Request accepted for processing",
  "CustomerMessage":"Success. Request accepted for processing" }
'''

class CoursePurchaseRequest(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    client_id = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)  # Changed to IntegerField 
    MerchantRequestID = models.CharField(max_length=255, blank=True, null=True) 
    CheckoutRequestID = models.CharField(max_length=255, blank=True, null=True) 
    ResponseCode = models.CharField(max_length=255, blank=True, null=True) 
    ResponseDescription = models.CharField(max_length=255, blank=True, null=True) 
    CustomerMessage = models.CharField(max_length=255, blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_id} request to buy course {self.course_id} with {self.phone}" 

 
class LNMOnline(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    ResultCode = models.IntegerField(blank=True, null=True)
    ResultDesc = models.CharField(max_length=120, blank=True, null=True)
    Amount = models.FloatField(blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    Balance = models.CharField(max_length=12, blank=True, null=True)
    TransactionDate = models.DateTimeField(blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.MpesaReceiptNumber}"
from django.contrib.postgres.fields import ArrayField

class CouponPurchase(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(max_length=255, blank=True, null=True)
    payment_receipt= models.FileField(blank=True, null=True,  upload_to=coupon_file_path)
    no_of_coupon = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

  

class CoursePurchaseCoupon(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    coupon_code = models.CharField(max_length=255, blank=True, null=True)
    course_id = models.CharField(max_length=255, blank=True, null=True)
    student_id = models.CharField(max_length=255, blank=True, null=True)



class Events(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    title = models.CharField(max_length=100)
    startingtime = models.CharField(max_length=120)
    endtime = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    class_link = models.TextField(blank=True, null=True)
    class_password = models.TextField(blank=True, null=True)
    startingday = models.DateField(blank=False, null=True)
    endingday = models.DateField(blank=False, null=True)
    audience = models.CharField(max_length=50, choices=AUDIENCE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update related users based on audience
        related_users = Users.objects.filter(my_courses=self.audience)
        for user in related_users:
            if user.my_events is not None and self not in user.my_events.all():
                user.my_events.add(self)

@receiver(post_save, sender=Events)
def update_users_on_event_save(sender, instance, **kwargs):
    # This function listens to post_save signals of Events model
    # and updates related Users accordingly
    related_users = Users.objects.filter(my_courses=instance.audience)
    for user in related_users:
        if user.my_events is not None and instance not in user.my_events.all():
            user.my_events.add(instance)


class Users(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_groups'
    )

    # Add related_name to user_permissions field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_permissions'
    )
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    gender = models.CharField(max_length=1, blank=True, null=True, choices=GENDER)
    birthday = models.CharField(max_length=255, blank=True, null=True)
    bio = models.CharField(max_length=255, blank=True, null=True)
    extracurricular = models.CharField(max_length=255, blank=True, null=True)
    mda_imageUrl = models.FileField(max_length=1000, blank=True, null=True)
    photo_imageUrl = models.ImageField(blank=True, null=True)
    school_credentials_imageUrl = models.FileField(blank=True, null=True)
    terms_and_agreement_imageUrl = models.FileField(blank=True, null=True)
    emailfield = models.CharField(max_length=255, blank=True, null=True, unique=True)
    profile_imageId =  models.CharField(max_length=255, blank=True, null=True)
    profile_imageUrl = models.ImageField(max_length=1000, blank=True, null=True)
    background_imageId =  models.CharField(max_length=255, blank=True, null=True)
    background_imageUrl = models.ImageField(max_length=1000, blank=True, null=True)
    address = models.TextField()
    Program = models.CharField(max_length=255, blank=True, null=True)
    my_events = models.ForeignKey(Events, on_delete=models.CASCADE, blank=True, null=True)
    courses = models.ManyToManyField(Course, blank=True)  # Change ForeignKey to ManyToManyField
    Term = models.CharField(max_length=255, blank=True, null=True)
    school_credentials_two_imageId = models.CharField(max_length=255, blank=True, null=True)
    school_credentials_two_imageUrl = models.CharField(max_length=1000, blank=True, null=True)
    school_credentials_three_imageId = models.CharField(max_length=255, blank=True, null=True)
    school_credentials_three_imageUrl = models.CharField(max_length=1000, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    sales_person_id = models.CharField(max_length=1000, blank=True, null=True)
    my_courses = models.CharField(max_length=50, blank=True, null=True, choices=AUDIENCE_CHOICES)
    is_notification = models.BooleanField(default=False)
    no_of_notifications = models.IntegerField(default=0, blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=True)
    is_monthly_paid = models.BooleanField(default=False)
    is_registeration_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_sales = models.BooleanField(default=False)
    isWebAdmin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_email_confirmed = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def save(self, *args, **kwargs):
        # Generate emailfield based on first_name, last_name if it's null or empty
        if not self.emailfield and (self.first_name or self.last_name):
            random_digits = ''.join(random.choices('0123456789', k=2))
            self.emailfield = f"{self.first_name.lower()}.{self.last_name.lower()}.{random_digits}@universal.edu"

  

class EmailSubscription(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    email = models.EmailField(max_length=255, blank=True, null=True)


class Post(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    image =  models.ImageField(upload_to='post/image', blank=True, null=True)
    video = models.FileField(upload_to='post/videos', blank=True, storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
    caption = models.CharField(max_length=10000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Books(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    Book_imageUrl = models.FileField(upload_to='pdf_files/')
    created_at = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    audience = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption    


    



class Video(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    
    description = models.CharField(max_length=1024)
    file = models.FileField(upload_to='videos/', blank=True, storage=VideoMediaCloudinaryStorage(),
                              validators=[validate_video])
    image = models.ImageField(upload_to='images/thumbnail', blank=True)  
    caption = models.CharField(max_length=255, blank=True, null=True)
    audience = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class meta:
        ordering = ['title']

