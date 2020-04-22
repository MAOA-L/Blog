from common.utils import requests_get, html_to_etree


def grab_base_bus():
    """抓取公交基础信息"""
    url = "http://bm.eyuyao.com/bus/mobile/lineList.php?k=pp&q="
    list_rule = "/html/body/div/ul[@class='list borderNone mbNone']/li/a"

    res = requests_get(url=url)
    parse_html = html_to_etree(html_raw=res)
    bus_list = parse_html.xpath(list_rule)
    bus = []
    # TODO 获取反向的车 -
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


def grab_bus_real_url(raw):
    """抓取公交实况url"""
    host = 'http://bm.eyuyao.com/bus/mobile/'
    result = []
    for i in raw:
        pk = i.get("id")
        grab_url = i.get("url")
        # 抓取实况url
        res = requests_get(url=host + grab_url)
        parse_html = html_to_etree(html_raw=res)
        real_url = parse_html.xpath('/html/body/header/div[2]/a/@href')
        print(real_url)
        if real_url:
            result.append({
                "id": pk,
                "real_url": real_url[0]
            })
    return result


def grab_bus_real_info(pk, url):
    """抓取公交实况url"""
    result = []
    # 抓取实况url
    res = requests_get(url=url)
    parse_html = html_to_etree(html_raw=res)
    station_list = parse_html.xpath('//*[@id="touchBox"]/li')
    for i in station_list:
        station_id = i.xpath("./@id")
        if station_id:
            result.append({
                "id": pk,
                "station_id": station_id[0],
                "name": i.text
            })
    return result


def grab_ajax_data(real_url):
    """根据real_url抓取ajax的url"""
    import re
    res = requests_get(url=real_url)
    # parse_html = html_to_etree(html_raw=res)
    # ajax = parse_html.xpath('/html/head/script[3]')
    m1 = re.findall("data:(.*)", res)
    m2 = re.findall(r"\"([a-zA-Z0-9=&]+)", "".join(m1))
    if m2:
        return m2[0]
    # parse_html = html_to_etree(html_raw=res)
    # station_list = parse_html.xpath('//*[@id="touchBox"]/li')


def grab_real_info(data, service=None):
    """抓取实时信息"""
    if service is None:
        service = "http://bm.eyuyao.com/bus/mobile/getGpsInfoCs.php?{data}"

    url = service.format(data=data)
    res = requests_get(url=url, j=True)
    return res


if __name__ == '__main__':
    grab_real_info(data="num=102&pdxianlu=1")
