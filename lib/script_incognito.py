'''
Script for logout incognito no cookies user
'''

from tools import IncognitoGoogle, Search, Save
import time


time.sleep(20)
browser_logout = IncognitoGoogle() 
#browser_logout_control = LogoutGoogle() 
#browser_logout_hon = LogoutGoogle() 

query_categories = ['Men_Health', 'Women_Health', 'Nutrition', 'Health_Conditions', 'Pharmacy']


for query_category in query_categories:

	# Logout Google search for Male queries
	dict_logout_google_male = Search(category=query_category,
	                                 browser=browser_logout,
	                                 NoCookies=True                              
	                               )


	# Save results                                 
	Save(dict_logout_google_male,
	     path='../../Results/Logout/Incognito{}.csv'.format(query_category)
	    )
