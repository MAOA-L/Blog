# -*- coding: utf-8 -*-
"""
 @Time    : 20/3/3 11:18
 @Author  : CyanZoy
 @File    : consumer.py
 @Software: PyCharm
 @Describe: 
 """
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, JsonWebsocketConsumer, AsyncJsonWebsocketConsumer
from channels.layers import get_channel_layer

from common.log import log_common


class ChatConsumer(AsyncJsonWebsocketConsumer):
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

    # async def receive_json(self, text_data=None, bytes_data=None):
    async def receive_json(self, content, **kwargs):
        log_common.info(content)
        await self.channel_layer.group_send(
            "chat",
            {
                "type": "p.chat",
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

    async def p_chat(self, event):
        await self.send_json(event)


class ViewSocket:
    @classmethod
    def group_send(cls, channel_name, event, channel_layer=None):
        if not channel_layer:
            channel_layer = cls.get_c_layer()
        async_to_sync(channel_layer.group_send)(channel_name, event)

    @classmethod
    def private_send(cls, channel_name, event, channel_layer=None):
        if not channel_layer:
            channel_layer = cls.get_c_layer()
        async_to_sync(channel_layer.send)(channel_name, event)

    @staticmethod
    def get_c_layer(name="default"):
        return get_channel_layer(alias=name)
