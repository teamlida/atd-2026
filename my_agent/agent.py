import requests
from google.adk.agents.llm_agent import Agent

MOCK_API_BASE_URL = "https://fake-json-api.mock.beeceptor.com/users"  # point this at your mock API


def get_user_data(user_id: str) -> dict:
    try:
        response = requests.get(f"{MOCK_API_BASE_URL}/{user_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}


root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Answer user questions to the best of your knowledge. Use the get_user_data tool to retrieve user data.',
    tools=[get_user_data],
)
