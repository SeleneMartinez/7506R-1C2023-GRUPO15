# -*- coding: utf-8 -*-
"""7506R_TP2_GRUPO15_ENTREGA.ipynb.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zaDlwJgaxIPZVv_IaUCW1IosuVGYwc4S

# Preparacion
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, classification_report, f1_score, recall_score
from sklearn.model_selection import cross_val_score, RepeatedStratifiedKFold
from sklearn.preprocessing import LabelEncoder

import seaborn as sns
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold,KFold
from sklearn.metrics import make_scorer
from sklearn.ensemble import RandomForestClassifier
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

import joblib
from google.colab import drive

#drive

drive.mount("/content/drive")

#datasets
df = pd.read_csv('/content/drive/MyDrive/Datasets_Datos/train.csv')
df_test = pd.read_csv('/content/drive/MyDrive/Datasets_Datos/test.csv')
df_test_original = df_test.copy()
df_original = df.copy()

df.columns

df

"""# Preprocesamiento"""

X_train, X_test, y_train, y_test = train_test_split(df.review_es,
                                                   df.sentimiento,
                                                   test_size = 0.30,
                                                   random_state=25,
                                                   shuffle=True)

"""# Modelo Bayes Naive"""

model1 = make_pipeline(TfidfVectorizer(), MultinomialNB())
model2 = make_pipeline(CountVectorizer(), MultinomialNB())

model1.fit(X_train, y_train)
model2.fit(X_train, y_train)

predicted_categories1 = model1.predict(X_test)
predicted_categories2 = model2.predict(X_test)

y_test

predicted_categories1

print("The f1score using TfidfVectorizer  is {}".format(f1_score(y_test,predicted_categories1 ,average='micro',)))
print("The accuracy using TfidfVectorizer  is {}".format(accuracy_score(y_test, predicted_categories1)))
print("The precision is TfidfVectorizer {}".format(precision_score(y_test, predicted_categories1, average='micro',)))
print("The recall TfidfVectorizer is {}".format(recall_score(y_test, predicted_categories1, average='micro',)))
print("The f1score countVectorizer is  {}".format(f1_score(y_test, predicted_categories2,average='micro',)))
print("The accuracy countVectorizer is  {}".format(accuracy_score(y_test, predicted_categories2)))
print("The precision countVectorizer is {}".format(precision_score(y_test, predicted_categories2, average='micro',)))
print("The recall countVectorizer is {}".format(recall_score(y_test, predicted_categories2, average='micro',)))

"""Por lo que vemos que usando el modelo de TfidVectorizer nos da un mejor accurcay y precision"""

tabla = confusion_matrix(y_test, predicted_categories1)
sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = model1.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_bn.csv', index=False)

joblib.dump(model1, '/content/drive/MyDrive/pkl/naive_bayes_tfidvectorizer.pkl')

"""## Busqueda de hiperparametros

"""

spanish_stop_words = list(set(stopwords.words('spanish'))) ## ELIMINARRR

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups

spanish_stop_words = list(set(stopwords.words('spanish')))

# Definir el pipeline con vectorizador y clasificador
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# Definir la cuadrícula de hiperparámetros a explorar
param_grid = {
    'vectorizer__max_features': [1000, 5000],
    'classifier__alpha': [0.1, 1.0, 10.0],
    'vectorizer__stop_words': [None, spanish_stop_words],
}

# Realizar la búsqueda de cuadrícula con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=5,scoring='f1_macro')
grid_search.fit(X_train, y_train)

# Imprimir los resultados
print("Mejores hiperparámetros encontrados:")
print(grid_search.best_params_)
print("Mejor puntuación f1 score de validación cruzada:")
print(grid_search.best_score_)

predicted_categories = grid_search.predict(X_test)

predicted_categories

tabla = confusion_matrix(y_test, predicted_categories)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = grid_search.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_gs1.csv', index=False)

joblib.dump(grid_search, '/content/drive/MyDrive/pkl/naive_bayes_cross_valgs1.pkl')

"""## Segunda Busqueda de Hiperparametros"""

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups


