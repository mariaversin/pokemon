import os 
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.model_selection import train_test_split



pd.set_option('display.max_columns', None)

nuestrosPokemon = pd.read_csv("src/datas/pokedex.csv")
nuestrosPokemon['LEGENDARIO'] = (nuestrosPokemon['LEGENDARIO']=='VERDADERO').astype(int)

combates = pd.read_csv("src/datas/combates.csv")

primeraPosicion = combates.groupby('Primer_Pokemon').count()
segundaPosicion = combates.groupby('Segundo_Pokemon').count()
cantidadTotalCombates = primeraPosicion + segundaPosicion
cantidadVictorias = combates.groupby('Pokemon_Ganador').count()

listaAgregar = combates.groupby('Pokemon_Ganador').count()
listaAgregar.sort_index()

listaAgregar['NUM_COMBATES'] = primeraPosicion.Pokemon_Ganador + segundaPosicion.Pokemon_Ganador
listaAgregar['NUM_VICTORIAS'] = cantidadVictorias.Primer_Pokemon
listaAgregar['PORCENTAJE_DE_VICTORIAS'] = cantidadVictorias.Primer_Pokemon/(primeraPosicion.Pokemon_Ganador + segundaPosicion.Pokemon_Ganador) 
nuevoPokedex = nuestrosPokemon.merge(listaAgregar, left_on="NUMERO", right_index=True, how="left")

nuevoPokedex.drop('NOMBRE', inplace=True, axis=1)

dataset = nuevoPokedex
dataset.to_csv("src/datas/dataset.csv", sep="\t")

dataset = pd.read_csv("src/datas/dataset.csv", delimiter='\t')
dataset = dataset.dropna(axis=0, how="any")


# Variables predicticas (X) y la variable que hay que predecir (y)
X = dataset.iloc[:,4:11].values
y = dataset.iloc[:, 16].values
# TRAIN AND TEST
X_TRAIN, X_TEST, Y_TRAIN, Y_TEST = train_test_split(X, y, test_size = 0.2, random_state = 0)
print("\n\n")

# - - - -   A L G O R I T M O S  - - - - 


from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression 
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import joblib


models = {
    "Linear Regression" : LinearRegression(),
    "Decision Tree" : DecisionTreeRegressor(),
    "Random Forest" : RandomForestRegressor()
}

accuracy = []
for modelName, model in models.items():
    print(f"Training model: {modelName}")
    model.fit(X_TRAIN, Y_TRAIN)
    prediccion = model.predict(X_TEST)
    precision = r2_score(Y_TEST, prediccion)
    accuracy.append({
        "modelName" : modelName,
        "accuracy" : precision,
        "model" : model
    })
max_acc = max(accuracy, key=lambda x:x['accuracy'])

print('El mejor algoritmo es: ', max_acc['modelName'], 'con un accuracy de: ', max_acc['accuracy'])

archivo = 'src/modelo/modelo_pokemon.mod'
joblib.dump(max_acc['model'], archivo)