# from pymongo.mongo_client import MongoClient
# MONGODB_URI="mongodb+srv://sushantkunjir34_db_user:Sushant8134@cluster0.qwfsqat.mongodb.net"
# client=MongoClient(MONGODB_URI)

# try:
#     client.admin.command('ping')
#     print('pinged your deployment, you are successfully connect with mongodb')
# except Exception as e:
#     print(e)


from pymongo import MongoClient
import certifi

uri ="mongodb+srv://sushantkunjir34_db_user:Sushant8134@cluster0.qwfsqat.mongodb.net"

client = MongoClient(
    uri,
    tlsCAFile=certifi.where()
)

print(client.admin.command("ping"))