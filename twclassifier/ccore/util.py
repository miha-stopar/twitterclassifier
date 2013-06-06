import re
import os
import time

#paths:
project_dir = '/home/miha/projects/twitterclassifier'
data_dir = '/home/miha/olaii'
web_static = os.path.join(project_dir, "web/static/")
classifiers_dir = os.path.join(project_dir, "classifiers")
config_dir = os.path.join(project_dir, "config")
web_template = os.path.join(project_dir, "web/views/htemplate")
#algorithm params:
users_per_category = 40
minimum_number_of_followers = 50
#web deployment params:
web_domain="localhost" # no slashes
web_port=8080

def get_classifier_mod_msg():
    filename = os.path.join(project_dir, "classifiers/vect.pkl")
    mtime = os.path.getmtime(filename)
    t = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
    time_msg = "Algorithm was last trained: %s" % t
    return time_msg

def get_data_mod_msg(category=None):
    if category == None:
        l = os.listdir(data_dir)
        t = os.path.getmtime(os.path.join(data_dir, l[0]))
        category = l[0]
        for i in l[1:]:
            t1 = os.path.getmtime(os.path.join(data_dir, i))
            if t1 > t:
                t = t1
                category = i
    path = os.path.join(data_dir, category)
    mtime = os.path.getmtime(path)
    t = time.strftime('%Y-%m-%d %H:%M', time.localtime(mtime))
    time_msg = "Last data collecting finished: %s" % t
    return time_msg

def list_categories():
    categories = os.listdir(data_dir)
    return categories

def list_categories_and_users_count():
    l = []
    categories = os.listdir(data_dir)
    for catdir in categories:
        path = os.path.join(data_dir, catdir)
        fs = os.listdir(path)
        l.append((catdir, len(fs)))
    return l

def extract_urls(text):
    urls = re.findall("https?://.*?(?:\s|$)", text)
    for url in urls:
        start = text.find(url)
        stop = start + len(url.strip())
        text = text[:start] + text[stop:]
    return text

def extract_hashtags(text):
    tags = re.findall("#\w*", text)
    for tag in tags:
        start = text.find(tag)
        stop = start + len(tag.strip())
        text = text[:start] + text[stop:]
    return text

def extract_user_mentions(text):
    mentions = re.findall("@\w*", text)
    for m in mentions:
        start = text.find(m)
        stop = start + len(m.strip())
        text = text[:start] + text[stop:]
    return text

def clear_tweet(text):
    text = extract_hashtags(text)
    text = extract_urls(text)
    text = extract_user_mentions(text)
    return text

 
    
