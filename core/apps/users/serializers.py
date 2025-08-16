from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models
import re

class RegisterSerializers(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    phone = serializers.CharField(
        required=True,
        min_length=12,
        error_messages={"min_length": "Введите правильный номер"},
    )

    class Meta:
        model = models.User
        fields = ["phone", "first_name"]



    def save(self, **kwargs):
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]

        user = models.User(
            phone=phone,
            first_name=first_name,
        )
        user.save()
        return user


class VerifyPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
    )
    code = serializers.IntegerField(
        required=True
    )

    class Meta:
        fields = ["phone", "code"]

    def validate(self, attrs):
        phone = ''.join(filter(str.isdigit, attrs.get("phone")))
        if not phone.startswith("996"):
            phone = f"996{phone}"
        attrs["phone"] = phone
        return super().validate(attrs)


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ["phone"]

    def validate_phone(self, value):
        phone = re.sub(r'\D', '', value)
        return phone

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(
        write_only=True,
        required=True,
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['phone'] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"
        return super().validate(attrs)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'avatar', 'email', 'phone', 'gender']