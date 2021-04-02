"""
SKYRIM LOCATION CRAWLER

This program will crawl the Locations on the Skyrim wiki for a user defined amount of
times at random and return back some basic info on the locations such as url, name, location type,
hold, relative location, location id(s), and a quick summary given on the page.

@author: Reis Gadsden
@version: v1.0.2

Attributes Scraped:
URL - URL of item page crawled to
Name - Name of the location
Location Type - What type the location is such as Cave, Shop, etc.
Relative Location - Some locations gave a location relative in the world
LocationID(s) - Reference ID used in game, important for modding and console commands
Summary - Typically the first <p> tag, gives a short summary of the location

Additional Data Included:
Hold Lookup Table - A small table stating the hold, its capital city, and its jarl, for each hold in game
Hold Summary Table - A small table that shows the distribution of locations in hold for crawled pages

Important Base Links:
Base Crawl Page - https://elderscrolls.fandom.com/wiki/Locations_(Skyrim)
Hold Lookup Table Page - https://elderscrolls.fandom.com/wiki/Holds

Five Base Links:
(I would like to note this program crawls based on user generated input at random. You could crawl 1 page, or you could
crawl all 562 base locations in Skyrim, each time the crawler will choose random locations, for example if you crawl
five times, and then crawl five times again, you only have (1/562)^5  or 0.00000000000179% chance of getting the same
exact links not even in the same order, mind you. However, I included some of the location links as it was specified in
the instructions.)
- https://elderscrolls.fandom.com/wiki/Whiterun_Marketplace
- https://elderscrolls.fandom.com/wiki/Horgeir%27s_House
- https://elderscrolls.fandom.com/wiki/Talking_Stone_Camp
- https://elderscrolls.fandom.com/wiki/Heimskr%27s_House
- https://elderscrolls.fandom.com/wiki/Dead_Men%27s_Respite

Additional work that allows this project to exceed a B:
- Used user generated input.
- Got a random assortment of items instead of predefined ones.
- Said random assortment is based of the user defined input.
- Exception handling of all types, including, but not limited to:
    - Constraints on user input such as:
        - Negative numbers
        - Strings
        - Zero value
        - Blank value
        - Values exceeding total number of locations
    - Modifying and cleaning up attributes from sites that were not all formatted the same as it is a fandom wiki,
      meaning each page is created by different users, which results in wonky and inconsistent formatting,
      however formatting was cleaned up in order to provide uniform output. (THERE WAS A LOT OF THIS!!!)
    - Possible exceptions in the data gathered from the website such as an attribute not existing rather then just
      printing None.
    - Alternative ways of searching for data such as in the get_hold method, in which if hold could not be found it
      searched the summary paragraph in order to see if there was a mention of hold or city in which we could deduce
      was the hold the location was in.
    - Possible exceptions that might rise from dumping to .json file.
- Adding the hold summary table, which gives some statistical data on attributes gathered during crawl
  also, I just thought it was a cute feature.
- Adding the type summary table, which gives some statistical data on attributes gathered during crawl, and yes,
  I also thought it was just a cute feature
- Implementing the use of my table data in methods for getting attributes, giving more purpose the data.
- Generally clean and readable formatting of output to console.


Linked Resources:
https://www.crummy.com/software/BeautifulSoup/bs4/doc/ (using select)
https://stackabuse.com/formatting-strings-with-python/ (formatting strings)
https://docs.python.org/3/library/json.html#exceptions (handling json exception)
https://www.geeksforgeeks.org/randomly-select-elements-from-list-without-repetition-in-python/
https://stackoverflow.com/questions/55590092/replace-br-with-space-in-beautifulsoap-output/55590217 (get_text separator)
"""

# needed imports
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from pip._vendor import requests
import random
import json
from collections import OrderedDict

# necessary initializations
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
rp = RobotFileParser()
init_url = "https://elderscrolls.fandom.com/wiki/Locations_(Skyrim)"


# will parse robots.txt and return boolean value based on if site be crawled
def get_rp(robot_url):
    # print("Robots.txt page: " + robot_url)
    r = requests.get(robot_url, headers=headers)
    rp.parse(r.text)
    return rp.can_fetch('*', robot_url)


