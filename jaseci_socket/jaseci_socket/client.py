import websocket
import rel
from orjson import dumps, loads
from os import environ


def on_message(ws, msg):
    print(loads(msg))


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")


def on_open(ws):
    print("Opened connection")


if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "ws://localhost:8001",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    ws.run_forever(
        dispatcher=rel, reconnect=5
    )  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly
    ws.send(dumps({"type": "connect", "data": {"auth": environ.get("SOCKET_AUTH")}}))
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
