'''

'''

###############
###LIBRARIES###
###############

# Necessary libraries
import numpy as np
import pandas as pd
import re
import time
import csv
from collections import OrderedDict

# Selenium web scrapping 
from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Rank-Biased Overlap analysis
import rbo
# Jaccard-Needham dissimilarity 
import distance
# Kendall’s tau
import scipy.stats as stats

# Graphs
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(font_scale=1.5)

import plotly.express as px
import plotly.graph_objects as go

###PATHS###


###FUNCTIONS###

# function start Chrome driver with login a user in a Google Account and a Chrome 
# ERROR: "This browser or app may not be secure"
# solution: https://gist.github.com/ikegami-yukino/51b247080976cb41fe93#
def LoginGoogle(email, password):
    # new driver for a new account (signed-in search)
    # install HONCode Toolbar Chrome Extension
    packed_extension_path = '../src/extension_3_1_3_0.crx'
    options = Options()
    options.add_extension(packed_extension_path)
    browser = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=None, options=options)

    # log in using stackoverflow.com  or soundcloud.com or pinterest.com   

    browser.get('https://www.pinterest.com/')
    try:
        browser.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div[3]/div[1]/div[1]/div[2]/div[2]/button').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div[1]/div/div[4]/button[2]').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div[2]/div/div/div[1]/div/div[2]/div/button[2]').click()
    except:
        pass
    try:
        browser.find_element_by_xpath('//*[@id="__PWS_ROOT__"]/div[1]/div[3]/div/div/div[3]/div[1]/div[1]/div[2]/div[1]').click()
    except:
        pass
    
    browser.find_element_by_xpath('//*[@id="googleConnectButton"]').click()
    
    time.sleep(3)
    window_before = browser.window_handles[0]
    window_after = browser.window_handles[1]
    browser.switch_to_window(window_after)
    
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="identifierId"]').send_keys(email + Keys.ENTER) 
    time.sleep(3)
    browser.find_element_by_xpath('//input[@type="password"]').send_keys(password + Keys.ENTER)
    
    time.sleep(3)
    browser.switch_to_window(window_before)
    
    return(browser)

# function start Chrome driver with logout user and turned-off search activity
def LogoutGoogle():
    # new driver for signed-out search
    # install HONCode Toolbar Chrome Extension

    packed_extension_path = '../src/extension_3_1_3_0.crx'
    options = Options()
    options.add_extension(packed_extension_path)
    browser = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=None, options=options)

    browser.get('https://www.google.com/history/optout?cb=1&hl=en&continue=https%3A%2F%2Fconsent.google.com%2Fui%2F%3Fcontinue%3Dhttps%3A%2F%2Fwww.google.com%2Fsearch%3Fsource%253Dhp%2526ei%253D-Q9VXriOKoHeas2YofAO%2526q%253DSoftware%252Btesting%26origin%3Dhttps%3A%2F%2Fwww.google.com%26if%3D1%26wp%3D71%26gl%3DFR%26hl%3Den%26pc%3Ds%23controls')
    browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/table/tbody/tr/td[2]/form/button/div').click()
    
    return(browser)



def IncognitoGoogle():
    # new driver for signed-out search
    # install HONCode Toolbar Chrome Extension

    packed_extension_path = '../src/extension_3_1_3_0.crx'
    options = Options()
    options.add_extension(packed_extension_path)
    options.add_argument("--incognito")
    browser = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=None, options=options)

    browser.get('https://www.google.com/history/optout?cb=1&hl=en&continue=https%3A%2F%2Fconsent.google.com%2Fui%2F%3Fcontinue%3Dhttps%3A%2F%2Fwww.google.com%2Fsearch%3Fsource%253Dhp%2526ei%253D-Q9VXriOKoHeas2YofAO%2526q%253DSoftware%252Btesting%26origin%3Dhttps%3A%2F%2Fwww.google.com%26if%3D1%26wp%3D71%26gl%3DFR%26hl%3Den%26pc%3Ds%23controls')
    browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div/table/tbody/tr/td[2]/form/button/div').click()

    def expand_shadow_element(element):
        shadow_root = browser.execute_script('return arguments[0].shadowRoot', element)
        return shadow_root

  
    browser.get("chrome://extensions/?id=migljoiadpobjnfkpmbpjekghdiilneb")
    root1 = browser.find_element_by_tag_name('extensions-manager')
    shadow_root1 = expand_shadow_element(root1)
    root2 = shadow_root1.find_element_by_css_selector('extensions-detail-view')
    shadow_root2 = expand_shadow_element(root2)
    shadow_root2.find_element_by_css_selector('extensions-toggle-row').click()

    browser.delete_all_cookies()

    return(browser) 



