import time, sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

emailId = ""
psswrd = ""
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
        #print(len(W))
        for w in W:
            techData = GetTechnologies(w)
            if techData is not None:
                data["Technologies"].append(techData)


    except NoSuchElementException:
        return None

    return data


def SaveProfileJsonData(emailId, psswrd, profileListFilePath):
    driver = GetDriver(emailId, psswrd)
    #GenerateProfileLinks(driver, profileListFilePath)
    file = open(profileListFilePath, 'r')
    urls = file.readlines()
    for i in range(0, len(urls)):
        url = urls[i]
        time.sleep(1)
        jsonFile = open("./../../../data/LinkedIn/ProfileData/" + str(1 + i) + ".json", "w")
        try:
            data = GetProfileInfo(driver, url.strip())
            if data is not None:
                jsonFile.write(str(data))
        except:
            print(i, url.strip())
        jsonFile.close()
    file.close()
    driver.close()


def WriteCsvCell(csvFile, data, last = False):
    csvFile.write(str(data).replace(",", ";"))
    if last is True:
        csvFile.write("\n")
    else:
        csvFile.write(",")


def WriteCsvHeader(csvFile):
    csvFile.write("Name,Url,Raw-Degree,Degree,College,College-Type,Degree-Year,TCS-Start,TCS-End,TCS-Duration,TCS-Position,TCS-Exp,Technology,TCS-Fresher,Next-Company\n")

def IsMBA(degree):
    if ("mba" in degree) or ("m.b.a" in degree):
        return True
    if ("master" in degree) and ("business" in degree):
        return True
    return False

def IsMTech(degree):
    if ("m.e" in degree) or ("mtech" in degree) or ("m.tech" in degree):
        return True
    if ("master" in degree) and (("tech" in degree) or ("eng" in degree)):
        return True
    return False

def IsBTech(degree):
    if ("b.e" in degree) or ("btech" in degree) or ("b.tech" in degree):
        return True
    if ("bachelor" in degree) and (("tech" in degree) or ("eng" in degree)):
        return True
    return False

def GetDegreeShort(degree):
    ldegree = degree.lower()
    if IsMBA(ldegree):
        return "MBA"
    elif IsMTech(ldegree):
        return "M.Tech"
    elif IsBTech(ldegree):
        return "B.Tech"
    else:
        return "Other"

def GetDuration(yearMont):
    yearMon = yearMont.split(" ")
    try:
        if 4 == len(yearMon):
            return float(yearMon[0]) + (float(yearMon[2]) / 12)
        elif "mo" in yearMon[1]:
            return (float(yearMon[0]) / 12)
        else:
            return int(yearMon[0])
    except:
        return yearMont

def GetIfFresher(data, tcsData):
    start = int(data["Education"]["EndTime"])
    ends = tcsData["To"].split(" ")
    end = 0
    if "Present" == ends[len(ends) - 1]:
        end = 2018
    else:
        end = int(ends[len(ends) - 1])
    if (end - start) < 2:
        return "Yes"
    else:
        return "No"

def GetTCSData(data):
    exData = data["Experiences"]
    for i in range(len(exData)):
        companyName = exData[i]["Company"].lower()
        if "tata" in companyName or "tcs" in companyName or "t.c.s" in companyName:
            return exData[i]
    return None

def GetExperience1(data, tcsData):
    start = int(data["Education"]["EndTime"])
    ends = tcsData["To"].split(" ")
    end = 0
    if "Present" == ends[len(ends) - 1]:
        end = 2018
    else:
        end = int(ends[len(ends) - 1])
    return str(end - start)

def GetNextCompany(data, tcsData):
    exData = data["Experiences"]
    for i in range(len(exData)):
        if tcsData == exData[i] and i > 0:
            return exData[i-1]["Company"]
    return "None"

def WriteTCSDataInCSV(csvFile, data):
    tcsData = GetTCSData(data)
    if tcsData is None:
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, "", True)
    else:
        WriteCsvCell(csvFile, tcsData["From"])
        WriteCsvCell(csvFile, tcsData["To"])
        WriteCsvCell(csvFile, GetDuration(tcsData["Duration"]))
        WriteCsvCell(csvFile, tcsData["Title"])
        WriteCsvCell(csvFile, GetExperience1(data, tcsData))
        WriteCsvCell(csvFile, "")
        WriteCsvCell(csvFile, GetIfFresher(data, tcsData))
        WriteCsvCell(csvFile, GetNextCompany(data, tcsData), True)


def WriteCsvData(csvFile, data):
    WriteCsvCell(csvFile, data["Name"])
    WriteCsvCell(csvFile, data["Url"])
    WriteCsvCell(csvFile, data["Education"]["Degree"])
    WriteCsvCell(csvFile, GetDegreeShort(data["Education"]["Degree"]))
    WriteCsvCell(csvFile, data["Education"]["College"])
    WriteCsvCell(csvFile, "")
    WriteCsvCell(csvFile, data["Education"]["EndTime"])
    WriteTCSDataInCSV(csvFile, data)


def CreateCsvFromJson(csvPath):
    csvFile = open(csvPath, "w")
    WriteCsvHeader(csvFile)
    for i in range(0, 1000):
        try:
            jsonFile = open("./../../../data/LinkedIn/ProfileData/" + str(1 + i) + ".json", "r")
            jsonstr = jsonFile.read()
            if 10 < len(jsonstr):
                data = eval(jsonstr)
                WriteCsvData(csvFile, data)
        except FileNotFoundError:
            break
    csvFile.close()

CreateCsvFromJson("./../../../data/LinkedIn/Data.csv")
#SaveProfileJsonData(emailId, psswrd, profileListFilePath)
