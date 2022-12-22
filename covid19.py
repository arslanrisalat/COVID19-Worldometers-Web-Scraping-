from bs4 import BeautifulSoup
import requests
import csv

#URL worldometers
def worldwide():
    BASEURL = 'https://www.worldometers.info/coronavirus/'
    source = requests.get(BASEURL).text
    soup = BeautifulSoup(source,'html.parser')
    world=[]
    for i in range(0,3):
        h1 = soup.select("h1")[i].getText().strip()
        data = soup.select("#maincounter-wrap span")[i].getText().strip()
        world.append(f"{h1} : {data}")
    print(world)
    table = soup.find('table',id="main_table_countries_today")
    table_header = table.find('thead').find_all('th')
    with open('results.csv','w',newline='') as f:
        writer = csv.writer(f)
        header = []
        new_list = []

        for th in table_header:
            header.append(th.text)

        for element in header:
            new_list.append(element.strip())

        #remove all new lines / weird unicode chars
        for i,data in enumerate(new_list):
            new_list[i] = data.replace('\xa0', ' ')
            new_list[i] = data.replace('\n',' ')

        writer.writerow(new_list)

        #go through each row in the table
        for row in table.find_all('tr'):

            csvRow = []

            #get the data and add it to the list
            for data in row.find_all('td'):
                csvRow.append(data.text)
            
            #remove all \n from the data
            for i in range(len(csvRow)):
                csvRow[i] = csvRow[i].replace('\n','')

            writer.writerow(csvRow)

    f.close()

worldwide()