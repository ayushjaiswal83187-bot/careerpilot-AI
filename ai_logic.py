from openai import OpenAI
import json


client = OpenAI(api_key="YOUR_API_KEY_HERE")

def analyze_resume(resume_text, user_goal):
    """Resume ko analyze karke JSON format mein result deta hai."""
    prompt = f"""
    You are a senior software engineer and hiring manager.
    Evaluate the resume for the goal: "{user_goal}"

    STRICT RULES:
    - Extract only relevant skills for this goal
    - Identify real gaps
    - Generate roadmap only for missing fields
    Return ONLY valid JSON:
    {{
    "Skills":[],
    "Missing_Skills":[],
    "Roadmap":[],
    "Interview_Questions":[]
    }}
    Resume: {resume_text}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You output only JSON."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content.strip()

        # JSON ko clean karne ke liye logic
        start = content.find("{")
        end = content.rfind("}") + 1
        return json.loads(content[start:end])
    except Exception as e:
        return {"error": str(e)}

def get_ai_answer(user_query):
    """Chatbot feature: User ke sawalon ka jawab dene ke liye."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful career assistant and chatbot."},
                {"role": "user", "content": user_query}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"