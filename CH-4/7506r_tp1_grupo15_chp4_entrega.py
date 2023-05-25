# -*- coding: utf-8 -*-
"""7506R_TP1_GRUPO15_CHP4_ENTREGA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YQIYprAk1YbCC1pOqKRQsulIINzYOJsQ

# Imports y Preparacion del dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn as sk
import sklearn.preprocessing as skp
import scipy.stats as stats
import scipy as sc
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_selection import VarianceThreshold
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression, LogisticRegressionCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
#joblib
#from joblib import dump, load
import joblib

# multivariado   
from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.neighbors import DistanceMetric

from sklearn import metrics

from sklearn.metrics import precision_score, recall_score, accuracy_score,f1_score#, precision_recall_curve, roc_curve, 
#KNN
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

#
from sklearn.model_selection import GridSearchCV, StratifiedKFold,KFold
from sklearn.metrics import make_scorer

from sklearn.model_selection import train_test_split

###
import tensorflow as tf
from tensorflow import keras
from keras.utils.vis_utils import plot_model

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('/content/drive/MyDrive/Datasetss/hotels_train_processed.csv') 
df_test= pd.read_csv('/content/drive/MyDrive/Datasetss/hotels_test_processed_with_id .csv')

features = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights',
       'adults', 'children', 'babies', 'is_repeated_guest',
       'previous_cancellations', 'previous_bookings_not_canceled',
       'booking_changes', 'agent', 'days_in_waiting_list',
       'average_daily_rate', 'required_car_parking_spaces',
       'total_of_special_requests', 'assigned_equals_reserved',
       'temporada_alta', 'hotel_Resort Hotel', 'meal_FB', 'meal_HB', 'meal_SC',
       'deposit_type_Non Refund', 'deposit_type_Refundable',
       'customer_type_Group', 'customer_type_Transient',
       'customer_type_Transient-Party', 'country_BEL', 'country_BRA',
       'country_CHE', 'country_CHN', 'country_CN', 'country_DEU',
       'country_ESP', 'country_FRA', 'country_GBR', 'country_IRL',
       'country_ISR', 'country_ITA', 'country_NLD', 'country_NOR',
       'country_OTHER', 'country_POL', 'country_PRT', 'country_RUS',
       'country_SWE', 'country_USA', 'distribution_channel_Direct',
       'distribution_channel_GDS', 'distribution_channel_TA/TO',
       'market_segment_Complementary', 'market_segment_Corporate',
       'market_segment_Direct', 'market_segment_Groups',
       'market_segment_Offline TA/TO', 'market_segment_Online TA']

features_without_dummies = ['lead_time', 'stays_in_weekend_nights', 'stays_in_week_nights',
       'adults', 'children', 'babies', 'previous_cancellations', 'previous_bookings_not_canceled',
       'booking_changes', 'agent', 'days_in_waiting_list',
       'average_daily_rate','required_car_parking_spaces','total_of_special_requests']

"""# Checkpoint 4

## Preparacion
"""

colummas_predictoras = df[features]
target = df['is_canceled']

x_train, x_test, y_train, y_test = train_test_split(colummas_predictoras,target,test_size=0.2, random_state=22)

sscaler=StandardScaler() #NORMALIZO
sscaler.fit(pd.DataFrame(x_train[features_without_dummies]))
x_train_transform_1=sscaler.transform(pd.DataFrame(x_train[features_without_dummies]))
x_test_transform_1=sscaler.transform(pd.DataFrame(x_test[features_without_dummies]))

x_train['lead_time'] = x_train_transform_1[:,0]

x_train['stays_in_weekend_nights'] = x_train_transform_1[:,1]
x_train['stays_in_week_nights'] = x_train_transform_1[:,2]
x_train['adults'] = x_train_transform_1[:,3]
x_train['children'] = x_train_transform_1[:,4]
x_train['babies'] = x_train_transform_1[:,5]
x_train['previous_cancellations'] = x_train_transform_1[:,6]
x_train['previous_bookings_not_canceled'] = x_train_transform_1[:,7]
x_train['booking_changes'] = x_train_transform_1[:,8]
x_train['agent'] = x_train_transform_1[:,9]
x_train['days_in_waiting_list'] = x_train_transform_1[:,10]
x_train['average_daily_rate'] = x_train_transform_1[:,11]
x_train['required_car_parking_spaces'] = x_train_transform_1[:,12]
x_train['total_of_special_requests'] = x_train_transform_1[:,13]


x_test['lead_time'] = x_test_transform_1[:,0]
x_test['stays_in_weekend_nights'] = x_test_transform_1[:,1]
x_test['stays_in_week_nights'] = x_test_transform_1[:,2]
x_test['adults'] = x_test_transform_1[:,3]
x_test['children'] = x_test_transform_1[:,4]
x_test['babies'] = x_test_transform_1[:,5]
x_test['previous_cancellations'] = x_test_transform_1[:,6]
x_test['previous_bookings_not_canceled'] = x_test_transform_1[:,7]
x_test['booking_changes'] = x_test_transform_1[:,8]
x_test['agent'] = x_test_transform_1[:,9]
x_test['days_in_waiting_list'] = x_test_transform_1[:,10]
x_test['average_daily_rate'] = x_test_transform_1[:,11]
x_test['required_car_parking_spaces'] = x_test_transform_1[:,12]
x_test['total_of_special_requests'] = x_test_transform_1[:,13]

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

"""# SGD (Modelo 1)

