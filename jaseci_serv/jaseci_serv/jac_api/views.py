import json
from base64 import b64encode
from io import BytesIO
from tempfile import _TemporaryFileWrapper
from time import time

from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jaseci.element.element import Element
from jaseci.utils.utils import logger, ColCodes as Cc
from jaseci_serv.base.models import Master as ServMaster
from jaseci_serv.svc import MetaService
from jaseci_serv.user_api import serializers as user_slzr


class JResponse(Response):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hook = master._h
        self.hook.commit_all_cache_sync()

    def close(self):
        super(JResponse, self).close()
        # Commit db changes after response to user
        self.hook.commit(True)


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
        self.log_request_stats(request)
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        General post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)
        api_result = self.caller.general_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats(request)
        return self.issue_response(api_result)

    def log_request_stats(self, request):
        """Api call preamble"""
        tot_time = time() - self.start_time
        save_count = 0
        touch_count = 0
        db_touches = 0
        touch_kb = 0
        if isinstance(self.caller, Element):
            save_count = len(self.caller._h.save_obj_list)
            touch_count = len(self.caller._h.mem.keys())
            db_touches = self.caller._h.db_touch_count
            red_touches = self.caller._h.red_touch_count
            touch_kb = self.caller._h.mem_size()
        logger.info(
            str(
                f"API call to {Cc.TG}{type(self).__name__}{Cc.EC}"
                f" completed in {Cc.TY}{tot_time:.3f} seconds{Cc.EC}"
                f" touched {Cc.TY}{touch_count}{Cc.EC} mem /"
                f" {Cc.TY}{red_touches}{Cc.EC} redis /"
                f" {Cc.TY}{db_touches}{Cc.EC} db "
                f" ({Cc.TY}{touch_kb:.1f}kb{Cc.EC}) and"
                f" saving {Cc.TY}{save_count}{Cc.EC} objects."
            )
        )

        hook = self.caller._h
        hook.meta.app.post_request_hook(type(self).__name__, request, tot_time) if (
            hook.meta.run_svcs and hook.meta.app != None
        ) else None

    def proc_prime_ctx(self, request, req_data):
        try:
            if "ctx" in request.FILES:
                ctx = request.FILES.pop("ctx")[0]
                if ctx.content_type == "application/json":
                    req_data["ctx"] = json.loads(ctx.read().decode("utf-8"))
            elif "ctx" in req_data and type(req_data["ctx"]) is not dict:
                req_data["ctx"] = json.loads(req_data["ctx"])
        except ValueError:
            logger.error("Invalid ctx format! Ignoring ctx parsing!")

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

    def proc_request_ctx(self, request, req_data, raw_req_data):
        user_slzr.requests_for_emails = request
        req_query = request.GET.dict()
        req_data.update(
            {
                "_req_ctx": {
                    "method": request.method,
                    "headers": dict(request.headers),
                    "query": req_query,
                    "body": req_data.copy(),
                },
                "_raw_req_ctx": raw_req_data.decode("utf-8"),
            }
        )
        req_data.update(req_query)

    def proc_request(self, request, **kwargs):
        """Parse request to field set"""
        raw_req_data = request.body
        pl_peek = str(dict(request.data))[:256]
        logger.info(str(f"Incoming call to {type(self).__name__} with {pl_peek}"))
        self.start_time = time()

        req_data = (
            request.data.dict() if type(request.data) is not dict else request.data
        )

        self.proc_prime_ctx(request, req_data)
        self.proc_file_ctx(request, req_data)
        self.proc_request_ctx(request, req_data, raw_req_data)

        req_data.update(kwargs)

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
        if (
            isinstance(api_result, dict)
            and "report_custom" in api_result.keys()
            and api_result["report_custom"] is not None
        ):
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
        self.log_request_stats(request)
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        Public post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)

        api_result = self.caller.public_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats(request)
        return self.issue_response(api_result)

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = ServMaster(
            h=MetaService().build_hook(),
            persist=False,
        )

    def issue_response(self, api_result):
        """Issue response from call"""
        # If committer set, results should be saved back
        status = self.pluck_status_code(api_result)

        if (
            isinstance(api_result, dict)
            and "report_custom" in api_result.keys()
            and api_result["report_custom"] is not None
        ):
            api_result = api_result["report_custom"]

        if self.caller._pub_committer:
            return JResponse(self.caller._pub_committer, api_result, status=status)
        else:
            return Response(api_result, status=status)
