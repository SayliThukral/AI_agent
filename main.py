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

@tool
def job_tool(input_text: str) -> str:
    """
    Use this tool to find jobs.
    Input format: skills and experience clearly mentioned.
    Example: "Skills: python, machine learning. Experience: 2 years"
    """
    
    try:
        # Simple extraction (safe parsing)
        parts = input_text.lower().split("experience:")
        
        skills_part = parts[0].replace("skills:", "").strip()
        experience_part = parts[1].strip()

        return search_jobs(skills_part, experience_part)

    except:
        return "❌ Please enter input like: Skills: python, ML. Experience: 2 years"



# 🚀 Agent
agent = create_agent(model, tools=[job_tool])

# 🎯 Run
if __name__ == "__main__":
    skills = input("Enter your skills: ")
    experience = input("Enter your experience: ")

    # combine both inputs
    query = f"skills: {skills}, experience: {experience}"
    response = agent.invoke({"messages": [("user", query)]})
    

    print("\n🔥 Recommended Jobs:\n")
    print(response["messages"][-1].content)