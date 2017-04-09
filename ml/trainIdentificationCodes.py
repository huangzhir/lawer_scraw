from PIL import Image
import os
import numpy as np
from sklearn import datasets, svm, metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.externals import joblib


#根据分隔后的图片取特征
def getImgFeature(imgPath):
    return getImgFeatureFromImg(Image.open(imgPath))

def getImgFeatureFromImg(img):
    nparray = np.array(img)
    nparray[nparray <= 128] = 0
    nparray[nparray > 128] = 1
    newny = nparray[8:24, 2:]
    newny = newny.reshape(1, -1)
    return newny

#取训练的X,Y
def getXY(imgPath="F:\\ml\\img\\"):
    imgList = []
    targetList = []
    for f in os.listdir(imgPath):
        for subf in os.listdir(imgPath + f):
            imgfile = imgPath + f + "\\" + subf
            newny = getImgFeature(imgfile)
            if (len(imgList) == 0):
                imgList = newny
            else:
                imgList = np.concatenate((imgList, newny))
            if (len(targetList) == 0):
                targetList = np.array([[int(f)]])
            else:
                targetList = np.concatenate((targetList, np.array([[int(f)]])))
    return imgList,targetList


#训练模型
def trainModel(X,Y):
    global adaboostClassModel
    # classifier = svm.SVC()
    classifier = DecisionTreeClassifier(criterion='entropy', max_depth=3)
    adaboostClassModel = AdaBoostClassifier(base_estimator=classifier, n_estimators=30, learning_rate=0.2)
    trainX, testX, trainY, testY = train_test_split(X, Y, test_size=0.2)
    # classifier.fit(dx,dy)
    # classifier.fit(trainX,trainY)
    # predictY=classifier.predict(testX)
    # print('DecisionTreeClassifier 正确率：',accuracy_score(predictY,testY))
    adaboostClassModel.fit(trainX, trainY)
    predictY = adaboostClassModel.predict(testX)
    print('AdaBoostClassifier 正确率：', accuracy_score(predictY, testY))
    return adaboostClassModel

if __name__ == "__main__":
    X,Y=getXY(imgPath="F:\\ml\\img\\")
    model=trainModel(X,Y)
    joblib.dump(adaboostClassModel,'classifier.m')


# joblib.dump(adaboostClassModel,'classifier.m')




