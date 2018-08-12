# 猫眼电影数据爬虫

### __两行代码 爬取想要的影评__

* 环境配置
1. Docker方式（推荐）

使用 打包好的Dockerfile构建(暂未提供)

2. 传统部署(默认已安装python环境)
***
    步骤：
    1. pip install requirement.txt 安装工程所需模块
    2. sudo apt install mongodb 安装mongodb(使用txt保存数据可跳过)
   
   
---
* 使用方法 
```python 
    # 引入Maoyan类
    from crawel_utils.download import Maoyan

if __name__ == '__main__':
    # movie_id是电影对应的猫眼id，pegesize是选择下载评论的页数，thread_max仅用于多线程下载，为线程数
    maoyan = Maoyan(movie_id=1175253, page_size=40, thread_max=20)
    # 保存到mongodb
    maoyan.multi_thread_download(func=maoyan.save_to_mongo)
    # 保存到txt文本
    maoyan.multi_thread_download(func=maoyan.save_to_txt)

```
