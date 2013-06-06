About
=====

Classifier for predicting users' interests based on their Twitter profile. Simple web UI is provided for 
managing the classifier.

.. image:: https://bitbucket.org/miha_stopar/twitterclassifier/raw/tip/webui.png

Collecting data
=====

First of all a set of categories/interests and their representing users needs to be defined. Categories are for example: *psychology, 
science, politics, fiction literature, programming* etc. For each category a representing user is needed - I put @JohnDCook for category 
*programming* for example. 

Once a new category and its representing user are added by submitting the second form (see the screenshot) - 
the tweets from this user and users that she/he is following are downloaded (assumption that users that are being followed share 
the same interest as the user that is following them is rather simplified and could be replaced by manually adding 
representing users for each category).

Some things to be noted here: only English tweets are stored (filtering is done based on English stop words), only users with more
that 50 followers are considered, and 40 users are collected per category. These parameters are configurable and can be changed in 
*/path/to/twitterclassifier/twclassifier/ccore/util.py*.

For more details see */path/to/twitterclassifier/twclassifier/ccore/categories.py*.

Training data
=====

Once categories are defined and tweets are extracted - the Train button at the bottom of the page should be used to run the machine
learning algorithm. Python library scikit-learn is used for data cleaning and machine learning (see *traincategories.py* inside
*/path/to/twitterclassifier/twclassifier/ccore* for more details).

Only words that appear in at least 4 documents (one document contains all tweets extracted from one user), have length greater than 3, 
and contain no numbers are considered - see the following line in *traincategories.py*: 
::
	vectorizer = TfidfVectorizer(stop_words='english', token_pattern=r'[a-zA-Z]{4,}', min_df=4)
	
*sklearn.multiclass.OneVsRestClassifier* combined with *sklearn.svm.LinearSVC* is used for training:
::
	clf = OneVsRestClassifier(LinearSVC(random_state=0)).fit(X_train, labels)
	
Trained classifier is stored into *categories.joblib.pkl* into */path/to/twitterclassifier/classifiers*, vectorizer is
stored into *vect.pkl*.

Predicting interests
=====

Insert some Twitter user name in the first form and submit it. You should get a list of interests predicted for this user. For details 
see *predictcategories.py* in */path/to/twitterclassifier/twclassifier/ccore*.

Dependencies
=====
::

	pip install twitter
	pip install bottle
	pip install joblib
	pip install -U scikit-learn
	
	
Install and run
=====

Go to */path/to/twitterclassifier/config/twitter.cfg* and put your Twitter credentials there.

Create a directory where tweets will be stored and edit data_dir parameter in */path/to/twitterclassifier/twclassifier/ccore/util.py*.

Execute the following command in the command-line:
::
	export PYTHONPATH=/path/to/twitterclassifier/twclassifier
	
Go into */path/to/twitterclassifier/web* and run:
::
	python web.py
	
Open http://localhost:8080/ in web browser. For further configuration see and edit */path/to/twitterclassifier/twclassifier/ccore/util.py*.
	