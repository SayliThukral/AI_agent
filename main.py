from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from tools import wiki_tool

load_dotenv()



class JobRecommendation(BaseModel):
    job_title: str = Field(description="Recommended job Title")
    description: str = Field(description="Why this job fits the candidate")


class JobRecommendationsOutput(BaseModel):
    recommendations: list[JobRecommendation]



llm = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini"   
)



parser = PydanticOutputParser(
    pydantic_object=JobRecommendationsOutput
)



prompt = ChatPromptTemplate.from_messages([
    ("system",
     """You are an intelligent Job Recommendation Agent.

Based on user skills and experience, suggest suitable jobs.

IMPORTANT:
- Output MUST be in JSON
- Do NOT write anything else

{format_instructions}
"""),

    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])



tools = [wiki_tool]



agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)



print("Enter your details:")
skills = input("Enter Skills: ")
exp = input("Enter Experience: ")

query = f"Skills: {skills}, Experience: {exp}"



try:
    raw_response = agent_executor.invoke({
        "input": query,
        "format_instructions": parser.get_format_instructions()
    })

    output_text = raw_response.get("output", "")

    structured_response = parser.parse(output_text)

    print("\n✅ Structured Output:")
    print(structured_response.model_dump_json(indent=2))

except Exception as e:
    print("❌ Error parsing response:", e)
    print("Raw Response:", raw_response)