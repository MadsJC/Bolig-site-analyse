from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np
import time


print('Starting script...')

csv_file_name = 'real_12_chrome.csv'

with open(csv_file_name, 'w') as f:
    f.write('ids; titel; addresse; oprettelsesdato; depositum; boligtype; etage; møbleret; delevenlig; husdyr; lejeperiode; overtagelsesdato; månedlig_leje; aconto; status; image_count \n')


def write_to_file(ids, titel, addresse, oprettelsesdato, depositum, boligtype, etage, møbleret, delevenlig, husdyr, lejeperiode,
                  overtagelsesdato, månedlig_leje, aconto, status, image_count):
    with open(csv_file_name, 'a') as f:
        f.write(str(ids) + ";" + titel + ";" + addresse + ";" + oprettelsesdato +
                ";" + depositum + ";" + boligtype + ";" + etage + ";" + møbleret +
                ";" + delevenlig + ";" + husdyr +
                ";" + lejeperiode + ";" + overtagelsesdato +
                ";" + månedlig_leje + ";" + aconto + ";" + status + ";" + image_count + "\n")


id_list = range(5911380, 5932015)
for_lang_loading_tid = 0
ids_404 = 0


options = Options()
options.headless = True

browser = webdriver.Chrome(options=options)

browser.set_page_load_timeout(7)


for ids in id_list:
    print(f'ID {ids} is starting...')

    url = f"URL-TIL-WEBSITE-{ids}"

    try:
        browser.get(url)
        print('Succesful ".get(url)"')
        pass
    except:
        print(f'---- For lang loading tid: {ids}')
        browser.execute_script("window.stop();")
        print()
        for_lang_loading_tid += 1
        continue

    '''
	Kontrol om URL'en er 404
	'''

    try:
        kontrol_404 = browser.find_element_by_xpath('/html/body/div[1]/p')
        print(f'{ids} er 404')
        print()
        ids_404 += 1

        continue
    except:
        pass

    '''
	Kontrol om boligen er udlejet eller ej.
	 - Hvis den er udlejet, så bruges der andre xpaths.
	'''
    udlejet_kontrol = browser.find_element_by_xpath(
        '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[1]/div')

    if len(udlejet_kontrol.text) <= 0:
        print(f'{ids} er ikke udlejet')
        print()

        try:
            titel = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[2]/div/div/h1').text
            addresse = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[2]/div/div/h2').text
            oprettelsesdato = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[8]/span[2]').text
            depositum = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[5]/span[2]').text
            boligtype = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[1]/span[2]').text
            etage = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[4]/span[2]').text
            møbleret = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[5]/span[2]').text
            delevenlig = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[6]/span[2]').text
            husdyr = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[1]/div[7]/span[2]').text
            lejeperiode = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[1]/span[2]').text
            overtagelsesdato = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[2]/span[2]').text
            månedlig_leje = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[3]/span[2]').text
            aconto = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div[2]/div/div/div[2]/div/div[2]/div[4]/span[2]').text
            image_count = browser.find_elements_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[1]/div/div/div/div')
            image_count = str(len(image_count))

            status = 'Ikke udlejet'

            write_to_file(ids, titel, addresse, oprettelsesdato, depositum, boligtype, etage, møbleret, delevenlig, husdyr, lejeperiode,
                          overtagelsesdato, månedlig_leje, aconto, status, image_count)

        except:
            print()
            print('------------------')
            print(f'failure for ID: {ids} (Ikke udlejet)')
            print('------------------')
            print()

# Allerede udlejede boliger:
    else:
        print(f'{ids} er udlejet')
        print()

        try:
            titel = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div/div/h1').text
            addresse = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[3]/div/div/h2').text
            oprettelsesdato = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[8]/span[2]').text
            depositum = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[5]/span[2]').text
            boligtype = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[1]/div[1]/span[2]').text
            etage = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[1]/div[4]/span[2]').text
            møbleret = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[1]/div[5]/span[2]').text
            delevenlig = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[1]/div[6]/span[2]').text
            husdyr = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[1]/div[7]/span[2]').text
            lejeperiode = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[1]/span[2]').text
            overtagelsesdato = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[2]/span[2]').text
            månedlig_leje = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[3]/span[2]').text
            aconto = browser.find_element_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[4]/div[2]/div/div/div[2]/div/div[2]/div[4]/span[2]').text
            image_count = browser.find_elements_by_xpath(
                '/html/body/div[3]/div/div[1]/div[3]/div[2]/div[2]/div/div/div/div')
            image_count = str(len(image_count))

            status = udlejet_kontrol.text

            write_to_file(ids, titel, addresse, oprettelsesdato, depositum, boligtype, etage, møbleret, delevenlig, husdyr, lejeperiode,
                          overtagelsesdato, månedlig_leje, aconto, status, image_count)

        except:
            print()
            print('------------------')
            print(f'failure for ID: {ids} (udlejet)')
            print('------------------')
            print()

browser.close()


print(f'Antal med for lang loadingtid: {for_lang_loading_tid}')
print(f'Antal med 404: {ids_404}')

print('End of script...')
