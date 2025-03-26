import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import uuid
#  Custom User Manager
class UserManager(BaseUserManager):
  def create_user(self, email, name, phone, gender, is_active, dob, referral_code, referrer_by, profile_image, tc, role, special_offers, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email = self.normalize_email(email),
          name = name,
          phone = phone,
          gender = gender,
          dob = dob,
          referral_code = referral_code,
          referrer_by = referrer_by,
          profile_image = profile_image,
          is_active = is_active,
          role = role,
          special_offers = special_offers,
          tc = tc,
      )

      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(verbose_name='Email', max_length=255, unique=True,)
  name = models.CharField(max_length=200)
  phone = models.CharField(max_length=200, default='', blank=True)
  gender = models.CharField(max_length=200, default='', blank=True)
  dob = models.CharField(max_length=200, default='', blank=True)
  referral_code = models.CharField(max_length=50, default='', blank=True)
  referrer_by = models.CharField(max_length=50, default='', blank=True)
  city = models.CharField(max_length=50, default='', blank=True)
  country = models.CharField(max_length=50, default='', blank=True)
  profile_image = models.CharField(max_length=300, default='', blank=True)
  role = models.CharField(max_length=100, default='')
  special_offers = models.DecimalField(max_digits=10, decimal_places=2, default=0)

  tc = models.BooleanField()
  is_active = models.BooleanField(default=False)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']

  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin
  

class ShortenedURL(models.Model):
    email = models.EmailField(verbose_name='Email', max_length=255)
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True)
    custom_url = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255, default='Untitled')
    created_at = models.DateTimeField(auto_now_add=True)
    qr = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
    
class URLVisit(models.Model):
    short_url = models.ForeignKey(
        ShortenedURL,
        on_delete=models.CASCADE,
        related_name='visits'
    )
    timestamp = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField()
    location = models.CharField(max_length=255, default="Unknown")
    user_agent = models.TextField()
    device_type = models.CharField(max_length=20, default="Unknown")

    # ✅ Added fields for advanced analytics
    referrer = models.CharField(max_length=500, null=True, blank=True)  # Tracks where the visit came from
    browser = models.CharField(max_length=50, default="Unknown")         # Browser type
    os = models.CharField(max_length=50, default="Unknown")               # Operating system (Windows, Mac, Android, etc.)
    is_mobile = models.BooleanField(default=False)                       # Mobile or Desktop flag
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True) # Longitude

    def __str__(self):
        return f"Visit to {self.short_url.short_code} from {self.ip_address} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']  # Latest visits first
        indexes = [
            models.Index(fields=['short_url', 'timestamp']),
            models.Index(fields=['ip_address']),
        ]