from pymongo import MongoClient
from bson import ObjectId

def getConnection():
    client = MongoClient("localhost", 27017)
    db = client["MovieLibrary"]
    connect = db["movies"]

    return connect

def insertData(data):
    con = getConnection()
    return con.insert(data)

def getData(filePath):
    con = getConnection()
    result = con.find_one({"path":filePath})

    return result

def getAllData(collection):
    con = getConnection()
    result = con.find({})

    return [i for i in result]

def editData(data):
    con = getConnection()

    item = con.find_one({"_id":"_id"})
    item = data

    con.save(item)

def deleteData(id):
    con = getConnection()
    con.delete_one({"_id": id})

if __name__ == "__main__":
    data = getData(r"E:\movies_test\Alien.mkv")
    print data