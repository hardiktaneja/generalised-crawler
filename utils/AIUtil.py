import random
import textwrap
import traceback

# Pydantic imports
from pydantic import BaseModel, Field

# Llama Index imports
from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage

# Type hints
from typing import Optional, Dict

# OpenAI imports
import openai

from utils.log import loggerClass

lg = loggerClass('generalised-crawler.log')

class EcommercePdtPattern(BaseModel):
    # Text Fields
    regex_pattern: str = Field(
        None, description="Pattern of Pdt URLs in this website"
    )
    
llm = OpenAI(model="gpt-4o-mini")
structured_llm = llm.as_structured_llm(output_cls=EcommercePdtPattern)

def getMatchingRegexPattern(all_urls):
    try:
        all_urls = random.sample(all_urls, 50)
        # all_urls = all_urls[:50]
        input_msg = ChatMessage.from_str(
        f"""
        I am using a python function in a web crawler to validate, which URLs are product URLs, A matching function will check if the URL contains a patternString which tells that this URL belongs to a product, and only a single product, not a cateogry, find me that regex patternString, I will do re.search(patternString,URL).Keep it simple, not complicated . Avoid including the main domain in th regex. Here are the URLs: {all_urls}
        """
        )

        output = structured_llm.chat([input_msg])
        output_obj = output.raw
        lg.logger.info(output_obj)
        return output_obj.regex_pattern
    except Exception as e:
        lg.logger.error(e)
        lg.logger.error(traceback.format_exc())
        return None    