# Definir el pipeline con vectorizador y clasificador
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Definir la cuadrícula de hiperparámetros a explorar
param_grid = {
    'vectorizer__max_features': [1000, 5000],
    'classifier__alpha': [0.1, 0.5, 1.0, 10.0],
    'vectorizer__stop_words': [None, spanish_stop_words],
}

# Realizar la búsqueda de cuadrícula con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=5,scoring='f1_macro')
grid_search.fit(X_train, y_train)

# Imprimir los resultados
print("Mejores hiperparámetros encontrados:")
print(grid_search.best_params_)
print("Mejor puntuación f1 score de validación cruzada:")
print(grid_search.best_score_)

predicted_categories = grid_search.predict(X_test)

tabla = confusion_matrix(y_test, predicted_categories)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = grid_search.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_gs2.csv', index=False)

joblib.dump(grid_search, '/content/drive/MyDrive/pkl/naive_bayes_cross_val_2.pkl')

"""## Tercera busqueda"""

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups


# Definir el pipeline con vectorizador y clasificador
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Definir la cuadrícula de hiperparámetros a explorar
param_grid = {
    'vectorizer__max_features': [1000, 5000, 6000, 9000],
    'classifier__alpha': [0.0001, 0.001, 0.01, 0.1, 1.0],
    'vectorizer__stop_words': [None, spanish_stop_words],
}

# Realizar la búsqueda de cuadrícula con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=5,scoring='f1_macro')
grid_search.fit(X_train, y_train)

# Imprimir los resultados
print("Mejores hiperparámetros encontrados:")
print(grid_search.best_params_)
print("Mejor puntuación f1 score de validación cruzada:")
print(grid_search.best_score_)

predicted_categories = grid_search.predict(X_test)

tabla = confusion_matrix(y_test, predicted_categories)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = grid_search.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_gs3_bn.csv', index=False)

joblib.dump(grid_search, '/content/drive/MyDrive/pkl/naive_bayes_cross_val_3.pkl')

"""## Cuarta busqueda"""

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups


# Definir el pipeline con vectorizador y clasificador
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Definir la cuadrícula de hiperparámetros a explorar
param_grid = {
    'vectorizer__max_features': [20000, 30000, 40000],
    'classifier__alpha': [0.01, 0.1, 1.0],
    'vectorizer__stop_words': [None, spanish_stop_words],
}

# Realizar la búsqueda de cuadrícula con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=5,scoring='f1_macro')
grid_search.fit(X_train, y_train)

# Imprimir los resultados
print("Mejores hiperparámetros encontrados:")
print(grid_search.best_params_)
print("Mejor puntuación f1 score de validación cruzada:")
print(grid_search.best_score_)

predicted_categories = grid_search.predict(X_test)

tabla = confusion_matrix(y_test, predicted_categories)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = grid_search.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_gs5_bn.csv', index=False)

joblib.dump(grid_search, '/content/drive/MyDrive/pkl/naive_bayes_cross_val_5.pkl')

"""## Preprocesamiento del database

"""

from keras.wrappers.scikit_learn import KerasClassifier

pip install Unidecode

pip install langdetect

pip install spacy

import spacy

!python -m spacy download es_core_news_sm

nlp = spacy.load("es_core_news_sm")

from langdetect import detect

from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from tensorflow import keras
import tensorflow as tf
from keras import layers
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import FunctionTransformer
from unidecode import unidecode
import re

def solo_espanol(data):
  reviews = data.review_es
  datitaset = data.copy()
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      datitaset = datitaset.drop(data.index[i])
  return datitaset



def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def preprocess_text(text):
    # Tokenize text into individual words
    tokens = nltk.word_tokenize(text.lower())
    # Remove stopwords
    stop_words_espanol = set(stopwords.words('spanish'))

    tokens = [token for token in tokens if token not in stop_words_espanol]
    text = " ".join([word for word in tokens if unidecode(word) == word])

    return text

