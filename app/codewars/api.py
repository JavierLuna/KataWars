from typing import Union

import requests


def get_profile(username: str) -> dict:
    url = f"https://www.codewars.com/api/v1/users/{username}"
    response = requests.get(url)
    if 199 < response.status_code < 300:
        return response.json()
    return {}


def get_score(profile: Union[str, dict]) -> int:
    if isinstance(profile, str):
        profile = get_profile(profile)

    return profile.get('ranks', {}).get('overall', {}).get('score', 0)


def get_completed_challenges(profile: Union[str, dict]) -> int:
    if isinstance(profile, str):
        profile = get_profile(profile)

    return profile.get('codeChallenges', {}).get('totalCompleted', 0)
