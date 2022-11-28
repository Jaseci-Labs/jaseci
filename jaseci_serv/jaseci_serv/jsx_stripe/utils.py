from .models import StripeVars
from django.db import IntegrityError


class stripe_hook:
    stripe_key = None

    def get_key():
        """get stripe config by name"""

        if not __class__.stripe_key:
            key = StripeVars.objects.get(name="STRIPE_API_KEY").value
            __class__.stripe_key = key

        return __class__.stripe_key

    def set_key(value: str):
        """set stripe config by name"""

        __class__.save_obj("STRIPE_KEY", value)
        __class__.stripe_key = value

    def get_obj(name: str):
        """get stripe config by name"""
        try:
            return StripeVars.objects.get(name=name).value
        except StripeVars.DoesNotExist:
            print(f"{name} doesn't exist")
            return None

    def save_obj(name: str, value: str):
        """set stripe config"""
        try:
            data = {"value": value}

            obj = StripeVars.objects.update_or_create(name=name, defaults=data)

            return obj
        except IntegrityError as e:
            print(f"{name} is already exist")
            return None

    def list_obj():
        """get list of stripe config"""

        cfg_list = list(StripeVars.objects.all().values())

        # exclude id from the list
        cfg_list = [
            {key: val for key, val in sub.items() if key != "id"} for sub in cfg_list
        ]

        return cfg_list

    def delete_obj(name: str):
        """get stripe config by name"""
        try:
            obj = StripeVars.objects.get(name=name)
            obj.delete()

            return True
        except StripeVars.DoesNotExist:
            print(f"{name} doesn't exist")
            return None
