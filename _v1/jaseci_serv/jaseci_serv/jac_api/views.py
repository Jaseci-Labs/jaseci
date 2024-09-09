import json
from io import BytesIO
from tempfile import _TemporaryFileWrapper
from time import time

from django.http import FileResponse
from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jaseci.jsorc.jsorc import JsOrc
from jaseci.prim.element import Element
from jaseci.utils.file_handler import FileHandler
from jaseci.utils.utils import logger, ColCodes as Cc
from jaseci.utils.actions.actions_manager import ActionManager
from jaseci_serv.base.models import Master as ServMaster
from jaseci_serv.user_api import serializers as user_slzr

# The limit for logging an object (request payload and response): 5MB
# Will truncate in the logs if the object exceeds this limit
OBJECT_LOG_LIMIT = 5 * 1024 * 1024


class JResponse(Response):
    def __init__(self, master, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hook = master._h
        self.hook.commit_all_cache_sync()

    def close(self):
        super(JResponse, self).close()
        # Commit db changes after response to user
        self.hook.clean_file_handler()
        self.hook.commit(True)


class JFileResponse(FileResponse):
    def __init__(self, hook, file_id: str) -> None:
        file_handler: FileHandler = hook.get_file_handler(file_id)
        file_handler.close()
        file_handler.open(mode="rb", encoding=None)

        super().__init__(file_handler.buffer, filename=file_handler.name)

        self.hook = hook
        self.hook.commit_all_cache_sync()

    def close(self) -> None:
        super().close()
        self.hook.clean_file_handler()
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
        self.log_request_stats(request, api_result)
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        General post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)
        api_result = self.caller.general_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats(request, api_result)
        return self.issue_response(api_result)

    def log_request_stats(self, request, api_result):
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

        res_peek = str(api_result)[:256]
        log_str = str(
            f"API call from {Cc.TG}{self.caller.name}{Cc.EC}:{self.caller.jid}"
            f" to {Cc.TG}{type(self).__name__}{Cc.EC}"
            f" completed in {Cc.TY}{tot_time:.3f} seconds{Cc.EC}"
            f" touched {Cc.TY}{touch_count}{Cc.EC} mem /"
            f" {Cc.TY}{red_touches}{Cc.EC} redis /"
            f" {Cc.TY}{db_touches}{Cc.EC} db "
            f" ({Cc.TY}{touch_kb:.1f}kb{Cc.EC}) and"
            f" saving {Cc.TY}{save_count}{Cc.EC} objects."
            f" Response: {res_peek}."
        )

        log_dict = {
            "api_name": type(self).__name__,
            "request_latency": tot_time,
            "objects_touched": touch_count,
            "redis_touches": red_touches,
            "db_touches": db_touches,
            "objects_touched_size": touch_kb,
            "objects_saved": save_count,
            "caller_name": self.caller.name,
            "caller_jid": self.caller.jid,
        }
        # Add custom fields depending on the type of API
        if log_dict["api_name"] == "walker_run":
            log_dict["walker_name"] = self.cmd.get("name", "")
            log_dict["success"] = (api_result.get("success", True),)
        try:
            api_result_str = json.dumps(api_result)[:OBJECT_LOG_LIMIT]
        except TypeError:
            api_result_str = str(api_result)[:OBJECT_LOG_LIMIT]
        log_dict["api_response"] = api_result_str

        log_dict["extra_fields"] = list(log_dict.keys())

        logger.info(log_str, extra=log_dict)
        JsOrc.get("action_manager", ActionManager).post_request_hook(
            type(self).__name__, request, tot_time
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
            logger.error("Invalid ctx format! Ignoring ctx parsing!")

    def proc_file_ctx(self, request, req_data):
        hook = self.caller._h
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
                    file_ref[key].append(
                        hook.add_file_handler(
                            FileHandler.fromBytesIO(
                                file.file, file.name, file.content_type, key
                            )
                        )
                    )
                elif file_type is _TemporaryFileWrapper:
                    file_ref[key].append(
                        hook.add_file_handler(
                            FileHandler.fromTemporaryFileWrapper(
                                file.file, file.name, file.content_type, key
                            )
                        )
                    )

    def proc_request_ctx(self, request, req_data, raw_req_data):
        user_slzr.requests_for_emails = request
        hook = self.caller._h
        req_query = request.GET.dict()
        req_data.update(
            {
                "_req_ctx": {
                    "method": request.method,
                    "headers": dict(request.headers),
                    "query": req_query,
                    "body": req_data.copy(),
                    "raw": hook.add_file_handler(
                        FileHandler.fromBytesIO(
                            BytesIO(raw_req_data), "raw_request", None
                        )
                    ),
                }
            }
        )
        req_data.update(req_query)

    def proc_request(self, request, **kwargs):
        """Parse request to field set"""
        raw_req_data = request.body
        pl_peek = str(dict(request.data))[:256]
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        self.set_caller(request)
        log_str = str(
            f"Incoming call from {Cc.TG}{self.caller.name}{Cc.EC}:{self.caller.jid} to {Cc.TG}{type(self).__name__}{Cc.EC} with {pl_peek} via {user_agent}"
        )
        log_dict = {
            "api_name": type(self).__name__,
            "caller_name": self.caller.name,
            "caller_jid": self.caller.jid,
            "request_user_agent": user_agent,
        }
        # Add custom field based on type of API
        if log_dict["api_name"] == "walker_run":
            log_dict["walker_name"] = request.data.get("name", "")
        try:
            request_payload_str = json.dumps(dict(request.data))[:OBJECT_LOG_LIMIT]
        except TypeError:
            request_payload_str = str(dict(request.data))[:OBJECT_LOG_LIMIT]
        log_dict["request_payload"] = request_payload_str
        log_dict["extra_fields"] = list(log_dict.keys())

        logger.info(log_str, extra=log_dict)

        self.start_time = time()

        req_data = (
            request.data.dict() if type(request.data) is not dict else request.data
        )

        self.set_caller(request)

        self.proc_prime_ctx(request, req_data)
        self.proc_file_ctx(request, req_data)
        self.proc_request_ctx(request, req_data, raw_req_data)

        req_data.update(kwargs)

        self.cmd = req_data
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
        if isinstance(api_result, dict):
            if (
                "report_custom" in api_result.keys()
                and api_result["report_custom"] is not None
            ):
                return JResponse(
                    self.caller, api_result["report_custom"], status=status
                )
            elif (
                "report_file" in api_result.keys()
                and api_result["report_file"] is not None
            ):
                return JFileResponse(self.caller._h, api_result["report_file"])

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
        self.log_request_stats(request, api_result)
        return self.issue_response(api_result)

    def post(self, request, **kwargs):
        """
        Public post function that parses api signature to load parms
        SuperSmart Post - can read signatures of master and process
        bodies accordingly
        """
        self.proc_request(request, **kwargs)

        api_result = self.caller.public_interface_to_api(self.cmd, type(self).__name__)
        self.log_request_stats(request, api_result)
        return self.issue_response(api_result)

    def set_caller(self, request):
        """Assigns the calling api interface obj"""
        self.caller = ServMaster(
            h=JsOrc.hook(),
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
