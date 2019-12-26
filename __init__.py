# /bin/python
# author - chancel.yang
import urllib.request
import os
import sys
import time
from bs4 import BeautifulSoup
import requests
import json
from collections import namedtuple


config_object = None

def get_local_record():
    """Read download record by local file"""
    records = []
    download_record_file_path = os.path.join(
        str(sys.path[0]), "download_record.txt")
    if os.path.exists(download_record_file_path) is False:
        return records
    for line in open(download_record_file_path):
        records.append(line)
    return records


def commit_download_task(url):
    """Create download task on aria2"""
    _accept = 'application/json, text/plain, */*'
    _content_type = 'application/json;charset=UTF-8'
    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    params = [[url]]
    if config_object.download_path is not None:
        file_path = config_object.download_path + \
            '/'.join(x for x in (url.split('/')[1:-1]))
        params.append({"dir": file_path})
    data = {'id': str(time.time()), 'jsonrpc': '2.0', "method": "aria2.addUri",
            "params": params}
    response = requests.post(config_object.aria2_rpc_url, json.dumps(data))
    return response.ok


def analyze_url(url):
    """Analyze url"""
    records = get_local_record()
    for _item in records:
        if _item == url + "\n":
            return
    if config_object.disable_file_type.enable is True:
        _file_format = url.split(".")[-1]
        if _file_format in config_object.disable_file_type.formats:
            return
    commit_result = commit_download_task(url)
    if commit_result:
        download_record_file_path = os.path.join(
            str(sys.path[0]), "download_record.txt")
        with open(download_record_file_path, "a") as f:
            f.write(url + '\n')


def get_href_by_nginx(url):
    """Get nginx webpage all href"""
    html = urllib.request.urlopen(url).read().decode("utf-8")
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
    with open(os.path.join(sys.path[0],'config.json'),'r') as f:
        config_object = f.read()
    config_object = json.loads(config_object, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    for nginx_url_item in config_object.nginx_url:
        hrefs = get_href_by_nginx(nginx_url_item)
        for href in hrefs:
            analyze_url(href)
