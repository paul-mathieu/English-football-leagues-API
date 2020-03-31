# -*- coding: UTF-8 -*-

from .core import *
from bs4 import BeautifulSoup


class Leagues(object):

    def __init__(self, *args):
        pass

    def json_leagues(self, parameters_dictionary):
        self.set_parameters_dictionary_leagues(parameters_dictionary)
        self.set_URL_leagues()
        # self.display_leagues()
        self.get_main_leagues()

    def set_parameters_dictionary_leagues(self, parameters_dictionary):
        self.parameters_dictionary = parameters_dictionary
        # print("test")

    def set_URL_leagues(self):
        self.URL = BASE_URL + LEAGUES_START_URL + \
                   "/" + self.parameters_dictionary["country"] + \
                   "/" + self.parameters_dictionary["league"] + \
                   "/" + self.get_year() + \
                   LEAGUES_END_URL

    def get_year(self):
        if "start year" in self.parameters_dictionary.keys():
            year = int(self.parameters_dictionary["start year"])
            return str(year) + str(year + 1)
        elif "end year" in self.parameters_dictionary.keys():
            year = int(self.parameters_dictionary["end year"])
            return str(year - 1) + str(year)
        else:
            return str(THIS_YEAR - 1) + str(THIS_YEAR)

    def display_leagues(self):
        print("url :", self.URL)
        print(get_HTML(self.URL))

    def get_main_leagues(self):
        """
        return a json object of the main english football leagues
        :return: json_object
        """
        html = get_HTML(self.URL)
        html_soup = BeautifulSoup(html, 'html.parser')
        liste = html_soup.find('ul', class_='left-tree')
        data_set = {"main_leagues": []}
        for url in liste.find_all('li'):
            if url['class'] == ['odd'] or url['class'] == ['even'] or url['class'] == ['expanded', 'odd'] or url[
                'class'] == ['expanded', 'even']:
                data_set['main_leagues'].append(url.a.string)

        # create json object
        json_dump = json.dumps(data_set)
        json_object = json.loads(json_dump)
        return json_object
        # je n'ai que les nom des leagues principales mais je n'ai pas les sous leagues de ces leagues.
        # pour cela il faut faire une requete pour chaque lien, pour qu'il me donne sa sous league.
        # remarque, il des fausses leagues parmi les leagues : Non League premier et Non League Div One
        # normalement y a 80 main leagues
        # result:
        # {'main_leagues': ['Premier League', 'Championship', 'League One', 'League Two', 'National League', 'National League N / S', 'Non League Premier', 'Non League Div One', 'North West Counties League Premier', 'FA Cup', 'League Cup', 'Community Shield', 'EFL Trophy', 'FA Trophy', 'FA Vase', 'Alan Turvey Trophy', 'Southern League Cup', 'Northern Premier League Challenge Cup', 'BBFA Senior Cup', 'Bedfordshire Senior Challenge Cup', 'Birmingham Senior Cup', 'Cheshire Senior Cup', 'Cumberland Senior Cup', 'Derbyshire Senior Cup', 'Durham County Challenge Cup', 'Gloucester Senior Challenge Cup', 'Huntingdonshire Senior Cup', 'Essex Senior Cup', 'East Riding Senior Cup', 'Hertfordshire Senior Challenge Cup', 'Kent Senior Cup', 'Lancashire FA Challenge Trophy', 'Lancashire Senior Cup', 'Lincolnshire Senior Cup', 'Liverpool Senior Cup', 'Leicestershire and Rutland Challenge Cup', 'London Senior Cup', 'Manchester Premier Cup', 'Manchester Senior Cup', 'Norfolk Senior Cup', 'Middlesex Senior Cup', 'North Riding Senior Cup', 'Northamptonshire Senior Cup', 'Northumberland Senior Cup', 'Nottinghamshire Saturday Senior Cup', 'Oxfordshire Senior Cup', 'Staffordshire Senior Cup', 'Sheffield and Hallamshire Senior Cup', 'Somerset Premier Cup', 'Suffolk FA Premier Cup', 'Surrey Senior Cup', 'Sussex Senior Challenge Cup', 'Walsall Senior Cup', 'West Riding County Cup', 'Central League', 'Central League Cup', 'Premier League 2 Division One', 'Premier League 2 Division Two', 'Professional Development League', 'Premier League Cup', 'U18 Premier League', 'FA Youth Cup', 'U18 Professional Development League', 'U18 Premier League Cup', 'Youth Alliance', 'Youth Alliance Cup', "Women's Super League", "Women's Championship", "Women's National League - Premier Division", "Women's National League - Division One", "FA Women's Cup", 'WSL Cup', 'U21 Premier League Division 1', 'U21 Premier League Division 2 ', 'Premier Reserve League', 'Conference League Cup', "Women's Premier League", "Women's League Cup", "Women's Play-offs 3/4", 'Club Friendlies']}
        #
        # REMARQUE: j'ai traite par classe car des fois les url n'ont pas de titre

    def get_all_leagues(self):
        '''
        return all the english football leagues, even sub leagues
        :return: json_object
        '''
        print(self.URL)
        html = get_HTML(self.URL)
        html_soup = BeautifulSoup(html, 'html.parser')
        liste = html_soup.find('ul', class_='left-tree')
        data_set = {}
        for url in liste.find_all('li'):
            if url['class'] == ['odd'] or url['class'] == ['even'] or url['class'] == ['expanded', 'odd'] or url[
                'class'] == ['expanded', 'even']:
                print(type(url.a['href']))
                new_url = BASE_URL + url.a['href']
                new_html = get_HTML(new_url)
                new_html_soup = BeautifulSoup(new_html, 'html.parser')
                list = new_html_soup.select('ul.left-tree > li.expanded')
                print('list :', list)
                for link in list[0].find_all('a'):
                    league = link.string
                    print(link)
                    parent = link.find_parent('ul').find_previous_sibling()  # parent link
                    if parent is not None:
                        print("parent : ", parent.string)
                        data_set[parent.string] = dict(league)
                    else:
                        data_set[league] = None  # it's the root
                print("data_set :", data_set)
                print("new html :", new_url)
            return 0
