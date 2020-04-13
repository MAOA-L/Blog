from bus.models import BusInfo
from common.utils import requests_get, html_to_etree


def grab_base_bus():
    url = "http://bm.eyuyao.com/bus/mobile/lineList.php?k=pp&q="
    list_rule = "/html/body/div/ul[@class='list borderNone mbNone']/li/a"

    res = requests_get(url=url)
    parse_html = html_to_etree(html_raw=res)
    bus_list = parse_html.xpath(list_rule)
    bus = []
    for i in bus_list:
        href_list = i.xpath('./@href')
        if href_list:
            href = href_list[0]
            name = i.text
            bus.append({
                "name": name,
                "href": href
            })
    return bus


if __name__ == '__main__':
    grab_base_bus()