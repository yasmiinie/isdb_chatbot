import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

import os
from dotenv import load_dotenv

load_dotenv()  

api_key = os.getenv("OPENAI_API_KEY")

def load_examples(json_path="islamic_finance_training_data_json.json", max_examples=10):
    with open(json_path, "r") as f:
        data = json.load(f)

    few_shot = ""
    for ex in data[:max_examples]:  # Load first N examples
        few_shot += f"""
### Scenario:
{ex["description"]}

FAS: {ex["standard_reference"]}
Confidence: 1.0
Justification: Based on a Musharaka financing scenario with profit-sharing, FAS 4 applies.
"""
    return few_shot


def build_chain():
    valid_fas_list = ["FAS 4", "FAS 7", "FAS 10", "FAS 28", "FAS 32"]
    examples_text = load_examples()

    template = f"""
You are an expert in Islamic Financial Accounting.

Your task is to select the most appropriate AAOIFI Financial Accounting Standard (FAS)
from the following valid list only: {', '.join(valid_fas_list)}.

Below are some example scenarios and their correct FAS:

{examples_text}

Now, given the new financial scenario, identify:
1. The most applicable FAS (from the list above)
2. Confidence score (0-1)
3. Justification for your selection

### Scenario:
{{scenario}}

Respond in the format:
FAS: <Standard from list>
Confidence: <Score between 0 and 1>
Justification: <Your reasoning>
"""

    prompt = PromptTemplate(
        input_variables=["scenario"],
        template=template
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key= api_key, )

    return LLMChain(llm=llm, prompt=prompt)
