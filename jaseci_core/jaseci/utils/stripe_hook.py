from django.db import IntegrityError
from jaseci_serv.base import models


class stripe_hook:
    def get_obj(name: str):
        """get stripe config by name"""
        try:
            return models.StripeVars.objects.get(name=name).value
        except models.StripeVars.DoesNotExist:
            print(f"{name} doesn't exist")
            return False

    def save_obj(name: str, value: str):
        """set stripe config"""
        try:
            obj = models.StripeVars.objects.create(name=name, value=value)
            # obj = self.get_obj(name)

            return True
        except IntegrityError as e:
            # f"{name} is already exist"
            return False

    def list_obj(self):
        """get list of stripe config"""

        cfg_list = list(models.StripeVars.objects.all().values())

        # exclude id from the list
        cfg_list = [
            {key: val for key, val in sub.items() if key != "id"} for sub in cfg_list
        ]

        return cfg_list

    def delete_obj(self, name: str):
        """get stripe config by name"""
        try:
            obj = models.StripeVars.objects.get(name=name)
            obj.delete()

            return True
        except models.StripeVars.DoesNotExist:
            # f"{name} doesn't exist"
            return False