Tomamos nuestro primer modelo usando SGD como parametro dado que no es el mejor optimizador, esperamos que los otros modelos sean mejores que este
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)

modelo_hotels_1 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,)),
    keras.layers.Dense(1, activation='sigmoid')])

modelo_hotels_1.summary()

modelo_hotels_1.compile(optimizer=keras.optimizers.SGD(learning_rate=0.001), loss='binary_crossentropy', metrics=[f1_m])


cant_epochs_hotels=100
modelo_hotels1_historia = modelo_hotels_1.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=50,verbose=False)

y_predic_1 = modelo_hotels_1.predict(x_test)
y_predic_cat_1 = np.where(y_predic_1>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_1, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_1

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones = modelo_hotels_1.predict(x_predic)

predicciones = np.where(predicciones>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red1.csv', index=False)

joblib.dump(modelo_hotels_1, 'red1.pkl')

"""# Adam (Modelo 2)

Ahora decido usar un mejor optimizador Adam, que combina a los optimizadores:Momentum + RMSProp
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)

modelo_hotels_2 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,)),
    keras.layers.Dense(1, activation='sigmoid')])

modelo_hotels_2.summary()

modelo_hotels_2.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='binary_crossentropy', metrics=[f1_m])


cant_epochs_hotels=100
modelo_hotels2_historia = modelo_hotels_2.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=50,verbose=False)

y_predic_2 = modelo_hotels_2.predict(x_test)
y_predic_cat_2 = np.where(y_predic_2>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_2, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_2

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones2 = modelo_hotels_2.predict(x_predic)

predicciones2 = np.where(predicciones2>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones2[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red2.csv', index=False)

joblib.dump(modelo_hotels_2,'red2.pkl')

"""# Adam - MSE(Modelo 3)

Cambiamos la funcion de error a el error cuadratico medio MSE
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)

modelo_hotels_3 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,)),
    keras.layers.Dense(1, activation='sigmoid')])

modelo_hotels_3.summary()

modelo_hotels_3.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='mse', metrics=[f1_m])


cant_epochs_hotels=100
modelo_hotels3_historia = modelo_hotels_3.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=50,verbose=False)

y_predic_3 = modelo_hotels_3.predict(x_test)
y_predic_cat_3 = np.where(y_predic_3>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_3, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_3

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones3 = modelo_hotels_3.predict(x_predic)

predicciones3 = np.where(predicciones3>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones3[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red3.csv', index=False)

joblib.dump(modelo_hotels_3, 'modelo_redes3.csv')

"""Concluimos que el f1score me da mejor usando funcion loss= 'mse' que 'binary_crossentropy'. Aunque la diferencia no es mucha, decidimos usarlo para los modelos siguientes.

# Busqueda de Hiperparametros(cant epochs, batch)
"""

!pip install scikeras

from keras.wrappers.scikit_learn import KerasClassifier   #o Sci-Keras!!!

from scikeras.wrappers import KerasClassifier

# Create the sklearn model for the network

def create_model():
    modelo = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,)),
    keras.layers.Dense(1, activation='sigmoid')])
    #PUEDE SER COSTOSO A NIVEL COMPUTACIONAL
    modelo.compile(
      optimizer=keras.optimizers.SGD(learning_rate=0.001), 
      loss='binary_crossentropy', 
      # metricas para ir calculando en cada iteracion o batch 
      metrics=[f1_m], 
    )
    
    return modelo

