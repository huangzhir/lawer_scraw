
import common.requestUtil as requestUtil
import json



url = "http://wenshu.court.gov.cn/List/TreeContent"
dataParam = {"Param": ""}
content=requestUtil.getContent(url, dataParam)
rslist=eval(content)
print(len(rslist))
print(rslist)