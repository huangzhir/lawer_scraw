from pymongo import MongoClient

class MongoSuport:
    __client = MongoClient("mongodb://localhost:27017")
    __db = __client.law
    __caseInfoCollection = __db.caseInfo

    def __init__(self,db,collection):
      self.__db=self.__client[db]
      self.__caseInfoCollection=self.__db[collection]

    def __init__(self):
        return

    def getCaseInfoCollection(self):
        return self.__caseInfoCollection

    def insertCaseInfo(self,obj):
        self.__caseInfoCollection.update({"_id":obj["_id"]},{"$setOnInsert":obj},upsert=True)

    def updateSubCaseInfoById(self,id,obj):
        self.__caseInfoCollection.update({"_id":id},{"$set":obj})

    def updateAllCaseInfoById(self,id,obj):
        self.__caseInfoCollection.update({"_id":id},obj)

    def findCaseInfo(self,id):
        return self.__caseInfoCollection.find({"_id":id})

    def close(self):
        self.__db.colse()



test={"_id":"9974be74-9db3-4fd0-9522-259ad03330298a2233333","案件名称":"被告人陈某应危险驾驶刑事判决书","文书ID":"9974be74-9db3-4fd0-9522-259ad00298a2"}
mongoSuport=MongoSuport()
#mongoSuport.insertCaseInfo(test)
uptest={"测试":True,"sd":23}
mongoSuport.updateSubCaseInfoById(test["_id"],uptest)
print(mongoSuport.findCaseInfo(test["_id"]))
