from django.shortcuts import render
from rest_framework import generics

from base.views import BaseAPIView
from common.return_tool import SuccessHR


class GetMoments(BaseAPIView, generics.ListAPIView):
    """获取片刻列表"""

    def list(self, request, *args, **kwargs):
        a = "我怀着饥饿感寻找家， 不清楚家和饥饿感两者 究竟谁是谁的代名词。 我想我即将和父亲对饮 杯中的浓茶，一如往常， 茶水浓腻的涡旋让我 分不清所处的时光，五岁 或者二十五岁，父亲或许 尚未苍老，我并未长大。 父亲不善言辞，惯于沉默， 戒烟前香烟代表他的情愫。 餐桌上我会揶揄他的厨艺， 他始终笨拙地学不会翻炒， 而我也尝不惯杯中的浓茶。 茶水的苦味在我年轻的时岁 被舌尖放大，仿佛生活的网。 而我已沉默多年，并未想清楚 如何在父亲身上原谅我，或者 如何从我身上理解我的父亲。"
        b = "走在路上我也是一个生动的人 我的头发茂盛像青草 像来自遥远，野外的处女地 胳膊有力地摆动。嘴角 含笑 一点点微微的倔强 "

        return SuccessHR([
            {"title": "记", "content": a[:40]},
            {"title": "随手", "content": b[:45]},
        ])
