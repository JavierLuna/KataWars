import argparse
import time
from getpass import getpass

import requests

HOST = "http://0.0.0.0:5000"

def log_in():
    username = input("Username: ")
    password = getpass("Password: ")
    response = requests.post(HOST+"/api/auth/login", json={'username': username, 'password': password})
    if not response.status_code == 200:
        raise Exception("User and password were not a match")
    return response.json()['token']

def get_auth_headers(token):
    return {'Authorization': f"Bearer {token}"}

def get(url, token):
    response = requests.get(HOST+url, headers=get_auth_headers(token))
    return response

def post(url, token, json=None):
    response = requests.post(HOST+url, headers=get_auth_headers(token), json=json)
    return response

def listen(token):
    all_notifications = set()
    current_page = 1
    print("Listening...")
    while 1:

        response = get(f'/api/notification?page={current_page}', token)
        if response.status_code == 200:
            response_json = response.json()
            for notification in response_json['objects']:
                if notification['id'] not in all_notifications:
                    print("------------------")
                    print()
                    print(f"From: {(notification.get('sender', {}) or {}).get('username', '---')}\t\tTo: You!")
                    print("Content:")
                    print(notification['description'])
                    print()
                    all_notifications.add(notification['id'])
            if response_json['next_page']:
                current_page = response_json['next_page']
        time.sleep(5)



def skill(token):
    pass

def notify(token):
    pass


if __name__ == '__main__':
    commands = {'listen': listen,
                'skill': skill,
                'notify': notify}

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to use", choices=list(commands.keys()))
    args = parser.parse_args()
    token = log_in()
    commands[args.command](token)