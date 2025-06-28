from rest_framework import serializers
from apps.member.models import Member
import random
from datetime import timedelta
from django.utils import timezone

from django.core.mail import send_mail


class MemberRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = Member
        fields = ['first_name', 'last_name','email', 'password','confirm_password']
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True, 'min_length': 8},
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'confirm_password': {'write_only': True, 'min_length': 8}
        }
        
    def validate(self, data):
        if data['password']!= data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        otp = str(random.randint(100000, 999999))
        print(otp)
        otp_exp = timezone.now() + timedelta(minutes=50)
        user = Member.objects.create_user(
            password=password,
            is_active=False,
            otp=otp,
            otp_exp=otp_exp,
            otp_verified=False,
            **validated_data
        )
        user.save()
        # send mail
        send_mail(
            subject="Account Verification",
            message=f"Your OTP is {otp}. It is valid for 50 minutes.",
            from_email="mmeibrahim505@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user
    

