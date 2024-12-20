import time
import re
import datetime
import pickle
import importlib

modules_to_import = [
    "selenium", "bs4"
]

print("-- Skype Message Purger -- ")

missing_packages = []
for module in modules_to_import:
    try:
        importlib.import_module(module)
    except Exception as e:
        missing_packages.append(str(e))

if len(missing_packages) > 0:
    print("It looks like you are missing packages required to run this script:")
    for message in missing_packages:
        print(f"\t{message}")
    input("Press enter to exit - then install packages and try again.\n>")
    exit()

from selenium import webdriver
from selenium.common.exceptions import MoveTargetOutOfBoundsException, StaleElementReferenceException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


####  This is only really helpful if you are wanting to clear but not leave chats
try:
    with open('cleared_records.pkl', 'rb') as f:
        fixed = pickle.load(f)
except FileNotFoundError:
    fixed = []


options = Options()
#options.add_argument("--headless")
#service = webdriver.FirefoxService(executable_path='/usr/local/bin/geckodriver')

browser = webdriver.Firefox(options=options)
browser.get("https://web.skype.com/")

input("Login into Skype in browser then press enter to continue >")

## Sign in manually in the browser at this point

def element_in_display(element, retries=5):
    for j in range(retries):
      if list.is_displayed():
          return True
      else:
        browser.execute_script(f"document.querySelector(\'[class=\"scrollViewport scrollViewportV\"]\').scrollBy(0,100)")
        browser.execute_script("arguments[0].scrollIntoView()", element)
        time.sleep(0.5)
    print("\tNot in view")
    time.sleep(0.5)
    return False

def open_context_menu(element, retries = 5):
    for j in range(retries):
        try:
            action.move_to_element_with_offset(element, 0, -10)
            action.context_click().perform()
            time.sleep(0.5)
            print("Context Menu Open")
            return True
        except MoveTargetOutOfBoundsException as e6:
            print("Context Menu Fail")
            action.click(body).perform()
            browser.execute_script("arguments[0].scrollIntoView()", element)
    return False


def click_context(label1, label2):
    icon = browser.find_elements(By.CSS_SELECTOR, f"[aria-label='{label1}']")
    if len(icon) == 0:
        print(f"{label1} Not Found")
        return False
    action.click(icon[0]).perform()
    print(f"{label1} Selected")
    time.sleep(1)
    icon = browser.find_elements(By.CSS_SELECTOR, f"[aria-label='{label2}']")
    if len(icon) == 0:
        print(f"{label2} Not Found")
        return False
    action.click(icon[0]).perform()
    print(f"{label2} Successful")
    time.sleep(1)
    return True

# Uncomment if you want to start from scratch everytime
#fixed = []

# scroll_by adjusts how far to scroll screen after the end of a set of messages
# too lowand you might waste time checking the same records over and over
# too high risks missing some records

print("Scroll controls how far to move down messages at end of each set")
scroll_input = input("Enter a number for scroll or leave blank for default(200):\n>")

try:
    scroll_by = int(scroll_input)
except:
    scroll_by = 200

print(f"Scroll set to {scroll_by}\n")

print("""Determining when to end the process is hard,
we base it on how long the program has ran without finding an entry to clear""")

progress_input = input("Enter scrolling amount or leave blank for default(10):\n>")

try:
    progress_limit = int(progress_input)
except:
    progress_limit = 10

print(f"Progress limit set to {progress_limit}\n")

leave_groups_input = input("Do you want to leave groups?: (y/n)\n>")
leave_groups = leave_groups_input == "y"

if leave_groups:
    print(f"Will leave groups after clearing\n")
else:
    print(f"Will clear groups but not leave\n")

date_before_input = input("Enter date you would like to retain message up to\nFormat should be dd/mm/yyyy otherwise default is one year ago:\n>")
try:
    date_before = datetime.datetime.strptime(date_before_input, "%d/%m/%Y").date()
except ValueError:
    year_ago = f"{datetime.datetime.now().strftime("%d/%m/")}{int(datetime.datetime.now().strftime("%Y")) - 1}"
    date_before = datetime.datetime.strptime(year_ago, "%d/%m/%Y").date()

print(f"Will delete/clear chats older than {datetime.datetime.strftime(date_before, '%d %B %Y')}")


print("\nAbout to Start Deletion and Clearing\n")
input("Press return to proceed >")

action = ActionChains(browser)

rounds_without_progress = 0
total_items_cleared=0

while rounds_without_progress < progress_limit:
    counter, items_cleared = 0, 0
    body = browser.find_element(By.TAG_NAME,"Body")
    lists = browser.find_elements(By.CSS_SELECTOR, "div[role = 'listitem']")
    try:
        for list in lists:
            action.click(body).perform() # clears context menu if clicked on wrong part of screen
            soup = BeautifulSoup(list.get_attribute('outerHTML'), features="html.parser")
            label = soup.find('div').get('aria-label')
            try:
                date_stamp = re.search("[0-9]+/[0-9]+/[0-9]+", label, re.IGNORECASE)[0]
            except TypeError:
                continue
            date_last_message = datetime.datetime.strptime(date_stamp, "%m/%d/%Y").date()
            browser.execute_script("arguments[0].scrollIntoView()", list)
            if label in fixed or date_last_message > date_before:
                print(f"{'.' if (counter < 50 or counter%50 !=0) else '\n.'}", end="")
                time.sleep(0.5)
                continue
            counter = 0
            print("\nAttempting to Clear or Delete")
            time.sleep(1)
            if not element_in_display(list, retries=5):
                continue
            print("Element on Screen")
            for retry in range(5):
                open_context_menu(list, retries=5)
                if click_context('Delete conversation', 'Delete'):
                    items_cleared += 1
                    break
                elif click_context('Clear conversation', 'Confirm'):
                    items_cleared += 1
                    if bool(re.match(".*group chat.*", label)) and leave_groups:
                                open_context_menu(list, retries=5)
                                time.sleep(0.5)
                                click_context('Leave', 'Confirm')
                    break
                elif retry == 4:
                    print("Failed to clear chat - moving on")
                    action.click(body).perform()
                    break
                time.sleep(0.5)
    except StaleElementReferenceException as e8:
        pass
    time.sleep(1)
    rounds_without_progress = 0 if items_cleared > 0 else rounds_without_progress + 1
    total_items_cleared += items_cleared
    browser.execute_script(f"document.querySelector(\'[class=\"scrollViewport scrollViewportV\"]\').scrollBy(0,{scroll_by})")
    time.sleep(1)
    print("\nNext Round")

browser.close()

print(f"Total items cleared: {total_items_cleared}")

# Use pickle to save list of cleared data if session needs restarted
save_pickle = input("Save records to cleared_records.pkl for re-running? (y/n)\n>")

if save_pickle == "y":
    with open('cleared_records.pkl', 'wb') as f:
        pickle.dump(fixed, f)
    print("Remember to delete cleared_records.pkl after you have finished deleting chats")

print("\nProgram Finished\n")
input("Press return to exit\n")
