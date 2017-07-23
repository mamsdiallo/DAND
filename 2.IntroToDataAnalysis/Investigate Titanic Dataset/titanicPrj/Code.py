# -*- coding: utf-8 -*-
"""
Created on Sat Jul 22 23:40:41 2017

@author: Diallo
"""

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import pandas as pd
matplotlib.style.use('ggplot') # Look Pretty
# If the above line throws an error, use plt.style.use('ggplot') instead

df = pd.read_csv("../Data/titanic-data.csv")

# Change feature representation 
df = pd.get_dummies(df,columns=['Embarked'])
# Change feature representation:
df = pd.get_dummies(df,columns=['Sex'])

print df.columns

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Fare')
ax.set_ylabel('Age')
ax.set_zlabel('Pclass')
ax.scatter(df.Fare, df.Age, df['Pclass'], c='r', marker='.')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Fare')
ax.set_ylabel('Age')
ax.set_zlabel('Embarked Cherbourg')
ax.scatter(df.Fare, df.Age, df['Embarked_C'], c='r', marker='.')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Fare')
ax.set_ylabel('Age')
ax.set_zlabel('Embarked Queenstown')
ax.scatter(df.Fare, df.Age, df['Embarked_Q'], c='r', marker='.')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Fare')
ax.set_ylabel('Age')
ax.set_zlabel('Embarked Southampton')
ax.scatter(df.Fare, df.Age, df['Embarked_S'], c='r', marker='.')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('Survived')
ax.set_ylabel('Sex (Female)')
ax.set_zlabel('Age')
ax.scatter(df.Survived, df.Sex_female, df['Age'], c='r', marker='.')


plt.show()
