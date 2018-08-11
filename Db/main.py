from Db.mongoutil import MongoUtil

if __name__ == '__main__':
    m = MongoUtil()
    c = m.get_collection()

    for i in c.find():
        pass
        # print(i.keys())

    # 在find中添加query进行查询
    query = {"city": "西安"}

    for i in c.find(query):
        print(i)
