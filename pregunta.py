"""
Ingestión de datos - Reporte de clusteres
-----------------------------------------------------------------------------------------

Construya un dataframe de Pandas a partir del archivo 'clusters_report.txt', teniendo en
cuenta que los nombres de las columnas deben ser en minusculas, reemplazando los espacios
por guiones bajos; y que las palabras clave deben estar separadas por coma y con un solo 
espacio entre palabra y palabra.


"""

# python -m venv .venv
# .venv\Scripts\activate
# python.exe -m pip install --upgrade pip
# pip3 install pyarrow pandas

import pandas as pd


def ingest_data():

    # Leemos el archivo como ancho fijo
    df = pd.read_fwf("clusters_report.txt",widths=[9, 16, 16, 76])
    
    # Corregimos los nombres de las columnas
    df.columns = df.columns + " " + list(df.iloc[0])
    df.columns = [columna.replace(" nan", "").replace(" ", "_").lower() for columna in df.columns]
    
    # Eliminamos las dos primeras filas
    df = df.iloc[2:]
    df.reset_index(inplace=True, drop=True)
    
    # Corregimos la columna de principales_palabras_clave
    # Concatenamos las palabras clave si la columna 'cluster' es NaN
    for i in range(1, len(df)):
        if pd.isna(df.loc[i, 'cluster']):
            df.loc[i, 'principales_palabras_clave'] = df.loc[i - 1, 'principales_palabras_clave'] + ' ' + df.loc[i, 'principales_palabras_clave']

    # Filtramos solo las filas donde 'cluster' no es NaN
    df = df[df['cluster'].notna()]
    
    # Eliminamos los dobles espacios
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('   ', ' ').str.replace('  ', ' ')
    df.reset_index(inplace=True, drop=True)
    
    return df

print(ingest_data())