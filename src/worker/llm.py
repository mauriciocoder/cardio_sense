import os

from . import logger
from static.cardio_report_llm_summary_template import llm_summary_template
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

from src.model.exams import CardioExam


class LLM:
    def __init__(self):
        self.model = ChatGroq(
            temperature=os.environ.get("GROQ_TEMPERATURE", 0),
            groq_api_key=os.environ.get("GROQ_API_KEY", "key"),
            model_name=os.environ.get("GROQ_MODEL_NAME", "name"),
        )

    def create_cardio_report_summary(self, exam: CardioExam) -> str:
        prompt_extract = PromptTemplate.from_template(llm_summary_template)
        chain_extract = prompt_extract | self.model
        res = chain_extract.invoke(input={"exam": str(exam)})
        logger.info(f"Cardio report summary from LLM: {res.content}")
        return res.content