# function search for specific category queris from csv on Google and HON in a particular session
def Search(category, # Male, Female, Health, Pharmacy
           browser, # logged-in (man or woman), logged-out, control
           max_num_res=8, # number of results
           data='../data/queries2019_20_5.csv', # path to queries
           NoCookies=False
           ):
    

    # get all queries and choose which to search
    queries_all = pd.read_csv(data, sep=';')     
    if category=='Men_Health':
        queries_search = queries_all.Men_Health
    elif category=='Women_Health':
        queries_search = queries_all.Women_Health        
    elif category=='Health_Conditions':
        queries_search = queries_all.Health_Conditions  
    elif category=='Nutrition':
        queries_search = queries_all.Nutrition  
    elif category=='Pharmacy':
        queries_search = queries_all.Pharmacy  
 
    # search for queries
    dict_results = {}
    for query in queries_search: 

        # find all elements provided on google search results 
        browser.get("https://google.com") 
        browser.find_element_by_xpath("//input[@name='q']").send_keys(query + Keys.ENTER)
        time.sleep(3)
        num_res=0
        search_results = []

        elements = browser.find_elements_by_class_name('rc')
        
        try:
            first_element = browser.find_element_by_css_selector("div[class='g mnr-c g-blk']")
            temp1 = first_element.find_element_by_css_selector("div[class='r']").find_element_by_css_selector('a').get_attribute('href')
            temp2 = first_element.find_element_by_css_selector('div[target="_blank"]').get_attribute('title')
            search_results.append([temp1, temp2])
            num_res+=1
        except:
            try:
                first_element = browser.find_elements_by_class_name('g')[0]
                temp1 = first_element.find_element_by_css_selector("div[class='r']").find_element_by_css_selector('a').get_attribute('href')
                temp2 = first_element.find_element_by_css_selector('div[target="_blank"]').get_attribute('title')
                search_results.append([temp1, temp2])
                num_res+=1
            except:
                pass

        temp = num_res
        try:
            browser.find_element_by_css_selector("div[class='g kno-kp mnr-c g-blk']")
            temp+=4
        except:
            pass
  
        for j in range(temp, len(elements)):

            temp1 = elements[j].find_element_by_css_selector("div[class='r']").find_element_by_css_selector('a').get_attribute('href')
            temp2 = elements[j].find_element_by_css_selector("div[class='r']").find_element_by_css_selector('div[target="_blank"]').get_attribute('title')
            search_results.append([temp1, temp2])
            num_res+=1

            if num_res==max_num_res:
                break
 
        # save results in a dict
        dict_results.update( {query: search_results} )
        if NoCookies:
            browser.delete_all_cookies()

        # wait 11 minutes to avoid a carry-over effect
        time.sleep(2) # commented for testing purposes (remove later) 
        
    return dict_results


# function save dictionary of the search results as a CSV file
def Save(my_dict,
         path='../Code/results.csv'):
    
    df_google = pd.DataFrame(dict([ (k,pd.Series(np.array(v)[:,0])) for k,v in my_dict.items() ]))
    df_hon = pd.DataFrame(dict([ ('Validation: '+k,pd.Series(np.array(v)[:,1])) for k,v in my_dict.items()]))
    df = pd.concat([df_google, df_hon], axis=1, sort=False)
    df.to_csv(path, index=False)



def RBO(list1, list2, p=1.0, k=8):
    RS = rbo.RankingSimilarity(list1, list2, verbose=False)
    res = RS.rbo(p=p, k=k, ext=True)   
    return (res)

def JACCARD(list1, list2):
    return 1 - distance.jaccard(list1, list2)

def KENDAL(list1, list2):
    return stats.kendalltau(list1, list2)[0]


def CalculatePersonalization(data,
              metrics,
              category
             ):
    
    res_man = []
    res_woman = []
    res_man_woman = []
    
    if category=='Men_Health':
        queries = data[0].Men_Health
    elif category=='Women_Health':
        queries = data[0].Women_Health        
    elif category=='Health_Conditions':
        queries = data[0].Health_Conditions  
    elif category=='Nutrition':
        queries = data[0].Nutrition  
    elif category=='Pharmacy':
        queries = data[0].Pharmacy  
    
    for query in queries:
    
        logout = list(OrderedDict.fromkeys([x for x in data[1].loc[:,query] if str(x) != 'nan']))
        #logout_control = list(OrderedDict.fromkeys([x for x in logout_control_male.loc[:,query] if str(x) != 'nan']))
        
#         if metrics == RBO:
#             assert(metrics(logout, logout_control) == 1.0)
#         if metrics == JACCARD:
#             assert(metrics(logout, logout_control) == 0.0)
#         if metrics == KENDAL:
#             assert(metrics(logout, logout_control)[0] > 0.99)

        man = list(OrderedDict.fromkeys([x for x in data[2].loc[:,query] if str(x) != 'nan']))
        #man_control = list(OrderedDict.fromkeys([x for x in man_control_male.loc[:,query] if str(x) != 'nan'])) 

        woman = list(OrderedDict.fromkeys([x for x in data[3].loc[:,query] if str(x) != 'nan']))
        #woman_control = list(OrderedDict.fromkeys([x for x in woman_control_male.loc[:,query] if str(x) != 'nan'])) 


        res_man_woman.append(metrics(man, woman)) 
        res_man.append(metrics(man, logout))
        res_woman.append(metrics(woman, logout))
    

    average = {}
    average.update({'Man-Logout':round(np.mean(res_man), 3), 'Woman-Logout':round(np.mean(res_woman), 3), 'Man-Woman':round(np.mean(res_man_woman), 3)})
        
        
        
    return res_man, res_woman, res_man_woman, average



