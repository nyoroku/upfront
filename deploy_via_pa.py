import requests
import re
import time

session = requests.Session()
login_url = "https://www.pythonanywhere.com/login/"

# 1. Login
response = session.get(login_url)
match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text)
csrf_token = match.group(1)

login_data = {
    'csrfmiddlewaretoken': csrf_token,
    'auth-username': 'worklane',
    'auth-password': '101010??',
    'login_view-current_step': 'auth'
}
response = session.post(login_url, data=login_data, headers={'Referer': login_url})
print("Login status:", response.status_code)

# 2. Get the new console (which the API just created: 45476047)
console_id = 45476047
console_frame_url = f"https://www.pythonanywhere.com/user/worklane/consoles/{console_id}/frame/"

# Ping the frame to 'start' the console
response = session.get(console_frame_url)
print("Pinged console frame, status:", response.status_code)

time.sleep(3) # Wait for it to boot

# 3. Use the API token to send the command
api_token = "e845bc213ce3afa4f7189d77185d4f36e0e55ad7"
api_url = f"https://www.pythonanywhere.com/api/v0/user/worklane/consoles/{console_id}/send_input/"
headers = {"Authorization": f"Token {api_token}", "Content-Type": "application/json"}
payload = {"input": "echo e845bc213ce3afa4f7189d77185d4f36e0e55ad7 > ~/.pythonanywhere\npa_autoconfigure_django.py --python=3.12 https://github.com/nyoroku/worklane.git\n"}

response = requests.post(api_url, headers=headers, json=payload)
print("Sent command, status:", response.status_code, response.text)
