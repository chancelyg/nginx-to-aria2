# 1. nginx-to-aria2
将Nginx文件服务器的链接转换为Aria2的任务列表，支持过滤已下载任务、过滤指定文件类型

> PS:可以用来把VPS上的电影定时Download到本地

运行环境
- Python 3以上
- urllib bs4 requests json等PIP安装包


程序会自动记录下载URL到本地文件，已下载的任务会记录到当前运行目录下的 **download_record.txt**文件中

因为每次下载前都会将链接与本地的下载记录文件中的记录对比，如下载链接一致则不再重复下载，所以可以设置为定时任务，这样可以定时同步Nginx服务器文件到本地



# 3. 如何使用
1. 安装3.x以上版本Python，并执行下面命令安装指定包

    ```shell
    pip install urllib bs4 requests json
    ```

2. 修改**config.json**文件

    | 变量             | 说明                            |
    | ---------------- | ------------------------------- |
    | nginx_url        | Nginx服务器页面地址             |
    | aria2_rpc_url    | aria2 API地址（通常是6800端口） |
    | download_path    | 文件下载根目录                  |
    | ignore_file_type | 忽略文件类型                    |

1. 运行程序

    ```shell
    python main.py
    ```



