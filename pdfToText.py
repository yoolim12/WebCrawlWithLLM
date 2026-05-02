import fitz
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

document = fitz.open("/Users/choiyoolim/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf");

text = ""

for page_num in range(len(document)) :
    page = document.load_page(page_num)
    text += page.get_text()

combined_prompt = (
            PromptTemplate.from_template("아래 텍스트 내용을 요약해주세요.")
            + "\n\n{content}"
)

# llm = OpenAI()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# 3. LLM 호출
chain = combined_prompt | llm | StrOutputParser()
result = chain.invoke({"content":text})


# # 1. 점검 키워드 있는 줄만 추출
# filtered_lines = [
#     line for line in text.split("\n")
#     if "점검" in line
# ]

# filtered_text = "\n".join(filtered_lines)

# result = ""

# # 2. 없으면 바로 NULL
# if not filtered_text.strip():
#     result = "NULL"

# else:
#     llm = OpenAI(temperature=0)

#     # combined_prompt = (
#     #               PromptTemplate.from_template("아래 텍스트는 pdf 파일에서 추출한 내용입니다. pdf 파일에서 추출한 내용을 읽고, 점검일자가 언제인지 말해주세요.")
#     #               + PromptTemplate.from_template("점검일자에 대한 언급이 없다면 NULL이라 말해주세요.")
#     #               + "\n\n{content}"
#     # )

#     combined_prompt = PromptTemplate.from_template("""
#     다음 조건을 반드시 지켜서 "텍스트" 하위 내용에서 "점검일자"를 추출해주세요:
#     1. "점검일자", "점검 일자", "점검일" 등 '점검'과 관련된 날짜만 찾으세요.
#     2. 단순 배포일, 작성일, 보도일 등은 절대 포함하지 마세요.
#     3. 점검과 관련된 키워드가 없는 경우에는 NULL을 출력하세요.
#     4. 반드시 텍스트에 실제로 존재하는 값만 답하세요. 추측하지 마세요.

#     출력 형식:
#     - 날짜가 있으면: YYYY-MM-DD
#     - 없으면: NULL

#     텍스트:
#     {content}
#     """)

#     # 3. LLM 호출
#     chain = combined_prompt | llm | StrOutputParser()
#     result = chain.invoke({"content":filtered_text})

print(result)