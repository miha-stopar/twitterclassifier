import os
import json
#from py2neo import neo4j
from socialweb.tweets import Tweets
import util
import random
import logging

class Categories(object):
    def __init__(self):
        self.tweets = Tweets()
        self.logger = logging.getLogger("tclas")
        path = os.path.join(util.config_dir, "english_stopwords.txt")
        content = open(path).read()
        self.stop_words = json.loads(content)
        #self.graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
        self.categories = [u'Blues, Country, Folk', u'Hard & Heavy', u'Folk Music', u'Classical', u'Rock Pop', \
                      u'Festival', u'Hip Hop', u'Metal', u'Jazz', u'Punk', u'Ballet, Dance', \
                      u'Opera, Operetta', u'Cabaret, Comedy', u'Theatre', u'Musical', u'Gospel', u'Reggae', u'Soul', \
                      u'Other sport events', u'Basketball, Tennis', u'Vaudeville', u'Football', u'Reading', u'Show', \
                      u'Balladeer, Chanson', u'Summer Stock', u'Lecture', u'Entertainment, miscellaneous', \
                      u'Movies, Cinema', u'Exhibition', u'Bus ride', u'Children', u'Clubbing', u'Circus', u'Ball', \
                      u'Fair', u'Party', u'Voucher', u'Gala', u'A cappella', u'Miscellaneous', u'Comedy', u'Swing', \
                      u'Tourism and Leisure']
        self.seed_users = {"Blues, Country, Folk" :["FolkAlley", "CountryMusic"], "Hard & Heavy":["BLABBERMOUTHNET"]}
        self.seed_users.update({"Folk Music":["FolkArtists"], "Classical":["classicfm"], "Rock Pop":["PopRockBands"]})
        self.seed_users.update({"Festival":["ultramusic"], "Hip Hop":["HipHopDX"], "Metal":["MetalBlade"]})
        self.seed_users.update({"Jazz":["APassion4Jazz"], "Punk":["PunkRockers"]})
        self.seed_users.update({"Ballet, Dance":["balletrusse"], "Opera, Operetta":["RoyalOperaHouse"], "Cabaret, Comedy":["cabaretuk"]})
        self.seed_users.update({"Theatre":["TimeOutTheatre"], "Musical":["BroadwayMusical"], "Gospel":["GospelMusic"]})
        self.seed_users.update({"Reggae":["thereggaevibe"], "Soul":["DeepCitySoul"]})

    def get_users_for_category(self, category_name, seed_user=None):
        # for example category_name = "football", seed_user = "BBCFootball1"
        #results = self.tweets.search(category_name)["results"]
        if seed_user == None:
            seed_user = self.seed_users[category_name][0]
        users = self.tweets.collect_user_follows(seed_user, "following")
        users.extend(self.tweets.collect_user_follows(seed_user, "followers"))
        return users
        
    def collect_category_data(self, category_name, seed_user=None):
        users = self.get_users_for_category(category_name, seed_user)
        self.logger.info("users for category %s: %s" % (category_name, len(users)))
        users = users[:util.users_per_category]
        user_infos = self.tweets.collect_users_info(users, use_ids=True)
        r_users = []
        for i in user_infos:
            info = json.loads(i)
            if info["followers_count"] > util.minimum_number_of_followers:
                r_users.append(info)
        self.logger.info("representative users: %s" % len(r_users))
        for ind, user in enumerate(r_users):
            user_name = user["screen_name"]
            base_dir = util.data_dir
            path = os.path.join(base_dir, category_name)
            if not os.path.exists(path):
                os.makedirs(path)
            tweets = self.tweets.collect_user_tweets(user["id"], 1, 200)
            self.logger.info("%s tweets extracted" % len(tweets))
            docs = []
            ids = []
            for t in tweets:
                t_id = str(t["id"])
                text = t["text"]
                text = text.replace("\n", " ")
                text = util.clear_tweet(text)
                if text.strip() == "":
                    continue
                docs.append(str(t_id) + " " + text + "\n")
                ids.append(t_id)
            file_path = os.path.join(path, user_name)
            user_doc = ""
            if os.path.exists(file_path):
                f = open(file_path)
                first_line = f.readline()
                last_tweet_id = first_line.split(" ")[0]
                for ind, doc in enumerate(docs):
                    t_id = ids[ind]
                    if t_id != last_tweet_id:
                        user_doc += doc
                    else:
                        break
                user_doc += "\n" + user_doc
                f.close()
                f = open(file_path, "w")
            else:
                f = open(file_path, "w+")
                for ind, doc in enumerate(docs):
                    user_doc += doc
            if user_doc.strip() == "":
                f.close()
                os.remove(file_path)
                continue
            is_english = False
            count = 0
            for stop_word in self.stop_words:
                if stop_word in user_doc:
                    count += 1
                    if count == 10:
                        is_english = True
                        break
            if is_english:
                f.write(user_doc.encode("utf-8"))
                f.close()
            else:
                self.logger.info("Seems to be a non english text.")
                f.close()
                os.remove(file_path)
        return len(r_users)
    
    def collect_categories_data(self):
        #cat_index = learn.graph_db.get_or_create_index(neo4j.Node, "Category")
        #cats = cat_index.query("c_id:*")
        cats = ['Blues, Country, Folk', 'Hard & Heavy', 'Folk Music', 'Classical', 'Rock Pop', 'Festival', 'Hip Hop', 'Metal', 'Jazz', 'Punk', 'Cabaret, Comedy', 'Ballet, Dance', 'Theatre', 'Musical', 'Gospel', 'Soul', 'Opera, Operetta', 'Reggae', 'Other sport events', 'Basketball, Tennis', 'Vaudeville', 'Football', 'Lecture', 'Reading', 'Show', 'Balladeer, Chanson', 'Summer Stock', 'Entertainment, miscellaneous', 'Movies, Cinema', 'Exhibition', 'Bus ride', 'Children', 'Clubbing', 'Circus', 'Ball', 'Fair', 'Party', 'Voucher', 'Gala', 'A cappella', 'Miscellaneous', 'Comedy', 'Swing', 'Tourism and Leisure']
        random.shuffle(cats) # to avoid updating always the same categories first
        for c in cats:
            #category_name = c["name"]
            category_name = c
            if category_name in self.seed_users.keys():
                self.collect_category_data(category_name)
        
if __name__ == "__main__":
    # for testing
    cat = Categories()
    cat.collect_categories_data()
    
    
    
    
    