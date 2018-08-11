import pymongo


def get_collection(db_name, set_name):
    connection = pymongo.MongoClient(host='127.0.0.1', port=27017)  # 连接MongDB数据库
    db = connection[db_name]
    return db[set_name]  # 返回集合


def get_one_doc(set):
    document = set.find_one()
    return document


def get_list_doc(set):
    # document = set.find()
    # print(type(document))
    # 返回list
    document = [doc for doc in set.find()]
    return document


if __name__ == '__main__':
    set = get_collection('数据分析', '爱情公寓')

    doc = get_one_doc(set)
    doc_list = get_list_doc(set)

    for dic in doc_list:
        pass
        if 'city' in dic:
            print(dic['city'])
