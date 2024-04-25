from django.conf import settings
from django.contrib.auth.models import Group, Permission
from rest_framework import serializers

from .models import *


class User_Representation_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class User_Create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "groups",
            "user_permissions",
        )

    def create(self, validated_data):
        # print(validated_data)
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def to_representation(self, value):
        return User_Representation_Serializer(value).data


class User_Retrieve_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class User_List_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class User_Update_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)


class User_Destroy_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def to_representation(self, value):
        return User_Representation_Serializer(value).data
