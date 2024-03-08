import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import pickle

data = pd.read_csv("")
le = LabelEncoder()

#independent and dependent columns
x = data[["", "", ""]]
y = data["target"]

#split in train and test
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

#model training
clf = make_pipeline(StandardScaler(), SVC(gamma='auto'))
clf.fit(x_train, y_train)

#model testing
predictions = clf.predict(x_test)
clf.score(x_test,y_test)

#save the model
file = open("classification_model.pkl", "wb")
pickle.dump(clf, file)
