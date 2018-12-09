from pymongo import MongoClient
from bson import ObjectId


def getConnection():
    # connection-t krealunk:
    client=MongoClient("localhost", 27017)

    #adatbazist keszitunk
    db=client["MovieLibrary"]

    #kollekciot keszitunk
    connect=db["movies"]

    #minend sorban letrejon egy osztaly
    return connect

def insertData(dictData):
    con=getConnection()
    return con.insert(dictData)

def getData(collection,id=False,name=False,type=False):
    con=getConnection()
    result=con.find_one({"_id":id})

def getAllData():
    con=getConnection()
    result=con.find({})

    return [i for i in result]


def editData(data):
    con=getConnection()
    item = con.find_one({"_id": data["_id"]})
    item=data
    con.save(item)

def removeData(id):
    con=getConnection()
    con.delete_one({"_id": ObjectId(id)})


if __name__=="__main__": #e nelkul nem fut le az app
    data=getData("employees",id="5c0d149ce2955622769f139f")
    data["Phone"]="111 111"

    editData("employees","5c0d149ce2955622769f139f",data)