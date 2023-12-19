import rel
import websocket
from websocket import WebSocketApp as wsa
from jaseci.jsorc.jsorc import JsOrc
from jaseci.utils.utils import logger
from orjson import loads, dumps
from requests import get


@JsOrc.service(
    name="socket",
    config="SOCKET_CONFIG",
    manifest="SOCKET_MANIFEST",
    priority=0,
    pre_loaded=True,
)
class SocketService(JsOrc.CommonService):
    def run(self):
        self.method = {
            "server_connect": self.server_connect,
            "client_connect": self.client_connect,
        }
        self.prefix = self.config.get("prefix") or "jws-"
        self.app = websocket.WebSocketApp(
            self.config.get("url"),
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
        )
        self.ping()

        self.app.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)

    def post_run(self):
        self.spawn_daemon(socket=rel.dispatch)

    def ping(self):
        get(self.config.get("ping_url")).raise_for_status()

    def send(self, ws: wsa, data: dict):
        try:
            ws.send(dumps(data))
        except Exception:
            logger.exception("Failed to send event!")

    ###################################################
    #                     METHODS                     #
    ###################################################

    def server_connect(self, ws: wsa, data: dict):
        if not self.quiet:
            logger.info(data)

    def client_connect(self, ws: wsa, data: dict):
        data["user"] = "public"
        self.send(ws, {"type": "client_connected", "data": data})

    ###################################################
    #                     ACTIONS                     #
    ###################################################

    def notify(self, type: str, target: str, data: dict):
        self.send(
            self.app,
            {"type": f"notify_{type}", "data": {"target": target, "data": data}},
        )

    ###################################################
    #                     EVENTS                      #
    ###################################################

    def on_message(self, ws: wsa, event):
        event: dict = loads(event)
        if not self.quiet:
            logger.info(event)

        method = self.method.get(event["type"])
        if method:
            method(ws, event.get("data") or {})

    def on_error(self, ws: wsa, error):
        self.failed(Exception(error))

    def on_close(self, ws: wsa, close_status_code, close_msg):
        if not self.quiet:
            msg = f"Socket connection closed!\n{close_msg}"
            logger.info(msg)
            self.failed(Exception(msg))

    def on_open(self, ws: wsa):
        self.send(
            ws,
            {"type": "server_connect", "data": {"auth": self.config.get("auth")}},
        )

    ###################################################
    #                     CLEANER                     #
    ###################################################

    def failed(self, error):
        super().failed(error)
        self.terminate_daemon("socket")

    # ---------------- PROXY EVENTS ----------------- #

    def on_delete(self):
        try:
            if self.is_running():
                self.app.close()

            self.terminate_daemon("socket")
        except Exception:
            pass
