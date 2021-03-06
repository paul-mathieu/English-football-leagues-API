# -*- coding: UTF-8 -*-
import psycopg2 as psycopg2

from .core import *
from bs4 import BeautifulSoup
import requests


class Players(object):
    """
    We find in this class all functions about players data
    """

    # ===============================================================
    #   Initialisation
    # ===============================================================
    def __init__(self, *args):
        self.parameters_dictionary = None
        self.URL = None
        self.choix = 0
        self.request_headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    def set_parameters_dictionary(self, parameters_dictionary):
        """
        Set the query option dictionary
            :param parameters_dictionary: dictionary of values
            :type parameters_dictionary: dict
        """
        self.parameters_dictionary = {"API type": None, "country": None, "league": None, "end year": None, "club": None,
                                      "firstName": None, "lastName": None, "matches": None, "dataPlayer": None,
                                      "career": None, "all": None, "idP": None}
        self.fill_parameters_dictionary(parameters_dictionary)

    # ===============================================================
    #   Setters
    # ===============================================================

    def set_URL_Players(self):
        """
        Add the attribute URL - We use site search system
            choice 1 - country and club, return information about team players
            choice 2 - firstName, lastName and matches(1), return information about matchs player
            choice 3 - firstName, lastName and dataPlayer(1), return information about player
            choice 4 - firstName, lastName and career(1), return information about player career
            choice 5 - firstName, lastName and all(1), retrun all informations about player
        """

        if self.parameters_dictionary["country"] is not None and self.parameters_dictionary["club"] is not None:
            param = str(self.parameters_dictionary["club"]).replace(" ", "+")
            self.URL = BASE_URL + "/search/?q=" + param
            self.choix = 1
        elif (self.parameters_dictionary["firstName"] is not None and self.parameters_dictionary[
            "lastName"] is not None and self.parameters_dictionary["matches"] is not None) or (
                self.parameters_dictionary["idP"] is not None and self.parameters_dictionary["matches"] is not None):
            param = str(self.parameters_dictionary["lastName"]).replace(" ", "+")
            self.URL = BASE_URL + "/search/?q=" + param
            self.choix = 2
        elif self.parameters_dictionary["firstName"] is not None and self.parameters_dictionary[
            "lastName"] is not None and self.parameters_dictionary["dataPlayer"] is not None or (
                self.parameters_dictionary["idP"] is not None and self.parameters_dictionary["dataPlayer"] is not None):
            param = str(self.parameters_dictionary["lastName"]).replace(" ", "+")
            self.URL = BASE_URL + "/search/?q=" + param
            self.choix = 3
        elif self.parameters_dictionary["firstName"] is not None and self.parameters_dictionary[
            "lastName"] is not None and self.parameters_dictionary["career"] is not None or (
                self.parameters_dictionary["idP"] is not None and self.parameters_dictionary["career"] is not None):
            param = str(self.parameters_dictionary["lastName"]).replace(" ", "+")
            self.URL = BASE_URL + "/search/?q=" + param
            self.choix = 4
        elif self.parameters_dictionary["firstName"] is not None and self.parameters_dictionary[
            "lastName"] is not None and self.parameters_dictionary["all"] is not None or (
                self.parameters_dictionary["idP"] is not None and self.parameters_dictionary["all"] is not None):
            param = str(self.parameters_dictionary["lastName"]).replace(" ", "+")
            self.URL = BASE_URL + "/search/?q=" + param
            self.choix = 5
        else:
            raise ValueError("Parameter's configuration not found")

    # ===============================================================
    #   Methods
    # ===============================================================

    def fill_parameters_dictionary(self, parameters_dictionary):
        """
        Fill the attribute parameters_dictionary
            :param parameters_dictionary: dictionary of query parameters
            :type parameters_dictionary: dict
        """
        for key in parameters_dictionary.keys():
            self.parameters_dictionary[key] = parameters_dictionary[key]

    def display(self):
        """
        Display some information about players
        """
        print(get_HTML(self.URL))
        print("\n\n\n" + self.URL)

    def json_players(self, parameters_dictionary):
        """
        Apply the query with parameters and return a dictionary (json)
            :param parameters_dictionary: dictionary of query parameters
            :type parameters_dictionary: dict
            :return json_data: json data
            :rtype json_data: dict
        """
        self.set_parameters_dictionary(parameters_dictionary)
        self.set_URL_Players()
        return self.processing()
        # self.display()

    # ===============================================================
    #   Core
    # ===============================================================

    def functionProcessing2(self, firstName='', lastName=''):
        """
        This function search the data for one players gived in parameters_dicitonary or in param.

        We can have three type of data:
            - All matchs for the players, we have the next information
                    - player
                    - Date
                    - Ligue
                    - winerTeam
                    - Score
                    - loserTeam
                    - G
                    - C

            - Player passport, we have the next information
                    - firstName
                    - lastName
                    - ationality
                    - DateOfBirth
                    - Age
                    - CountryOfbirth
                    - position
                    - height
                    - weight
                    - foot

            - Player career, we have the next information
                    - player
                    - season
                    - teams
                    - competition
                    - game_minutes
                    - appearances
                    - lineups
                    - subs_in
                    - subs_out
                    - subs_on_bench
                    - goals
                    - yellow_cards
                    - nd_yellow_cards
                    - red_cards


        This can data can be searched separately or grouped

        This function is only used in the "processing" function.

        :param firstName: Not compulsory, used for a player different than the starter
        :param lastName: Not compulsory, used for a player different than the starter
        :return: liste of dict
        """
        finalreturn = {}
        if self.parameters_dictionary["idP"] is not None:
            numPlayerL = self.parameters_dictionary["idP"]
            playerUrl = BASE_URL + "/players/a/" + str(numPlayerL)
            # print(playerUrl)

            html = requests.get(playerUrl, headers=self.request_headers)
            html_soup = BeautifulSoup(html.text, 'html.parser')
            try:
                pnam = html_soup.find_all("div", {"id": "subheading"})[0].find_all("h1")[0].text
            except:
                # print(html_soup.find_all("div", {"id": "subheading"})[0]).find_all("h1")
                pnam = "None"
        else:
            if firstName != '' and lastName != '':
                param = str(lastName).replace(" ", "+")
                self.URL = BASE_URL + "/search/?q=" + param
                self.parameters_dictionary["firstName"] = str(firstName)

            # For search one players we use the query option of the web site
            # The query parameter is the last name of the player
            # After we look for when the first name give in parameter is the same

            html = requests.get(self.URL, headers=self.request_headers)
            # html = urlopen(request)
            html_soup = BeautifulSoup(html.text, 'html.parser')
            rows = html_soup.findAll("tr")
            del html, html_soup
            find = False

            for row in rows:
                cells = row.findAll("td")
                try:
                    if str(self.parameters_dictionary["firstName"]).upper() in str(cells[0].text).upper():
                        print("Player name is ", cells[0].text)
                        pnam = cells[0].text
                        playerUrl = BASE_URL + "/" + str(cells[0].a.get('href'))
                        find = True
                        break
                except:
                    pass

            if not find: raise ValueError("Player name not found")

            # When the player was found, we recover the specific URL of this player

            html = requests.get(playerUrl, headers=self.request_headers)
            html_soup = BeautifulSoup(html.text, 'html.parser')

            numPlayerL = playerUrl.split("/")[-2]

        if self.choix == 2 or self.choix == 5:
            matchs = []

            i = 0

            while True:
                # Get method use by web site for recover all matches - We inject the player number and a page identifier
                getMeth = 'https://uk.soccerway.com/a/block_player_matches?block_id' \
                          '=page_player_1_block_player_matches_3&callback_params=%7B%22page%22%3A0%2C' \
                          '%22block_service_id%22%3A%22player_matches_block_playermatches%22%2C%22people_id%22%3A' + \
                          numPlayerL + '%2C%22type%22%3Anull%2C%22formats%22%3Anull%7D&action=changePage&params=%7B' \
                                       '%22page%22%3A' + str(i) + '%7D'
                listGetMeth = getMeth.split("%")
                # print(listGetMeth)

                # recover html code
                htmlMatchs = requests.get(getMeth, headers=self.request_headers).json()["commands"][0]["parameters"][
                    "content"]

                # Processing for recover all matches
                if len(str(htmlMatchs)) < 100:
                    finalreturn['MatchPlayer'] = matchs
                    break
                html_soup1 = BeautifulSoup(htmlMatchs, 'html.parser')
                rows = html_soup1.findAll("tr")

                for row in rows:
                    cells = row.findAll("td")
                    try:
                        Match = {
                            "player": [{"PlayerID": numPlayerL, "PlayerName": pnam, }],
                            # "PlayerID": numPlayerL,
                            # "PlayerName": pnam,
                            "Date": cells[1].text,
                            "Ligue": cells[2].text,
                            "winerTeam": str(cells[3].text).replace('\'', ''),
                            "Score": cells[4].text,
                            "loserTeam": str(cells[5].text).replace('\'', ''),
                            "G": 0,
                            "C": 0
                        }

                        yellowAndGoal = []
                        index = 0
                        for nb in cells[6]:

                            try:
                                nbr = int(nb[-1])

                                yellowAndGoal[index - 1][1] = nbr
                            except:
                                type = nb.get("src")[-5]
                                yellowAndGoal.append([type, 1])
                            index += 1

                        Match.update(dict(yellowAndGoal))

                        # print(Match)
                        matchs.append(Match)

                    except:
                        pass
                i = i - 1

        if self.choix == 3 or self.choix == 5:
            returns = []
            rows = html_soup.findAll("dl")

            for row in rows:
                cells = row.findAll("dd")

                try:
                    data = {"firstName": cells[0].text,
                            "lastName": cells[1].text,
                            "Nationality": cells[2].text,
                            "DateOfBirth": cells[3].text,
                            "Age": cells[4].text,
                            "CountryOfbirth": cells[5].text,
                            "position": cells[6].text,
                            "height": cells[7].text,
                            "weight": cells[8].text,
                            "foot": cells[9].text}
                    returns.append(data)
                except:
                    data = {"firstName": cells[0].text,
                            "lastName": cells[1].text,
                            "Nationality": cells[2].text,
                            "DateOfBirth": cells[3].text,
                            "Age": cells[4].text,
                            "CountryOfbirth": '',
                            "position": '',
                            "height": '',
                            "weight": '',
                            "foot": ''
                            }
                    returns.append(data)
            # finalreturn["passport"] = returns
            finalreturn['passport'] = returns

        if self.choix == 4 or self.choix == 5:

            rows = html_soup.findAll("table", {"class": 'playerstats career sortable table'})
            retrourner = []
            for row in rows:
                cellss = row.findAll("tr")

                for a in cellss:
                    cells = a.findAll("td")
                    try:
                        data = {
                            "player": [{"PlayerID": numPlayerL, "PlayerName": pnam, }],
                            "season": cells[0].text,
                            "teams": cells[1].text,
                            "competition": cells[2].text,
                            "game_minutes ": cells[3].text,
                            "appearances ": cells[4].text,
                            "lineups ": cells[5].text,
                            "subs_in": cells[6].text,
                            "subs_out": cells[7].text,
                            "subs_on_bench": cells[8].text,
                            "goals ": cells[9].text,
                            "yellow_cards": cells[10].text,
                            "nd_yellow_cards": cells[11].text,
                            "red_cards": cells[12].text
                        }
                        retrourner.append(data)

                    except:
                        pass
            # print(retrourner)
            finalreturn["career"] = retrourner

        return finalreturn

    def functionProcessing1(self):
        '''
        Function used for serch all players (and players data) of a team
        For each player in team we have to the maximum the next information :
            - shirtnumber
            - name
            - age
            - position
            - game_minutes
            - appearances
            - lineups
            - subs_in
            - subs_out
            - subs_on_bench
            - number_statistic_goals
            - number_statistic_assists
            - yellow_cards
            - nd_yellow_cards
            - red_cards
        '''

        html = requests.get(self.URL, headers=self.request_headers)
        html_soup = BeautifulSoup(html.text, 'html.parser')
        rows = html_soup.findAll("div", {"class": "block_search_results_teams real-content clearfix"})
        for row in rows:
            row = row.findAll("li")

            for i in row:
                if (str(self.parameters_dictionary["country"]).upper() in str(i.text).upper()):
                    self.URL = BASE_URL + "/" + str(i.a.get('href')) + "/squad/"
                    break

        html = requests.get(self.URL, headers=self.request_headers)
        # html = urlopen(request)
        html_soup = BeautifulSoup(html.text, 'html.parser')

        rows = html_soup.findAll("table", {"class": "table squad sortable"})
        players = []

        for row in rows:
            cellss = row.findAll("tr")
            for a in cellss:
                cells = a.findAll("td")
                if len(cells) == 17:
                    try:
                        players_entry = {
                            "shirtnumber": cells[0].text,
                            "name": cells[2].text,
                            "age": cells[4].text,
                            "position": cells[5].text,
                            "game_minutes": cells[6].text,
                            "appearances": cells[7].text,
                            "lineups": cells[8].text,
                            "subs_in": cells[9].text,
                            "subs_out": cells[10].text,
                            "subs_on_bench": cells[11].text,
                            "number_statistic_goals": cells[12].text,
                            "number_statistic_assists": cells[13].text,
                            "yellow_cards": cells[14].text,
                            "nd_yellow_cards": cells[15].text,
                            "red_cards": cells[16].text
                        }
                        players.append(players_entry)

                    except:
                        pass
                elif len(cells) == 14:
                    try:
                        players_entry = {
                            "age": cells[3].text,
                            "game_minutes": cells[5].text,
                            "number_statistic_goals": cells[11].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[12].text,
                            "red_cards": cells[14].text}
                        players.append(players_entry)
                    except:
                        pass
                elif len(cells) == 15:
                    try:
                        players_entry = {
                            "age": cells[3].text,
                            "game_minutes": cells[5].text,
                            "number_statistic_goals": cells[11].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[12].text,
                            "red_cards": cells[14].text}
                        players.append(players_entry)
                    except:
                        pass
                elif len(cells) == 16:
                    try:
                        players_entry = {
                            "age": cells[4].text,
                            "game_minutes": cells[6].text,
                            "number_statistic_goals": cells[12].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[13].text,
                            "red_cards": cells[15].text}
                        players.append(players_entry)
                    except:
                        pass

        return {'TeamPlayer': players}

    def processing(self):
        """
        This function execute the processing chosen by the user in the variable parametre_dictionaty
            :return json_data: json data
            :rtype json_data: liste[dict]
        """

        # If we search a team squad. This part of the function return all players of team choose
        # This part is run if : parameters_dictionary["country"] != None and self.parameters_dictionary["club"] != None

        if self.choix == 1:
            finalreturn = self.functionProcessing1()
        # ----------------------------------------------------------------------------------------------------------

        # This part of the function return all matches plays by one player
        # If we search a player
        if self.choix == 2 or self.choix == 3 or self.choix == 4 or self.choix == 5:
            finalreturn = self.functionProcessing2()

        return finalreturn

    def functionProcessing1b(self, u):
        '''
        This function is used in match.py
            For each player in team we have to the maximum the next information :
            - shirtnumber
            - name
            - age
            - position
            - game_minutes
            - appearances
            - lineups
            - subs_in
            - subs_out
            - subs_on_bench
            - number_statistic_goals
            - number_statistic_assists
            - yellow_cards
            - nd_yellow_cards
            - red_cards
        :param u: Team URL
        :return: Dict
        '''
        html = requests.get(u, headers=self.request_headers)
        html_soup = BeautifulSoup(html.text, 'html.parser')

        rows = html_soup.findAll("table", {"class": "table squad sortable"})
        players = []

        for row in rows:
            cellss = row.findAll("tr")
            for a in cellss:
                cells = a.findAll("td")
                if len(cells) == 17:
                    try:
                        players_entry = {
                            "shirtnumber": cells[0].text,
                            "name": cells[2].text,
                            "age": cells[4].text,
                            "position": cells[5].text,
                            "game_minutes": cells[6].text,
                            "appearances": cells[7].text,
                            "lineups": cells[8].text,
                            "subs_in": cells[9].text,
                            "subs_out": cells[10].text,
                            "subs_on_bench": cells[11].text,
                            "number_statistic_goals": cells[12].text,
                            "number_statistic_assists": cells[13].text,
                            "yellow_cards": cells[14].text,
                            "nd_yellow_cards": cells[15].text,
                            "red_cards": cells[16].text
                        }
                        players.append(players_entry)

                    except:
                        pass
                elif len(cells) == 14:
                    try:
                        players_entry = {
                            "age": cells[3].text,
                            "game_minutes": cells[5].text,
                            "number_statistic_goals": cells[11].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[12].text,
                            "red_cards": cells[14].text}
                        players.append(players_entry)
                    except:
                        pass
                elif len(cells) == 15:
                    try:
                        players_entry = {
                            "age": cells[3].text,
                            "game_minutes": cells[5].text,
                            "number_statistic_goals": cells[11].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[12].text,
                            "red_cards": cells[14].text}
                        players.append(players_entry)
                    except:
                        pass
                elif len(cells) == 16:
                    try:
                        players_entry = {
                            "age": cells[4].text,
                            "game_minutes": cells[6].text,
                            "number_statistic_goals": cells[12].text,
                            "number_statistic_assists": 0,
                            "yellow_cards": cells[13].text,
                            "red_cards": cells[15].text}
                        players.append(players_entry)
                    except:
                        pass

        return [{'TeamPlayer': players}]
