
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time


# In[2]:


driver=webdriver.Chrome(executable_path='chromedriver_linux64/chromedriver')


# In[3]:


url="https://dissenter.com/discussion/begin-extension?url=https%3A%2F%2Fwww.google.com%2F"
driver.get(url)
driver.implicitly_wait(10)





while True:
    try:
        load_more_button = driver.find_element_by_css_selector('.btn.btn-block.btn-outline-primary.text-secondary')
        driver.execute_script("arguments[0].click();", load_more_button)
        time.sleep(2)
    except NoSuchElementException:
        print('complete scraping of the comments of this website')
        break


# In[7]:


box = driver.find_element_by_css_selector('.comment-page-list.mb-3')
box


# In[8]:


comments = box.find_elements_by_css_selector('.comment-container')


# In[9]:


len(comments)


# In[10]:


c = comments[0].find_element_by_css_selector('.comment')
name = c.find_element_by_css_selector('.profile-name').text
comment_text = c.find_element_by_css_selector('.comment-body').text
name , comment_text

# In[11]:


dissenter_url_comment  = {}
for idx , comment in enumerate(comments):
    c = comment.find_element_by_css_selector('.comment')
    name = c.find_element_by_css_selector('.profile-name').text
    comment_text = c.find_element_by_css_selector('.comment-body').text
    dissenter_url_comment[idx]={}
    dissenter_url_comment[idx]['name'] = name
    dissenter_url_comment[idx]['comment_text'] = comment_text
print(dissenter_url_comment)


# In[13]:


import json
#save json
with open('dissenter_data.json', 'w') as f:
    json.dump(dissenter_url_comment, f)


# In[ ]:




