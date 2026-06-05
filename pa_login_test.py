import requests
import re

session = requests.Session()
login_url = "https://www.pythonanywhere.com/login/"

response = session.get(login_url)
match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
if not match:
    print("Could not find CSRF token.")
    exit(1)
csrf_token = match.group(1)

login_data = {
    'csrfmiddlewaretoken': csrf_token,
    'auth-username': 'worklane',
    'auth-password': '101010??',
    'login_view-current_step': 'auth'
}

response = session.post(login_url, data=login_data, headers={'Referer': login_url})

if "Log out" in response.text or "dashboard" in response.url:
    print("SUCCESS: Logged into PythonAnywhere!")
    
    # Get the API token page
    account_url = "https://www.pythonanywhere.com/user/worklane/account/"
    response = session.get(account_url)
    
    with open('pa_account_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Dumped account page to pa_account_page.html")
    match = re.search(r'Token: <span[^>]*>([^<]+)</span>', response.text)
    if match:
        print("API Token:", match.group(1).strip())
    else:
        # Sometimes token needs to be generated first
        print("Token not found on account page. Attempting to create one.")
        token_csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text).group(1)
        create_token_url = "https://www.pythonanywhere.com/user/worklane/account/api_token"
        response = session.post(create_token_url, data={'csrfmiddlewaretoken': token_csrf}, headers={'Referer': account_url})
        match = re.search(r'Token: <span[^>]*>([^<]+)</span>', response.text)
        if match:
            print("API Token:", match.group(1).strip())
        else:
            print("Failed to get or create API token.")
            # Let's just dump part of the page around 'API token'
            idx = response.text.find("API token")
            print(response.text[idx:idx+1000])
else:
    print("FAILED to log in.")
    print("URL:", response.url)
    if "Incorrect username or password" in response.text:
        print("Incorrect username or password.")
