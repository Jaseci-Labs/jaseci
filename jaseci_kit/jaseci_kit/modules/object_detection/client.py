import asyncio
import websockets
import base64
import cv2


def base64EncodeImage(img):
    """Takes an input image and returns a base64 encoded string representation of that image (jpg format)"""
    _, im_arr = cv2.imencode(".jpg", img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode("utf-8")

    return im_b64

#TODO Allow user to input jpeg image of their choice
#TODO Add video streaming functionality
img = cv2.imread('images/sherry-christian-8Myh76_3M2U-unsplash.jpg')
encoded_img = base64EncodeImage(img)


async def test():
    async with websockets.connect('ws://localhost:8000/ws') as Websocket:
        while True:
            print("sending image to server::")
            await Websocket.send(encoded_img)
            #response = await Websocket.recv()
            #print("This is the response::", response)


asyncio.get_event_loop().run_until_complete(test())