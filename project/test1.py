from sklearn import datasets
from sklearn import model_selection
iris = datasets.load_iris()
digits = datasets.load_digits()
X, Y = iris.data, iris.target
X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X, Y, test_size = 0.2, train_size=0.8, random_state=0)
print(iris.data[-1:])
print(iris.target[-1:])
from sklearn import svm
clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(X_train,Y_train) 
print(clf.score(X_test,Y_test))
cnt = 0
k=0
for i in clf.predict(X_test):
    print(str(int(round(i)))+"  "+str(Y_test[k]))
    if(int(round(i)) == Y_test[k]):
        cnt = cnt+1
    k=k+1

print("Linear SVC score without split")
print(float(cnt)/len(Y_test))