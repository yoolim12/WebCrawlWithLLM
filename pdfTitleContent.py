import pymupdf4llm
import pathlib
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import fitz

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'


# 1. PDF 파일 경로 설정
pdf_path = "/Users/choiyoolim/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf"

# 2. 🚀 단 한 줄의 코드로 PDF 전체를 Markdown 문자열로 변환!
# 표(Table)는 마크다운 표 형식으로, 볼드체는 **텍스트** 로 완벽히 변환됩니다.
# md_text = pymupdf4llm.to_markdown(pdf_path)

# combined_prompt = (
#             PromptTemplate.from_template("아래 글을 읽고, 주요 수거 품목에는 어떤 것들이 있는지 알려주세요.")
#             + "\n\n{content}"
# )

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# # 3. LLM 호출
# chain = combined_prompt | llm | StrOutputParser()
# result = chain.invoke({"content":md_text})

document = fitz.open("/Users/choiyoolim/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf");

text = ""

for page_num in range(len(document)) :
    page = document.load_page(page_num)
    text += page.get_text()

combined_prompt = (
            PromptTemplate.from_template("아래 글을 읽고, 주요 수거 품목에는 어떤 것들이 있는지 알려주세요.")
            + "\n\n{content}"
)

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
llm = OpenAI(temperature=0)

chain = combined_prompt | llm | StrOutputParser()
result = chain.invoke({"content":text})

print(result)