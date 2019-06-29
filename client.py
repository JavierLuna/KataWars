import argparse
import time
from getpass import getpass

import requests

HOST = "http://0.0.0.0:5000"


def log_in():
    username = input("Username: ")
    password = getpass("Password: ")
    response = requests.post(HOST + "/api/auth/login", json={'username': username, 'password': password})
    if not response.status_code == 200:
        raise Exception("User and password were not a match")
    return response.json()['token']


def get_auth_headers(token):
    return {'Authorization': f"Bearer {token}"}


def get(url, token):
    response = requests.get(HOST + url, headers=get_auth_headers(token))
    return response


def post(url, token, json=None):
    response = requests.post(HOST + url, headers=get_auth_headers(token), json=json)
    return response


def list_participants(token):
    response = get('/api/participant', token)
    if not response.status_code == 200:
        raise Exception("Something went wrong!")
    usernames = response.json()
    print("Usernames:")
    for username in usernames:
        print(username)
    return usernames


def get_me(token):
    response = get('/api/participant/me', token)
    if not response.status_code == 200:
        raise Exception("Something went wrong!")
    return response.json()


def list_skills(token):
    me = get_me(token)
    response = get('/api/skill', token)
    if not response.status_code == 200:
        raise Exception("Something went wrong!")
    response_json = response.json()['objects']
    skill_ids = []
    print("SKILLS:")
    print("id", "\t\tAmmount", "\t\tname", "\t\tdescription")
    print("=========================================================")
    for skill in response_json:
        skill_ids.append(skill['id'])
        print(skill['id'], f"\t\t{me['skills'].count(skill['id'])}", "\t\t\t\t" + skill['name'],
              "\t\t" + skill['description'])
    return skill_ids


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
    skill_ids = list_skills(token)
    target_skill = -1
    while target_skill not in skill_ids:
        target_skill = int(input("What skill do you want to use (id)?"))

    usernames = list_participants(token)
    target_foe = -1
    while target_foe not in usernames:
        target_foe = input("Who is going to be your opponent?")
    print("Aiming... Fire!!")
    response = post(f'/api/skill/{target_skill}', token, json={'target': target_foe})

    if not response.status_code == 204:
        raise Exception("Something went wrong! Maybe you couldn't use this skill?")

    print("Done :)")



if __name__ == '__main__':
    commands = {'listen': listen,
                'skill': skill}

    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command to use", choices=list(commands.keys()))
    args = parser.parse_args()
    token = log_in()
    commands[args.command](token)
