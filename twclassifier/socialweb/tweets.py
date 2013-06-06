import twitter
from tweetsutil import exec_twitter_request 
import json
import ConfigParser
import os
from ccore import util
import logging

class Tweets():
    def __init__(self):
        self.logger = logging.getLogger("tclas")
        config_path = os.path.join(util.config_dir, "twitter.cfg")
        config = ConfigParser.ConfigParser()
        config.read(config_path)
        token = config.get("Twitter", "token")
        token_secret = config.get("Twitter", "token_secret")
        consumer_key = config.get("Twitter", "consumer_key")
        consumer_secret = config.get("Twitter", "consumer_secret")
        self.tw = twitter.Twitter(auth=twitter.OAuth(token, token_secret, consumer_key, consumer_secret)) 
    
    def search(self, keyword):
        twitter_search = twitter.Twitter(domain="search.twitter.com")
        r = twitter_search.search(q=keyword)
        return r
        
    def collect_user_follows(self, screen_name, twitter_call):
        cursor = -1
        follower_ids = []
        while cursor != 0:
            if twitter_call == "followers":
                response = exec_twitter_request(self.tw, self.tw.followers.ids, screen_name=screen_name, cursor=cursor)
            elif twitter_call == "following":
                response = exec_twitter_request(self.tw, self.tw.following.ids, screen_name=screen_name, cursor=cursor)
            if response != None:
                for f_id in response['ids']:
                    follower_ids.append(f_id)
                cursor = response['next_cursor']
            else:
                cursor = 0
        return follower_ids
    
    def collect_users_info(self, users, use_ids=True):
        """
        Collect and store user's info.
        :param users: ids or screen_names
        :type users: list
        :param use_ids: whether ids or screen names are used
        :type use_ids: bool
        """
        infos = []
        while len(users) > 0:
            users_req = ','.join([str(_id) for _id in users[:100]])
            users = users[100:]
            if use_ids:
                response = exec_twitter_request(self.tw, self.tw.users.lookup, user_id=users_req)
            else:
                response = exec_twitter_request(self.tw, self.tw.users.lookup, screen_name=users_req)
            if response != None:
                for info in response:
                    infos.append(json.dumps(info))
        return infos

    def collect_user_tweets(self, user_id, pages_num, count):
        """
        Collect and store user's last (pages_num * "tweets_per_page") tweets.
        :param user_id: user's id
        :type user_id: str
        :param pages_num: number of pages to be retrieved
        :type pages_num: int
        :param count: number of tweets to retrieve, max is 200
        :type count: int
        """
        num = 0
        tweets = []
        while num < pages_num:
            num += 1
            kwargs = {'count': count, 'skip_users': 'true', 'include_entities': 'true', 'since_id': 1,}
            kwargs['id'] = user_id
            kwargs['page'] = num
            api_call = getattr(self.tw.statuses, 'user_timeline')
            tws = exec_twitter_request(self.tw, api_call, **kwargs)
            if tws == None or len(tws) == 0:
                break
            self.logger.info('Fetched %i tweets' % len(tweets))
            tweets.extend(tws)
        return tweets
    
    def collect_users_from_state(self, state, locations, pages_num):
        num = 0
        users = []
        while num < pages_num:
            num += 1
            self.logger.info("page number when retrieving users for state %s: %s" % (state, num))
            kwargs = {'q':state}
            kwargs['page'] = num
            api_call = getattr(self.tw.users, 'search')
            candidates = exec_twitter_request(self.tw, api_call, **kwargs)
            if len(candidates) == 0:
                break
            new_users, new_users_loc = self._filter_users(candidates, state, locations)
            users.extend(new_users)
        return users

    def _filter_users(self, candidates, state, locations):
        users = []
        users_loc = {}
        for candidate in candidates:
            candidate_loc = candidate['location']
            if candidate_loc == None:
                continue
            #print candidate["screen_name"], " : ", loc
            user_added = False
            screen_name = candidate["screen_name"]
            if state.lower() in candidate_loc.lower():
                users.append(screen_name)
                user_added = True
                users_loc[screen_name] = candidate_loc
            else:
                for loc in locations:
                    if loc.lower() in candidate_loc.lower():
                        users.append(screen_name)
                        user_added = True
                        users_loc[screen_name] = candidate_loc
                        break
            if not user_added:
                print candidate["screen_name"], " : ", candidate_loc
        return users, users_loc
    
    
    
    
    
    
    
    
    
    
    
    
