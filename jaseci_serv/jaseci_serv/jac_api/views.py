from rest_framework.views import APIView
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from jaseci.utils.utils import logger
from jaseci.element.element import element
from jaseci_serv.base.orm_hook import orm_hook
from jaseci_serv.base.models import JaseciObject, GlobalVars
from jaseci_serv.base.models import master as core_master
from time import time


class JResponse(Response):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master = master
        for i in self.master._h.save_obj_list:
            self.master._h.commit_obj_to_redis(i)
        self.master._h.skip_redis_update = True

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

    def post(self, request, **kwargs):
        """
        General post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)
        api_result = self.caller.general_interface_to_api(
            self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def log_request_stats(self):
        """Api call preamble"""
        TY = '\033[33m'
        TG = '\033[32m'
        EC = '\033[m'  # noqa
        tot_time = time()-self.start_time
        save_count = 0
        if(isinstance(self.caller, element)):
            save_count = len(self.caller._h.save_obj_list)
        logger.info(str(
            f'API call to {TG}{type(self).__name__}{EC}'
            f' completed in {TY}{tot_time:.3f} seconds{EC}'
            f' saving {TY}{save_count}{EC} objects.'))

    def proc_request(self, request, **kwargs):
        """Parse request to field set"""
        pl_peek = str(dict(request.data))[:256]
        logger.info(str(
            f'Incoming call to {type(self).__name__} with {pl_peek}'))
        self.start_time = time()
        self.cmd = request.data.dict() if type(
            request.data) is not dict else request.data
        self.cmd.update(kwargs)
        self.set_caller(request)
        self.res = "Not valid interaction!"

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = request.user.get_master()

    def pluck_status_code(self, api_result):
        """Extracts status code out of payload"""
        status = 200
        if(isinstance(api_result, dict) and 'status_code' in api_result):
            status = api_result['status_code']
        return status

    def issue_response(self, api_result):
        """Issue response from call"""
        # self.caller._h.commit()
        # return Response(api_result)
        # for i in self.caller._h.save_obj_list:
        #     self.caller._h.commit_obj_to_redis(i)
        status = self.pluck_status_code(api_result)
        return JResponse(self.caller, api_result, status=status)


class AbstractAdminJacAPIView(AbstractJacAPIView):
    """
    The abstract base for Jaseci Admin APIs
    """
    permission_classes = (IsAuthenticated, IsAdminUser)


class AbstractPublicJacAPIView(AbstractJacAPIView):
    """
    The abstract base for Jaseci Admin APIs
    """
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        """
        Public post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)

        api_result = self.caller.public_interface_to_api(
            self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = core_master(h=orm_hook(
            objects=JaseciObject.objects,
            globs=GlobalVars.objects
        ), persist=False)

    def issue_response(self, api_result):
        """Issue response from call"""
        # If committer set, results should be saved back
        status = self.pluck_status_code(api_result)
        if(self.caller._pub_committer):
            return JResponse(self.caller._pub_committer,
                             api_result, status=status)
        else:
            return Response(api_result, status=status)
