import time, sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

emailId = ""
psswrd = ""
testUsr = "https://www.linkedin.com/in/vijay-srikanth-28a90231/"
profileListFilePath = "./../../../data/LinkedIn/ProfileLinksBengaluru.txt"

def GetDriver(eml, pss):
    driver = webdriver.Chrome()

    # Log in
    driver.get("https://www.linkedin.com/");

    e = driver.find_element_by_id("login-email")
    for a in emailId:
        e.send_keys(a)

    e = driver.find_element_by_id("login-password")
    for a in psswrd:
        e.send_keys(a)

    driver.find_element_by_id("login-submit").click()

    return driver

# function to generate text file with links to profiles of people worked in TCS
def GenerateProfileLinks(driver, fp):

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


def GetExperience(elem):
    expData = {
        "Title": "",
        "Company": "",
        "From": "",
        "To": "",
        "Duration": ""
    }
    try:
        sC = elem.find_element_by_class_name("pv-entity__summary-info")
        expData["Title"] = sC.find_element_by_tag_name("h3").text
        expData["Company"] = sC.find_element_by_class_name("pv-entity__secondary-title").text

        dC = sC.find_element_by_class_name("pv-entity__date-range")
        d = dC.find_elements_by_tag_name("span")[-1]
        fromto = d.text.split("–")
        expData["From"] = fromto[0].strip()
        expData["To"] = fromto[1].strip()

        expData["Duration"] = sC.find_element_by_class_name("pv-entity__bullet-item").text
        return expData

    except NoSuchElementException:
        return None

def GetTechnologies(elem):
    if (elem.text is not None) and (elem.text != ""):
        return elem.text
    else:
        return elem.find_element_by_tag_name("span").text


def GetEducation(driver):
    education = {
        "College": "",
        "Degree": "",
        "StartTime": "",
        "EndTime": ""
    }

    education["College"] = driver.find_element_by_class_name("pv-entity__school-name").text
    elem = driver.find_element_by_class_name("pv-entity__degree-name")
    education["Degree"] = elem.find_element_by_class_name("pv-entity__comma-item").text
    elem = driver.find_element_by_class_name("pv-entity__dates")
    education["StartTime"] = elem.find_element_by_tag_name("time").text
    education["EndTime"] = elem.find_elements_by_tag_name("time")[1].text

    return education



def GetProfileInfo(driver, url):
    driver.get(url)
    time.sleep(1)
    data = {
        "Name": "",
        "Url": url,
        "Technologies": [],
        "Experiences": [],
        "Education": {}
    }

    try:
        ne = driver.find_element_by_class_name("pv-top-card-section__name")
        data["Name"] = ne.text


        e = driver.find_element_by_id("experience-section")
        W = e.find_elements_by_class_name("pv-profile-section__card-item")
        for w in W:
            expdata = GetExperience(w)
            if expdata is not None:
                data["Experiences"].append(expdata)

        data["Education"] = GetEducation(driver)
        driver.execute_script("window.scrollTo(0, 2000);")
        time.sleep(2)
        W = e.find_elements_by_class_name("pv-skill-category-entity__name")    #("pv-skill-category-entity__top-skill")
        print(len(W))
        for w in W:
            techData = GetTechnologies(w)
            if techData is not None:
                data["Technologies"].append(techData)


    except NoSuchElementException:
        return None

    return data



driver = GetDriver(emailId, psswrd)
#GenerateProfileLinks(driver, profileListFilePath)
print(GetProfileInfo(driver, testUsr))
time.sleep(1)
driver.close()