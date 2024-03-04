from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.utils.translation import gettext_lazy as _
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, username, password, firstname, lastname, phone_1, phone_2=None, **other_fields):
        if not email:
            raise ValueError(_("Vous devez renseigner une adresse email"))
        if not username:
            raise ValueError(_("Vous devez renseigner un nom utilisateur"))
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            username=username, 
            firstname=firstname, 
            lastname=lastname, 
            phone_1=phone_1,
            phone_2=phone_2,
            **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, firstname, lastname, password, **other_fields):
        """ other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_admin", True)
        if other_fields.get("is_staff") is not True:
            raise ValueError('is staff is set to False')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser is set to False')
        if other_fields.get('is_admin') is not True:
            raise ValueError('is_admin is set to False')
        return self.create_user(email, username, first_name, password, **other_fields) """
        user = self.model(
            email=email,
            username=username,
            firstname=firstname,
            lastname=lastname,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_admin=True,
            **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=60, unique=True)
    username = models.CharField(max_length=60, unique=True)
    firstname = models.CharField(max_length=60, blank=True, null=True)
    lastname = models.CharField(max_length=60, blank=True, null=True)
    phone_1 = models.CharField(max_length=60, unique=True, blank=False, null=False)
    phone_2 = models.CharField(max_length=60, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'firstname', 'lastname', 'phone_1', 'phone_2']

    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.lastname} {self.firstname}"

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    # this methods are require to login super user from admin panel
    def has_module_perms(self, app_label):
        return self.is_staff
    