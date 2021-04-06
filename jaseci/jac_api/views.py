from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.utils.utils import logger
from core.element import element
from time import time
import uuid


class JResponse(Response):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master

    def close(self):
        super(JResponse, self).close()
        # Commit db changes after response to user
        self.master._h.commit()


class AbstractJacAPIView(APIView):
    """
    The builder set of Jaseci APIs
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        General post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request)
        param_map = {}
        for i in self.api_sig.parameters.keys():
            if (i == 'self'):
                continue
            p_name = i
            p_type = self.api_sig.parameters[i].annotation
            param_map[i] = self.get_param(name=p_name, typ=p_type)
            if (param_map[i] is None):
                logger.error(self.res)
                return Response(self.res)
        if (len(param_map) < len(self.cmd)-1):
            logger.warning(
                str(f'Unused parameters in API call - '
                    f'got {self.cmd.keys()}, expected {param_map.keys()}'))
        api_result = getattr(self.master, type(self).__name__)(**param_map)
        self.log_request_time()
        return JResponse(self.master, api_result)

    def log_request_time(self):
        """Api call preamble"""
        TY = '\033[33m'
        TG = '\033[32m'
        EC = '\033[m'  # noqa
        tot_time = time()-self.start_time
        logger.info(str(
            f'API call to {TG}{type(self).__name__}{EC}'
            f' completed in {TY}{tot_time:.3f} seconds.{EC}'))

    def proc_request(self, request):
        """Parse request to field set"""
        pl_peek = str(dict(request.data))[:256]
        logger.info(str(
            f'Incoming call to {type(self).__name__} with {pl_peek}'))
        self.start_time = time()
        self.cmd = request.data
        self.master = request.user.get_master()
        self.res = "Not valid interaction!"

    def get_param(self, name, typ):
        """Parse request to field set, req flags if required"""
        if (name in self.cmd.keys()):  # TODO: BETTER ERROR REPORTING IF ISSUE
            val = self.cmd[name]
            if (issubclass(typ, element)):
                val = self.master._h.get_obj(uuid.UUID(val))
                if (isinstance(val, typ)):
                    return val
                else:
                    self.res += f'{type(val)} is not {typ}'
                    return None
            else:
                return val
        else:
            self.res += f'\nInvalid API parameter set - {self.cmd}'
            logger.error(self.res)
            return None
