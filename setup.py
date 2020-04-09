# -*- coding: UTF-8 -*-
import psycopg2

import footballAPI


# ===============================================================
#   Players
# ===============================================================

parameters_dictionary = {"API type": "players", "lastName": "pogba", "firstName": "paul"}
dataBase = ""
# dataBase = psycopg2.connect(host="localhost",database="Foot", user="postgres", password="Motsdepassesécu")

client = footballAPI.FootballAPI()
client.set_parameters(parameters_dictionary, dataBase)

print("===============")
# matches = client.json_data
# print(matches)
print("===============")


# ===============================================================
#   Teams
# ===============================================================

# parameters_dictionary = {"API type": "teams", "country": "england", "league": "league-one", "end year": 2019}

# client = footballAPI.FootballAPI()
# client.set_parameters(parameters_dictionary)
# client.tests_api_teams()

# print("===============")
# print(client.json_data)
# print("===============")


# ===============================================================
#   Leagues
# ===============================================================


# noah_parameters_dictionary = {"API type": "leagues", "country": "england", "league": "league-one", "end year": 2019}
#
# client = footballAPI.FootballAPI()
# client.set_parameters(noah_parameters_dictionary)
# client.tests_api_teams()

# print("===============")
# print(client.json_data)
# print("===============")

