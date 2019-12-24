import csv
from selenium import webdriver
import os
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys



# search name extracted from list in outputs.csv and scrape data associated with search
def search(name, driver):

    # if press and hold exists press & hold, else continue
    driver.find_element_by_css_selector('input[class^="mat-primary"]').clear()
    sleep(3)

    input_search = driver.find_element_by_css_selector('input[class^="mat-primary"]')

    # if data from outputs.csv is denominated by US character, continue
    # if not write error into error.csv
    try:
        input_search.send_keys('{}'.format(name))
        sleep(3.5)
    except UnicodeDecodeError:
        csvm.writerow([name, 'Non-English Characters'])
        print('Non-English Characters')
        return

    # send keys from output.csv
    input_search.send_keys(Keys.RETURN)
    sleep(2)

    # if name search leads to multiple outcomes search by name and company name
    results_length = len(driver.find_elements_by_css_selector('grid-row[class^=ng-star-inserted]'))

    # if multiple profiles are correlated with the same search key,
    # then write 'multiple profiles' into error.csv
    if results_length > 1:
        print('results > 1')
        csvm.writerow([name, 'Multiple Profiles'])
        return

    # try to click element associated with a profile, if not
    # write 'No profile' into noprofile.csv
    try:
        driver.find_element_by_css_selector('div[class^=flex-no-grow]').click()

        # if 'Investor' is present on the page write 'Investor' into investor.csv
        title = driver.find_element_by_css_selector("div[class*='last'][class*='ng-star-inserted']").text
        if '(Investor)' in title:
            i = 'Investor'
            print('Investor')
            sleep(2)

            # write rank associated with name into investor.csv
            rankdiv = driver.find_element_by_css_selector("div[class*='last'][class*='ng-star-inserted']" )
            rank = rankdiv.find_element_by_css_selector( "a[class^='cb-link']" ).text
            print(rank)

            csvi.writerow([name, i, rank])

        # if 'Investor' is not present, write 'Person' into persons.csv
        else:
            p = 'Person'
            print('Person')
            sleep(2)

            # write rank associated with name into persons.csv
            rankdiv = driver.find_element_by_css_selector("div[class*='last'][class*='ng-star-inserted']")
            rank = rankdiv.find_element_by_css_selector("a[class^='cb-link']").text
            print(rank)

            csvp.writerow([name, p, rank])

    except NoSuchElementException:
        print('No Profile')
        csvno.writerow([name])
        return False
    


# boiler plate code for csv files
csv.register_dialect('unixpwd', delimiter=':', quoting=csv.QUOTE_NONE)
fieldnames = ['Name', 'CB Type', 'CB Rank']

icsvfile = open('investor.csv', 'a')
csvi = csv.writer(icsvfile)

# if file is empty write header**
file_is_empty = os.stat('investor.csv').st_size == 0
if file_is_empty:
    csvi.writerow(fieldnames)

pcsvfile = open('persons.csv', 'a')
csvp = csv.writer(pcsvfile)

# **
file_is_empty = os.stat('persons.csv').st_size == 0
if file_is_empty:
    csvp.writerow(fieldnames)

ncsvfile = open('noprofile.csv', 'a')
csvno = csv.writer(ncsvfile)

# **
file_is_empty = os.stat('noprofile.csv').st_size == 0
if file_is_empty:
    csvno.writerow('Name')

mcsvfile = open('error.csv', 'a')
csvm = csv.writer(mcsvfile)

#**
file_is_empty = os.stat('error.csv').st_size == 0
if file_is_empty:
    csvm.writerow(['Name', 'Error'])

driver = webdriver.Chrome('/Users/danielcovelli/Documents/Python/linkedin_scraper_tut/chromedriver' )
driver.get('https://www.crunchbase.com')

# skip first row and begin searching names starting at second row
with open('outputs2.csv') as h:
    reader = csv.reader(h)
    i = 0
    for row in reader:
        if i == 0:
            i += 1
            continue
        else:
            print(row[0])
            search(row[0], driver)

icsvfile.close()
pcsvfile.close()
ncsvfile.close()

print('done')

