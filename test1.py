from inspect import getfile
import os
import re
from urllib import request
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests

overlap = []
# url = "https://ors.gir.go.kr/home/orah010/usedOpenList.do?menuId=10&condition.bizNm=&condition.qtaOjEnpNm=&condition.usedOpenYn=&pagerOffset="
url = "https://www.mfds.go.kr/brd/m_99/view.do?seq=49854"
site = "https://ors.gir.go.kr"
rec = "/home/orah010/usedOpenRead.do;"
dl = "/home/file/readOrDownload.do?"

def get_download(url, fname, directory):
    try:
        os.chdir(directory)
        request.urlretrieve(url, fname)
        print('다운로드 완료\n')
    except HTTPError as e:
        print('error')
        return

def downSearch(getDLATag, filename):
   for getDLLink in getDLATag:
       try:
           if dl in getDLLink.get('href'):
               accessDLUrl = site + getDLLink.get('href')
               print("다운로드 링크: ", accessDLUrl)
               path = "/Users/choiyoolim/Desktop/webcrawlDownloadTest"
               if os.path.isfile(path + filename):
                   print("다운로드 실패 : 동일 파일 존재\n")
               else:
                   get_download(accessDLUrl, filename, path)
       except:
           pass

def Search(getA, num):
    for getLink in getA:
        data = getLink.get('href')
        try:
            if rec in getLink.get("href"):
                if data not in overlap:
                    overlap.append(data)
                    accessUrl = site + getLink.get("href")
                    r = requests.get(accessUrl)
                    soup = BeautifulSoup(r.text, "html.parser")
                    getDLATag = soup.find_all("a")
                    getfilenameTag = soup.find_all("td")
                    td = getfilenameTag[len(getfilenameTag)-1]
                    filename = str(num) + ". " + str(td)[4:int(str(td).find(".pdf"))+4].strip()
                    #print(filename)
                    num = num - 1
                    downSearch(getDLATag, filename)
        except:
            pass

def main():
    pageoffset = 0
    num = 627
    while pageoffset <= 620:
        # request 모듈을 사용하여 웹 페이지의 내용을 가져온다
        r = requests.get(url+str(pageoffset))

        # beautiful soup 초기화
        soup = BeautifulSoup(r.text, "html.parser")

        # 태그로 찾기 (모든 항목)
        getA = soup.find_all("a")
        Search(getA, num)

        pageoffset += 10
        num -= 10

main()