import math
import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains

print(time.localtime())

options = webdriver.ChromeOptions()
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-notifications")


# navigate to Dice login page
chrome_driver = webdriver.Chrome(options=options)
chrome_driver.get("https://www.dice.com/dashboard/login")
chrome_driver.maximize_window()

wait = WebDriverWait(chrome_driver, 60)

# Login to Dice
username = chrome_driver.find_element(By.NAME, "email")
username.send_keys("******")
password = chrome_driver.find_element(By.ID, "password")
password.send_keys("******")
password.send_keys(Keys.ENTER)

# navigate to job search
time.sleep(5)
# chrome_driver.get(
#     "https://www.dice.com/jobs?q=data%20engineer&location=United%20States&latitude=37.09024&longitude=-95.712891&countryCode=US&locationPrecision=Country&radius=30&radiusUnit=mi&page=1&pageSize=20&filters.postedDate=ONE&filters.easyApply=true&language=en&eid=S2Q_/")

# search for java and remote filter by easy apply
# time.sleep(5)
searchTerm = chrome_driver.find_element(By.XPATH, "//*[@id='typeaheadInput']")
searchTerm.send_keys("Data engineer")
searchLocation = chrome_driver.find_element(By.ID, "google-location-search")
searchLocation.send_keys("United states")
searchLocation.send_keys(Keys.ENTER)
time.sleep(5)
easyApplyFilter = chrome_driver.find_element(By.XPATH, "//*[@id='facets']/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[2]")
easyApplyFilter.click() #today apply
time.sleep(2)
easyApplyFilter = chrome_driver.find_element(By.XPATH, "//*[@id='facets']/dhi-accordion[3]/div[2]/div/js-multi-select-filter/div/ul/li[3]")
easyApplyFilter.click() #Contract apply
time.sleep(2)
easyApplyFilter = chrome_driver.find_element(By.XPATH, "//*[@id='facets']/dhi-accordion[3]/div[2]/div/js-multi-select-filter/div/ul/li[4]")
easyApplyFilter.click() #Contract apply
time.sleep(2)
easyApplyFilter = chrome_driver.find_element(By.XPATH, "//*[@id='singleCheckbox']/span")
easyApplyFilter.click()
time.sleep(3)
# easyapply=chrome_driver.find_element(By.ID, 'singleCheckbox')
# ActionChains(chrome_driver).move_to_element(easyapply).click(easyapply).perform()
# time.sleep(3)
# set posted by date to last 3 days (optional)
# postedDate = chrome_driver.find_element(By.XPATH, "//*[@id="facets"]/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[3]")
# postedDate.click()

numOfJobs = chrome_driver.find_element(By.XPATH, "//*[@id='totalJobCount']").text
numOfPages = math.ceil(int(numOfJobs.replace(",", "")) / 20)
pageCount = 0

# iterate through links from job search and apply
while pageCount < numOfPages:
#this is for the webpage to check the loaded the jobs or not
    jobPostingLinksParent = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='searchDisplay-div']/div["
                                                                                 "3]/dhi-search-cards-widget/div")))
    time.sleep(3)
    # print(jobPostingLinksParent)
    jobPostingLinks = jobPostingLinksParent.find_elements(By.TAG_NAME, "a")
    stringURL = chrome_driver.current_url
    # print(jobPostingLinksParent)
    count = 0
    while count < len(jobPostingLinks):
        # time.sleep(5)
        jobPostingLinksParent = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='searchDisplay-div']/div[3]/dhi-search-cards-widget/div")))
        time.sleep(3)
        jobPostingLinks = jobPostingLinksParent.find_elements(By.TAG_NAME, "a")

        actions = ActionChains(chrome_driver)
        actions.move_to_element(jobPostingLinks[count]).perform()
        time.sleep(3)
        if "DO NOT APPLY" in jobPostingLinks[count].text:
            # move to next link for dice test account
            count = count + 2
            continue
        Jobsapplied = 1
        print(jobPostingLinks[count].text,Jobsapplied)
        Jobsapplied = Jobsapplied+ 1
        # print(jobPostingLinks)
        jobPostingLinks[count].click()
        count = count + 3
        time.sleep(2)
        try:
            clickdam=chrome_driver.find_element(By.XPATH, "/html/body/div[3]/div/main/header/div/div/div[4]/div[2]/apply-button-wc")
            ActionChains(chrome_driver).move_to_element(clickdam).click(clickdam).perform()
            time.sleep(3)
            clickdam=chrome_driver.find_element(By.CLASS_NAME, "navigation-buttons")
            ActionChains(chrome_driver).move_to_element(clickdam).click(clickdam).perform()
            time.sleep(3)
            clickdam=chrome_driver.find_element(By.XPATH, "/html/body/div[3]/div[4]/div/div[1]/div/div/span/div/main/div[3]/button[2]")
            ActionChains(chrome_driver).move_to_element(clickdam).click(clickdam).perform()
            time.sleep(3)
            clickdam=chrome_driver.find_element(By.PARTIAL_LINK_TEXT, " Go to Search ")
            ActionChains(chrome_driver).move_to_element(clickdam).click(clickdam).perform()
            time.sleep(3)

            # Iterate over the window handles and close all the pop-ups
        except:
            chrome_driver.execute_script("window.onbeforeunload = function() {};")
            chrome_driver.get(stringURL)

    print("Flag3:i am going to next page")
    time.sleep(3)
    # nextPage = wait.until(EC.visibility_of_element_located((By.XPATH, "///*[@id='pagination_2']/pagination/ul/li[7]/a")))
    # nextPage = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-cy='page-next']")))
    nextPage = chrome_driver.find_element(By.XPATH, "//*[@id='pagination_2']/pagination/ul/li[7]/a")
    ActionChains(chrome_driver).move_to_element(nextPage).click(nextPage).perform()
    nextPage.click()
    pageCount = pageCount + 1
    print(count)
    print(pageCount)
    print(time.localtime())
