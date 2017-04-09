from urllib.parse import urlencode
import urllib
import urllib.request
import urllib.parse

def addCommonHeader(req):
    req.add_header("Accept", "*/*")
    req.add_header("Accept-Encoding", "gzip,deflate")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    req.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    req.add_header("X-Requested-With", "XMLHttpRequest")

def getContent(url,dataParam):
    data = urllib.parse.urlencode(dataParam)
    data = data.encode('utf-8')
    req = urllib.request.Request(url,data=data)
    addCommonHeader(req)
    with urllib.request.urlopen(req) as f:
         return f.read().decode('utf-8')