def solo_espanol_test(data):
  reviews = data.review_es
  datitaset = data.copy()
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      print(x, i)
      datitaset = datitaset.drop(data.index[i])
  return datitaset

def obtener_id_no_espanol(data):
  reviews = data.review_es
  ids = []
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      print(x)
      ids.append(i)
  return ids

def lemmatizacion(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    lemmas = " ".join(lemmas)
    return lemmas

dataset = solo_espanol(df)

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(dataset.sentimiento)

cleaned_texts = [clean_text(text) for text in dataset.review_es]
preprocessed_texts = [preprocess_text(text) for text in cleaned_texts]

lemmas =  [lemmatizacion(text) for text in preprocessed_texts]

labels = pd.DataFrame(encoded_labels, columns=["sentimiento"])

reviews_train, reviews_test, labels_train, labels_test = train_test_split(lemmas, labels, test_size=0.2, random_state=42)

"""## Tercera Busqueda de hiperparametros"""

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.datasets import fetch_20newsgroups

spanish_stop_words = list(set(stopwords.words('spanish')))

# Definir el pipeline con vectorizador y clasificador
pipeline = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

# Definir la cuadrícula de hiperparámetros a explorar
param_grid = {
    'vectorizer__max_features': [1000, 5000],
    'classifier__alpha': [0.1, 1.0, 10.0],
    'vectorizer__stop_words': [None, spanish_stop_words],
}

# Realizar la búsqueda de cuadrícula con validación cruzada
grid_search = GridSearchCV(pipeline, param_grid, cv=5,scoring='f1_macro')
grid_search.fit(reviews_train, labels_train.sentimiento)

# Imprimir los resultados
print("Mejores hiperparámetros encontrados:")
print(grid_search.best_params_)
print("Mejor puntuación f1 score de validación cruzada:")
print(grid_search.best_score_)

predicted_categories = grid_search.predict(reviews_test)

len(predicted_categories)

tabla = confusion_matrix(labels_test.sentimiento, predicted_categories)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

print("The f1score countVectorizer is  {}".format(f1_score(labels_test.sentimiento, predicted_categories,average='micro',)))
print("The accuracy countVectorizer is  {}".format(accuracy_score(labels_test.sentimiento, predicted_categories)))
print("The precision countVectorizer is {}".format(precision_score(labels_test.sentimiento, predicted_categories, average='micro',)))
print("The recall countVectorizer is {}".format(recall_score(labels_test.sentimiento, predicted_categories, average='micro',)))

"""### df test sin porocesar"""

y_pred = grid_search.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_gs_naivebayes_crossval_hiperparametros3.csv', index=False)

joblib.dump(grid_search, '/content/drive/MyDrive/pkl/naive_bayes_cross_val_tercera_busqueda_countvect.pkl')

"""# Modelo Random Forest

## Modelo Base
"""

rf = RandomForestClassifier()

model3 = make_pipeline(TfidfVectorizer(), rf)
model4 = make_pipeline(CountVectorizer(), rf)

model3.fit(X_train, y_train)
model4.fit(X_train, y_train)

#predicted_categories = model3.predict(X_test)
predicted_categories3 = model3.predict(X_test)
predicted_categories4 = model4.predict(X_test)

print("The f1score using TfidfVectorizer  is {}".format(f1_score(y_test,predicted_categories3 ,average='micro',)))
print("The accuracy using TfidfVectorizer  is {}".format(accuracy_score(y_test, predicted_categories3)))
print("The precision is TfidfVectorizer {}".format(precision_score(y_test, predicted_categories3, average='micro',)))
print("The f1score countVectorizer is  {}".format(f1_score(y_test, predicted_categories4,average='micro',)))
print("The accuracy countVectorizer is  {}".format(accuracy_score(y_test, predicted_categories4)))
print("The precision countVectorizer is {}".format(precision_score(y_test, predicted_categories4, average='micro',)))

"""Por lo que decidimos quedarnos con el CountVectorizer"""

tabla = confusion_matrix(y_test, predicted_categories4)

sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

y_pred = model4.predict(df_test.review_es)

#df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
#df_submission.to_csv('/content/drive/MyDrive/submissions/submission_2.csv', index=False)

#joblib.dump(model4, '/content/drive/MyDrive/pkl/rf_base_countvectorizer.pkl')

"""## Tokenizer+CountVectorizer"""

import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import f1_score
from scipy.stats import randint

# Descargar recursos adicionales de NLTK
nltk.download('punkt')

# Dataset de ejemplo
textos = X_test
etiquetas = y_test  # Etiquetas correspondientes a cada texto

# Tokenizar los textos
textos_tokenizados = [word_tokenize(texto) for texto in textos]

# Crear un vectorizador de palabras
vectorizador = CountVectorizer()

# Obtener la matriz de características
matriz_caracteristicas = vectorizador.fit_transform([' '.join(tokens) for tokens in textos_tokenizados])

# Crear un clasificador de Random Forest
clf = RandomForestClassifier()

# Definir los hiperparámetros a ajustar
parametros = {
    'n_estimators': randint(10, 100),
    'max_depth': randint(2, 10),
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5)
}

