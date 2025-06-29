from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    password=None,
                    first_name=None, 
                    last_name=None,
                    **extra_fields
                    ):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        
        # Create a dictionary with only the fields that exist in the model
        user_data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        
        # Filter out None values and create the user object
        user = self.model(**{k: v for k, v in user_data.items() if v is not None})
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Made compatible with Django's built-in createsuperuser management command.
        """
        # Set default values for first_name and last_name if not provided
        if 'first_name' not in extra_fields:
            extra_fields['first_name'] = 'Admin'
        if 'last_name' not in extra_fields:
            extra_fields['last_name'] = 'User'
            
        # Create a regular user
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        
        # Set superuser attributes
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)


#CustomerUser Details
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email is already required by USERNAME_FIELD
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True
    )
    
    class Meta:
        ordering = ['first_name']
        verbose_name = 'Custom User'
        verbose_name_plural = 'Custom Users'
        
    def __str__(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.email
    

# Tailor Details - Create a separate manager for TailorDetail model
class TailorManager(BaseUserManager):
    def create_user(self,
                    username,
                    full_name,
                    national_id_number,
                    phone_number,
                    password=None,
                    email=None,
                    sex=None,
                    area_of_residence=None,
                    area_of_work=None,
                    **extra_fields
                    ):
        """
        Creates and saves a Tailor with the given details.
        """
        if not username:
            raise ValueError('Tailors must have a username')
        
        if email:
            email = self.normalize_email(email)
            
        user = self.model(
            username=username,
            full_name=full_name,
            national_id_number=national_id_number,
            phone_number=phone_number,
            email=email,
            sex=sex,
            area_of_residence=area_of_residence,
            area_of_work=area_of_work,
            **extra_fields
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, full_name, national_id_number, phone_number, password=None, **extra_fields):
        """
        Creates and saves a tailor superuser.
        """
        user = self.create_user(
            username=username,
            full_name=full_name,
            national_id_number=national_id_number,
            phone_number=phone_number,
            password=password,
            
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
class TailorDetail(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = TailorManager() 
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name', 'national_id_number', 'phone_number']
    
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    national_id_number = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    area_of_residence = models.CharField(max_length=255)
    area_of_work = models.CharField(max_length=255)
    date_of_registration = models.DateField(auto_now_add=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='tailordetail_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(  # Fixed typo in field name
        'auth.Permission',
        related_name='tailordetail_set',
        blank=True,
    )

    def __str__(self):
        return self.full_name

# Tailor Products
class TailorProduct(models.Model):
    CATEGORY_CHOICES = [
        ('SUIT', 'Suit'),
        ('TSHIRT', 'T-Shirt'),
        ('TROUSER', 'Trouser'),
        ('GAUNI', 'Gauni'),
    ]

    tailor = models.ForeignKey(TailorDetail, related_name='products', on_delete=models.CASCADE)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    product_name = models.CharField(max_length=255)
    product_image = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    measurement_guides = models.TextField()  # Measurement instructions for this product
    
    def clean(self):
        if self.cost < 0:
             raise ValidationError('Cost cannot be negative.')
         
    def save(self, *args, **kwargs):
        self.full_clean()  # This will call the clean method before saving
        super().save(*args, **kwargs)     

    def __str__(self):
        return f"{self.product_name} - {self.category}"