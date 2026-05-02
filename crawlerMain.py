from bs4 import BeautifulSoup
from openai import BadRequestError
from requests import get
import os
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urljoin
import requests
import certifi
import urllib3
import pymupdf4llm
import fitz
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
import time
import random
from langchain_core.output_parsers import JsonOutputParser

def split_text(text, chunk_size=2000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def get_ai_short(fileUrl):
   os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'
#    md_text = pymupdf4llm.to_markdown(fileUrl)
#    chunks = split_text(md_text, 2000)
   
   document = fitz.open(fileUrl);
   
   text = ""
   
   for page_num in range(len(document)):
      page = document.load_page(page_num)
      text += page.get_text()
   
   combined_prompt = (
      PromptTemplate.from_template("아래 글의 본문 내용을 요약해주세요.")
      + "\n\n{content}"
    )
   
   # 3. LLM 호출
   llm = OpenAI(temperature=0)
   chain = combined_prompt | llm | StrOutputParser()

   while len(text) > 2000:
      results = []
      chunks = split_text(text, 2000)

      for chunk in chunks:
         result = chain.invoke({"content":chunk})
         results.append(result)

      text = "\n".join(results)
    
    # 마지막에 전체 요약
   final_prompt = "다음 요약들을 하나로 정리해줘:\n\n" + text
   final_result = ""
   
   try:
      final_result = llm.invoke(final_prompt)
   except BadRequestError as e:
      if "maximum context length" in str(e):
         print(f"요청 토큰 길이 초과 : {e.message}")

   return final_result

def get_download(url, fname):
    try:
        os.chdir("/Users/choiyoolim/Desktop/webcrawlDownloadTest")
        # request.urlretrieve(url, fname)

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        

        response = requests.get(url, headers=headers, verify=False)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        with open(fname, "wb") as f:
            f.write(response.content)

        print('다운로드 완료\n')
    except HTTPError as e:
        print('error')
        return

def extract_files(keyword):
  base_url = "https://www.mfds.go.kr"
  main_url = f"https://www.mfds.go.kr/search/search.do?collection=nation&query={keyword}"
  headers = {
     "User-Agent": "Mozilla/5.0"
  }
  response = get(main_url, headers=headers, timeout=10)
  time.sleep(random.uniform(5, 10))
  linkList = []

  if response.status_code == 200 :
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    ulList = soup.find("ul", class_ = "sr_result_list")
    liList = ulList.find_all('li', recursive=False)

    

    for li in liList:
      
      link = li.find("a", class_ = None)["href"]
      
      if not link.startswith(base_url) :
        link = urljoin(base_url, link)
        page_response = get(link, headers=headers, timeout=10)
        time.sleep(random.uniform(5, 10))

        if page_response.status_code == 200 :
          
          page_html = page_response.text
          page_soup = BeautifulSoup(page_html, 'html.parser')
          downloadLink = ""
          downloadTitle = ""

          if page_soup.find("a", class_="bbs_icon_filedown"):
            find_all_links = page_soup.find_all("a", class_="bbs_icon_filedown")
            downloadLink = page_soup.find("a", class_="bbs_icon_filedown")["href"]
            if page_soup.find("div", class_="bbs_file_cont"):
               if page_soup.find("div", class_="bbs_file_cont").find("strong"):
                  downloadTitle = page_soup.find("div", class_="bbs_file_cont").find("strong").text
        
          
          
          if downloadLink != "":
             if not downloadLink.startswith(link):
                downloadLink = urljoin(link, downloadLink)
        
          pageInfo = {
             "title" : downloadTitle,
             "downUrl" : downloadLink
          }

          linkList.append(pageInfo)
            
        else :
          return page_response.status_code
  else :
    return response.status_code
  return linkList

# print(extract_files("점검"))

def main():
#    downloadList = extract_files("점검")
#    for download in downloadList:
#     #   print(download)
#     title = download['title']
#     link = download['downUrl']

#     # print(f"title={title} / link={link}")
#     if title and link:
#         get_download(url=link, fname=title)
    
#     print(get_ai_short("/Users/choiyoolim/Desktop/webcrawlDownloadTest/" + downloadList[0]['title']))
    print(get_ai_short('/Users/choiyoolim/Desktop/webcrawlDownloadTest/★2026년 정부포상 후보자 공개검증 (제25회 식품안전의 날).pdf'))

main()