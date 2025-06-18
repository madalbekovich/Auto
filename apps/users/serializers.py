from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from . import models
import re

class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    first_name = serializers.CharField(required=True)
    phone = serializers.CharField(
        required=True,
        min_length=12,
        error_messages={"min_length": "Введите правильный номер"},
    )

    class Meta:
        model = models.User
        fields = ["phone", "first_name", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        attrs["phone"] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"

        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают!")

        if models.User.objects.filter(phone=attrs.get("phone")).exists():
            raise serializers.ValidationError("Такой номер уже существует!")

        return attrs

    def save(self, **kwargs):
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]
        password = self.validated_data["password"]

        user = models.User(
            phone=phone,
            first_name=first_name,
        )
        user.set_password(password)
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
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=True,
        error_messages={"min_length": "Не менее 8 символов."},
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