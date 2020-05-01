'''
Script for first_non_click behaviour user
'''
from tools import LoginGoogle, SearchAndSave
import time
import schedule

LOGIN_TIME = 60
# login to Google Account
start =  time.time()
browser = LoginGoogle(email='alexfromensk@gmail.com', password='Ensk2capitana') #CHANGE
end = time.time()
SESSION_TIME = end - start
time.sleep (LOGIN_TIME - SESSION_TIME)

schedule.every().day.at("08:00").do(SearchAndSave, browser=browser, user='first_non_click')
#schedule.every(1).minutes.do(SearchAndSave, browser=browser, user='first_non_click') #CHANGE

while True:
    schedule.run_pending()
    time.sleep(1)