# will attempt to fetch provided url and will return the necessary BeautifulSoup object if it can fetch the site
# returns false if it is not reachable
def get_page(page_url, site_count=None):
    if page_url == init_url:
        pass
        # print("Base page: " + page_url)
    else:
        pass
        # print(str(site_count) + ". Crawled to: " + page_url)
    if rp.can_fetch('*', page_url):
        pr = requests.get(page_url, headers=headers)
        bs = BeautifulSoup(pr.text, "html.parser")
        return bs
    else:
        return False


# crawler class that contains main logic for crawling and parsing information into readable format
class Crawler:
    # necessary initializations for crawler class
    page_attr = dict()
    links = []
    robot_page = ""
    robot_check = False
    base_page = ""
    crawl_page = ""
    hold_page = ""
    sites_to_crawl = 0
    hold_list = []
    city_list = []
    jarl_list = []
    type_sum = 0
    hold_sum = 0

    # constructor for crawler class, does some neat stuff such as getting base url, robot url, and calling
    # functions for a simple main method
    def __init__(self, base_url, sites_to_crawl):
        self.sites_to_crawl = sites_to_crawl
        self.crawl_page = base_url
        for site in base_url.split('/'):
            if "https:" in site:
                self.base_page += site + "//"
            else:
                self.base_page += site
            if ".com" in site:
                break
        self.robot_page = self.base_page + "/robots.txt"
        self.hold_page = self.base_page + "/wiki/Holds"
        # print("Base site & robots.txt: ")
        self.robot_check = get_rp(self.robot_page)
        if self.robot_check:
            self.populate_links(self.crawl_page)
            self.get_info()
            # self.format_print()
        else:
            # just in case robots.txt cannot be parsed, or if user is not allowed to crawl.
            # not sure what would cause this besides ip bans but i figured i should let the user know there is an
            # issue.
            print("Robots.txt specifies that this site cannot be crawled :(")

    # populates the links list with links that can be crawled to
    def populate_links(self, base_link):
        bs = get_page(base_link)
        # print("\nCrawled Sites: ")  # fun formatting :)
        bs.find('div', {'class': 'mw-parser-output'}).find('table').extract()  # gets rid of pesky table at start
        crawlable_links = set()

        # keeps and index of how many non repeated location links there are.
        # this is necessary because in the main body links are repeated and also there are links that are not locations
        # at the end of the page such as links to forums and bugs.
        for c in bs.find('div', {'class': 'mw-parser-output'}).find_all('li'):
            if "Dawnguard" == c.find('a').get_text().strip():  # first occurrence of non-location link in <li>
                break
            # cast links to set in order to remove duplicates
            crawlable_links.add(c.find('a').attrs['href'])

        # if user entered a value greater then the number of pages there are it will default to the total number
        # of crawlable page.
        if self.sites_to_crawl > len(crawlable_links):
            self.sites_to_crawl = len(crawlable_links)

        # populates the list with random choices from crawlable links, makes sure not duplicate
        while len(self.links) < self.sites_to_crawl:
            rand_choice = random.choice(tuple(crawlable_links))  # cast to tuple because random.choice doesnt do sets
            # check if none just to be safe
            if rand_choice is not None \
                    and self.base_page + rand_choice not in self.links:
                self.links.append(self.base_page + rand_choice)

    # the following three methods fill lists from a table, these lists are one to one such that each index of each list
    # corresponds to the information found in the other lists

    # method that fills a list with all names of holds from table
    def get_holds(self, bs_obj):
        for hold in bs_obj.find('table', {'class': 'wikitable sortable'}).find('tbody').find_all('tr')[1:]:
            self.hold_list.append(hold.find_all('td')[0].get_text().strip().split('\n')[0])

    # method that fills a list with all names of cities from table
    def get_cities(self, bs_obj):
        for city in bs_obj.find('table', {'class': 'wikitable sortable'}).find('tbody').find_all('tr')[1:]:
            self.city_list.append(city.find_all('td')[1].get_text().strip().split('\n')[0])

    # method that fills a list with all names of jarls from table
    def get_jarls(self, bs_obj):
        for jarl in bs_obj.find('table', {'class': 'wikitable sortable'}).find('tbody').find_all('tr')[1:]:
            self.jarl_list.append(jarl.find_all('td')[2].get_text().strip().split('\n')[0])

    # method that condenses all calls to methods that gather the necessary information, appends to main dictionary
    def get_info(self):
        site_count = 1
        bs = get_page(self.hold_page, site_count)
        self.get_holds(bs)
        self.get_cities(bs)
        self.get_jarls(bs)
        for link in self.links:
            loc_data = dict()
            site_count += 1
            bs = get_page(link, site_count)
            loc_data["Location Name: "] = self.get_loc_name(bs).replace("\xa0", " ")
            loc_data["Location Type: "] = self.get_loc_type(bs).replace("\xa0", " ")
            loc_data["Hold: "] = self.get_hold(bs).replace("\xa0", " ")
            loc_data["Relative Location: "] = self.get_loc(bs).replace("\xa0", " ")
            loc_data["Location ID(s): "] = self.get_loc_ids(bs).replace("\xa0", " ")
            loc_data["Summary: "] = self.get_summary(bs).replace("\xa0", " ")
            self.page_attr[link] = loc_data

    # gets the name of the location which is the only constant similarity in structure between pages
    def get_loc_name(self, bs_obj):
        loc_name = bs_obj.find('h1', {'id': 'firstHeading'}).get_text().replace("(Skyrim)", "")\
            .replace("(Skyrim Location)", "").replace("(Location)", "").strip()
        return loc_name

    # gets the summary of the location which is usually the first paragraph in the main body, handles fringe cases
    # where it is not the first paragraph.
    def get_summary(self, bs_obj):
        # some times the first paragraph will have an 'aside' tag nested in it.
        # this will remove the aside tage leaving only the first paragraph
        if bs_obj.find('div', {'class': 'mw-parser-output'}).find('aside') is not None:
            bs_obj.find('div', {'class': 'mw-parser-output'}).find('aside').extract()
        # sets value of summary to text contained in first paragraph
        summary = bs_obj.find('div', {'class': 'mw-parser-output'}).find('p').get_text().strip()

        # handles cases where first paragraph is NOT the summary, if the first paragraph is not the summary
        # summary will always return an empty string. Allowing us to deduce that the summary is in the next
        # paragraph tag. It could be possible that it is not the second paragraph tag however running this program
        # many times never resulted in this, it was always the first or second paragraph tag.
        if summary == "":
            summary = bs_obj.find('div', {'class': 'mw-parser-output'}).find_all('p')[1].get_text().strip()

        return summary

    # will return the hold that the location belongs to. will attempt to handle the fringe cases where a hold is not
    # specified.
    def get_hold(self, bs_obj):
        holds = bs_obj.find_all('div', {"class": "pi-item pi-data pi-item-spacing pi-border-color"})

        # it is necessary to include this as sometimes a table is not given for the location
        if holds is not None:
            for hold in holds:
                # it is necessary to include the first conditional as sometimes the table will contain data that
                # does not have a corresponding h3 tag, such as a quote or link to another article.
                if hold.find('h3') is not None and hold.find('h3').get_text().strip() == "Hold":
                    # weird replaces as the formatting is not uniform for each page, this covers fringe cases and allows
                    # all data in hold fields to be formatted the same

                    if hold.find('div').get_text(separator=", ").strip().replace(" Hold", "").split(", ")[0] \
                            in self.hold_list:
                        # necessary to replace Hold as sometimes the hold is titled "x Hold"
                        return hold.find('div').get_text(separator=", ").strip().replace(" ,", "")\
                            .replace(",  Hold", "").replace(" Hold", "")

                    elif hold.find('div').get_text(separator=", ").strip().replace(" Hold", "").split(", ")[0] \
                            in self.city_list:
                        return self.hold_list[self.city_list.index(hold.find('div').get_text(separator=", ")
                                                                   .strip().replace(" ,", "").replace(",  Hold", "")
                                                                   .replace(" Hold", ""))]

        # these two loops will search the summary for an instance where either a hold or a city is specified

        # this loop will search for an instance of hold in the summary
        for hold_search in self.hold_list:
            if hold_search in bs_obj.find('div', {'class': 'mw-parser-output'}).find('p').get_text().strip():
                return hold_search

        #  this loop will search for instance of city being stated in the summary if the hold is not
        # if a city is found it will get the corresponding hold to the city
        for city_search in self.city_list:
            if city_search in bs_obj.find('div', {'class': 'mw-parser-output'}).find('p').get_text().strip():
                return self.hold_list[self.city_list.index(city_search)]

        # this will only happen if a hold is not located anywhere in the table or the summary
        # it still says to check the summary just in case it is located in a village or other location that implies
        # the hold it is located in
        return "Hold was not able to be found, summary might give some insight on the hold."

    # this returns a relative location in the world. some pages include a specific location such as
    # "in the southwest of skyrim", or specific location in a city if it is located in one on top of giving the hold.
    def get_loc(self, bs_obj):
        locs = bs_obj.find_all('div', {"class": "pi-item pi-data pi-item-spacing pi-border-color"})

        # it is necessary to include this as sometimes a table is not given for the location
        if locs is not None:
            for loc in locs:
                # it is necessary to include the first conditional as sometimes the table will contain data that
                # does not have a corresponding h3 tag, such as a quote or link to another article.
                if loc.find('h3') is not None and loc.find('h3').get_text().strip() == "Location":
                    return loc.find('div').get_text().strip()
        # often a lot of places dont have specific locations specified so this is for those cases
        return "No relative location is specified."

    def get_loc_type(self, bs_obj):
        loc_types = bs_obj.find_all('div', {"class": "pi-item pi-data pi-item-spacing pi-border-color"})

        # it is necessary to include this as sometimes a table is not given for the location
        if loc_types is not None:
            for loc_type in loc_types:
                # it is necessary to include the first conditional as sometimes the table will contain data that
                # does not have a corresponding h3 tag, such as a quote or link to another article.
                if loc_type.find('h3') is not None and loc_type.find('h3').get_text().strip() == "Type":
                    # this return statement includes a separator as sometimes there is multiple location types
                    # separated by a <br> tag.
                    # this conditional checks for a shop in the name as for some reason shop and the type of shop
                    # as well as legion and 's camps in the imperial camps are separated by a random whitespace,
                    # this conserves appropriate formatting
                    if "shop" in loc_type.find('div').get_text(separator=", ").strip().lower()\
                            or "legion" in loc_type.find('div').get_text(separator=", ").strip().lower():
                        return loc_type.find('div').get_text().strip().replace("shop", "Shop")
                    else:
                        # since pages are inconsistently formatted replace statements were utilized for uniformity also,
                        # occasionally there will be a weird whitespace character causing the separator to add a
                        # blankspace followed by a comma, this else statement covers these cases
                        return loc_type.find('div').get_text(separator=", ").strip().replace(" ,", "")\
                            .replace(",  ", "").replace("HouseRuin", "House, Ruin")\
                            .replace("/", ", ").replace("home", "Home").replace(" (Skyrim)", "")\
                            .replace(" (Solitude)", "").replace("Cave, , Barrow", "Cave, Barrow")

        # handles the fringe cases where no type is attributed to a location, this is rare but there are some pages that
        # dont include a type
        return "No location type is attributed to this location."

    # this method gets an attribute called 'LocationIDs' this is important in game as it is the games way of referencing
    # a location in game, this gets all IDs associated with a location and formats accordingly
    def get_loc_ids(self, bs_obj):
        loc_ids = bs_obj.select_one('td[data-source = "LocationID"]')
        if loc_ids is not None:
            return loc_ids.get_text(separator=", ").strip()
        return "This location has no associated Location ID(s)."

    # this method gets all the holds in locations and sums up how many locations are located in each hold
    # also iterates a field so we can get a total of hold occurrences
    def get_hold_summary(self):
        self.hold_sum = 0
        hold_summary = dict()
        for hold in self.hold_list:
            hold_summary[hold] = 0
        hold_summary["N/A"] = 0  # cases for when hold is not specified
        for key in self.page_attr:
            if self.page_attr[key]["Hold: "] != \
                    "Hold was not able to be found, summary might give some insight on the hold." \
                    and len(self.page_attr[key]["Hold: "].split(", ")) <= 1:
                hold_summary[self.page_attr[key]["Hold: "]] += 1
                self.hold_sum += 1

            # conditional for the fringe case where a location has more then one hold
            elif self.page_attr[key]["Hold: "] != \
                    "Hold was not able to be found, summary might give some insight on the hold." and \
                    len(self.page_attr[key]["Hold: "].split(", ")) > 1:
                for h in self.page_attr[key]["Hold: "].split(", "):
                    hold_summary[h] += 1
                    self.hold_sum += 1
            else:
                hold_summary["N/A"] += 1
                self.hold_sum += 1
        return hold_summary

    # this method gets all the location types and sums up how many location types there are in total
    # also iterates a field so we can get a total of location type occurrences
    def get_type_summary(self):
        self.type_sum = 0
        type_summary = dict()
        # populates a dictionary with all location types
        # only does this for existing links as to save space in console
        for key in self.page_attr:
            if self.page_attr[key]["Location Type: "] == "No location type is attributed to this location.":
                type_summary["N/A"] = 0
            elif len(self.page_attr[key]["Location Type: "].split(", ")) <= 1:
                type_summary[self.page_attr[key]["Location Type: "]] = 0
            else:
                for val in self.page_attr[key]["Location Type: "].split(", "):
                    type_summary[val] = 0

        # gets count of all location types
        # adds to N/A value if no type is specified
        for key in self.page_attr:
            if self.page_attr[key]["Location Type: "] == "No location type is attributed to this location.":
                type_summary["N/A"] += 1
                self.type_sum += 1
            # case if there is more then one type attributed to the location
            elif len(self.page_attr[key]["Location Type: "].split(", ")) <= 1:
                type_summary[self.page_attr[key]["Location Type: "]] += 1
                self.type_sum += 1
            # handles standard case of one none N/A type
            else:
                for val in self.page_attr[key]["Location Type: "].split(", "):
                    type_summary[val] += 1
                    self.type_sum += 1

        # returns a dictionary that has keys sorted alphabetically
        return OrderedDict(sorted(type_summary.items()))

    # attempts to dump all second level dictionaries to a .json file
    def dump_to_json(self):
        # attempts to dump to json file
        try:
            with open('data.json', 'w') as fp:
                json.dump(self.page_attr, fp, indent=4)
            fp.close()
        except json.JSONDecodeError:
            print("Error dumping to JSON file :(")
        else:
            # print("\nSuccessfully dumped " + str(self.sites_to_crawl) + " dictionaries to a JSON file!")
            pass


# main method to get user input and initialize an instance of the crawler class
def main():
    print("Welcome to the Skyrim Location Crawler!\n")
    # this loop gets user input and checks to make sure it is valid input.
    # only possible invalid input are integers that are too large but these are handled later
    # in the crawler class itself.
    while True:
        sites_crawl_amount = input("Please enter an integer value of the number of sites you would like to crawl to: ")
        try:
            sites_crawl_amount = int(sites_crawl_amount)
        except ValueError:
            print("Please enter an integer value.\n")
        else:
            if sites_crawl_amount < 1:
                print("Please enter a value of at least one.\n")
            else:
                print("Okay crawling " + str(sites_crawl_amount) + " pages!(Note: If entered value exceeds total"
                      + " number of pages, the program will default to the max number of pages.)\n")
                break
    crawler = Crawler("https://elderscrolls.fandom.com/wiki/Locations_(Skyrim)", sites_crawl_amount)


# checks if file is the main aka not imported, and will run the main method if it is.
if __name__ == "__main__":
    main()