# Definir una función de puntuación personalizada usando F1 score
def f1_scoring(estimator, X, y):
    y_pred = estimator.predict(X)
    return f1_score(y, y_pred, pos_label='positivo')

# Realizar la búsqueda de hiperparámetros con la función de puntuación personalizada
busqueda = RandomizedSearchCV(clf, parametros, n_iter=10, cv=3, scoring=f1_scoring)
busqueda.fit(matriz_caracteristicas, etiquetas)

# Obtener los mejores hiperparámetros y el mejor modelo
mejores_hiperparametros = busqueda.best_params_
mejor_modelo = busqueda.best_estimator_

print(mejores_hiperparametros)

# Realizar predicciones con el mejor modelo
nuevo_texto = X_test
nuevo_texto_tokenizado = [word_tokenize(texto) for texto in nuevo_texto]
nueva_matriz_caracteristicas = vectorizador.transform([' '.join(tokens) for tokens in nuevo_texto_tokenizado])
prediccion = mejor_modelo.predict(nueva_matriz_caracteristicas)

print("Mejores hiperparámetros:", mejores_hiperparametros)
print("Predicción:", prediccion)

len(prediccion)

tabla = confusion_matrix(y_test, prediccion)
sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

print("The accuracy :{}".format(accuracy_score(y_test, prediccion)))

# Realizar predicciones con el mejor modelo
nuevo_texto = df_test.review_es
nuevo_texto_tokenizado = [word_tokenize(texto) for texto in nuevo_texto]
nueva_matriz_caracteristicas = vectorizador.transform([' '.join(tokens) for tokens in nuevo_texto_tokenizado])
y_predict = mejor_modelo.predict(nueva_matriz_caracteristicas)

print("Mejores hiperparámetros:", mejores_hiperparametros)
print("Predicción:", prediccion)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_predict})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_rf_tc.csv', index=False)

import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

# Descargar recursos adicionales de NLTK
nltk.download('punkt')

# Dataset de ejemplo
textos = df.
etiquetas = [0, 1, 0]  # Etiquetas correspondientes a cada texto

# Tokenizar los textos
textos_tokenizados = [word_tokenize(texto) for texto in textos]

# Crear un vectorizador de palabras
vectorizador = CountVectorizer()

# Obtener la matriz de características
matriz_caracteristicas = vectorizador.fit_transform([' '.join(tokens) for tokens in textos_tokenizados])

# Crear un clasificador de Random Forest
clf = RandomForestClassifier()

# Entrenar el clasificador
clf.fit(matriz_caracteristicas, etiquetas)

# Realizar predicciones
nuevo_texto = "Este es un nuevo texto para predecir."
nuevo_texto_tokenizado = word_tokenize(nuevo_texto)
nueva_matriz_caracteristicas = vectorizador.transform([' '.join(nuevo_texto_tokenizado)])
prediccion = clf.predict(nueva_matriz_caracteristicas)

print(prediccion)

"""## Procesamiento"""

