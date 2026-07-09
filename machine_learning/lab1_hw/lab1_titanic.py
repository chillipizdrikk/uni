import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("Titanic-Dataset.csv")

data = df[["Survived", "Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]].copy()

data["Age"] = data["Age"].fillna(data["Age"].median())
data["Embarked"] = data["Embarked"].fillna(data["Embarked"].mode()[0])
data["Sex"] = data["Sex"].map({"male": 0, "female": 1})
data = pd.get_dummies(data, columns=["Embarked"], drop_first=True)

X = data.drop("Survived", axis=1).astype(float).values
y = data["Survived"].values.reshape(-1, 1)

rng = np.random.RandomState(42)
indices = rng.permutation(len(X))
split = int(0.8 * len(X))

train_idx = indices[:split]
test_idx = indices[split:]

X_train = X[train_idx]
X_test = X[test_idx]
y_train = y[train_idx]
y_test = y[test_idx]

mean = X_train.mean(axis=0)
std = X_train.std(axis=0)
std[std == 0] = 1

X_train = (X_train - mean) / std
X_test = (X_test - mean) / std

def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1 / (1 + np.exp(-z))

def binary_cross_entropy(y_true, y_pred):
    eps = 1e-9
    y_pred = np.clip(y_pred, eps, 1 - eps)
    loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
    return loss

def accuracy(y_true, y_pred):
    y_class = (y_pred >= 0.5).astype(int)
    return np.mean(y_class == y_true)

def train_logistic_regression(X, y, learning_rate=0.05, epochs=2000):
    m, n = X.shape
    X_bias = np.hstack((np.ones((m, 1)), X))
    w = np.zeros((n + 1, 1))

    loss_history = []
    acc_history = []

    for epoch in range(epochs):
        z = X_bias @ w
        y_pred = sigmoid(z)

        loss = binary_cross_entropy(y, y_pred)
        grad = (X_bias.T @ (y_pred - y)) / m
        w = w - learning_rate * grad

        loss_history.append(loss)
        acc_history.append(accuracy(y, y_pred))

    return w, loss_history, acc_history

weights, loss_history, acc_history = train_logistic_regression(
    X_train,
    y_train,
    learning_rate=0.05,
    epochs=2000
)

X_test_bias = np.hstack((np.ones((X_test.shape[0], 1)), X_test))
test_probs = sigmoid(X_test_bias @ weights)
test_acc = accuracy(y_test, test_probs)
test_loss = binary_cross_entropy(y_test, test_probs)

print("Кількість ознак:", X_train.shape[1])
print("Кількість ваг з bias:", len(weights))
print("Фінальна втрата на train:", loss_history[-1])
print("Фінальна точність на train:", acc_history[-1])
print("Втрата на test:", test_loss)
print("Точність на test:", test_acc)

plt.figure(figsize=(8, 5))
plt.plot(loss_history)
plt.xlabel("Епоха")
plt.ylabel("Loss")
plt.title("Зміна функції втрат під час тренування")
plt.grid(True)
plt.show()

plt.figure(figsize=(8, 5))
plt.plot(acc_history)
plt.xlabel("Епоха")
plt.ylabel("Accuracy")
plt.title("Зміна точності моделі під час тренування")
plt.grid(True)
plt.show()