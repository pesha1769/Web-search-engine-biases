'''
Script for woman user
'''

from tools import LoginGoogle, Search, Save




# account: sex:female, age:43, ip:FR, purpose:testing selenium 
browser_woman = LoginGoogle(email='carenfromensk@gmail.com',
                            password='Ass12345')

# browser_woman_control = LoginGoogle(email='katefromensk@gmail.com',
#                                   password='Ensk2capitana')

# browser_woman_hon = LoginGoogle(email='katefromensk@gmail.com',
#                                  password='Ensk2capitana')

query_categories = ['Men_Health', 'Women_Health', 'Nutrition', 'Health_Conditions', 'Pharmacy']

for query_category in query_categories:

	# Login Man Google search for Male queries
	dict_woman_google_male = Search(category=query_category,
	                              browser=browser_woman
	                             )
	# Save results                                 
	Save(dict_woman_google_male,
	     path='../../Results/Login/Woman/Google{}.csv'.format(query_category)
	    )







