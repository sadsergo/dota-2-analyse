
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix


matchup_data = pd.read_csv('backend/data_proc/data/data_for_predict.csv', encoding='ISO-8859-`1`')
x_data = matchup_data[['dire_1', 'dire_2', 'dire_3', 'dire_4', 'dire_5', 'radiant_1', 'radiant_2', 'radiant_3', 'radiant_4', 'radiant_5']]
y_data = matchup_data.radiant_win

x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size = 0.33, random_state = 12)
model = LogisticRegression()
model.fit(x_train, y_train)

prediction = dict()
prediction['Logistic'] = model.predict(x_test)

print('Log:', accuracy_score(y_test, prediction['Logistic']))
print(model.coef_)