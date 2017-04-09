from PIL import Image
from sklearn.externals import joblib
import numpy as np
import ml.trainIdentificationCodes as trainModel
import urllib
from sklearn.metrics import accuracy_score

def getDigistImgs(f):
    im = Image.open(f)
    gray = im.convert("L")
    digistImgList=[]
    #分隔图片的数字
    for i in range(4, 56, 13):
        region = (i, 0, i + 13, 30)
        digistImgList.append(gray.crop(region))
    return digistImgList

def getFeatureFromCodeImg(imgpath):
    featurelist=[]
    digistList = getDigistImgs(imgpath)
    for digistImg in digistList:
        feature=trainModel.getImgFeatureFromImg(digistImg)
        featurelist.append(feature[0])
    return np.array(featurelist)


def getCodeStr(m='classifier.m'):
    model = joblib.load(m)
    codeurl = "http://wenshu.court.gov.cn/User/ValidateCode"
    req = urllib.request.Request(codeurl)
    with urllib.request.urlopen(req) as f:
        digistFeature = getFeatureFromCodeImg(f)
        # print(digistFeature)
        predictY=model.predict(digistFeature)
        return "".join(map(lambda i: str(i), predictY))
        # return predictY.tolist()


if __name__=="__main__":
    # X,Y=trainModel.getXY()
    # model=joblib.load('classifier.m')
    # predictY=model.predict(X)
    # print("正确率:",accuracy_score(Y,predictY))

    # imgpath = 'F:\\ml\\code\\1804.jpg'
    print(getCodeStr())






