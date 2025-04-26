import requests
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("MYFXBOOK_EMAIL")
PASSWORD = os.getenv("MYFXBOOK_PASSWORD")
BASE_URL = "https://www.myfxbook.com/api"

def login_myfxbook():
    response = requests.get(f"{BASE_URL}/login.json?email={EMAIL}&password={PASSWORD}")
    return response.json().get("session")

def get_accounts(session):
    return requests.get(f"{BASE_URL}/get-my-accounts.json?session={session}").json()

def get_account_performance(session, account_id):
    return requests.get(f"{BASE_URL}/get-account-performance.json?session={session}&id={account_id}").json()
