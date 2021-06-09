#!/usr/bin/env python
# coding: utf-8

# ## Integration von Beschäftigtenzahlen auf Bundeslandebene 

# In[147]:


# Autor: Roman Schulze
# Datenquelle: Bundesagentur für Arbeit


# In[148]:


# Bibliotheken importieren
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join


# In[149]:


# Liste aller Datein 
files = [f for f in listdir("Beschäftigte") if isfile(join("Beschäftigte", f))]


# ### 1. Funktionen zur Formattierung und Bereinigung der Daten

# In[150]:


# Formattierung der Daten
def get_data_formatted(df):
    try:
        mask = df.loc[:, "Unnamed: 0"]  == "Keine Zuordnung möglich"
        ind_pos = mask[mask==True].index[0] + 1
        df = df.iloc[0:ind_pos, :]
        df = df.iloc[1:, :]
        df.drop(index=2, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.rename(columns={"Unnamed: 0":"Berufsgruppe","Unnamed: 1":"Insgesamt"}, inplace=True)
    except IndexError:
        mask = df.loc[:, "Unnamed: 0"]  == "Sonstige / Keine Angabe"        
        ind_pos = mask[mask==True].index[0] + 1
        df = df.iloc[0:ind_pos, :]
        df = df.iloc[1:, :]
        df.drop(index=2, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.rename(columns={"Unnamed: 0":"Berufsgruppe","Unnamed: 1":"Insgesamt"}, inplace=True)
    return df


# In[151]:


# Bereinigung der Daten
def clean_data(df):
    df.replace("*", np.nan, inplace=True)
    for col in df.columns:
        if col not in ["Berufsgruppe"]:
            df[col] = df[col].astype("float64")
    return df


# ### 2. Laden und Zusammenführung der Daten - aGB

# In[152]:


# Lade Daten für jeden Zeitpunkt 
list_of_dataframes = []
for file in files:
    df = pd.read_excel("Beschäftigte/" + file, sheet_name="aGB - Tabelle II", header = 9, nrows=300)
    df = get_data_formatted(df)
    df = clean_data(df)
    df["Jahr"] = file[20:28].replace("_", " ")
    list_of_dataframes.append(df)


# In[153]:


# Auflistung der Bundesländer
# Bundesländer = ["Bayern_Beschäftigte_Jun_2019"]


# In[155]:


# Zusammenführen aller individuellen Dataframes in einen ganzen
df_all = pd.concat(list_of_dataframes)


# In[156]:


# Überprüfung des Formats
for element in list_of_dataframes:
    print(element.shape)


# In[158]:


# Sortierung der Spalten
cols = list(df_all.columns)
cols = [cols[-1]] + cols[:-1]
df_all = df_all[cols]


# In[159]:


# ID variable zum matchen
df_all["ID"] = df_all.Jahr


# In[160]:


# Ausgabe des finalen Dataframes
df_all.shape


# ##### Speicherung der Daten als Excel Datei

# In[161]:


# ALs Excel File speichern
df_all.to_excel("generierte Datensätze/aGB_Beschäftigte_nach_BL.xlsx")  


# ### 3. Laden und Zusammenführung der Daten - SVB

# In[162]:


# Lade Daten für jeden Zeitpunkt 
list_of_dataframes = []
for file in files:
    df = pd.read_excel("Beschäftigte/" + file, sheet_name="SVB - Tabelle II", header = 9, nrows=300)
    df = get_data_formatted(df)
    df = clean_data(df)
    df["Jahr"] = file[20:28].replace("_", " ")
    list_of_dataframes.append(df)


# In[164]:


# Zusammenführen aller individuellen Dataframes in einen ganzen
df_all = pd.concat(list_of_dataframes)


# In[165]:


# Überprüfung des Formats
for element in list_of_dataframes:
    print(element.shape)


# In[166]:


# Sortierung der Spalten
cols = list(df_all.columns)
cols = [cols[-1]] + cols[:-1]
df_all = df_all[cols]


# In[167]:


# ID variable zum matchen
df_all["ID"] = df_all.Jahr


# In[168]:


# Ausgabe des finalen Dataframes
df_all.head()


# ##### Speicherung der Daten als Excel Datei

# In[169]:


# ALs Excel File speichern
df_all.to_excel("generierte Datensätze/SVB_Beschäftigte_nach_BL.xlsx") 


# In[170]:


# Anmerkung: Beim Öffnen der Excel Datei in Excel, entsprechen leere Zellen Missings (NaN) im Dataframe


# In[ ]:




