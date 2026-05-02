import fitz
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['OPENAI_API_KEY'] = 'OPENAI_API_KEY'

document = fitz.open("/Users/username/Desktop/webcrawlDownloadTest/4.10 (보도참고) 의료기기관리과.pdf");

text = ""

for page_num in range(len(document)) :
    page = document.load_page(page_num)
    text += page.get_text()

combined_prompt = (
            PromptTemplate.from_template("아래 텍스트 내용을 요약해주세요.")
            + "\n\n{content}"
)

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# 3. LLM 호출
chain = combined_prompt | llm | StrOutputParser()
result = chain.invoke({"content":text})

print(result)