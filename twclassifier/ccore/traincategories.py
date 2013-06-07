import os
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import util
import logging

class TrainCategories():
    def __init__(self):
        self.categories = util.list_categories()
        self.logger = logging.getLogger("tclas")
        
    def train(self):
        data = []
        labels = []
        for cdir in util.list_categories():
            path = os.path.join(util.data_dir, cdir)
            fs = os.listdir(path)
            self.logger.info("%s users for category %s" % (len(fs), cdir))
            for ind, f in enumerate(fs):
                if ind == util.users_per_category:
                    break
                p = os.path.join(path, f)
                lines = open(p).readlines()
                doc = ""
                for l in lines:
                    text = " ".join(l.split(" ")[1:]) # remove tweet id
                    if text.strip() != "":
                        doc += text
                if doc.strip() != "":
                    data.append(doc)
                    labels.append(cdir)
        vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'[a-zA-Z]{4,}', min_df=4)
        X_train = vectorizer.fit_transform(data)
        clf = LinearSVC(random_state=0).fit(X_train, labels)
        filename = os.path.join(util.classifiers_dir, 'categories.joblib.pkl')
        joblib.dump(clf, filename, compress=9)
        filename = os.path.join(util.classifiers_dir, 'vect.pkl')
        joblib.dump(vectorizer, filename, compress=9)
        return True
        
    def get_top_keywords(self):
        filename = os.path.join(util.classifiers_dir, 'categories.joblib.pkl')
        clf = joblib.load(filename)
        filename = os.path.join(util.classifiers_dir, 'vect.pkl')
        vectorizer = joblib.load(filename)
        self.logger.info("vocabulary length: %s" % len(vectorizer.vocabulary_))
        feature_names = vectorizer.get_feature_names()
        top_keywords = {}
        for i, category in enumerate(clf.classes_):
            top10 = np.argsort(clf.coef_[i])[-14:]
            text = ""
            for top in top10:
                text += " " + feature_names[top]
            top_keywords[category] = text
        return top_keywords
        
if __name__ == "__main__":
    # for testing
    t = TrainCategories()
    t.train()
    
    
    
    
    
    
    
    
    
    