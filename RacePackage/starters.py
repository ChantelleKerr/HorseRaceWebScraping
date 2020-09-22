import bs4

class Starters:
    def __init__(self, res):
        self.res = res
        self.rows = []

    def select_data(self):
        """ Selects data from the race page """
        race_soup = bs4.BeautifulSoup(self.res.text, "lxml")
        current_race = race_soup.find("span", {"id": "ctl00_ContentPlaceHolderMain_labelHeading"})
        global race_info
        race_info = current_race.text
        table = race_soup.find("table", {"class": "tblcris raceField"})
        # Selects table rows
        for row in table.findAll("tr"):
            current_row = []
            # Grab the table headers
            for th_txt in row.findAll('th', {"scope": "col"}):
                current_row.append(th_txt.text)
            # Grab the table data
            for td_txt in row.findAll('td'):
                stripped_txt = td_txt.text.strip()
                current_row.append(stripped_txt)
            if current_row:
                self.rows.append(current_row)

        # Finds the link that brings up the results page
        try:
            race_results = race_soup.findAll("a", {"id": "ctl00_ContentPlaceHolderMain_hyperLinkRaceResults"})
            global results_address
            for id in race_results:
                results_address = id['href']
            results_address = "https://cris.rwwa.com.au/" + results_address
        except:
            results_address = None

    def clean_data(self):
        """ Removes rows and columns that are not needed from race page """
        # Remove any row that is SCRATCHED
        self.rows[:] = [row for row in self.rows if "SCRATCHED" not in row]
        # Remove the list items we aren't using
        self.rows.pop()  # Remove the last item in list
        for row in self.rows:
            split_string = row[10].split("$", 2)
            if len(split_string) >= 3:
                row[10] = split_string[1]
            # Remove the columns we aren't using
            columns_to_remove = [0, 3, 4, 6, 7]
            for column in sorted(columns_to_remove, reverse=True):
                del row[column]

    def display_info(self):
        """ Displays race information"""
        print(" ")
        print(race_info)
        # Print the rows
        for row in self.rows:
            print("{:<4} {:<25} {:<4} {:<25} {:<25} {:<5}".format(row[0], row[1], row[2], row[3], row[4], row[5]))

    def find_results_page(self):
        return results_address

    def main(self):
        self.select_data()
        self.clean_data()
        self.display_info()