def CalculateFairness(data,
              metrics,
              category
             ):
    
    res_man = []
    res_woman = []
    res_logout = []
    
    if category=='Men_Health':
        queries = data[0].Men_Health
    elif category=='Women_Health':
        queries = data[0].Women_Health        
    elif category=='Health_Conditions':
        queries = data[0].Health_Conditions  
    elif category=='Nutrition':
        queries = data[0].Nutrition  
    elif category=='Pharmacy':
        queries = data[0].Pharmacy  
    
    for query in queries:
        
        if metrics=='Count':
            hon_logout_metrics = data[1].loc[:,'Validation: '+query].dropna().count() 
            hon_man_metrics = data[2].loc[:,'Validation: '+query].dropna().count() 
            hon_woman_metrics = data[3].loc[:,'Validation: '+query].dropna().count() 
            
        if metrics=='RBO':
            
            list1 = data[1].loc[:,'Validation: '+query].fillna('NOT certified')
            indices1 = []
            for i, j in enumerate(list1.index[list1 == 'HONcode certified'].tolist()):
                indices1.insert(j, i)
            for i, j in enumerate(list1.index[list1 == 'NOT certified'].tolist()):
                indices1.insert(j, i)
            hon_logout = np.asarray(list(map(str,indices1)))+np.asarray(' '+list1)
            
            list2 = data[2].loc[:,'Validation: '+query].fillna('NOT certified')
            indices2 = []
            for i, j in enumerate(list2.index[list2 == 'HONcode certified'].tolist()):
                indices2.insert(j, i)
            for i, j in enumerate(list2.index[list2 == 'NOT certified'].tolist()):
                indices2.insert(j, i)
            hon_man = np.asarray(list(map(str,indices2)))+np.asarray(' '+list2)  
            
            list3 = data[3].loc[:,'Validation: '+query].fillna('NOT certified')
            indices3 = []
            for i, j in enumerate(list3.index[list3 == 'HONcode certified'].tolist()):
                indices3.insert(j, i)
            for i, j in enumerate(list3.index[list3 == 'NOT certified'].tolist()):
                indices3.insert(j, i)
            hon_woman = np.asarray(list(map(str,indices3)))+np.asarray(' '+list3) 
            
            hon_logout_metrics = RBO(hon_man, hon_woman)
            hon_man_metrics = RBO(hon_man, hon_logout)
            hon_woman_metrics = RBO(hon_woman, hon_logout)
            
        res_logout.append(hon_logout_metrics) 
        res_man.append(hon_man_metrics)
        res_woman.append(hon_woman_metrics)
        
    average = {}
    average.update({'Man-Logout':round(np.mean(res_man), 3), 'Woman-Logout':round(np.mean(res_woman), 3), 'Man-Woman':round(np.mean(res_logout), 3)})
        
    return res_man, res_woman, res_logout, average


def Plot(data,
         metrics,
         category
         ):
    
    data[0]['metrics_man'] = data[1] 
    data[0]['metrics_woman'] = data[2] 
    data[0]['metrics_man_woman_logout'] = data[3] 
    
    data[0] = data[0].sort_values(by=['metrics_man', 'metrics_woman', 'metrics_man_woman_logout'])
    
    if metrics=='RBO' or metrics=='KENDALL' :
        names=['Man-Logout', 'Woman-Logout', 'Man-Woman']
        autorange=None
    if metrics==metrics=='JACCARD':
        names=['Man-Logout', 'Woman-Logout', 'Man-Woman']
        autorange="reversed"
    if metrics=='Count':
        names=['Man', 'Woman', 'Logout'] 
        autorange=None
    
    
    layout = go.Layout(
        title=go.layout.Title(
                text='{0} of {2} for "{1}" queries'.format(metrics, category, data[-1])),
        yaxis=go.layout.YAxis(
            autorange=autorange,
            title=go.layout.yaxis.Title(
                text='{0}'.format(metrics))),
         xaxis=go.layout.XAxis(
            autorange=autorange,
            )
    )

    
    fig = go.Figure(layout=layout)
    
    fig.add_scatter(x=data[0][category], y=data[0]['metrics_man'], name=names[0]+' (average:{})'.format(list(data[4].values())[0]),
                    mode='markers', marker_symbol='line-ew', marker_line_width=2, marker_line_color='red', marker_color='red')
    
    fig.add_scatter(x=data[0][category], y=data[0]['metrics_woman'], name=names[1]+' (average:{})'.format(list(data[4].values())[1]), 
                    mode='markers', marker_symbol='line-ns', marker_line_width=2, marker_line_color='green', marker_color='green')
    
    fig.add_scatter(x=data[0][category], y=data[0]['metrics_man_woman_logout'], name=names[2]+' (average:{})'.format(list(data[4].values())[2]),
                    mode='markers', marker_symbol='line-ne', marker_line_width=2, marker_line_color='blue', marker_color='blue')

    fig.update_layout(legend=dict(x=0.7, y=1.4))
    fig.show()































