import pandas as pd

acc_fijo_tec_loc = pd.read_csv('data/Accesos_a_Internet_fijo_por_tecnologia_y_localidad.csv')

test = acc_fijo_tec_loc['DIAL UP']
tipo = type(test[0])
muestra = test[0:50]
print(muestra, '\nSu tipo de dato es: ', tipo)
