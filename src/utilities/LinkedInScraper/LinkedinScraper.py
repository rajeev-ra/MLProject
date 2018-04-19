import time, sys
from selenium import webdriver

emailId = ""
psswrd = ""

# function to generate text file with links to profiles of people worked in TCS
def GenerateProfileLinks(eml, pss, fp):
    driver = webdriver.Chrome()

    # Log in
    driver.get("https://www.linkedin.com/");
    time.sleep(2)

    e = driver.find_element_by_id("login-email")
    for a in emailId:
        e.send_keys(a)

    e = driver.find_element_by_id("login-password")
    for a in psswrd:
        e.send_keys(a)

    driver.find_element_by_id("login-submit").click()
    time.sleep(2)

    # Search for people who have worked in TCS and write their url to file
    pathList = []
    for page in range(1, 101):
        driver.get("https://www.linkedin.com/search/results/people/?company=&facetGeoRegion=%5B%22in%3A7127%22%5D&facetPastCompany=%5B%221353%22%5D&firstName=&lastName=&origin=FACETED_SEARCH&school=&title=&page=" + str(page))
        time.sleep(2)
        links = driver.find_elements_by_class_name("search-result__result-link")
        for link in links:
            href = link.get_property("href")
            if (href not in pathList) and ("search/results/people" not in href):
                pathList.append(href)

    file = open(fp, "a")
    for path in pathList:
        file.write(path)
        file.write('\n')
    file.close()
    driver.close()



GenerateProfileLinks(emailId, psswrd, "./../../../data/LinkedIn/ProfileLinksBengaluru.txt")