About
=====

Classifier for predicting user interests based on Twitter profile. Python library scikit-learn is used for machine learning part.


.. image:: https://raw.github.com/miha-stopar/twitterclassifier/master/webui.png



Collecting data
=====

Add category name and its representing user using the second form (see screenshot). Categories are for example: *psychology, 
science, politics, fiction literature, programming* etc. For each category a representing user is needed - @JohnDCook for category 
*programming* for example. 

Once a new category is added tweets from representing user and users that she/he is following are downloaded - assumption that users 
that are being followed share the same interest as the representing user is rather simplified and could be improved with some
additional filtering.

Some things to be noted here: only English tweets are stored (filtering is done based on English stop words) and only users with more
that 50 followers are considered. These and some other parameters can be configured in 
*/path/to/twitterclassifier/twclassifier/ccore/util.py*.

For more details see */path/to/twitterclassifier/twclassifier/ccore/categories.py*.

Training data
=====

Once categories are defined and tweets are extracted Train button should be used to run the machine
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

Go to */path/to/twitterclassifier/config* and add twitter.cfg file with your Twitter credentials there:
::
	[Twitter]
	token = 
	token_secret = 
	consumer_key = 
	consumer_secret = 

Create a directory where tweets will be stored and edit data_dir parameter in */path/to/twitterclassifier/twclassifier/ccore/util.py*.

Execute the following command in the command-line:
::
	export PYTHONPATH=/path/to/twitterclassifier/twclassifier
	
Go into */path/to/twitterclassifier/web* and run:
::
	python web.py
	
Open http://localhost:8080/ in a web browser. For further configuration see and edit */path/to/twitterclassifier/twclassifier/ccore/util.py*.
	