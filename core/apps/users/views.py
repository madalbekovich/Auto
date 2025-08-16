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
            phone = serializer.validated_data["phone"]  # Используем validated_data вместо data
            if models.User.objects.filter(phone=phone).exists():
                return Response(
                    {
                        "response": False,
                        "message": "Такой номер уже существует!"
                    },
                    status=status.HTTP_400_BAD_REQUEST  # 400 вместо 200 для ошибки
                )

            user = serializer.save()
            sms = service.send_sms(phone, "Подтвердите номер телефона", user.code)
            if sms:
                return Response(
                    {
                        "response": True,
                        "message": "Код подтверждения был отправлен на ваш номер."
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    "response": False,
                    "message": "Ошибка при отправке SMS"
                },
                status=status.HTTP_400_BAD_REQUEST
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
                    return Response(
                        {
                            "message": "Аккаунт уже подтвержден"
                        }
                )

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
                token, created = Token.objects.get_or_create(user=user)
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
                {"response": False, "message": "Аккаунт уже подтвержден", "token": token.key}
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

