# /bin/python
# author - chancel.yang
import urllib.request
import os
import time
from bs4 import BeautifulSoup
import requests
import json

nginx_url = "http://127.0.0.1:9092/"
aria2_url = "http://127.0.0.1:6800/jsonrpc"
restrict_download_format = {
    "enable": True,
    "format": ["mp4", "mkv", "rmvb", "flv", "avi", "mov", "mpg"]
}


def get_href(url):
    """Get Webpage all href"""
    html = urllib.request.urlopen(url).read().decode("utf-8")
    soup = BeautifulSoup(html, features='html.parser')
    tags = soup.find_all('a')
    _hrefs = []
    for tag in tags:
        href = tag.get('href').strip()
        if href == "../":
            continue
        if href[-1] == "/":
            _hrefs.extend(get_href(url+href))
            continue
        _hrefs.append(url+href)
    return _hrefs


def get_local_record():
    """Read download record by local file"""
    records = []
    download_record_file_path = os.path.join(
        str(os.getcwd()), "download_record.txt")
    if os.path.exists(download_record_file_path) is False:
        return records
    for line in open(download_record_file_path):
        records.append(line)
    return records


def analyze_url(url):
    """Analyze url"""
    records = get_local_record()
    for _item in records:
        if _item == url + "\n":
            return
    if restrict_download_format["enable"] is True:
        _file_format = url.split(".")[-1]
        if _file_format not in restrict_download_format["format"]:
            return
    commit_result = commit_download_task(url)
    if commit_result:
        download_record_file_path = os.path.join(
            str(os.getcwd()), "download_record.txt")
        with open(download_record_file_path, "a") as f:
            f.write(url + '\n')


def commit_download_task(url):
    """Create download task on aria2"""
    _accept = 'application/json, text/plain, */*'
    _content_type = 'application/json;charset=UTF-8'
    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    data = {'id': str(time.time()), 'jsonrpc': '2.0', "method": "aria2.addUri",
            "params": [[url]]}
    response = requests.post(aria2_url, json.dumps(data))
    return response.ok


if __name__ == "__main__":
    hrefs = get_href(nginx_url)
    for href in hrefs:
        analyze_url(href)