def clean(text):
    wn = nltk.WordNetLemmatizer()
    stopword = stopwords.words('spanish')
    tokens = nltk.word_tokenize(text)
    lower = [word.lower() for word in tokens]
    no_stopwords = [word for word in lower if word not in stopword]
    no_alpha = [word for word in no_stopwords if word.isalpha()]
    lemm_text = [wn.lemmatize(word) for word in no_alpha]
    clean_text = lemm_text
    return clean_text

df['clean']=df['review_es'].map(clean)

def vectorize(data,tfidf_vect_fit):
    X_tfidf = tfidf_vect_fit.transform(data)
    words = tfidf_vect_fit.get_feature_names_out()
    X_tfidf_df = pd.DataFrame(X_tfidf.toarray())
    X_tfidf_df.columns = words
    return(X_tfidf_df)

tfidf_vect = TfidfVectorizer(analyzer=clean)
tfidf_vect_fit=tfidf_vect.fit(X_train)
X_train=vectorize(X_train,tfidf_vect_fit)

y_train=vectorize(y_train,tfidf_vect_fit)

params_grid = { "criterion" : ["gini", "entropy"],
               "min_samples_leaf" : [1, 5, 10],
               "min_samples_split" : [2, 4, 10, 12, 16],
               "n_estimators": [10,20, 50] }

clf = make_pipeline(CountVectorizer(),
                    RandomizedSearchCV(rf,
                                 params_grid,
                                 scoring='f1', n_iter=10,
                                random_state=5))

clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

#Creo matriz de confusión
tabla=confusion_matrix(y_test,y_pred)

