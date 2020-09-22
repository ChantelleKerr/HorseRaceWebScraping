import requests, bs4


class Results:
    def __init__(self, res):
        self.res = res
        self.rows = []
        self.dividend_list = []

    def select_data(self):
        race_soup = bs4.BeautifulSoup(self.res.text, "lxml")
        current_race = race_soup.find("span", {"id": "ctl00_ContentPlaceHolderMain_labelHeading"})
        global race_info
        race_info = current_race.text
        dividends = race_soup.find("td", {"id": "ctl00_ContentPlaceHolderMain_dividendCell"})
        global dividend_address
        dividend_address = dividends.find("a").get("href")

        table = race_soup.find("table", {"class": "tblcris tbldata"})

        for row in table.findAll("tr"):
            current_row = []
            # Grab the table headers
            for th_txt in row.findAll('th', {"scope": "col"}):
                current_row.append(th_txt.text)
            for td_txt in row.findAll('td'):
                stripped_txt = td_txt.text.strip()
                current_row.append(stripped_txt)
            if current_row:
                self.rows.append(current_row)

    def clean_data(self):
        # Remove any row that is SCRATCHED
        self.rows[:] = [row for row in self.rows if "SCRATCHED" not in row]
        # Remove the list items we aren't using
        self.rows.pop(1)  # Remove the last item in list as we don't need it
        for row in self.rows:
            # If the list contains the header info
            if len(row) == 10:
                columns_to_remove = [3, 7, 8, 9]
                # Remove the headers we as not using
                for column in sorted(columns_to_remove, reverse=True):
                    del row[column]
            # contains race info
            else:
                columns_to_remove = [3, 5, 6, 9, 10, 11, 12, 13, 14]
                # Remove the columns we as not using
                for column in sorted(columns_to_remove, reverse=True):
                    del row[column]

    def win_place_info(self):
        res = requests.get(dividend_address)
        win_soup = bs4.BeautifulSoup(res.text, "lxml")
        win = win_soup.select('#race-results > tbody > tr:nth-child(1) > td:nth-child(8) > strong')
        place = win_soup.select('#race-results > tbody > tr:nth-child(1) > td:nth-child(9) > strong')
        for r in win:
            self.dividend_list.append(r.text)
        for r in place:
            self.dividend_list.append(r.text)

    def display_info(self):
        print(" ")
        print(race_info)
        print("-----> Win: ", self.dividend_list[0], "Place:", self.dividend_list[1])
        # Print the rows
        for row in self.rows:
            frmt = "{:<25}" * len(row)
            print(frmt.format(*row))

    def main(self):
        self.select_data()
        self.clean_data()
        self.win_place_info()
        self.display_info()
