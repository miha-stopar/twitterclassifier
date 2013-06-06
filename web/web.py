import bottle
from bottle import route, run, template, static_file
import json
import logging
import sys
from ccore import util
from ccore import categories
from ccore import traincategories
from ccore import predictcategories

logger = logging.getLogger("tclas")
logger.setLevel(logging.INFO)
fh = logging.FileHandler('tclas.log')
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)

#fsock_err = open("twclas_err.log", "w")
#fsock_out = open("twclass_out.log", "w")
#sys.stderr = fsock_err
#sys.stdout = fsock_out

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=util.web_static)

@route('/:name', method='GET')
def action(name):
    cmds = name.split("___")
    if cmds[0] == "addcat":
        category = cmds[1]
        user = cmds[2]
        cat = categories.Categories()
        cat.collect_category_data(category, user)
        data_time_msg = util.get_data_mod_msg(category)
        return json.dumps(data_time_msg)
    elif cmds[0] == "predict":
        user = cmds[1]
        p = predictcategories.PredictCategories()
        pvalue = p.predict_for_user(user)
        s = ""
        for ind, p in enumerate(pvalue):
            if ind == 0:
                s += p
            else:
                s += " | " + p
        if s.strip() == "":
            s = "no category predicted"
        return json.dumps(s)
    elif name == "train":
        t = traincategories.TrainCategories()
        is_trained = t.train()
        if is_trained:
            time_msg = util.get_classifier_mod_msg()
            logger.info("trained finished")
        else:
            time_msg = "training can't be executed"
            logger.info("training can't be executed")
        return json.dumps(time_msg)

@route('/')
def hello():
    data_time_msg = util.get_data_mod_msg()
    categories = util.list_categories_and_users_count()
    try:
        time_msg = util.get_classifier_mod_msg()
        train = traincategories.TrainCategories()
        top_keywords = train.get_top_keywords()
        trained_categories=[]
        for c in categories:
            if c[0] in top_keywords:
                trained_categories.append(c)
    except Exception, e:
        logger.error(str(e))
        time_msg = "Algorithm was last trained: never. You should train it."
        trained_categories = []
        top_keywords = {}
    return template(util.web_template, web_domain=util.web_domain, web_port=util.web_port, categories=trained_categories, time_msg=time_msg, predict_msg="no category predicted", data_time_msg=data_time_msg, top_keywords=top_keywords)
   
bottle.debug(True) 
run(host=util.web_domain, port=util.web_port)




