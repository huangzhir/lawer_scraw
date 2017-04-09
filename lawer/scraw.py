from urllib.parse import urlencode
import urllib
import urllib.request
import urllib.parse
import json
import configparser
import os
import lawer.mongoSuport
import time


# urllib.request 用于打开和读取URL,
# urllib.error 用于处理前面request引起的异常,
# urllib.parse 用于解析URL,
# urllib.robotparser用于解析robots.txt文件



def addHeader(req):
    req.add_header("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
    req.add_header("Accept-Encoding", "gzip, deflate")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    req.add_header("Accept", "*/*")
    req.add_header("Origin", "http://wenshu.court.gov.cn")
    req.add_header("Referer", "http://wenshu.court.gov.cn/List/List?sorttype=1")
    req.add_header("X-Requested-With", "XMLHttpRequest")

def addMobileHeader(req):
    req.add_header("User-Agent", "Dalvik/2.1.0 (Linux; U; Android 6.0; M685U Build/MRA58K)")
    req.add_header("Content-Type", "application/json")
    req.add_header("Host", "wenshuapp.court.gov.cn")
    req.add_header("Connection", "Keep-Alive")
    req.add_header("Accept-Encoding", "gzip")



def getContenListJson(param):
    url = "http://wenshu.court.gov.cn/List/ListContent";
    data=urllib.parse.urlencode(param);
    data=data.encode("utf-8")
    req = urllib.request.Request(url,data=data)
    addHeader(req)
    with urllib.request.urlopen(req) as f:
         return f.read().decode('utf-8')

def getFujianCriminalCaseListJsonOrderByDate(index,page):
    param = {
        'Param': '案件类型:刑事案件,法院地域:福建省',
        'Index': index,
        'Page': page,
        'Order': '裁判日期',
        'Direction': 'asc'
    }
    return getContenListJson(param)

case_dict={"CaseDocId":"文书ID","CaseName":"案件名称","CaseCourt":"法院名称","CaseNation":"法院国家","CaseDate":"裁判日期",
           "CaseProvince":"法院省份","CaseCity":"法院地市","CaseCounty":"法院区县","CaseArea":"法院区域","CaseType":"案件类型","CaseTrialLevel":"审判程序","CaseFileType":"文书类型",
           "CaseNumber": "案号","CaseReason":"案由","CasePerson":"姓名或名称","CaseTrialPerson":"审判人员","CaseClerk":"书记员","CaseYear":"裁判年份","裁判月份":"CaseMonth","CaseDay":"裁判日份",
           "CaseUploadCourt": "上传法院","CaseUploadDept":"上传部门","CaseUploadPerson":"上传人员","CaseUploadDay":"上传日份","CaseUploadYear":"上传年份","CaseUploadCaseDocId":"上传包ID",
           "CaseFileMend":"补正文书","CaseCourtLevel1":"一级法院","CaseCourtLevel2": "二级法院","CaseCourtLevel3":"三级法院","CaseCourtLevel4":"四级法院"}

def getSummary(caseId):
    getSummaryPreUrl="http://wenshu.court.gov.cn/Content/GetSummary?"
    param={"docId":caseId}
    data = urllib.parse.urlencode(param);
    data = data.encode("utf-8")
    req = urllib.request.Request(getSummaryPreUrl,data=data)
    addHeader(req)
    with urllib.request.urlopen(req) as f:
         return f.read().decode('utf-8')

def getContent(caseId):
    mobileGetContentUrl="http://wenshuapp.court.gov.cn/MobileServices/GetAllFileInfoByIDNew"
    dataParam={"fileId":caseId}
    data = json.dumps(dataParam).encode("utf8")
    req = urllib.request.Request(mobileGetContentUrl,data=data)
    addMobileHeader(req)
    with urllib.request.urlopen(req) as f:
         return f.read().decode('utf-8')


def srawList():
    confPath = "list.ini"
    cf = configparser.ConfigParser()
    cf.read(confPath)
    if not os.path.exists(confPath) or not cf.has_section("list"):
        cf.add_section("list")
        cf.set("list", "page", "20")
        cf.set("list", "index", "1")
        cf.set("list", "count", "99999999")
        f = open(confPath, "w")
        cf.write(f)
        f.close()
    cf.read(confPath)
    page = int(cf.get("list", "page"))
    index = int(cf.get("list", "index"))
    count = int(cf.get("list", "count"))
    start = page * (index - 1)
    mongoSuport = lawer.mongoSuport.MongoSuport()
    while page * index < count:
        print(start)
        josnStr = getFujianCriminalCaseListJsonOrderByDate(index, page)
        index += 1
        print(josnStr)
        contentList = json.loads(josnStr)
        if contentList == "remind":
            print("遇到验证码")
            exit(-1)
        contentList = json.loads(contentList)
        if len(contentList)==0:
            print("已无法获取到内容")
            return 0
        count = int(contentList[0]["Count"])
        for content in contentList[1:]:
            start += 1
            content["indextCount"] = start
            content["flag"] = 0
            content["_id"] = content["文书ID"]
            mongoSuport.insertCaseInfo(content)
        cf.set("list", "page", str(page))
        cf.set("list", "index", str(index))
        cf.set("list", "count", str(count))
        confFile = open(confPath, "w")
        cf.write(confFile)
        confFile.close()

        time.sleep(1)


srawList()
#fileId="9aed51ab-f8b3-4f20-bf6e-06d8960c53d0"
#str=getFujianCriminalCaseListJsonOrderByDate(100,20)
#str=getSummary(fileId)
#str=getContent(fileId)
#print(str)



