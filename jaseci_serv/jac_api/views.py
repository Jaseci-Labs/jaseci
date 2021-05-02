from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from jaseci.utils.utils import logger
from time import time


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

        api_result = self.master.general_interface_to_api(
            self.cmd, type(self).__name__)
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
