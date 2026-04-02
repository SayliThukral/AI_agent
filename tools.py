import requests
import os

def search_jobs(skills: str, experience: str) -> str:
    # 🔹 Create query from user input
    query = f"{skills} jobs with {experience} experience"

    # 🔹 API endpoint
    url = "https://jsearch.p.rapidapi.com/search"

    # 🔹 Headers (API key from .env)
    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    # 🔹 Query parameters
    params = {
        "query": query,
        "num_pages": "1"
    }

    try:
        # 🔹 API call
        response = requests.get(url, headers=headers, params=params)

        # 🔹 Check if request successful
        if response.status_code != 200:
            return "❌ Error fetching jobs from API"

        # 🔹 Convert response to JSON
        data = response.json()

        # 🔹 Extract job list
        jobs = data.get("data", [])

        # 🔹 If no jobs found
        if not jobs:
            return "❌ No jobs found"

        # 🔹 Format results
        result = []
        for job in jobs[:5]:  # top 5 jobs
            title = job.get("job_title", "N/A")
            company = job.get("employer_name", "N/A")
            location = job.get("job_city", "N/A")

            result.append(
                f"🔹 {title}\n🏢 {company}\n📍 {location}\n"
            )

        # 🔹 Return final output
        return "\n".join(result)

    except Exception as e:
        return f"❌ Something went wrong: {str(e)}"