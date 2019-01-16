from project import data
import numpy as np
from sklearn import model_selection
from sklearn.svm import LinearSVC
from sklearn.decomposition import PCA


def predict(X,Y):
	dat=data.parseData("path")
	dataset=np.array(dat)
	# X = dataset[:,0:5] #Feature set
	# Y = dataset[:,5]    #target
	pca = PCA(n_components=2, whiten=True).fit(X)   # n denotes number of components to keep after Dimensionality Reduction
	X_new = pca.transform(X)
	modelSVM = LinearSVC(C=0.1)
	X_train,X_test,Y_train,Y_test = model_selection.train_test_split(X_new, Y, test_size = 0.2, train_size=0.8, random_state=0)
	modelSVM = modelSVM.fit(X_train,Y_train)
	print("SVM ")
	print(modelSVM.score(X_test, Y_test))

	modelSVMRaw = LinearSVC(C = 0.1)
	modelSVMRaw = modelSVMRaw.fit(X_new, Y)
	cnt = 0
	for i in modelSVMRaw.predict(X_new):
		if(i == Y[1]):
			cnt = cnt+1
	print("SVM")
	print(float(cnt)/75)
	return float(cnt)/75

# dat=data.parseData("path")
# dataset=np.array(dat)
# X = dataset[:,0:5] #Feature set
# Y = dataset[:,5]    #t
# predict(X,Y)