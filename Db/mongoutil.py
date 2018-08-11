import pymongo


class MongoUtil():
    def get_collection(self):
        connection = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 连接MongDB数据库
        db = connection.数据分析  #
        return db.爱情公寓  # 爱情公寓集合

    def get_doc(self):
        document = self.get_collection()
        return document


if __name__ == '__main__':
    person = {
        'id': '00001',
        'name': 'Abc',
        'age': 19
    }
