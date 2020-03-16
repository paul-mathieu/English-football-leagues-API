# -*- coding: UTF-8 -*-
import json
import requests
import datetime

BASE_URL = "https://uk.soccerway.com"

PLAYERS_URL = None

TEAMS_START_URL = "/national"
TEAMS_END_URL = "/regular-season/tables"

LEAGUES_URL = None

THIS_YEAR = int(str(datetime.datetime.now())[:4])


def get_HTML(url, convert_to_json=False):
    html_content = requests.get(url).text
    if not convert_to_json:
        return html_content
    else:
        return json.loads(json.dumps(html_content))


def is_players_request(parameters_dictionary):
    if "API type" not in parameters_dictionary.keys():
        return False
    return parameters_dictionary["API type"] in ["players", "Players", "PLAYERS"]


def is_teams_request(parameters_dictionary):
    if "API type" not in parameters_dictionary.keys():
        return False
    return parameters_dictionary["API type"] in ["teams", "Teams", "TEAMS"]


def is_leagues_request(parameters_dictionary):
    if "API type" not in parameters_dictionary.keys():
        return False
    return parameters_dictionary["API type"] in ["leagues", "Leagues", "LEAGUES"]