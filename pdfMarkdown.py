# before
# import fitz

# document = fitz.open("/Users/choiyoolim/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf");

# text = ""

# for page_num in range(len(document)) :
#     page = document.load_page(page_num)
#     text += page.get_text()

# print(text)







# after
import pymupdf4llm
import pathlib

# 1. PDF 파일 경로 설정
pdf_path = "/Users/choiyoolim/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf"

# 2. 🚀 단 한 줄의 코드로 PDF 전체를 Markdown 문자열로 변환!
# 표(Table)는 마크다운 표 형식으로, 볼드체는 **텍스트** 로 완벽히 변환됩니다.
md_text = pymupdf4llm.to_markdown(pdf_path)

# 3. 추출된 마크다운을 파일로 저장 (이제 이 파일을 LangChain 등에 던지면 끝!)
# pathlib.Path("output.md").write_bytes(md_text.encode("utf-8"))

# print("✅ PDF의 완벽한 AI용 마크다운 변환이 완료되었습니다.")
# print(md_text)