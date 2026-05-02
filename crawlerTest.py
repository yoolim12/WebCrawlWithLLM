from bs4 import BeautifulSoup
from requests import get
import os
from urllib import request
from urllib.error import HTTPError
from urllib.parse import urljoin

response = get("https://www.mfds.go.kr/brd/m_487/view.do?seq=698")
html = response.text
soup = BeautifulSoup(html, 'html.parser')
downloadTitle = soup.find("div", class_="bbs_file_cont").find("strong").text

print(downloadTitle)