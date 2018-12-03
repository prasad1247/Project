import data
from sklearn import tree
from sklearn import neighbors
from sklearn import model_selection
import numpy as np
from sklearn.preprocessing import MinMaxScaler

clf = tree.DecisionTreeRegressor()
dat=data.parseData("path")
dataset=np.array(dat)
X = dataset[:,0:5] #Feature set
Y = dataset[:,5]

min_max=MinMaxScaler()
X_train_minmax=min_max.fit_transform(dataset)
# Y_train_minmax=min_max.fit_transform(Y)

X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X_train_minmax, Y_train_minmax, test_size = 0.2, train_size=0.8, random_state=0)
clf = clf.fit(X_train, Y_train)
print("clf clf values with Split")
print(clf.score(X_test, Y_test))
knn = neighbors.KNeighborsRegressor()
knn.fit(X_train,Y_train)
print("knn knn values with Split")
print(knn.score(X_test, Y_test))
modelSVMRaw = neighbors.KNeighborsRegressor()
modelSVMRaw = knn.fit(X_train,Y_train)
cnt = 0
k=0
for i in modelSVMRaw.predict(X_test):
    # print(str(i)+"  "+str(Y_test[k]))
    if(int(round(i)) == Y_test[k]):
        cnt = cnt+1
    k=k+1

print("Linear SVC score without split")
print(float(cnt)/len(Y_test))

# prediction = clf.predict([[65,1,4,116]])

# print(prediction)