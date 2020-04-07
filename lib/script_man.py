'''
Script for man user
'''

from tools import LoginGoogle, Search, Save

#import time

#start = time.time()


# account: sex:male, age:43, ip:FR, purpose:testing selenium 
browser_man = LoginGoogle(email='hankfromensk@gmail.com',
                          password='Ass12345')

#end = time.time()
#print(end - start)

# browser_man_control = LoginGoogle(email='alexfromensk@gmail.com',
#                                   password='Ensk2capitana')

# browser_man_hon = LoginGoogle(email='alexfromensk@gmail.com',
#                                  password='Ensk2capitana')

query_categories = ['Men_Health', 'Women_Health', 'Nutrition', 'Health_Conditions', 'Pharmacy']

for query_category in query_categories:

	# Login Man Google search for Male queries
	dict_man_google_male = Search(category=query_category,
	                              browser=browser_man
	                             )
	# Save results                                 
	Save(dict_man_google_male,
	     path='../../Results/Login/Man/Google{}.csv'.format(query_category)
	    )







