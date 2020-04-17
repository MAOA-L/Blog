# -*- coding: utf-8 -*-
"""
 @Time    : 20/3/3 11:18
 @Author  : CyanZoy
 @File    : consumer.py
 @Software: PyCharm
 @Describe: 
 """
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.channel_layer.group_add(
            "chat",
            self.channel_name
        )
        await self.accept()
        # Or accept the connection and specify a chosen subprotocol.
        # A list of subprotocols specified by the connecting client
        # will be available in self.scope['subprotocols']
        # await self.accept("subprotocol")
        # To reject the connection, call:
        # await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        await self.channel_layer.group_send(
            "chat",
            {
                "msg": "Hello"
            }
        )
        # await self.send(json.dumps({
        #     "msg": "Hello"
        # }))
        # Or, to send a binary frame:
        # await self.send(bytes_data="Hello world!")
        # Want to force-close the connection? Call:
        # await self.close()
        # Or add a custom WebSocket error code!
        # await self.close(code=4123)

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.channel_layer.group_discard(
            "chat",
            self.channel_name
        )
