from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(
        self,
        username,
        email,
        first_name,
        last_name,
        password,
        is_staff,
        is_superuser,
        **extra_fields,
    ):
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
        self, username, email, first_name, last_name, password=None, **extra_fields
    ):
        return self._create_user(
            username,
            email,
            first_name,
            last_name,
            password,
            False,
            False,
            **extra_fields,
        )

    def create_superuser(
        self, username, email, first_name, last_name, password=None, **extra_fields
    ):
        return self._create_user(
            username, email, first_name, last_name, password, True, True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Nombre de usuario",
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Correo",
    )
    first_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nombre",
    )
    last_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Apellido",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )
    is_staff = models.BooleanField(
        default=True, verbose_name="Puede Entrar a la Adminstración"
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]  #

    def __str__(self):
        return f"{self.username}"
