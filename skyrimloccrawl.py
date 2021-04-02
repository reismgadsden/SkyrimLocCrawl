"""
SKYRIM LOCATION CRAWLER GUI

This program will take data collected in a scrape from the locations on the Elder Scrolls Wiki page for Skyrim and
build a GUI that creates a more user friendly, navigable format for the idea. It allows varies functions including:
- Displaying random locations
- Displaying hold and type data summaries for all info gathered
- Creating a .json file from the info

@author: Reis Gadsden
@version: v1.1.0

GitHub: https://github.com/reismgadsden

Necessary import for full project:
-bs4.BeautifulSoup
-urllib.robotparser.RobotFileParser
-pip._vendor.requests
-random.*
-json.*
-collections.OrderedDict
-webbrowser.*
-tkinter.font
-tkinter.ttk.*
-tkinter.tix.**
-subprocess.*
"""

# needed imports
import time
import webbrowser
from tkinter import font
from tkinter.ttk import *
from tkinter.tix import *
import project_one_reis_gadsden
import random
import subprocess
import threading


# class that builds root window and contains all logic to build following windows
class SkyrimLocGUI:
    # values that are needed in entire class scope (initializing here to suppress soft warnings)
    page_attr = ""
    dumped = False
    crawler = ""
    e1var = ""
    s1var = ""
    s2var = ""
    s3var = ""
    s4var = ""
    s5var = ""
    json_var = ""
    search_label1 = ""
    search_label2 = ""
    search_label3 = ""
    search_label4 = ""
    search_label5 = ""

    # creates starting window upon initial class call
    def __init__(self):
        # builds main window
        self.master = Tk()
        self.frame = Frame(width=1280, height=720)
        self.frame.pack()

        # allows for scrolling in case of overflowing (pretty much only happens on type summary, and view all page)
        swin = ScrolledWindow(self.frame, width=1280, height=720)
        swin.pack()
        self.win = swin.window

        # builds main elements of starting page
        label = Label(self.win, text="Welcome to the Skyrim Location Crawler!", font=50)
        label.pack(side=TOP, pady=10)
        label2 = Label(self.win,
                       text="Please enter an integer value of the number of sites you would like to crawl to")
        label2.pack(side=TOP)

        number_to_crawl = Entry(self.win, width=52)  # entry for amount to crawl
        number_to_crawl.pack(side=TOP, pady=10)
        btn = Button(self.win, text="Crawl!")
        btn.pack(pady=10)
        btn.bind("<Button>", lambda b: self.start_crawl(number_to_crawl.get()))
        self.master.title("Skyrim Location Scraper")
        self.input_error_var = StringVar()
        self.input_error_var.set("")
        self.error_label = Label(self.win, textvariable=self.input_error_var)
        self.error_label.pack()
        self.pgf = font.Font(size=10)
        self.progname_label = Label(self.win, text="Skyrim Location Scraper", font=self.pgf, foreground="#828282")
        self.progname_label.pack()
        self.nf = font.Font(size=10)
        self.name_label = Label(self.win, text="Reis Gadsden - 2021", font=self.nf, foreground="#828282")
        self.name_label.pack()
        self.git_label = Label(self.win, text="GitHub - reismgadsden", foreground="#8282ee")
        self.gitf = font.Font(self.git_label, self.git_label.cget('font'))
        self.gitf.configure(underline=True, size=10)
        self.git_label.configure(font=self.gitf)
        self.git_label.pack()
        self.git_label.bind('<Button-1>', lambda e: webbrowser.open_new_tab("https://github.com/reismgadsden"))

    # validates input for crawl amount
    def start_crawl(self, num_crawl):
        try:
            sites_crawl_amount = int(num_crawl)
        except ValueError:
            self.input_error_var.set("Please enter an integer value.")
            self.win.update()
        else:
            if sites_crawl_amount < 1:
                self.input_error_var.set("Please enter a value of at least one.")
                self.win.update()
            else:
                threading.Thread(target=self.init_crawl, args=(sites_crawl_amount,)).start()
                self.load_crawl(sites_crawl_amount)

    # allows for a loading page during crawl
    def load_crawl(self, num_sites):
        # clears frame
        for child in self.win.winfo_children():
            child.destroy()
        # sets value to max amount
        if num_sites > 562:
            crawl_site = 562
        else:
            crawl_site = num_sites

        # cute loading message
        loadvar = StringVar()
        loadvar.set("")
        waitvar = StringVar()
        waitvar.set("Loading " + str(crawl_site) + " Site(s) from https://elderscrolls.fandom.com"
                                                   "/wiki/Locations_(Skyrim) (this may take a minute "
                                                   "or two)" + loadvar.get())
        label = Label(self.win, textvariable=waitvar)
        label.pack(side=TOP, pady=10)

        i = 0
        loadmessagevar = StringVar()
        loadmessagevar.set("")
        loadmessagelabel = Label(self.win, textvariable=loadmessagevar)
        loadmessagelabel.pack(pady=10)
        loadingmessages = ["Oh man this is taking a while, but I promise it is loading :)",
                           "Damn bro how many locations did you ask for?",
                           "Great things come to those who wait :)",
                           "I promise I am loading I am just trying to be respectful and not overload the servers :(",
                           "( ͡° ͜ʖ ͡°)", "One day I will load...",
                           "If you asked for or more than 562 you are going to be here for a few minutes lol.",
                           "Veuillez patienter, merci beaucoup.",
                           "While you wait check this out this link ahku.portfoliobox.net",
                           "Here, while you wait reddit.com"]
        while True:
            if self.page_attr == "":
                time.sleep(0.25)
                loadvar.set("."*(i % 4))
                waitvar.set("Loading " + str(crawl_site) + " Site(s) from https://elderscrolls.fandom.com"
                                                           "/wiki/Locations_(Skyrim) (this may take a minute "
                                                           "or two)" + loadvar.get())
                i += 1
                self.win.update()
                if i % 25 == 0:
                    loadmessagevar.set(random.choice(loadingmessages))
                    loadmessagelabel.unbind("<Button-1>")
                    if "ahku.portfoliobox.net" in loadmessagevar.get():
                        loadmessagelabel.bind("<Button-1>", lambda e: webbrowser.open_new_tab("https://ahku.portfoliobox.net/"))
                    elif "reddit.com" in loadmessagevar.get():
                        loadmessagelabel.bind("<Button-1>",
                                              lambda e: webbrowser.open_new_tab("https://www.reddit.com/"))
                    if i % 50 == 0:
                        loadmessagevar.set("")
            else:
                break

    # initializes the actual crawl of websites and pushes data to page_attr to be used else where
    # also loads up the main start page
    def init_crawl(self, num_sites):
        self.crawler = project_one_reis_gadsden.Crawler(
            "https://elderscrolls.fandom.com/wiki/Locations_(Skyrim)", num_sites)
        self.page_attr = self.crawler.page_attr
        self.start_page()

    # main page for program, this page includes some important labels such as
    # reactive search
    # list of all locations crawled
    # hold distribution
    # type distribution
    # hold reference table
    # Option for creating and viewing json
    # A concrete way to exit
    def start_page(self):
        for child in self.win.winfo_children():
            child.destroy()

        # Entry to search that will dynamically update a StringVar in order to give reactive searching
        label = Label(self.win, text="Search for locations here!")
        label.pack()
        self.e1var = StringVar()
        self.e1var.trace('w', self.reactive_search)
        search_entry = Entry(self.win, width=52, textvariable=self.e1var)
        search_entry.pack(pady=10)

        # Place holders for search results
        self.s1var = StringVar()
        self.s1var.set("")
        self.search_label1 = Label(self.win, textvariable=self.s1var)
        self.search_label1.pack(pady=10)

        self.s2var = StringVar()
        self.s2var.set("")
        self.search_label2 = Label(self.win, textvariable=self.s2var)
        self.search_label2.pack(pady=10)

        self.s3var = StringVar()
        self.s3var.set("")
        self.search_label3 = Label(self.win, textvariable=self.s3var)
        self.search_label3.pack(pady=10)

        self.s4var = StringVar()
        self.s4var.set("")
        self.search_label4 = Label(self.win, textvariable=self.s4var)
        self.search_label4.pack(pady=10)

        self.s5var = StringVar()
        self.s5var.set("")
        self.search_label5 = Label(self.win, textvariable=self.s5var)
        self.search_label5.pack(pady=10)

        # Labels that lead to functions
        all_label = Label(self.win, text="Check out all locations!", foreground="#0000ee", font='Verdana 11 underline')
        all_label.pack(pady=10)
        all_label.bind('<Button-1>', lambda e: self.view_all_results())

        random_label = Label(self.win, text="Check out a random location!", foreground="#0000ee",
                             font='Verdana 11 underline')

        random_label.pack(pady=10)
        random_label.bind('<Button-1>', lambda e: self.display_results(random.choice(list(self.page_attr.values())), 3))

        hold_sum_label = Label(self.win, text="Check out the distributions of locations in each hold!",
                               foreground="#0000ee", font='Verdana 11 underline')
        hold_sum_label.pack(pady=10)
        hold_sum_label.bind('<Button-1>', lambda e: self.render_hold_sum())

        type_sum_label = Label(self.win, text="Check out the distributions of the types of locations!",
                               foreground="#0000ee", font='Verdana 11 underline')
        type_sum_label.pack(pady=10)
        type_sum_label.bind('<Button-1>', lambda e: self.render_type_sum())

        hold_label = Label(self.win, text="Check out the handy hold reference table!",
                           foreground="#0000ee", font='Verdana 11 underline')
        hold_label.pack(pady=10)
        hold_label.bind('<Button-1>', lambda e: self.render_holds())

        json_label = Label(self.win, text="View JSON", font='Verdana 11 underline', foreground="#0000ee")
        json_label.pack(pady=10)
        json_label.bind('<Button-1>', lambda e: self.json_run())

        # Place holder variable for json dump label
        self.json_var = StringVar()
        self.json_var.set("")
        dump_label = Label(self.win, textvariable=self.json_var)
        dump_label.pack(pady=10)

        quit_label = Label(self.win, text="Exit Skyrim Location Scraper", font='Verdana 11 underline',
                           foreground="#0000ee")
        quit_label.pack(pady=20)
        quit_label.bind('<Button-1>', lambda e: self.quit())

    # shows reactive searching and will get and display 5 locations that match the string currently in the entry box
    def reactive_search(self, a, b, c):
        search_results = self.search_results(self.e1var.get().lower().strip())

        # conditional statements for reactive searching
        if search_results[0] == "":  # handles case where a non matched string is in entry box
            self.s1var.set("No results for your query!")
            self.s2var.set("")
            self.s3var.set("")
            self.s4var.set("")
            self.s5var.set("")
            f1 = font.Font(self.search_label1, self.search_label1.cget("font"))
            f1.configure(size=12, underline=False)
            self.search_label1.configure(font=f1, foreground="#000000")
            self.win.update()

        elif self.e1var.get() == "":  # handles case where nothing is in entry box
            self.s1var.set("")
            self.s2var.set("")
            self.s3var.set("")
            self.s4var.set("")
            self.s5var.set("")
            self.win.update()

        # handles matching cases for reactive search
        else:
            self.s1var.set("")
            self.s2var.set("")
            self.s3var.set("")
            self.s4var.set("")
            self.s5var.set("")

            self.s1var.set(search_results[0]["Location Name: "])
            f1 = font.Font(self.search_label1, self.search_label1.cget("font"))
            f1.configure(underline=True, size=12)
            self.search_label1.configure(font=f1, foreground="#0000ee")
            self.search_label1.bind('<Button-1>', lambda e: self.display_results(search_results[0], 1))

            if search_results[1] != "":
                self.s2var.set(search_results[1]["Location Name: "])
                f2 = font.Font(self.search_label2, self.search_label2.cget("font"))
                f2.configure(underline=True, size=12)
                self.search_label2.configure(font=f2, foreground="#0000ee")
                self.search_label2.bind('<Button-1>', lambda e: self.display_results(search_results[1], 1))

            if search_results[2] != "":
                self.s3var.set(search_results[2]["Location Name: "])
                f3 = font.Font(self.search_label3, self.search_label3.cget("font"))
                f3.configure(underline=True, size=12)
                self.search_label3.configure(font=f3, foreground="#0000ee")
                self.search_label3.bind('<Button-1>', lambda e: self.display_results(search_results[2], 1))

            if search_results[3] != "":
                self.s4var.set(search_results[3]["Location Name: "])
                f4 = font.Font(self.search_label4, self.search_label3.cget("font"))
                f4.configure(underline=True, size=12)
                self.search_label4.configure(font=f4, foreground="#0000ee")
                self.search_label4.bind('<Button-1>', lambda e: self.display_results(search_results[3], 1))

            if search_results[4] != "":
                self.s5var.set(search_results[4]["Location Name: "])
                f5 = font.Font(self.search_label5, self.search_label3.cget("font"))
                f5.configure(underline=True, size=12)
                self.search_label5.configure(font=f5, foreground="#0000ee")
                self.search_label5.bind('<Button-1>', lambda e: self.display_results(search_results[4], 1))

            self.win.update()  # updates the window to load searches

    # main logic for handling the searches
    # return all matching results, blank results if no matches, blank results if matches is less then 5 to fill up
    # remaining indexes
    def search_results(self, chars):
        # array for holding all results
        results = []

        # variable i makes sure that search does not extend past 5
        i = 0

        # variable j makes sure that search does not extend past end of list
        j = 0

        # loop to populate results with at most 5 matches
        while i < 4 and j < len(self.page_attr):
            for key in self.page_attr:
                if chars == self.page_attr[key]["Location Name: "][0:len(chars)].lower() and \
                        self.page_attr[key] not in results:
                    results.append(self.page_attr[key])
                    i += 1
                j += 1

        # Fills unused list spots with blank string as to ensure len(results) is always 5
        x = 5 - len(results)
        while x > 0:
            results.append("")
            x -= 1
        return results

    # clears frame and shows the attributes of the selected location
    # takes a directed_from_search argument in order to tell how it got there, important for viewing all results
    # and for coming from random results
    def display_results(self, val, directed_from):
        # clear frame of all elements
        for child in self.win.winfo_children():
            child.destroy()

        # loops through page_attrs in order to build page for location
        for key, value in self.page_attr.items():
            if val == value:
                label_url = Label(self.win, text="Learn more here: " + key, foreground="#0000ee", font='Verdana 11 '
                                                                                                       'underline')
                label_url.pack(pady=10)
                label_url.bind('<Button-1>', lambda e: webbrowser.open_new_tab(key))

                label_name = Label(self.win, text="Location Name: " + self.page_attr[key]["Location Name: "], font=25)
                label_name.pack(pady=10)

                label_type = Label(self.win, text="Location Type: " + self.page_attr[key]["Location Type: "], font=25)
                label_type.pack(pady=10)

                label_hold = Label(self.win, text="Hold: " + self.page_attr[key]["Hold: "], font=25)
                label_hold.pack(pady=10)

                label_rel_loc = Label(self.win,
                                      text="Relative Location: " + self.page_attr[key]["Relative Location: "], font=25)
                label_rel_loc.pack(pady=10)

                label_loc_id = Label(self.win, text="Location ID(s): " + self.page_attr[key]["Location ID(s): "],
                                     wraplength=500, justify=CENTER, font=25)
                label_loc_id.pack(pady=10)

                label_sum = Label(self.win, text="Summary: " + self.page_attr[key]["Summary: "], wraplength=500,
                                  justify=CENTER, font=25)
                label_sum.pack(pady=10)

                # case 1 - came here from reactive search
                # case 2 - came here from "View All" page
                # case 3 - came here from random location page

                # came here from search page will only allow user to go back to search page
                if directed_from == 1:
                    label_back = Label(self.win, text="Search some more!", foreground="#0000ee",
                                       font='Verdana 11 underline')
                    label_back.pack(pady=10)
                    label_back.bind('<Button-1>', lambda e: self.start_page())

                # came here from view all page will only allow user to go back to view all page
                elif directed_from == 2:
                    label_back = Label(self.win, text="Go back to all results!", foreground="#0000ee", font='Verdana '
                                                                                                            '11 '
                                                                                                            'underline')
                    label_back.pack(pady=10)
                    label_back.bind('<Button-1>', lambda e: self.view_all_results())

                # random location page results, will allow user to go to another random results or go back to search
                else:
                    label_back = Label(self.win, text="View another random!", foreground="#0000ee",
                                       font='Verdana 11 underline')
                    label_back.pack(pady=10)
                    label_back.bind('<ButtonRelease-1>',
                                    lambda e: self.display_results(random.choice(list(self.page_attr.values())), 3))

                    label_go_back = Label(self.win, text="Go back to search!", foreground="#0000ee",
                                          font='Verdana 11 underline')
                    label_go_back.pack(pady=10)
                    label_go_back.bind('<Button-1>', lambda e: self.start_page())

    # builds a page that contain links to all locations that were crawled
    def view_all_results(self):
        # clear all elements from frame
        for child in self.win.winfo_children():
            child.destroy()

        # Header
        top_label = Label(self.win, text="All Locations Crawled")
        tl = font.Font(top_label, top_label.cget("font"))
        tl.configure(size=18)
        top_label.configure(font=tl)
        top_label.pack(pady=10)

        # contains all labels created
        labels = []

        # contains location created
        locations = []

        # variable i is used to be able to pair up indexes of labels and locations list
        i = 0

        # loop that procedurally generates labels and binds them to location
        for key in self.page_attr:
            locations.append(self.page_attr[key])
            labels.append(Label(self.win, text=self.page_attr[key]["Location Name: "], foreground="#0000ee",
                                font='Verdana 11 underline'))
            labels[i].bind("<Button-1>", lambda e, index=i: self.display_results(locations[index], 2))
            labels[i].pack()
            i += 1

        label_back = Label(self.win, text="Go back to search!", foreground="#0000ee", font='Verdana 11 underline')
        label_back.pack(pady=10)
        label_back.bind('<Button-1>', lambda e: self.start_page())

    # renders the hold reference table
    def render_holds(self):
        # clear elements in frame
        for child in self.win.winfo_children():
            child.destroy()

        # formatted output from hold info gathered during crawl (format is still a mess but readable)
        output = '{0:<20}\t{1:<20}\t{2:<20}\n\n'.format("Hold", "Capital City", "Jarl")
        for hold in self.crawler.hold_list:
            output += '{0:<20}\t{1:<20}\t{2:<20}\n' \
                .format(hold, self.crawler.city_list[self.crawler.hold_list.index(hold)],
                        self.crawler.jarl_list[self.crawler.hold_list.index(hold)])

        hold_label = Label(self.win, text=output, font=25)
        hold_label.pack()

        label_back = Label(self.win, text="Back to search", foreground="#0000ee", font='Verdana 11 underline')
        label_back.pack(pady=10)
        label_back.bind('<Button-1>', lambda e: self.start_page())

    # renders the hold summary table
    def render_hold_sum(self):
        # clear elements from frame
        for child in self.win.winfo_children():
            child.destroy()

        # formatted output for hold summary (surprisingly okay formatting considering the other table)
        hold_sum = self.crawler.get_hold_summary()
        output = "{0:<35}\t{1:<20}{2:>32}\n\n".format("Type", "Occurrences", "Percentage of Total Occurrences")
        for key in hold_sum:
            output += '{0:<35}\t{1:<20}{2:>32}\n'.format(key, hold_sum[key],
                                                         str((hold_sum[key] / self.crawler.hold_sum) * 100) + "%")
        hold_sum_label = Label(self.win, text=output, font=25)
        hold_sum_label.pack()

        label_back = Label(self.win, text="Back to search", foreground="#0000ee", font='Verdana 11 underline')
        label_back.pack(pady=10)
        label_back.bind('<Button-1>', lambda e: self.start_page())

    # renders the type summary page
    def render_type_sum(self):
        # clear all elements in frame
        for child in self.win.winfo_children():
            child.destroy()

        # formatted output for type summary (this was literally the best i got it to look, but it still looks awful)
        type_sum = self.crawler.get_type_summary()
        output = "{0:<50}\t{1:<20}{2:>18}\n\n".format("Type", "Occurrences", "Percentage of Total Occurrences")
        for key in type_sum:
            output += "{0:<50}\t\t{1:<20}{2:>18}\n".format(key, type_sum[key],
                                                           str((type_sum[key] / self.crawler.type_sum) * 100) + "%")

        tslf = font.Font(size=12)
        type_sum_label = Label(self.win, text=output, font=tslf)
        type_sum_label.pack()

        label_back = Label(self.win, text="Back to search", foreground="#0000ee", font='Verdana 11 underline')
        label_back.pack(pady=10)
        label_back.bind('<Button-1>', lambda e: self.start_page())

    # will dump a file to json if has not already, and open up a file explorer window to the json file
    # note: not sure if this works on OSs other then Windows
    def json_run(self):
        if not self.dumped:
            self.crawler.dump_to_json()
            subprocess.Popen(r'explorer /select, ".\data.json"')
            self.json_var.set("Successfully outputted data to .json file!")
            self.win.update()
            self.dumped = True
        else:
            subprocess.Popen(r'explorer /select, ".\data.json"')
            self.json_var.set("")
            self.win.update()

    # quits the program but displays a goodbye message before closing
    def quit(self):
        for child in self.win.winfo_children():
            child.destroy()

        goodbye = Label(self.win, text="Goodbye!\nThank you for using the Skyrim Location Scraper!",
                        font="Verdana 30", justify=CENTER)
        goodbye.pack()
        self.master.after(2000, self.master.destroy)


# main executions
def main():
    SkyrimLocGUI()
    mainloop()


# will execute the file if it is not being imported and run elsewhere
if __name__ == "__main__":
    main()
