import uuid
from datetime import datetime

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from django.contrib.auth import get_user_model
from base.orm_hook import orm_hook
from jaseci import master


class UserManager(BaseUserManager):
    """
    Custom User Manager for Jaseci

    Note: Every user is linked to a single root node that is created upon the
    creation of the user.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if(not get_user_model().objects.filter(is_admin=True).exists()):
            return self.create_superuser(email, password, **extra_fields)
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create user's root node
        user.master = master.master(h=user._h, email=email).id
        user._h.commit()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new super user"""
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_activated = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        # Create user's root node
        user.master = master.master(h=user._h, email=email).id
        user._h.commit()

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model to use email instead of username

    Root node  is attached to each User and created at user creation
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    master = models.UUIDField(default=uuid.uuid4)
    objects = UserManager()

    def __init__(self, *args, **kwargs):
        self._h = orm_hook(
            user=self,
            objects=JaseciObject.objects,
            globs=GlobalVars.objects
        )
        AbstractBaseUser.__init__(self, *args, **kwargs)
        PermissionsMixin.__init__(self, *args, **kwargs)

    USERNAME_FIELD = 'email'

    def get_master(self):
        """Returns main user Jaseci node"""
        return self._h.get_obj(caller_id=self.master.urn, item_id=self.master)


class JaseciObject(models.Model):
    """
    Generalized object model for Jaseci object types

    There is one table in db for all object types in the Jaseci machine
    which include nodes, edges, actions, contexts, walkers, and
    sentinels.

    Keep in mind Django's ORM can support many to many relationships
    between recursive schema's which may be useful if necessary in the
    future.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False,
                             on_delete=models.CASCADE)
    jid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    j_parent = models.UUIDField(null=True, blank=True)
    j_master = models.UUIDField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    kind = models.CharField(max_length=255, blank=True)
    j_timestamp = models.DateTimeField(default=datetime.utcnow)
    j_type = models.CharField(max_length=15, default='node')
    j_access = models.CharField(max_length=15, default='private')
    j_r_acc_ids = models.TextField(blank=True)
    j_rw_acc_ids = models.TextField(blank=True)
    jsci_obj = models.TextField(blank=True)


class GlobalVars(models.Model):
    """Global configuration item"""
    name = models.CharField(max_length=31, unique=True)
    value = models.TextField(blank=True)


def lookup_global_config(name, default=None):
    """Helper for looking up GlobalVars, returns default if not found"""
    try:
        return GlobalVars.objects.get(name=name).value
    except GlobalVars.DoesNotExist:
        return default
