from PIL import Image
import os
import urllib
import json
import ml.verificationcode as mlcode
import numpy as np


path="F:\\ml\\code\\"
imgPath="F:\\ml\\img\\"
for f in os.listdir(imgPath):
    for subf in os.listdir(imgPath+f):
        os.remove(imgPath+f+"\\"+subf)

def creatImg():
    for f in os.listdir(path):
        im = Image.open(path+f)
        gray = im.convert("L")
        #分隔图片的数字
        for i in range(4, 56, 13):
            j = int((i - 4) / 13)
            region = (i, 0, i + 13, 30)
            cropImg = gray.crop(region)
            strJ=imgPath + f[j]+"\\"
            imgName=str(len(os.listdir(strJ))+1)+".jpg"
            cropImg.save(strJ+imgName)
            # nparray = np.array(cropImg)
            # print(nparray)
        #cropImg.show()

# creatImg()
#gray.show()

def addCommonHeader(req):

    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "gzip,deflate")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-Requested-With", "XMLHttpRequest")



#取得验证码并提交
def getCodeAndSubmit():
    submit_code_url="http://wenshu.court.gov.cn/Content/CheckVisitCode"
    code=mlcode.getCodeStr(m="../ml/classifier.m")
    print("取得验证码：",code)
    dataParam={"ValidateCode":code}
    # data = json.dumps(dataParam).encode("utf8")
    data = urllib.parse.urlencode(dataParam)
    data = data.encode('utf-8')
    req = urllib.request.Request(submit_code_url,data=data)
    # addCommonHeader(req)
    print("提交验证码：",dataParam)
    with urllib.request.urlopen(req) as f:
         return f.read().decode("utf-8")

def getContent(url,dataParam):
    data = urllib.parse.urlencode(dataParam)
    data = data.encode('utf-8')
    req = urllib.request.Request(url,data=data)
    addCommonHeader(req)
    with urllib.request.urlopen(req) as f:
         return f.read().decode('utf-8')

if __name__=="__main__":
    # rs=getCodeAndSubmit()
    # 1 成功 2 失败
    # print('结果',int(rs))
    # dataParam = {"Param": "法院地域: 福建省"}
    dataParam = {"Param": ""}
    url="http://wenshu.court.gov.cn/List/TreeContent"
    print(getContent(url,dataParam))








