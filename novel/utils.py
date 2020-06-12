# -*- coding: utf-8 -*-
"""
 @Time    : 2020/4/11 23:24
 @Author  : CyanZoy
 @File    : utils.py
 @Software: PyCharm
 @Describe: 
 """
from common.log import log_common
from common.utils import requests_get, html_to_etree


def get_content(sections, content_rule, host=None, decode="utf-8"):
    # 遍历章节 [{"id":'xxx', "url": 'xxx'}]
    result = []
    count = 1
    for obj in sections:
        pk = obj.get("id")
        url = obj.get("url")
        log_common.info(msg=f"章节名{obj.get('name')}-{count}")
        # 获取章节内容
        content = parse_content(sections_url=host + url, content_rule=content_rule, decode=decode)
        result.append({
            "id": pk,
            "content": content
        })
        count += 1

    return result


def parse_content(sections_url, content_rule, decode="utf-8"):
    """提取小说内容"""
    # TODO 多线程获取小说内容
    # if isinstance(sections_url, str):
    #     sections_url = [sections_url]
    # assert not isinstance(sections_url, list)

    # 发送请求获取页面数据
    res = requests_get(url=sections_url, decode=decode)
    # 解析页面
    parse_html = html_to_etree(res)
    # 获取规则下的标签
    content_tab = parse_html.xpath(content_rule)
    # 提取主体内容
    if content_tab:
        return "".join([i.tail if i.tail else "\n\n" for i in content_tab[0]])
        # content = content_tab[0].xpath("string(.)")
        # log_common.out(msg=f"内容{content[:10]}")
    return None
