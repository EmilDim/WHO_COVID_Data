# %%
import numpy as np
import requests
import io
import re
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileReader
from datetime import datetime
from datetime import timedelta
#import urllib3
from urllib.request import urlopen
import matplotlib.pyplot as plt

# %%
def find_files(url):

    r = requests.get(url)
    response = urlopen(url).read()
    soup = BeautifulSoup(response, "html.parser")
    links = soup.find_all('a', href=re.compile(r'(.pdf)'))

    files = []
    for i in links:
        files.append('https://www.who.int' + i['href'])
        
    return(files)

def extract_cases(url, country):
    print('Scraping '+url)
    # Scrape page for file
    r = requests.get(url)
    
    f = io.BytesIO(r.content)
    reader = PdfFileReader(f)

    for page in range(reader.numPages+1):
        contents = reader.getPage(page).extractText().split('\n')
        if country in contents:
            break

    # Get total confirmed new cases    
    cases = contents[contents.index('Brazil')+4]

    return(cases)

# %%

url = "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/"

country = 'Brazil'

files = find_files(url)
files
get_latest = 20

files = files[:20][::-1]
cases = []
for file in files:
    cases.append(extract_cases(url=file, country=country))
cases = [int(i) for i in cases]  
# %%
# Plot
dates = []
for date in np.arange(1,get_latest+1):
    dates.append((datetime.today() - timedelta(days=int(date))).strftime('%b-%d'))
dates=dates[::-1]
# Estimate 7 day average
avgs = [0,]*7
for case in cases[7:]:
    avgs.append(np.mean(cases[cases.index(case)-7:cases.index(case)]))

fig, ax = plt.subplots(figsize=(12,7))
ax.tick_params(axis='both',labelsize=16)
ax.set_xticklabels(dates, rotation=45)
ax.set_ylabel('New cases', fontsize=16)
ax.plot(dates,cases, 'o-', lw=4, markersize=10, label='cases')
ax.plot(avgs, lw =4, label='7-day avg')
ax.legend(loc='best', fontsize=16)
ax.set_title('Daily New Cases in Brazil', fontsize=18)
plt.show()
