import uuid
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin
from jaseci_serv.jaseci_serv.settings import JASECI_CONFIGS
from django.contrib.auth import get_user_model
from jaseci_serv.base.orm_hook import orm_hook
from jaseci.element.master import master as core_master
from jaseci.element.super_master import super_master as core_super
from jaseci.api.interface import interface


class master(core_master):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._valid_configs += JASECI_CONFIGS

    @interface.private_api()
    def master_create(self, name: str, set_active: bool = True,
                      other_fields: dict = {}):
        """
        Create a master instance and return root node master object

        other_fields used for additional fields for overloaded interfaces
        (i.e., Django interface)
        """
        data = {'email': name}
        for i in other_fields.keys():
            data[i] = other_fields[i]
        from jaseci_serv.user_api.serializers import UserSerializer
        serializer = UserSerializer(data=data)
        if(serializer.is_valid(raise_exception=False)):
            mas = serializer.save().get_master()
            mas._h = self._h
            return self.make_me_head_master_or_destroy(mas)
        else:
            return {'response': "Errors occurred",
                    'errors': serializer.errors}

    @interface.private_api()
    def master_delete(self, name: str):
        """
        Permanently delete master with given id
        """
        if(not self.sub_master_ids.has_obj_by_name(name)):
            return {'response': f"{name} not found"}
        self.sub_master_ids.destroy_obj_by_name(name)
        get_user_model().objects.get(email=name).delete()
        return {'response': f"{name} has been destroyed"}


class super_master(master, core_super):

    @interface.admin_api()
    def master_createsuper(self, name: str, set_active: bool = True,
                           other_fields: dict = {}):
        """
        Create a super instance and return root node super object
        """
        data = {'email': name}
        for i in other_fields.keys():
            data[i] = other_fields[i]
        from jaseci_serv.user_api.serializers import SuperUserSerializer
        serializer = SuperUserSerializer(data=data)
        if(serializer.is_valid(raise_exception=False)):
            mas = serializer.save().get_master()
            mas._h = self._h
            return self.make_me_head_master_or_destroy(mas)
        else:
            return {'response': "Errors occurred",
                    'errors': serializer.errors}

    @interface.admin_api()
    def master_allusers(self, num: int = 0, start_idx: int = 0):
        """
        Returns info on a set of users, num specifies the number of users to
        return and start idx specfies where to start
        """
        users = get_user_model().objects.all()
        start = start_idx if start_idx else 0
        end = start_idx + num if num else len(users)
        ret = []
        for i in users[start:end]:
            ret.append({'user': i.email, 'jid': i.master.urn})
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
        if(not get_user_model().objects.filter(is_admin=True).exists()):
            return self.create_superuser(email, password, **extra_fields)
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        # Create user's root node
        user.master = master(h=user._h, name=email).id
        if('set_sent_global' in extra_fields and
           extra_fields['set_sent_global']):
            user.master.sentinel_active_global()
        if('create_graph' in extra_fields and
           extra_fields['create_graph']):
            user.master.graph_create()
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
        user.master = super_master(h=user._h, name=email).id
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
        self._h = orm_hook(
            objects=JaseciObject.objects,
            globs=GlobalVars.objects
        )
        AbstractBaseUser.__init__(self, *args, **kwargs)
        PermissionsMixin.__init__(self, *args, **kwargs)

    USERNAME_FIELD = 'email'

    def get_master(self):
        """Returns main user Jaseci node"""
        return self._h.get_obj(caller_id=self.master.urn, item_id=self.master)

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
