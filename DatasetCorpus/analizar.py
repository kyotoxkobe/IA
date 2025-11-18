import pandas as pd
from textblob import TextBlob
import scipy.stats as stats

# Cargar el dataset
df = pd.read_csv('DatasetCorpus/datasetTexto.csv')

# Filtrar solo las filas de la categoría "Frankenstein"
df_frank = df[df['Categoria'] == 'Frankenstein']

# Analizar sentimiento de los comentarios
def get_sentiment(text):
    analysis = TextBlob(str(text))
    if analysis.sentiment.polarity > 0.1:
        return 'positivo'
    elif analysis.sentiment.polarity < -0.1:
        return 'negativo'
    else:
        return 'neutro'

df_frank.loc[:, 'Sentimiento'] = df_frank['Comentario_Reaccion'].apply(get_sentiment)

# Estadísticas descriptivas
total = len(df_frank)
positivos = (df_frank['Sentimiento'] == 'positivo').sum()
negativos = (df_frank['Sentimiento'] == 'negativo').sum()
neutros = (df_frank['Sentimiento'] == 'neutro').sum()

# Proporciones
prop_positivos = positivos / total
prop_negativos = negativos / total

# Prueba de hipótesis: ¿La proporción de opiniones positivas es significativamente mayor que la de negativas?
result = stats.binomtest(positivos, n=positivos+negativos, p=0.5, alternative='greater')
p_value = result.pvalue

# Conclusiones
print(f"Total de opiniones analizadas: {total}")
print(f"Opiniones positivas: {positivos} ({prop_positivos:.2%})")
print(f"Opiniones negativas: {negativos} ({prop_negativos:.2%})")
print(f"Opiniones neutras: {neutros} ({neutros/total:.2%})")
print("\nConclusión sobre una posible secuela:")

if prop_positivos > 0.6 and p_value < 0.05:
    print("La mayoría de las opiniones son positivas y estadísticamente significativas. Es probable que el público acepte una secuela de Frankenstein.")
elif prop_positivos > prop_negativos:
    print("Predominan las opiniones positivas, lo que sugiere una buena aceptación de una posible secuela.")
else:
    print("No hay suficiente evidencia para afirmar que una secuela sería bien recibida.")

if p_value is not None:
    print(f"p-valor de la prueba binomial: {p_value:.4f}")