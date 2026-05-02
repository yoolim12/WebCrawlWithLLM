import os
from urllib import request
from urllib.error import HTTPError
import requests

def get_download(url, fname, directory):
    try:
        os.chdir(directory)
        # request.urlretrieve(url, fname)

        response = requests.get(url, verify=False)  # 🔥 핵심
        with open(fname, "wb") as f:
            f.write(response.content)
        
        print('다운로드 완료\n')
    except HTTPError as e:
        print('error')
        return

def main() :
    get_download(url = "https://www.mfds.go.kr/brd/m_99/down.do?brd_id=ntc0021&seq=49854&data_tp=A&file_seq=1", fname= "4.10 (보도참고) 의료기기관리과.hwpx", directory="/Users/choiyoolim/Desktop/webcrawlDownloadTest")
    # get_download(url = "https://www.mfds.go.kr/brd/m_99/down.do?brd_id=ntc0021&seq=49854&data_tp=A&file_seq=2", fname= "4.10 (보도참고) 의료기기관리과.pdf", directory="/Users/choiyoolim/Desktop/webcrawlDownloadTest")
    # get_download(url = "https://www.mfds.go.kr/brd/m_487/down.do?brd_id=cmnt0013&seq=714&data_tp=A&file_seq=1", fname= "유리미.pdf", directory="/Users/choiyoolim/Desktop/webcrawlDownloadTest")

main()