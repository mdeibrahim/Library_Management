from rest_framework import serializers
from .models import Member, Profile

class ProfileNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['name', 'age', 'gender', 'address', 'phone']


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileNestedSerializer(read_only=True)

    class Meta:
        model = Member
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'is_active', 'date_joined', 'profile']
        read_only_fields = ['id', 'email', 'date_joined']
