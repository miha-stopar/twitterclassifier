import json
import re
import os
from sklearn.externals import joblib
from socialweb.tweets import Tweets
import util
import logging
import collections

class PredictCategories(object):
    def __init__(self):
        self.base_dir = util.data_dir
        self.logger = logging.getLogger("tclas")
        self.tweets = Tweets()
        filename = os.path.join(util.classifiers_dir, 'categories.joblib.pkl')
        self.clf = joblib.load(filename)
        filename = os.path.join(util.classifiers_dir, 'vect.pkl')
        self.vectorizer = joblib.load(filename)
        
    def predict_for_user(self, user):
        use_ids = False
        interests = collections.defaultdict(int)
        if re.findall("[a-zA-Z]", user) == []:
            use_ids = True
        users_info = self.tweets.collect_users_info([user], use_ids=use_ids)
        info = json.loads(users_info[0])
        following = self.tweets.collect_user_follows(info["screen_name"], "following")
        tweets = self.tweets.collect_user_tweets(info["id"], 1, 200)
        user_infos = self.tweets.collect_users_info(following, use_ids=True)
        if len(user_infos) == 0:
            return []
        r_users = []
        for i in user_infos:
            info = json.loads(i)
            if info["followers_count"] > util.minimum_number_of_followers:
                r_users.append(info)
        self.logger.info("representative users: %s" % len(r_users))
        for ind, info in enumerate(r_users):
            if ind == util.number_of_users_used_to_predict:
                break
            tweets = self.tweets.collect_user_tweets(info["id"], 1, 200)
            self.logger.info("%s tweets extracted ------------------------------" % len(tweets))
            user_doc = ""
            for t in tweets:
                text = t["text"]
                text = util.clear_tweet(text)
                user_doc += text
            test = self.vectorizer.transform([user_doc])
            cat = self.clf.predict(test)
            interests[str(cat[0])] += 1
            self.logger.info("%s predicted category: %s" % (info["screen_name"], cat))
        # return categories which appear at least three times
        categories = filter(lambda x: interests[x] > 2, interests.keys())
        return categories
        
    def predict_for_document(self, category, user_name):
        f = os.path.join(self.base_dir, category, user_name)
        doc = open(f).read()
        transformed_doc = self.vectorizer.transform([doc])
        reduced_doc = self.pca.transform(transformed_doc.toarray())
        pvalue = self.clf.predict(reduced_doc)
        #print "%s - %s: %s" % (category, user_name, pvalue)
        return pvalue
           
if __name__ == "__main__":
    # for testing
    p = PredictCategories()
    p.predict_for_user("bla") # some Twitter username
    categories = os.listdir(p.base_dir)
    wrong = 0
    right = 0
    for cat in categories:
        break
        path = os.path.join(p.base_dir, cat)
        fs = os.listdir(path)
        for f in fs:
            p_value = p.predict_for_document(cat, f)
            if p_value != cat:
                logging.getLogger("tclas").info("%s: %s" % (cat, p_value))
                wrong += 1
            else:
                right += 1
    print "wrong: ", wrong
    print "right: ", right
    
    
    
    
    
    
    
    
    
    
    
    
    