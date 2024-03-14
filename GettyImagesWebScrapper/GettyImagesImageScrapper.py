from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

def is_url_from_getty(url):
    #Check if the Url matches the Regex of GettyImage Url
    if bool(re.match('^(https://www.gettyimages.com/).*$', url)) or bool(re.match('^(www.gettyimages.com/).*$', url)):
        return True

    else:
        return False

def does_directory_exist(path):
    #Check if the path exists
    return os.path.exists(path)

def is_directory(path):
    #Check if the path leads to a directory
    return os.path.isdir(path)

def create_folder(folder_name):
    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full path for the new folder
    new_folder_path = os.path.join(current_directory, folder_name)

    # Create the folder
    os.mkdir(new_folder_path)

    return new_folder_path

def change_working_directory(new_directory):
    #Change the current working directory
    os.chdir(new_directory)

    return os.getcwd()


while True:
    #Ask for input until a valid url is received
    url = str(input('Url of GettyImages page you want to start from: '))

    if is_url_from_getty(url):
        break

    else:
        print('Invalid Url! Please use one from GettyImages after inputing information into the search bar.')

while True:
    #Ask for input until a valid integer is received
    try: 
        pages = int(input('Number of pages you want to scrape: '))
        break

    except ValueError as e:
        print('That is not an integer! Please try again.')

download_address = input('Absolute path of directory you would like to download images to: ')

#Check if the path received is valid and if it is not, create a folder at the current working directory and make it 
#the current working directory
if does_directory_exist(download_address) == False or is_directory(download_address) == False:
    
    current_timestamp = datetime.now()
    current_timestamp_str = current_timestamp.strftime("%Y-%m-%d_%H-%M-%S")
    download_address = create_folder('Scrapped_Images_' + current_timestamp_str)
    change_working_directory(download_address)
else:

    change_working_directory(download_address)

name_of_files = input('Name of images (WARNING! If the File name already exists, it will get replaced): ')

#Create instance of Firefox webdriver
driver = webdriver.Firefox()

#Navigate to starting page
driver.get(url)

try:

    #Instantiate a counter to ensure the file names do not overlap
    counter = 0

    #Control the number of Pages being Scrapped
    for _ in range(pages):
        #Locate the part of HTML that contains the Image Links
        current_url = driver.current_url
        html = urlopen(current_url)
        bsObj = BeautifulSoup(html)
        images = bsObj.findAll('img', {'src' : re.compile('^(https://media.gettyimages.com).*$')})

        for image in images:
            #Locate and get the Image links from the Beautiful Soup Object
            image_url = image.attrs['src']
            response = requests.get(image_url)

            #Download the files and name them
            with open(name_of_files + str(counter) + ".jpeg", 'wb') as f:
                f.write(response.content)
            counter += 1

        #Wait for the button to be clickable
        button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-testid='pagination-button-next']")))
    
        # Scroll to the button element using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        
        # Once the button is scrolled into view, click it
        button.click()

finally:
    #Close instance of webdriver
    driver.quit()



