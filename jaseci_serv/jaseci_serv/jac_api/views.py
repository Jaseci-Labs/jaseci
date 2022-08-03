import json
from tempfile import _TemporaryFileWrapper
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
from base64 import b64encode
from io import BytesIO


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

    http_method_names = ["post"]
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        """
        General GET function that parses api signature to load parms
        SuperSmart GET - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)
        api_result = self.caller.general_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        General post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)
        api_result = self.caller.general_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def log_request_stats(self):
        """Api call preamble"""
        TY = "\033[33m"
        TG = "\033[32m"
        EC = "\033[m"  # noqa
        tot_time = time() - self.start_time
        save_count = 0
        if isinstance(self.caller, element):
            save_count = len(self.caller._h.save_obj_list)
        logger.info(
            str(
                f"API call to {TG}{type(self).__name__}{EC}"
                f" completed in {TY}{tot_time:.3f} seconds{EC}"
                f" saving {TY}{save_count}{EC} objects."
            )
        )

    def proc_prime_ctx(self, request, req_data):
        try:
            if "ctx" in request.FILES:
                ctx = request.FILES.pop("ctx")[0]
                if ctx.content_type == "application/json":
                    req_data["ctx"] = json.loads(ctx.read().decode("utf-8"))
            elif "ctx" in req_data and type(req_data["ctx"]) is not dict:
                req_data["ctx"] = json.loads(req_data["ctx"])
        except ValueError:
            logger.error(str(f"Invalid ctx format! Ignoring ctx parsing!"))

    def proc_file_ctx(self, request, req_data):
        for key in request.FILES:

            req_data.pop(key)
            file_ref = (
                req_data["ctx"]
                if "ctx" in req_data and type(req_data["ctx"]) is dict
                else req_data
            )
            file_ref[key] = []

            for file in request.FILES.getlist(key):

                file_type = type(file.file)
                if file_type is BytesIO:
                    file_base64 = b64encode(file.file.getvalue()).decode("utf-8")
                elif file_type is _TemporaryFileWrapper:
                    file_base64 = b64encode(file.file.read()).decode("utf-8")

                if "file_base64" in vars():
                    file_ref[key].append(
                        {
                            "name": file.name,
                            "base64": file_base64,
                            "content-type": file.content_type,
                        }
                    )

    def proc_request_ctx(self, request, req_data):
        req_query = request.GET.dict()
        req_data.update(
            {
                "_req_ctx": {
                    "method": request.method,
                    "headers": dict(request.headers),
                    "query": req_query,
                    "body": req_data.copy(),
                }
            }
        )
        req_data.update(req_query)

    def proc_request(self, request, **kwargs):
        """Parse request to field set"""
        pl_peek = str(dict(request.data))[:256]
        logger.info(str(f"Incoming call to {type(self).__name__} with {pl_peek}"))
        self.start_time = time()

        req_data = (
            request.data.dict() if type(request.data) is not dict else request.data
        )

        req_data.update(kwargs)

        self.proc_prime_ctx(request, req_data)
        self.proc_file_ctx(request, req_data)
        self.proc_request_ctx(request, req_data)

        self.cmd = req_data
        self.set_caller(request)
        self.res = "Not valid interaction!"

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = request.user.get_master()

    def pluck_status_code(self, api_result):
        """Extracts status code out of payload"""
        status = 200
        if isinstance(api_result, dict) and "status_code" in api_result:
            status = api_result["status_code"]
        return status

    def issue_response(self, api_result):
        """Issue response from call"""
        # self.caller._h.commit()
        # return Response(api_result)
        # for i in self.caller._h.save_obj_list:
        #     self.caller._h.commit_obj_to_redis(i)
        status = self.pluck_status_code(api_result)
        if isinstance(api_result, dict) and "report_custom" in api_result.keys():
            api_result = api_result["report_custom"]
        return JResponse(self.caller, api_result, status=status)


class AbstractAdminJacAPIView(AbstractJacAPIView):
    """
    The abstract base for Jaseci Admin APIs
    """

    http_method_names = ["post"]
    permission_classes = (IsAuthenticated, IsAdminUser)


class AbstractPublicJacAPIView(AbstractJacAPIView):
    """
    The abstract base for Jaseci Admin APIs
    """

    http_method_names = ["post"]
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs):
        """
        Public GET function that parses api signature to load parms
        SuperSmart GET - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)

        api_result = self.caller.public_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        Public post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)

        api_result = self.caller.public_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats()
        return self.issue_response(api_result)

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = core_master(
            h=orm_hook(objects=JaseciObject.objects, globs=GlobalVars.objects),
            persist=False,
        )

    def issue_response(self, api_result):
        """Issue response from call"""
        # If committer set, results should be saved back
        status = self.pluck_status_code(api_result)

        if isinstance(api_result, dict) and "report_custom" in api_result.keys():
            api_result = api_result["report_custom"]

        if self.caller._pub_committer:
            return JResponse(self.caller._pub_committer, api_result, status=status)
        else:
            return Response(api_result, status=status)