modelo_cv = KerasClassifier(model=create_model) #GUARDAMOS TODA LA FUNCION

"""# Primera prueba de hiperparametros

Usamos Grid Search para optimizar cantidad de epocas y batches. Este algoritmo tiene costo computacional, dado que a diferencia de RandomSearch va evaluando cada una de las opciones.
"""

from sklearn.model_selection import GridSearchCV 

epochs = [10, 30,50]
batches = [100, 200, 500] #Mejor modelo: 0.783130 {'batch_size': 100, 'epochs': 50}

param_grid = dict( epochs=epochs, batch_size=batches)

print(param_grid)

grid = GridSearchCV(estimator=modelo_cv, param_grid=param_grid)
grid_result = grid.fit(x_train,y_train)

print("Mejor modelo: %f %s" % (grid_result.best_score_, grid_result.best_params_))

"""Seguimos buscando mejores hiperparametros

# Segunda Busqueda de Hiperparametros

En esta seccion, nos basamos de los mejores parametros obtenidos anteriormente y decidimos agregar mas epochs(iteraciones) y darle otros valores al batch
"""

from sklearn.model_selection import GridSearchCV #QUE OPTIMICE LA CANT DE EPOCAS Y BATCHES


epochs = [50, 100]
batches = [75,100, 200]
param_grid = dict( epochs=epochs, batch_size=batches)#Mejor modelo: 0.798804 {'batch_size': 75, 'epochs': 100}

print(param_grid)

grid = GridSearchCV(estimator=modelo_cv, param_grid=param_grid)
grid_result = grid.fit(x_train,y_train)

print("Mejor modelo: %f %s" % (grid_result.best_score_, grid_result.best_params_))

"""Con los mejores parametros obtenidos procedemos a entrenar nuestro modelo.

## Adam

### Sigmoid(Modelo 4)
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)

modelo_hotels_4 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,)),
    keras.layers.Dense(1, activation='sigmoid')])

modelo_hotels_4.summary()

modelo_hotels_4.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='mse', metrics=[f1_m])


cant_epochs_hotels=100
modelo_hotels4_historia = modelo_hotels_4.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=75,verbose=False)

y_predic_4 = modelo_hotels_4.predict(x_test)
y_predic_cat_4 = np.where(y_predic_4>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_4, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_4

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones4 = modelo_hotels_4.predict(x_predic)

predicciones4[:,0].size

predicciones4 = np.where(predicciones4>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones4[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones4[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red4.csv', index=False)

joblib.dump(modelo_hotels_4, 'red4_grid.pkl')

"""### Relu

#### 2 capas ocultas( Modelo 5)
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)
d_out = 1

modelo_hotels_5 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,), activation="relu"),
    keras.layers.Dense(2, activation='relu'), # 2 capas ocultas 
    keras.layers.Dense(d_out, )])

modelo_hotels_5.summary()

modelo_hotels_5.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='mse', metrics=[f1_m])


cant_epochs_hotels=100
modelo_hotels5_historia = modelo_hotels_5.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=75,verbose=False)

y_predic_5 = modelo_hotels_5.predict(x_test)
y_predic_cat_5 = np.where(y_predic_5>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_5, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_5

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones5 = modelo_hotels_5.predict(x_predic)

predicciones5[:,0].size

predicciones5 = np.where(predicciones5>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones5[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones5[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red5.csv', index=False)

joblib.dump(modelo_hotels_5, 'red5_grid.csv')

"""#### 32 capas ocultas, Early Stopping (Modelo 6)

Decido aumentar la cantidad de capas ocultas, dado que me parece un buen numero entre la cantidad de entradas y salida
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)
d_out = 1

modelo_hotels_6 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,), activation="relu"),
    keras.layers.Dense(32, activation='relu'), # 2 capas ocultas 
    keras.layers.Dense(d_out, ),
    ]
    )

modelo_hotels_6.summary()

modelo_hotels_6.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='mse', metrics=[f1_m])
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5)

cant_epochs_hotels=100
modelo_hotels6_historia = modelo_hotels_6.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=75,callbacks=[callback],verbose=False)

y_predic_6 = modelo_hotels_6.predict(x_test)
y_predic_cat_6 = np.where(y_predic_6>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_6, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_6

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones6 = modelo_hotels_6.predict(x_predic)

predicciones6[:,0].size

predicciones6 = np.where(predicciones6>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones6[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones6[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red6.csv', index=False)

joblib.dump(modelo_hotels_6, 'red6_grid.pkl')

"""### Sigmoid + Relu

#### 32 capas ocultas, Early Stopping(Modelo 7)

*   Elemento de lista
*   Elemento de lista
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)
d_out = 1

modelo_hotels_7 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,), activation="sigmoid"),
    keras.layers.Dense(32, activation='relu'), # 2 capas ocultas 
    keras.layers.Dense(d_out, ),
    ]
    )

