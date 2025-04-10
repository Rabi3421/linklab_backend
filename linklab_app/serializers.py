from .models import User, SubscriptionPlan, UserSubscription
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

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ['user', 'plan', 'start_date', 'end_date']

class SubscribeUserSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()

    def validate_plan_id(self, value):
        try:
            return SubscriptionPlan.objects.get(id=value)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Invalid subscription plan ID.")


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'