# example links
# "https://cris.rwwa.com.au/racefield.aspx?meeting=5159209&race=1"
# "https://cris.rwwa.com.au/racefield.aspx?meeting=5162274&race=7"

import sys, requests
from RacePackage.starters import Starters
from RacePackage.results import Results


def get_address():
    """ Gets the address from the command line"""
    if len(sys.argv) > 1:
        # Get address from command line.
        address = ' '.join(sys.argv[1:])
    response = requests.get(address)
    return response


if __name__ == '__main__':
    res = get_address()
    if res.status_code == 200:
        starters = Starters(res)
        starters.main()
        resultsAddress = starters.find_results_page()
        if(resultsAddress is not None):
            newRes = requests.get(resultsAddress)
            if newRes.status_code == 200:
               results = Results(newRes)
               results.main()
        else:
            print(" ")
            print("Race results are not available yet, try again later!")