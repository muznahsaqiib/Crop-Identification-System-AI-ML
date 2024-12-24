import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import pickle

df = pd.read_csv('D:/Flask_App/Flask_App/Dataset.csv')


df['NDVI'].fillna(df['NDVI'].median(), inplace=True)
df.drop_duplicates(inplace=True)


from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df['Crop_Type'] = label_encoder.fit_transform(df['Crop_Type'])


X = df.iloc[:, :-1]
y = df.iloc[:, -1]

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)


sc = StandardScaler()
x_train = sc.fit_transform(x_train)
x_test = sc.transform(x_test)


model = DecisionTreeClassifier()
model.fit(x_train, y_train)


train_accuracy = accuracy_score(y_train, model.predict(x_train))
test_accuracy = accuracy_score(y_test, model.predict(x_test))

print(f"Training Accuracy: {train_accuracy}")
print(f"Test Accuracy: {test_accuracy}")


filename = 'model.pkl'
pickle.dump(model, open(filename, 'wb'))
print(f"Model saved to {filename}")
