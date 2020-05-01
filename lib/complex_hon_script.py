'''
Script for complex_hon_click behaviour user
'''
from tools import LoginGoogle, SearchAndSave
import time
import schedule

LOGIN_TIME = 60
# login to Google Account
start =  time.time()
browser = LoginGoogle(email='hankfromensk@gmail.com', password='Ass12345') #CHANGE
end = time.time()
SESSION_TIME = end - start
time.sleep (LOGIN_TIME - SESSION_TIME)

#schedule.every().day.at("08:00").do(SearchAndSave, browser=browser, user='complex_hon_click')
schedule.every(12).minutes.do(SearchAndSave, browser=browser, user='complex_hon_click') #CHANGE

while True:
    schedule.run_pending()