# 猫眼电影数据爬虫

### **两行代码 爬取想要的影评**

##### 使用方法
1. Docker方式（推荐）

使用 打包好的Dockerfile构建

2. 传统部署
```python
    from crawel_utils.download import Maoyan

if __name__ == '__main__':
    # movie_id是电影对应的猫眼id，pegesize是选择下载评论的页数，thread_max仅用于多线程下载，为线程数
    maoyan = Maoyan(movie_id=1175253, page_size=40, thread_max=20)
    maoyan.multi_thread_download(func=maoyan.save_to_mongo)
```

通过实例化化Maoyan类，调用multi_thread_download即可爬取数据