#Grafico matriz de confusión
sns.heatmap(tabla, cmap='Blues',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

#Reporte
print(classification_report(y_test,y_pred))

y_pred = clf.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_4.csv', index=False)

joblib.dump(clf, '/content/drive/MyDrive/pkl/rf_base_countvectorizer_random_search.pkl')

"""# Modelo XGBoost

## Preparacion
"""

#Creo el modelo y lo entreno

import xgboost as xgb

xgb_model = xgb.XGBClassifier(random_state=0, n_estimators=100)

dataset = pd.get_dummies(df, columns=["sentimiento"], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(dataset['review_es'],
                                                   dataset['sentimiento_positivo'],
                                                   test_size = 0.30,
                                                   random_state=25,
                                                   shuffle=True)

"""## Modelo Base"""

model5 = make_pipeline(CountVectorizer(), xgb_model)

model5.fit(X_train, y_train)

#Matriz de Confusion
y_pred=model5.predict(X_test)

cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm, cmap='Blues',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

#Reporte
print(classification_report(y_test,y_pred))

#Matriz de Confusion
y_pred=model5.predict(df_test.review_es)

df_submission.loc[df_submission.loc[:,"sentimiento"]== 1,"sentimiento"]="positivo"
df_submission.loc[df_submission.loc[:,"sentimiento"]== 0,"sentimiento"]="negativo"

df_submission

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.loc[df_submission.loc[:,"sentimiento"]== 1,"sentimiento"]="positivo"
df_submission.loc[df_submission.loc[:,"sentimiento"]== 0,"sentimiento"]="negativo"

df_submission

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_5.csv', index=False)

joblib.dump(model5, '/content/drive/MyDrive/pkl/XGBOOST__base_countvectorizer_.pkl')

"""##Busqueda de hiperparametros

"""

param_grid = {
    'n_estimators': [100, 200, 300],  # Number of trees in the forest
    'max_depth': [3, 5, 7],  # Maximum depth of each tree
    'learning_rate': [0.1, 0.01, 0.001]  # Learning rate
}

clf = make_pipeline(CountVectorizer(),
                    RandomizedSearchCV(xgb_model,
                                 param_grid,
                                 scoring='f1', n_iter=10,
                                random_state=5))

clf.fit(X_train, y_train)

#Matriz de Confusion
y_pred=clf.predict(X_test)

cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm, cmap='Blues',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

#Reporte
print(classification_report(y_test,y_pred))

#Matriz de Confusion
y_pred=clf.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.loc[df_submission.loc[:,"sentimiento"]== 1,"sentimiento"]="positivo"
df_submission.loc[df_submission.loc[:,"sentimiento"]== 0,"sentimiento"]="negativo"

df_submission

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_6.csv', index=False)

joblib.dump(model5, '/content/drive/MyDrive/pkl/XGBOOST__GridSearch_countvectorizer_.pkl')

"""## Otros hiperparametros"""

param_grid = {
    # Percentage of columns to be randomly samples for each tree.
    "colsample_bytree": [ 0.3, 0.5 , 0.8 ],
    # reg_alpha provides l1 regularization to the weight, higher values result in more conservative models
    "reg_alpha": [0, 0.5, 1, 5],
    # reg_lambda provides l2 regularization to the weight, higher values result in more conservative models
    "reg_lambda": [0, 0.5, 1, 5],
    'learning_rate': [0.012]
    }

# Set up the k-fold cross-validation
kfoldcv = StratifiedKFold(n_splits=10)

#Ramdom Search CV
randomcv = RandomizedSearchCV(xgb.XGBClassifier(), param_grid, n_jobs=10, scoring='f1',cv=kfoldcv, n_iter=10)

clf = make_pipeline(CountVectorizer(),
                    RandomizedSearchCV(xgb_model,
                                 param_grid,
                                 scoring='f1', n_iter=10,
                                random_state=5))

clf.fit(X_train, y_train)

#Matriz de Confusion
y_pred=clf.predict(X_test)

cm = confusion_matrix(y_test,y_pred)
sns.heatmap(cm, cmap='Blues',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

#Reporte
print(classification_report(y_test,y_pred))

#Matriz de Confusion
y_pred=clf.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':y_pred})
df_submission.loc[df_submission.loc[:,"sentimiento"]== 1,"sentimiento"]="positivo"
df_submission.loc[df_submission.loc[:,"sentimiento"]== 0,"sentimiento"]="negativo"

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_10.csv', index=False)

joblib.dump(clf, '/content/drive/MyDrive/pkl/XGBOOST__GridSearch_countvectorizer_cross_val.pkl')

df_submission

"""# Red Neuronal

## Preparacion
"""

pip install Unidecode

pip install langdetect

pip install spacy

import spacy

!python -m spacy download es_core_news_sm

nlp = spacy.load("es_core_news_sm")

from langdetect import detect

from sklearn.preprocessing import LabelEncoder
from nltk.corpus import stopwords
from tensorflow import keras
import tensorflow as tf
from keras import layers
from keras.preprocessing.text import Tokenizer
from sklearn.preprocessing import FunctionTransformer
from unidecode import unidecode
import re

from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

def solo_espanol(data):
  reviews = data.review_es
  datitaset = data.copy()
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      datitaset = datitaset.drop(data.index[i])
  return datitaset



def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^a-zA-Z ]', '', text)
    return text

def preprocess_text(text):
    # Tokenize text into individual words
    tokens = nltk.word_tokenize(text.lower())
    # Remove stopwords
    stop_words_espanol = set(stopwords.words('spanish'))
    stop_words_ingles = set(stopwords.words('english'))

    tokens = [token for token in tokens if token not in stop_words_espanol]
    text = " ".join([word for word in tokens if unidecode(word) == word])

    return text

def solo_espanol_test(data):
  reviews = data.review_es
  datitaset = data.copy()
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      print(x, i)
      datitaset = datitaset.drop(data.index[i])
  return datitaset

def obtener_id_no_espanol(data):
  reviews = data.review_es
  ids = []
  for i, x in enumerate(reviews):
    if(detect(x) != 'es'):
      print(x)
      ids.append(i)
  return ids

def lemmatizacion(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc]
    lemmas = " ".join(lemmas)
    return lemmas

reviews_train, reviews_test, labels_train, labels_test = train_test_split(df.review_es, df.sentimiento, test_size=0.2, random_state=42)

"""Nos quedamos con las reviews que estan en español"""

dataset = solo_espanol(df)

"""Transformamos la columna de sentimientos en 0 y 1"""

label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(dataset.sentimiento)

labels = pd.DataFrame(encoded_labels, columns=["sentimiento"])

"""Limpiamos las reviews con clean texts eliminando numeros, caracteres especiales, tildes.
Con preprocessed text transformamos el texto a minuscula y quitamos las stop-words
"""

cleaned_texts = [clean_text(text) for text in dataset.review_es]
preprocessed_texts = [preprocess_text(text) for text in cleaned_texts]

preprocessed_texts

"""Utilizamos la lematizacion para transformar las palabras y devolverlas a su palabra raiz"""

lemmas =  [lemmatizacion(text) for text in preprocessed_texts]

lemmas

"""Separamos en train y test"""

reviews_train, reviews_test, labels_train, labels_test = train_test_split(lemmas, labels, test_size=0.2, random_state=42)

"""Utilizamos CountVectorizer para tokenizar y contar las ocurrencias, seleccionamos 0.25 como minimo para eliminar las palabras que menos aparecen y como maximo 0.70 para eliminar palabras que aparecen en 70% o mas de las reviews ya que pueden ser conectores."""

vectorizer = CountVectorizer(min_df=0.25, max_df=0.7)
X_train_transformed = vectorizer.fit_transform(reviews_train)
X_test_transformed = vectorizer.transform(reviews_test)

"""Creamos el modelo y lo compilamos"""

modelo = keras.Sequential([
    keras.layers.Dense(1,input_dim=X_train_transformed.shape[1]),
    keras.layers.Dense(1, activation='sigmoid')])

modelo.compile(optimizer=keras.optimizers.SGD(learning_rate=0.001), loss='binary_crossentropy', metrics="accuracy")

"""Entrenamos el modelo"""

modelo.fit(X_train_transformed.toarray(), labels_train.sentimiento,epochs=100,batch_size=50,verbose=False)

"""Analizamos"""

y_predic_1 = modelo.predict(X_test_transformed.toarray())
y_predic_cat_1 = np.where(y_predic_1>0.49, 1,0)

data = pd.Series(labels_test.sentimiento)

ds_validacion=pd.DataFrame(y_predic_cat_1, data).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

print("The f1score countVectorizer is  {}".format(f1_score(labels_test, y_predic_cat_1,average='micro',)))
print("The accuracy countVectorizer is  {}".format(accuracy_score(labels_test, y_predic_cat_1)))
print("The precision countVectorizer is {}".format(precision_score(labels_test, y_predic_cat_1, average='micro',)))
print("The recall countVectorizer is {}".format(recall_score(labels_test, y_predic_cat_1, average='micro',)))

"""## Predicciones"""

df_test

datatest = solo_espanol_test(df_test)

datatest

cleaned_texts_test = [clean_text(text) for text in datatest.review_es]
preprocessed_texts_test = [preprocess_text(text) for text in cleaned_texts_test]

lemmastest =  [lemmatizacion(text) for text in preprocessed_texts_test]

X_predict_transformed = vectorizer.transform(lemmastest)

y_predicciones = modelo.predict(X_predict_transformed.toarray())

y_predic_cat_2 = np.where(y_predicciones>0.4, 1,0)

ids = obtener_id_no_espanol(df_test)

predicciones = pd.DataFrame(y_predic_cat_2)

predicciones_sentimiento = pd.DataFrame({'sentimiento': predicciones.iloc[:,0]})

df_submission = pd.DataFrame()

df_submission['id'] = datatest['ID']

df_submission

df_submission['sentimiento'] = predicciones_sentimiento['sentimiento']

df_submission.isna().sum()

df_submission['sentimiento'] = df_submission['sentimiento'].fillna(0)

"""Reemplazamos la fila que fue eliminada a la hora de quitar las filas que no estaban en español.
Elegimos positivo porque la mayoria eran positivas
"""

new_row = pd.DataFrame({'id':[61048], 'sentimiento':[1.0]})

new_row

df_submission_1 = pd.concat([df_submission.iloc[:1048], new_row, df_submission.iloc[1048:]]).reset_index(drop=True)

df_submission_1['sentimiento'].replace(to_replace = 0, value = 'negativo', inplace=True)
df_submission_1['sentimiento'].replace(to_replace = 1, value = 'positivo', inplace=True)
df_submission_1

df_submission_1.to_csv('/content/drive/MyDrive/submissions/submission_red_neuronal.csv', index=False)

df_submission_1

"""## Probamos con otro minimo y maximo de CountVectorizer y da mejor"""

reviews_train, reviews_test, labels_train, labels_test = train_test_split(lemmas, labels, test_size=0.2, random_state=42)

vectorizer = CountVectorizer(min_df=0.20, max_df=0.85)
X_train_transformed = vectorizer.fit_transform(reviews_train)
X_test_transformed = vectorizer.transform(reviews_test)

modelo = keras.Sequential([
    keras.layers.Dense(1,input_dim=X_train_transformed.shape[1]),
    keras.layers.Dense(1, activation='sigmoid')])

modelo.compile(optimizer=keras.optimizers.SGD(learning_rate=0.001), loss='binary_crossentropy', metrics="accuracy")

modelo.fit(X_train_transformed.toarray(), labels_train.sentimiento,epochs=100,batch_size=50,verbose=False)

y_predic_1 = modelo.predict(X_test_transformed.toarray())
y_predic_cat_1 = np.where(y_predic_1>0.49, 1,0)

data = pd.Series(labels_test.sentimiento)

ds_validacion=pd.DataFrame(y_predic_cat_1, data).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

print("The f1score countVectorizer is  {}".format(f1_score(labels_test, y_predic_cat_1,average='micro',)))
print("The accuracy countVectorizer is  {}".format(accuracy_score(labels_test, y_predic_cat_1)))
print("The precision countVectorizer is {}".format(precision_score(labels_test, y_predic_cat_1, average='micro',)))
print("The recall countVectorizer is {}".format(recall_score(labels_test, y_predic_cat_1, average='micro',)))

"""# Ensamble

## Voting

### Preparacion
"""

from sklearn.ensemble import VotingClassifier

from sklearn.linear_model import LinearRegression, LogisticRegressionCV
from sklearn.ensemble import StackingClassifier

xgboost_model = joblib.load('/content/drive/MyDrive/pkl/XGBOOST__GridSearch_countvectorizer_cross_val.pkl')
bn_model = joblib.load('/content/drive/MyDrive/pkl/naive_bayes_cross_valgs1.pkl')
rf_model = joblib.load('/content/drive/MyDrive/pkl/rf_base_countvectorizer_random_search.pkl')

reviews_train, reviews_test, labels_train, labels_test = train_test_split(df.review_es, df.sentimiento, test_size=0.2, random_state=42)

label_encoder = LabelEncoder()
encoded_labels_train = label_encoder.fit_transform(labels_train)
encoded_labels_test = label_encoder.fit_transform(labels_test)

#Creo ensemble de Votación
vot_clf = VotingClassifier(estimators = [('xgb', xgboost_model), ('nb', bn_model), ('rf', rf_model)], voting = 'hard')

#Entreno el ensemble
vot_clf.fit(reviews_train, encoded_labels_train)

#Evaluo en conjunto de test
pred = vot_clf.predict(reviews_test)
accuracy_score(encoded_labels_test, pred)

tabla = confusion_matrix(encoded_labels_test, pred)
sns.heatmap(tabla,cmap='GnBu',annot=True,fmt='g')
plt.xlabel('Predicted')
plt.ylabel('True')

"""### Prediccion"""

prediccion = vot_clf.predict(df_test.review_es)

df_submission = pd.DataFrame({'id':df_test['ID'], 'sentimiento':prediccion})
df_submission['sentimiento'].replace(to_replace = 0, value = 'negativo', inplace=True)
df_submission['sentimiento'].replace(to_replace = 1, value = 'positivo', inplace=True)
df_submission.to_csv('/content/drive/MyDrive/submissions/submission_bvoting_tp2.csv', index=False)