# NaiveBayes-LogisticRegression

## Naive Bayes

Stop-words not removed :::
``` python NaiveBayes.py "train/ham" "train/spam" "test/ham" "test/spam" "n" ```

Stop-words removed :::
``` python NaiveBayes.py "train/ham" "train/spam" "test/ham" "test/spam" "n" ```

ham training set = sys.argv[1]<br />
spam training set = sys.argv[2]<br />
ham testing set = sys.argv[3]<br />
spam testing set = sys.argv[4]<br />
should Stopwords be removed?  = sys.argv[5]


## Logistic Regression

Remove stop words, 1000 iterations, 0.01 learning rate, no regularization :::
``` python LogisticRegression.py ”train/ham" "train/spam" "test/ham" "test/spam" "y" 1000 0.01 “n” ```


Remove stop words, 1000 iterations, 0.01 learning rate, params to be regularized, lambda = 0.1 :::
``` python LogisticRegression.py ”train/ham" "train/spam" "test/ham" "test/spam" "y" 1000 0.01 “y” 0.1 ```


Don’t remove stop-words, 1000 iterations, 0.01 learning rate, no regularization :::
``` python LogisticRegression.py ”train/ham" "train/spam" "test/ham" "test/spam" “n” 1000 0.01 “n” ```


Don’t remove stop words, 1000 iterations, 0.01 learning rate, params to be regularized, lambda = 0.1 :::
``` python LogisticRegression.py ”train/ham" "train/spam" "test/ham" "test/spam" “n” 1000 0.01 “y” 0.1 ```


ham training set = sys.argv[1]<br />
spam training set = sys.argv[2]<br />
ham testing set = sys.argv[3]<br />
spam testing set = sys.argv[4]<br />
should Stopwords be removed?  = sys.argv[5]<br />
number of iterations to be run = int(sys.argv[6])<br />
learning Rate to be taken = float(sys.argv[7])<br />
should params be Regularized = sys.argv[8]<br />
lambda value to be taken = sys.argv[9]
