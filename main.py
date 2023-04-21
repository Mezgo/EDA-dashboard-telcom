import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import seaborn as sns

acc_fijo_tec_loc = pd.read_csv(
    'data/Accesos_a_Internet_fijo_por_tecnologia_y_localidad.csv')

print('#######\nANALIZANDO "ACCESOS A INTERNET POR  TECNOLOGIA Y LOCALIDAD"\n#######')

# analizar composicion
cols = acc_fijo_tec_loc.columns
shape = acc_fijo_tec_loc.shape

print(f'MUESTRA\n {acc_fijo_tec_loc.head()}\n')
print(f'SHAPE\n{shape}\n')
print(f'COLUMNAS\n{cols}\n')

# analizando datos

print(f' COMPOSICION\n{acc_fijo_tec_loc.describe()}')