modelo_hotels_7.summary()

modelo_hotels_7.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999), loss='mse', metrics=[f1_m])
callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5)

cant_epochs_hotels=100
modelo_hotels7_historia = modelo_hotels_7.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=75,callbacks=[callback],verbose=False)

y_predic_7 = modelo_hotels_7.predict(x_test)
y_predic_cat_7 = np.where(y_predic_7>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_7, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_7

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones7 = modelo_hotels_7.predict(x_predic)

predicciones7[:,0].size

predicciones7 = np.where(predicciones7>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones7[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones7[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red7.csv', index=False)

joblib.dump(modelo_hotels_7, 'red7_grid.pkl')

"""Concluimos que de los modelos entrenados con los mejores hiperpametros hallados por GridSearch. El mejor basado en el mejor f1 score fue el modeo 6. Este usa funcion de activacion Relu.

## Nadam

### Relu

#### 32 capas ocultas, Early Stopping(Modelo 8)
"""

# calcula la cantidad de clases
cant_clases=len(np.unique(y_train))
d_in=len(x_train.columns)
d_out = 1

modelo_hotels_8 = keras.Sequential([
    keras.layers.Dense(1,input_shape=(d_in,), activation="relu"),
    keras.layers.Dense(32, activation='relu'), # 2 capas ocultas 
    keras.layers.Dense(d_out, ),
    ]
    )

modelo_hotels_8.summary()

modelo_hotels_8.compile(optimizer=keras.optimizers.Nadam(learning_rate=0.001,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07), loss='mse', metrics=[f1_m])

callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5)

cant_epochs_hotels=100
modelo_hotels8_historia = modelo_hotels_8.fit(x_train,y_train,epochs=cant_epochs_hotels,batch_size=75,callbacks=[callback],verbose=False)

y_predic_8 = modelo_hotels_8.predict(x_test)
y_predic_cat_8 = np.where(y_predic_8>0.4,1,0)

ds_validacion=pd.DataFrame(y_predic_cat_8, y_test).reset_index()
ds_validacion.columns=['y_pred','y_real']

tabla=pd.crosstab(ds_validacion.y_pred, ds_validacion.y_real)
grf=sns.heatmap(tabla,annot=True, cmap = 'Blues')
plt.show()

y_predic_cat_8

ds_validacion.y_pred

print('accuracy: ' + str(accuracy_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('f1_score: ' + str(f1_score(ds_validacion.y_pred,ds_validacion.y_real)))
print('recall: '+ str(recall_score(ds_validacion.y_pred, ds_validacion.y_real)))
print('precision: '+str(precision_score(ds_validacion.y_pred,ds_validacion.y_real)))

x_predic = df_test[features]
sscaler=StandardScaler()
sscaler.fit(pd.DataFrame(df_test[features_without_dummies]))
x_predic_transform=sscaler.transform(pd.DataFrame(x_predic[features_without_dummies]))

pd.Series(x_predic_transform[:,0])

predicciones8 = modelo_hotels_8.predict(x_predic)

predicciones8[:,0].size

predicciones8 = np.where(predicciones8>0.4,1,0) #deberia dar 0 o 1 SI MAS DEL 40% EL MODELO TE DEFINE QUE CANCELA LA RESERVA

predicciones8[:,0].size

df_submission = pd.DataFrame({'id':df_test['id'], 'is_canceled':predicciones8[:,0]})
df_submission.head()
df_submission.shape

df_submission.to_csv('/content/drive/MyDrive/submissions/submission_red8.csv', index=False)

joblib.dump(modelo_hotels_8, 'red8_grid.pkl')