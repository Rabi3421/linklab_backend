from .models import User
from rest_framework import serializers

class UserRegistrationSerializerwithgoogle(serializers.ModelSerializer):
  # We are writing this becoz we need confirm password field in our Registratin Request
  # password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
  class Meta:
    model = User
    fields=['email', 'name', 'phone', 'gender', 'dob', 'profile_image', 'referral_code', 'referrer_by', 'tc', 'is_active', 'role', 'special_offers']

class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'name', 'phone', 'gender', 'profile_image', 'dob', 'city', 'country', 'referral_code', 'referrer_by', 'is_active', 'tc', "role", 'special_offers']