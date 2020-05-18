from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

url = 'https://report.boonecountymo.org/mrcjava/servlet/RMS01_MP.R00040s?run=2&R001=&R002=&ID=3641&hover_redir=&width=950'

r = requests.get(url, headers = {'user-agent':'Mozilla/5.0'})

html = r.content

soup = BeautifulSoup(html)

mugshots = soup.find_all('div', class_ = 'mugshotDiv')

info_rows = []
for mugshot in mugshots:
    id_number = mugshot.attrs['id']
    dic = {"id" : id_number}
    info = mugshot.find('div', attrs = {'class' : 'infoContainer'})
    for tr in info.find_all('tr'):
        tds = tr.find_all('td')
        key = tds[0].text.strip()
        value = tds[1].text.strip()
        dic[key] = value
    info_rows.append(dic)

pd.DataFrame(info_rows).to_csv('inmate_info.csv', index = False)

charges_rows = []
for mugshot in mugshots:
    charges = mugshot.find('div', attrs = {'class' : 'chargesContainer'})
    charges_tbody = charges.find('tbody')
    for tr in charges_tbody.find_all('tr'):
        id_number = mugshot.attrs['id']
        list_of_cells = []
        list_of_cells.append(id_number)
        charges_rows.append(list_of_cells)
        for td in tr.find_all('td', attrs = {'class' : 'two td_left'}):
            text = td.text.replace('&nbsp;', '')
            list_of_cells.append(text)

outfile = open("./charges.csv", "w")
writer = csv.writer(outfile)
writer.writerow(["id", "case_number", "charge_description", "charge_status", "bail_amount", "bond_type", "court_date", "court_time", "court_of_jurisdiction"])
writer.writerows(charges_rows)
