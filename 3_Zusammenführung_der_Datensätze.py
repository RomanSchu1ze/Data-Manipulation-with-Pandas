#!/usr/bin/env python
# coding: utf-8

# ## Zusammenführung der Beschäftigungs- und Arbeitslosenzahlen in eine einheitliche Datenmatrix

# In[462]:


# Bibliotheken
import numpy as np
import pandas as pd


# In[463]:


# laden und vorformatieren Daten 

# Arbeitslose und Stellen
df_alo = pd.read_excel("generierte Datensätze/Arbeitslose_nach_BL.xlsx", index_col=0)
df_alo.rename(columns={'Gesamt': 'Insgesamt'}, inplace=True)
df_alo['Berufsgruppe'] = df_alo['Berufsgruppe'].str.strip()

# ausschließlich geringfügig Beschäftigte 
df_agb = pd.read_excel("generierte Datensätze/aGB_Beschäftigte_nach_BL.xlsx", index_col=0)
Id = df_agb.iloc[:, -1]
df_agb = df_agb.iloc[:, :7]
df_agb["ID"] = Id

# sozialversicherungspflichtig Beschäftigte
df_svb = pd.read_excel("generierte Datensätze/SVB_Beschäftigte_nach_BL.xlsx", index_col=0)
Id = df_svb.iloc[:, -1]
df_svb = df_svb.iloc[:, :9]
df_svb["ID"] = Id
df_svb.drop(["in Vollzeit", "in Teilzeit"], axis=1, inplace=True)


# In[464]:


# erste fünf Zeilen Alo
df_alo.head()


# In[465]:


# erste fünf Zeilen agB
df_agb.head()


# In[466]:


# erste fünf Zeilen svb
df_svb.head()


# In[467]:


# Format der SVB Daten, entspricht dem Format der aGB Daten
df_svb.shape


# In[468]:


# Format der Alo Daten
df_alo.shape


# In[469]:


# Merge von SVB und agB
result = pd.merge(df_svb, df_agb, how="outer", on=["ID", "Berufsgruppe"], suffixes=["_svB", "_agB"])


# In[470]:


# erste fünf Zeilen
result.head()


# In[471]:


# Merge von alo und Kombination aus svb und agB
final = pd.merge(result, df_alo, how="outer", on=["ID", "Berufsgruppe"])


# In[472]:


# erste 5 Zeilen der finalen Datenmatrix
final.head()


# In[474]:


# Format des finalen Datensatzes
final.shape


# ###### Speicherung der Daten als Excel Datei

# In[475]:


# ALs Excel File speichern
final.to_excel("generierte Datensätze/Datensatz_komplett.xlsx") 


# In[ ]:




