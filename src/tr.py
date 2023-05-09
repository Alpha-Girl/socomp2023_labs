from sklearn.naive_bayes import BernoulliNB, CategoricalNB, ComplementNB
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, recall_score, precision_score
import pandas as pd
import xgboost as xgb
from xgboost import plot_importance
from matplotlib import pyplot as plt
# load data
# train_file = 'htos_node.csv'  # training set
# df = pd.read_csv(train_file, header=None)
# X = df.iloc[:, 2:-1]
# y = df.iloc[:, 1]
# X_train,X_test,y_train,y_test=train_test_split(X, y, test_size=0.2, random_state=0)
# # X_test, X_train, y_test, y_train = train_test_split(X, y, test_size=0.2, random_state=0)
# params = {
#     'booster': 'gbtree',
#     'objective': 'multi:softmax',  # 多分类的问题
#     'num_class': 2,               # 类别数，与 multisoftmax 并用
#     'gamma': 0.1,                  # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
#     'max_depth': 12,               # 构建树的深度，越大越容易过拟合
#     'lambda': 2,                   # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
#     'subsample': 0.7,              # 随机采样训练样本
#     'colsample_bytree': 0.7,       # 生成树时进行的列采样
#     'min_child_weight': 3,
#     'silent': 1,                   # 设置成1则没有运行信息输出，最好是设置为0.
#     'eta': 0.007,                  # 如同学习率
#     'seed': 1000,
#     'nthread': 4,                  # cpu 线程数
# }
# dtrain = xgb.DMatrix(X_train, y_train)
# num_rounds = 500
# model = xgb.train(params, dtrain, num_rounds)
# dtest = xgb.DMatrix(X_test)
# ans = model.predict(dtest)
# # print(type(y_test))
# y_test=y_test.tolist()
# # 计算准确率
# cnt1 = 0
# cnt2 = 0
# for i in range(len(y_test)):
#     if ans[i] == y_test[i]:
#         cnt1 += 1
#     else:
#         cnt2 += 1
#         print(ans[i],y_test[i])

# print("Accuracy: %.2f %% " % (100 * cnt1 / (cnt1 + cnt2)))

# # 显示重要特征


from numpy import loadtxt
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
df = pd.read_csv("htos_node_t.csv",header=None
                #  [  34    ,35    ,36 ,   37,        38,   39,     40,       41,      42,      43,       44,       45,         46,     4 7,   48,    49
# "name_1","name_2","conv","bn","relu","maxpool","avgpool","add","layer","downsample","fc","flatten","classifier","features","dropout","cat","pool","mul","conv","bn","relu","maxpool","avgpool","add","layer","downsample","fc","flatten","classifier","features","dropout","cat","pool","mul","conv","bn","relu","maxpool","avgpool","add","layer","downsample","fc","flatten","classifier","features","dropout","cat","pool","mul","label"
# ]
)
#  我们将各位众议员的，，最后三届众议员任期内的提案数变化情况，累计发起各类提案数量，累计联合发起各类提案数量，，联合发起的提案的平均行动数量，以及前述定义的与众议院内其他议员的投票决策距离的平均值作为判断依据，并采用XGBoost分类器进行分类判断。
data=df.iloc[:,1:]
data.rename(columns={1:"平均每届发起提案数",
                     2:"平均每届联合发起提案数",
                     3:"最后一届任期发起提案数",
                     4:"倒二届任期发起提案数",
                     5:"倒三届任期发起提案数", 
                     6:"最后一届任期联合发起提案数",
                     7:"倒二届任期联合发起提案数",
                     8:"倒三届任期联合发起提案数",
                     9:"发起a类提案数",
                     10:"发起b类提案数",
                     11:"发起c类提案数",
                     12:"发起d类提案数",
                     13:"发起e类提案数",
                    14:"发起f类提案数",
                     15:"发起g类提案数",
                     16:"发起h类提案数",
                     17:"所发起的提案的平均行动数量",
                     18:"联合发起a类提案数",
                     19:"联合发起b类提案数",
                     20:"联合发起c类提案数",
                     21:"联合发起d类提案数",
                     22:"联合发起e类提案数",
                    23:"联合发起f类提案数",
                     24:"联合发起g类提案数",
                     25:"联合发起h类提案数",
                     26:"所联合发起的提案的平均行动数量",
                     27:"与众议院内其他议员的投票决策距离的平均值"},inplace=True)
target=df.iloc[:,0]
# dataset = loadtxt('htos_node_t.csv', delimiter=",")
# X = dataset[:,1:]
# Y = dataset[:,0]
seed = 7
test_size = 0.2
X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=test_size, random_state=seed)
# 不可视化数据集
#model = XGBClassifier()
#model.fit(X_train, y_train)
##可视化测试集的loss
model = XGBClassifier()
eval_set = [(X_test, y_test)]
model.fit(X_train, y_train, early_stopping_rounds=100, eval_metric="auc", eval_set=eval_set, verbose=True)

y_pred = model.predict(X_test)

predictions = [round(value) for value in y_pred]
print(predictions)
accuracy = accuracy_score(y_test, predictions)
# plt.figure(figsize=(20,10))
plt.rcParams['figure.figsize']=(10,5)
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签
print("Accuracy: %.2f%%" % (accuracy * 100.0))
xgb.plot_importance(model,height=0.8,title=u'', ylabel=u'特征')

# plot_importance(model)
# plt.show()
plt.savefig('tight.png', bbox_inches='tight')
# print(y_test)
# test_file = 'D:\\AMCS_2022\\data\\Bayesian_Dataset_test.csv'  # test set
# df = pd.read_csv(test_file, header=None)
# X_test = df.iloc[:, :-1]
# X_test_before_transform = X_test
# y_test = df.iloc[:, -1]

# X = pd.concat([X_test, X_train])

# # data preprocessing

# OrdEnc = OrdinalEncoder()
# X = OrdEnc.fit_transform(X)
# X = pd.DataFrame(X)
# X_test = X.iloc[:len(X_test), :]
# X_train = X.iloc[len(X_test):, :]

# naive bayes
# select Naive Bayes classifier
# and set parameters
# nb = BernoulliNB()  # Naive Bayes classifier for multivariate Bernoulli models.
# nb = GaussianNB(var_smoothing=1e-9)  # Gaussian Naive Bayes
# nb = CategoricalNB(alpha=1.0,fit_prior=True)  # Naive Bayes classifier for categorical features.
# # nb = ComplementNB()  # Complement Naive Bayes classifier
# # nb = MultinomialNB()  # Naive Bayes classifier for multinomial models
# y_pred = nb.fit(X_train, y_train).predict(X_test)

# # print result statistics
# print("positive label : ' >50K'")
# print("Number of mislabeled points out of a total %d points : %d"
#       % (X_test.shape[0], (y_test != y_pred).sum()))
# print("Accuracy = %.4f" % (1-(y_test != y_pred).sum()/X_test.shape[0]))
# print("Precision = %.4f" % (precision_score(y_test, y_pred, pos_label=' >50K')))
# print("Recall = %.4f" % (recall_score(y_test, y_pred, pos_label=' >50K')))
# print("F1_score = %.4f" % (f1_score(y_test, y_pred, pos_label=' >50K')))

# # save prediction
# y_pred = pd.Series(y_pred)
# result = pd.concat([X_test_before_transform, y_test, y_pred], axis=1)
# result.to_csv("D:\\AMCS_2022\\data\\Bayesian_Dataset_pred.csv", header=0)
