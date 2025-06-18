from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from . import models, serializers
from apps.helpers.services import sms as service
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            phone = serializer.data["phone"]
            user = models.User.objects.get(phone=phone)

            sms = service.send_sms(phone, "Подтвердите номер телефона", user.code)
            if sms:
                return Response(
                    {
                        "response": True,
                        "message": "Код подверждение был отправлен на ваш номер.",
                    },
                    status=201,
                )
            return Response(
                {"response": False, "message": "Введите правильные данные!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyPhoneView(generics.GenericAPIView):
    serializer_class = serializers.VerifyPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            phone = serializer.data["phone"]

            try:
                user = models.User.objects.get(phone=phone)

                if user.activated:
                    return Response({"message": "Аккаунт уже подтвержден"})

                if user.code == code:
                    user.activated = True
                    user.save()

                    token, created = Token.objects.get_or_create(user=user)

                    return Response(
                        {
                            "response": True,
                            "message": "Пользователь успешно зарегистрирован.",
                            "token": token.key,
                        }
                    )
                return Response(
                    {"response": False, "message": "Введен неверный код"}
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": "Пользователь с таким телефоном не существует",
                    }
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendCodeView(generics.GenericAPIView):
    serializer_class = serializers.SendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]

            try:
                user = models.User.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "reponse": False,
                        "message": "Пользователь с таким телефоном не существует",
                    },
                )
            if not user.activated:
                user.save()

                service.send_sms(phone, "Ваш новый код подтверждения", user.code)

                return Response({"response": True, "message": "Код отправлен"})

            return Response(
                {"response": False, "message": "Аккаунт уже подтвержден"}
            )
        return Response(serializer.errors)


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = request.data.get("phone")
            password = request.data.get("password")

            try:
                models.User.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": "Пользователь с указанными телефоном не существует",
                    }
                )

            user = authenticate(request, phone=f"{''.join(filter(str.isdigit, phone))}", password=password)

            if not user:
                return Response(
                    {
                        "response": False,
                        "message": "Неверный пароль",
                    }
                )

            if user.activated:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "response": True,
                        "message": "",
                        "token": token.key,
                    }
                )
            return Response(
                {
                    "response": False,
                    "message": "Подтвердите номер чтобы войти!",
                    "isactivated": False,
                }
            )

        return Response(serializer.errors)

class UserUpdateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = serializers.UserUpdateSerializer

    def patch(self, request):
        user = request.user
        serializer = self.serializer_class(user, request=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"response": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors)

