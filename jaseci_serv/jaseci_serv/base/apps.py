from django.apps import AppConfig


class CoreApiConfig(AppConfig):
    name = 'base'

    def ready(self):
        from jaseci.actions.live_actions import load_preconfig_actions
        from jaseci_serv.base.orm_hook import orm_hook
        from jaseci_serv.base.models import JaseciObject, GlobalVars
        hook = orm_hook(
            objects=JaseciObject.objects,
            globs=GlobalVars.objects
        )
        load_preconfig_actions(hook)
