from langchain.tools import tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import search_jobs
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    max_tokens=1000,
    
)

# 🧰 Tool with split logic
def job_wrapper(q):
    try:
        skills, experience = q.split(",")
        return search_jobs(skills.strip(), experience.strip())
    except:
        return "❌ Please enter input in this format: skills, experience"

@tool
def job_tool(q: str) -> str:
    """ Use this tool to find jobs.Input should be: skills, experience """
    return job_wrapper(q)

# 🤖 LLM
#model = ChatOpenAI(temperature=0)

# 🚀 Agent
agent = create_agent(model, tools=[job_tool])

# 🎯 Run
if __name__ == "__main__":
    skills = input("Enter your skills: ")
    experience = input("Enter your experience: ")

    # combine both inputs
    query = f"{{\"skills\": \"{skills}\", \"experience\": \"{experience}\"}}"

    response = agent.invoke({"input": query})

    print("\n🔥 Recommended Jobs:\n")
    print(response)