# /bin/python
# author - chancel.yang
import urllib.request
import os
import sys
import time
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import unquote
from collections import namedtuple


config_object = None

def get_local_record():
    ''' 读取本地已下载列表
    '''
    print("读取本地已下载列表")
    records = []
    download_record_file_path = os.path.join(
        str(sys.path[0]), "download_record.txt")
    if os.path.exists(download_record_file_path) is False:
        return records
    for line in open(download_record_file_path):
        records.append(line)
    return records


def commit_download_task(url):
    ''' 提交下载任务到Aria2

    Args：
        url：下载链接
    '''
    print("正在发布任务(url：%s)" % url)
    _accept = 'application/json, text/plain, */*'
    _content_type = 'application/json;charset=UTF-8'
    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    params = [[url]]
    if config_object.download_path is not None:
        file_path = config_object.download_path
        for _item in [unquote(x,'utf-8') for x in (url.split('/')[3:-1])]:
            file_path = os.path.join(file_path,_item)
        params.append({"dir": file_path})
    data = {'id': str(time.time()), 'jsonrpc': '2.0', "method": "aria2.addUri",
            "params": params}
    response = requests.post(config_object.aria2_rpc_url, json.dumps(data))
    return response.ok


def analyze_url(url):
    ''' 分析下载链接

    Args:
        url: 下载链接
    '''
    records = get_local_record()
    for _item in records:
        if _item == url + "\n":
            print("Url [%s] 已存在下载历史，正在跳过")
            return
    if config_object.ignore_file_type.enable is True:
        _file_format = url.split(".")[-1]
        if _file_format in config_object.ignore_file_type.formats:
            print("Url [%s] 文件格式属于忽略名单，正在跳过")
            return
    commit_result = commit_download_task(url)
    if commit_result:
        print("发布成功，写入本地记录文件")
        download_record_file_path = os.path.join(
            str(sys.path[0]), "download_record.txt")
        with open(download_record_file_path, "a") as f:
            f.write(url + '\n')
        return
    print("任务发布失败")


def get_href_by_nginx(url):
    ''' 分析文件下载链接

    Args：
        Nginx的页面地址
    '''
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features='html.parser')
    tags = soup.find_all('a')
    _hrefs = []
    for tag in tags:
        href = tag.get('href').strip()
        if href == "../":
            continue
        if href[-1] == "/":
            _hrefs.extend(get_href_by_nginx(url+href))
            continue
        _hrefs.append(url+href)
    return _hrefs


if __name__ == "__main__":
    print("正在读取配置文件")
    with open(os.path.join(sys.path[0],'config.json'),'r') as f:
        config_object = f.read()
    print("配置文件内容 %s" % config_object)
    config_object = json.loads(config_object, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    print("开始解析Nginx服务器的文件列表")
    for nginx_url_item in config_object.nginx_url:
        hrefs = get_href_by_nginx(nginx_url_item)
        print("解析文件下载Url集合完成，开始发布下载任务")
        for href in hrefs:
            analyze_url(href)
