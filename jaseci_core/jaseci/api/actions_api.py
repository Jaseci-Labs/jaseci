"""
Admin Global api functions as a mixin
"""
from jaseci.api.interface import interface
import jaseci.actions.live_actions as lact
import json


class actions_api():
    """
    Admin global APIs
    """

    @interface.admin_api(cli_args=['file'])
    def actions_load_local(self, file: str):
        """
        Hot load a python module and assimlate any Jaseci Actions
        """
        success = lact.load_local_actions(file)
        if(success):
            cur_config = self.config_get('ACTION_SETS')
            if(cur_config and (not isinstance(cur_config, list))):
                config = json.loads(cur_config)
                if file not in config['local']:
                    config['local'].append(file)
                    self.config_set('ACTION_SETS', json.dumps(config))
            else:
                self.config_set('ACTION_SETS',
                                json.dumps({'local': [file], 'remote': []}))
        return {"success": success}

    @interface.admin_api(cli_args=['url'])
    def actions_load_remote(self, url: str):
        """
        Hot load an actions set from live pod at URL
        """
        success = lact.load_remote_actions(url)
        if(success):
            cur_config = self.config_get('ACTION_SETS')
            if(cur_config and (not isinstance(cur_config, list))):
                config = json.loads(cur_config)
                if url not in config['remote']:
                    config['remote'].append(url)
                    self.config_set('ACTION_SETS', json.dumps(config))
            else:
                self.config_set('ACTION_SETS',
                                json.dumps({'local': [], 'remote': [url]}))
        return {"success": success}

    # @interface.admin_api()
    # def actions_get(self, name: str, value: str):
    #     """
    #     """

    @interface.admin_api()
    def actions_list(self, name: str = ''):
        """
        List all live jaseci actions
        """
        actions = list(lact.live_actions.keys())
        if(len(name)):
            actions = list(filter(lambda a: a.startswith(name), actions))
        return actions

    # @interface.admin_api()
    # def actions_delete(self, name: str, value: str):
    #     """
    #     """
