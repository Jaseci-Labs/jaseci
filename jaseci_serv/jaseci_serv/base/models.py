import uuid
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.db.models import Q

from jaseci.api.interface import Interface
from jaseci.element.master import Master as CoreMaster
from jaseci.element.super_master import SuperMaster as CoreSuper
from jaseci_serv.settings import JASECI_CONFIGS
from jaseci_serv.svc import MetaService
from jaseci_serv.base.jsorc import JsOrcApi


class Master(CoreMaster):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._valid_configs += JASECI_CONFIGS

    def user_creator(self, name, password, other_fields: dict = {}):
        """
        Create a master instance and return root node master object

        other_fields used for additional fields for overloaded interfaces
        (i.e., Django interface)
        """
        from jaseci_serv.user_api.serializers import UserSerializer, SuperUserSerializer

        data = {"email": name, "password": password}
        for i in other_fields.keys():
            data[i] = other_fields[i]
        serializer = (
            UserSerializer(data=data)
            if get_user_model().objects.count()
            else SuperUserSerializer(data=data)
        )
        if serializer.is_valid(raise_exception=False):
            mas = serializer.save().get_master()
            mas._h = self._h
            return mas
        else:
            return {"error": serializer._errors, "status_code": 400}

    def superuser_creator(self, name, password, other_fields: dict = {}):
        """
        Create a master instance and return root node master object

        other_fields used for additional fields for overloaded interfaces
        (i.e., Django interface)
        """
        from jaseci_serv.user_api.serializers import SuperUserSerializer

        data = {"email": name, "password": password}
        for i in other_fields.keys():
            data[i] = other_fields[i]
        serializer = SuperUserSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            mas = serializer.save().get_master()
            mas._h = self._h
            return mas
        else:
            return {"error": serializer._errors, "status_code": 400}

    def user_destroyer(self, name: str):
        """
        Permanently delete master with given id
        """
        try:
            get_user_model().objects.get(email=name).delete()
            return True
        except Exception:
            return False


class SuperMaster(Master, JsOrcApi, CoreSuper):
    @Interface.admin_api()
    def master_allusers(
        self, limit: int = 10, offset: int = 0, asc: bool = False, search: str = None
    ):
        """
        Returns info on a set of users, limit specifies the number of users to
        return and offset specfies where to start
        """

        if (limit < 0) or (offset < 0):
            return {"response": "Error occured! Parameters must be `positive numbers`!"}
        users = get_user_model().objects.all()

        if not asc:
            users = users.order_by("-time_created")

        if search:
            condition = Q(email__icontains=search) | Q(name__icontains=search)
            users = users.complex_filter(condition)

        total = users.count()
        end = offset + limit if limit else total
        filtered_users = []

        for i in users[offset:end]:
            filtered_users.append(
                {
                    "id": i.id,
                    "user": i.email,
                    "jid": i.master.urn,
                    "name": i.name,
                    "created_date": i.time_created.isoformat(),
                    "is_activated": i.is_activated,
                    "is_superuser": i.is_superuser,
                }
            )
        ret = {"total": total, "data": filtered_users}

        return ret


class UserManager(BaseUserManager):
    """
    Custom User Manager for Jaseci

    Note: Every user is linked to a single root node that is created upon the
    creation of the user.
    """

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        # Makes first user admin
        if not get_user_model().objects.filter(is_admin=True).exists():
            return self.create_superuser(email, password, **extra_fields)
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create user's root node
        user.master = MetaService().build_master(h=user._h, name=email).id
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
        user.master = MetaService().build_super_master(h=user._h, name=email).id
        user._h.commit()

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model to use email instead of username

    Root node  is attached to each User and created at user creation
    """

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_activated = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    master = models.UUIDField(default=uuid.uuid4)
    objects = UserManager()

    def __init__(self, *args, **kwargs):
        self._h = MetaService().build_hook()
        AbstractBaseUser.__init__(self, *args, **kwargs)
        PermissionsMixin.__init__(self, *args, **kwargs)

    USERNAME_FIELD = "email"

    def get_master(self):
        """Returns main user Jaseci node"""
        return self._h.get_obj(caller_id=self.master.urn, item_id=self.master.urn)

    def delete(self):
        JaseciObject.objects.filter(j_master=self.master.urn).delete()
        JaseciObject.objects.filter(jid=self.master.urn).delete()
        super().delete()


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

    jid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    j_parent = models.UUIDField(null=True, blank=True)
    j_master = models.UUIDField(null=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    kind = models.CharField(max_length=255, blank=True)
    j_timestamp = models.DateTimeField(default=datetime.utcnow)
    j_type = models.CharField(max_length=15, default="node")
    j_access = models.CharField(max_length=15, default="private")
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
