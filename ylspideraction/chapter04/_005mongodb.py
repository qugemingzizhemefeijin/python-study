# mongoDB使用案例
import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017, username="root", password="123456", authSource="test", authMechanism='SCRAM-SHA-1')
# 获取数据库
db = client['test']
# 获取集合
# collection = db['aaa']
# 或
# collection = db.aaa

for i in db.aaa.find({'by': '菜鸟教程'}):
    print("data = %s" %(i))

# 插入数据库
json = {
    'title': 'Python教程',
    'description': 'Python是一门脚本语言',
    'by': '小橙子',
    'url': 'http://www.baidu.com',
    'tags': ['python', 'script'],
    'likes': 101
}
res = db['aaa'].insert_one(json)
print(res, res.inserted_id)

# 查询一条符合条件的数据    
data = db['aaa'].find_one({'by': '小橙子'})
print("data = %s" %(data))

# 修改数据
res = db.aaa.update_one({'by': '小橙子'}, {'$set': {'title': 'Python基础教程'}})
# modified_count，返回更新的条数
print(res, res.modified_count)

# 更新数据
#res = db.chat.update_many({"age": {"$gte": 0}}, {"$set": {"age": 888}})
# print(res, res.modified_count)

# 查询一条符合条件的数据    
data = db['aaa'].find_one({'by': '小橙子'})
print("data = %s" %(data))
    
# 关闭数据库
client.close()
