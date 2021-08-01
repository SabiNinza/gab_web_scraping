
#import 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

#start webdriver
driver=webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver')
driver.maximize_window()




# # login



def login(
    username,
    passwd,
):
    "login function!"
    url = 'https://gab.com/auth/sign_in'
    driver.get(url)
    driver.implicitly_wait(10)
    input_elements = driver.find_elements_by_tag_name('input')
    button = driver.find_element_by_tag_name('button')
    email = input_elements[1]
    password = input_elements[2]
    email.send_keys(username)
    password.send_keys(passwd)
    button.click()
    time.sleep(2)



#enter your user name or password
def user_info(
    gab_user_name = "impuneet",
    username = '??',
    passwd = '??'
):
    
    #login into window
    login(
    username=username,
    passwd=passwd,
    )
    
    
    #open user info in another browser
    user_info = {}
    driver.execute_script("window.open('" + "https://gab.com/"+ gab_user_name + "');")
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)
    
    #user_name or datejoined
    user_info['username'] = gab_user_name
    date_box = driver.find_element_by_css_selector('._UuSG._ayWa._3dGg1.Vlb1o._1vyTb')
    driver.execute_script("arguments[0].scrollIntoView();",date_box)
    join_element = date_box.find_elements_by_tag_name('span')
    user_info['date_joined'] = join_element[8].text

    #user_Basi._info 
    first_box = driver.find_element_by_css_selector('._UuSG.w77Za')
    infos = first_box.find_elements_by_tag_name('a')
    user_info['gab'] = infos[12].text
    user_info['followers'] = infos[13].text
    user_info['following'] = infos[14].text
    
    #last 50 post retries
    timeline = driver.find_element_by_css_selector('._UuSG.w77Za._3cqkW')
    articles = timeline.find_elements_by_tag_name('article')
    driver.execute_script("arguments[0].scrollIntoView();", articles[len(articles)-1])
    comment_extract(
        timeline,
        articles
    )
    timeline = driver.find_element_by_css_selector('._UuSG.w77Za._3cqkW')
    articles = timeline.find_elements_by_tag_name('article')
    post_info = last_50_post_info_extract(articles)
    user_info['last_50_post'] = post_info
    
    
    return user_info


# In[8]:


def last_50_post_info_extract(
    comments,
):
    comment_info = {}
    for idx , comment in enumerate(comments):
        comment_info[idx] = {}
        
        driver.execute_script("arguments[0].scrollIntoView();", comment)
        text = comment.find_element_by_css_selector('._UuSG')
        box_extra = comment.find_elements_by_tag_name('button')
        
        try:
            comts_num = text.find_elements_by_tag_name('a')[4].text
        except:
            comts_num = 0
        
        #save result in dict
        likes = box_extra[1].text
        reposts = box_extra[2].text
        comment_info[idx]['text'] = text.text
        comment_info[idx]['likes'] = likes
        comment_info[idx]['no_of_comments'] = comts_num
        comment_info[idx]['reposts'] = reposts
    return comment_info


# In[9]:


def comment_extract(
    timeline,
    articles
):
    current_element = 0
    while True:
        if current_element > 50:
            print(len(articles))
            time.sleep(4)
            break
        else:
            articles = timeline.find_elements_by_tag_name('article')
            if current_element == len(articles):
                break
            driver.execute_script("arguments[0].scrollIntoView();", articles[len(articles)-1])
            print(len(articles))
            current_element = len(articles)
            time.sleep(4)


# In[10]:


import json
json_object = user_info()
print(json.dumps(json_object, indent = 3))

#save json
with open('data.json', 'w') as f:
    json.dump(json_object, f)





