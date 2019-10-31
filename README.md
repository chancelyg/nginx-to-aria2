# nginx-to-aria2
将Nginx文件服务器链接转换为Aria2的任务列表，支持指定格式/记录过滤已下载任务

# 运行环境
Python版本
- Python 3.x以上

依赖包
- urllib
- bs4
- requests
- json


# 用法
1. 安装3.x以上版本Python，并执行下面命令安装指定包

    ```shell
    pip install urllib bs4 requests json
    ```

2. 修改**__init__.py**文件开头3个变量
- nginx_url
    - nginx 文件服务器的url
- aria2_url
    - aria2 jsonrpc的url
- restrict_download_format
    - 限制指定下载的文件格式，如需要指定下载文件的格式，修改enable为True，在format中添加指定的格式即可（白名单制）

3. 运行程序

    ```shell
    python __init__.py
    ```

可重复运行，已下载的任务会记录到当前运行目录下的 **download_record.txt**文件中

每次下载前都会将链接与本地的下载记录文件中的记录对比，如下载链接一致则不再重复下载，所以可以设置为定时任务，这样可以定时同步Nginx服务器文件到本地



