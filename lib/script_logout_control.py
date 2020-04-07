'''
Script for logout user
'''

from tools import LogoutGoogle, Search, Save
import time


time.sleep(15)
browser_logout = LogoutGoogle() 
#browser_logout_control = LogoutGoogle() 
#browser_logout_hon = LogoutGoogle() 

query_categories = ['Men_Health', 'Women_Health', 'Nutrition', 'Health_Conditions', 'Pharmacy']


for query_category in query_categories:

	# Logout Google search for Male queries
	dict_logout_google_male = Search(category=query_category,
	                                 browser=browser_logout	                              
	                               )


	# Save results                                 
	Save(dict_logout_google_male,
	     path='../../Results/Logout/Control{}.csv'.format(query_category)
	    )



