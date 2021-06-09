#!/usr/bin/env python
# coding: utf-8

# ## Integration von Arbeitslosenzahlen auf Bundeslandebene

# In[163]:


# Autor: Roman Schulze
# Datenquelle: Bundesagentur für Arbeit


# In[164]:


# Bibliotheken importieren
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join


# In[165]:


# Liste aller Datein 
files = [f for f in listdir("Arbeitslose") if isfile(join("Arbeitslose", f))]


# ### 1. Funktionen zur Formattierung und Bereinigung der Daten

# In[168]:


# Formattierung der Daten
def get_data_formatted(df, key=1, val="Arbeitslose_Mai19"):
    df.loc[0, "Unnamed: 1"] = " "
    df.drop(index=5, inplace=True)
    df.reset_index(drop=True, inplace=True)
    mask = df.loc[:, "Unnamed: 0"]  == "© Statistik der Bundesagentur für Arbeit"
    ind_pos = mask[mask==True].index[0] + 1
    df = df.iloc[0:ind_pos, :]
    df = df.rename(columns={"Unnamed: 0":"Berufsbereich","Unnamed: 1":"Berufe", "Unnamed: 2":"Anforderungsniveau", key:val})
    df = df.loc[:, ["Berufsbereich","Berufe","Anforderungsniveau", val]]
    df["Berufsgruppe"] = df["Berufsbereich"] + " " + df["Berufe"]
    cols = ["Berufsgruppe", "Anforderungsniveau", val]
    df = df[cols]
    df.Berufsgruppe = df.Berufsgruppe.fillna(method='ffill')
    df["Anforderungsniveau"] = df["Anforderungsniveau"].str.strip()
    return df


# In[169]:


# Transformation der Daten mithilfe der Pivot-Tabelle
def transform_data(df, val="Arbeitslose_Mai19"):
    table = pd.pivot_table(df, values=val, index=["Berufsgruppe"], columns=["Anforderungsniveau"], aggfunc=np.sum)
    flattened = pd.DataFrame(table.to_records())
    return flattened


# In[170]:


# Sortierung der Spalten & Datentypassung
def convert_data(df):
    cols = ["Jahr", "Berufsgruppe", "Gesamt", "Helfer", "Fachkraft", "Spezialist", "Experte"]
    df = df[cols]
    # Bereinigung der Daten
    df.replace("* ", np.nan, inplace=True)
    df.replace("- ", np.nan, inplace=True)
    for col in df.columns:
        if col not in ["Jahr", "Berufsgruppe"]:
            df[col] = df[col].astype("float64")
    df = df.sort_values(by=["Jahr", "Berufsgruppe"])
    return df


# ### 2. Laden und Zusammenführung der Daten

# In[171]:


# Lade Daten für jeden Zeitpunkt 
list_of_dataframes_1 = []
list_of_dataframes_2 = []

for file in files:
    
    df = pd.read_excel("Arbeitslose/" + file, sheet_name="1.12", header = 14, nrows=1000)
    
    df_1 = get_data_formatted(df, val=file[0:20])
    df_1 = transform_data(df_1, val=file[0:20])
    df_1["Jahr"] = file[12:20].replace("_", " ")
    list_of_dataframes_1.append(df_1)
    
    df_2 = get_data_formatted(df, key=9, val="gem. Stellen")
    df_2 = transform_data(df_2, val="gem. Stellen")
    df_2["Jahr"] = file[12:20].replace("_", " ")
    list_of_dataframes_2.append(df_2)

# Anmerkung: Berechnung nimmt einige Minuten in Anspruch.


# In[172]:


# Zusammenführen aller individuellen Dataframes in einen ganzen
df_1 = pd.concat(list_of_dataframes_1)


# In[173]:


# Zusammenführen aller individuellen Dataframes in einen ganzen
df_2 = pd.concat(list_of_dataframes_2)


# In[176]:


# finale Anpassungen
df_1 = convert_data(df_1)
df_2 = convert_data(df_2)


# In[177]:


# Erste fünf Zeilen des ersten dfs
df_1.head()


# In[178]:


# Erste fünf Zeilen des zweiten dfs
df_2.head()


# In[179]:


# Zusammenführung der Datensätze
df_all=pd.merge(df_1, df_2.iloc[:, 0:3], how='left', left_on=["Jahr","Berufsgruppe"], right_on=["Jahr","Berufsgruppe"], 
                suffixes=["_Alo", "_gem_Stellen"])


# In[180]:


# erste fünf Zeilen
df_all.head()


# In[181]:


# Format
df_all.shape


# In[182]:


# Matching Id
df_all["ID"] = np.nan


# In[183]:


# generiere Matching-ID für matching mit Beschäftigten-Daten
df_all.loc[df_all.Jahr == "Apr 2019", "ID"] = "Sep 2018"


# In[185]:


# dictionary mit allen Paarungen: Beschäftigte & Alos
dic = {"Jun 2018": ["Mrz 2019"], 
       "Sep 2018": ["Apr 2019", "Mai 2019", "Jun 2019"],
       "Dez 2018": ["Jul 2019", "Aug 2019", "Sep 2019"],
       "Mrz 2019": ["Okt 2019", "Nov 2019", "Dez 2019"],
       "Jun 2019": ["Jan 2020", "Feb 2020", "Mrz 2020"],
       "Sep 2019": ["Apr 2020", "Mai 2020", "Jun 2020"],
       "Dez 2019": ["Jul 2020", "Aug 2020", "Sep 2020"],
       "Mrz 2020": ["Okt 2020", "Nov 2020", "Dez 2020"],
       "Jun 2020": ["Jan 2021", "Feb 2021", "Mrz 2021"],
       "Sep 2020": ["Apr 2021", "Mai 2021"]
      }


# In[187]:


# generiere Matching-ID für matching mit Beschäftigten-Daten
for element in dic:
        for value in dic[element]:
            df_all.loc[df_all["Jahr"] == value, "ID"] = element


# In[188]:


# erste fünf Zeilen 
df_all.head()


# ###### Speicherung der Daten als Excel Datei

# In[189]:


# ALs Excel File speichern
df_all.to_excel("generierte Datensätze/Arbeitslose_nach_BL.xlsx")  


# In[ ]:




