#!/usr/bin/env python
# coding: utf-8

# ## gemeldete Stellen

# In[32]:


# Bibliotheken
import numpy as np
import pandas as pd


# In[33]:


# Daten einlesen
df = pd.read_excel("generierte Datensätze/Datensatz_komplett.xlsx", index_col=0)


# In[34]:


# erste fünf Zeilen
df.head()


# In[35]:


# definiere technische Berufe
Technische_Berufe  = df.Berufsgruppe.isin(["24 Metallerzeugung,-bearbeitung, Metallbau", 
                                "25 Maschinen- und Fahrzeugtechnikberufe", 
                                "26 Mechatronik-, Energie- u. Elektroberufe"])


# In[36]:


# definiere Verkehrsberufe
Verkehr_Logistikberufe = df.Berufsgruppe.isin(["51 Verkehr, Logistik (außer Fahrzeugführ.)", 
                                                  "52 Führer von Fahrzeug- u. Transportgeräten"])


# In[37]:


# definiere Gastgewerbeberufe
Gastgewerbeberufe = df.Berufsgruppe.isin(["632 Hotellerie", "633 Gastronomie"])


# In[38]:


# definiere Elektroberufe
Elektroberufe = df.Berufsgruppe.isin(["262 Energietechnik", "263 Elektrotechnik"])


# In[39]:


# Berechne Arbeitslosenquote nach Berufsgruppe und Zeitpunkt
def get_stellen(data, Berufsgruppe, label):
    stellen_liste = []
    Jahre = []
    for element in data.Jahr.unique():
        sub = data[Berufsgruppe]
        sub = sub.loc[sub.Jahr==element, :]
        stellen = sub["Gesamt_gem_Stellen"].sum()
        stellen_liste.append(stellen)
        Jahre.append(element)    
    df_stellen = pd.DataFrame({"Zeitpunkt":Jahre, "DB Berufsgruppe":label, "gemeldete Stellen":stellen_liste})
    return df_stellen


# In[40]:


# Elektroberufe
df_elektro = get_stellen(df, Elektroberufe, "Elektroberufe")


# In[41]:


# technische Berufe
df_tech = get_stellen(df, Technische_Berufe, "Technische Berufe")


# In[42]:


# Verkehr und Logistik
df_verkehr = get_stellen(df, Verkehr_Logistikberufe, "Verkehr -/ Logistikberufe")


# In[43]:


# Gastgewerberufe
df_gg = get_stellen(df, Gastgewerbeberufe, "Gastgewerbeberufe")


# In[44]:


# Zusammenführung
df = pd.concat([df_elektro, df_tech, df_verkehr, df_gg])


# In[45]:


# Missings entfernen
df = df.dropna()


# In[46]:


# erste fünf Zeilen
df.head()


# In[47]:


# Monat
df["Monat"] = df.Zeitpunkt.str[:3]


# In[48]:


# Jahr
df["Jahr"] = df.Zeitpunkt.str[4:8]


# In[49]:


# kreiere neue Spalte: Monat als Zahl
df["Monat Zahl"] = df.Monat.replace(
                     ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",],
                     ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
)


# In[50]:


# Kreeire neue Datum Spalte
df["Datum"] = df["Jahr"] + "-" + df["Monat Zahl"] + "-" + "1"


# In[51]:


# konvertiere Strinf zu Datum
df["Datum"] = pd.to_datetime(df.Datum, format="%Y-%m-%d")


# In[53]:


# Filter dataframe
df = df[["Datum", "DB Berufsgruppe", "gemeldete Stellen"]]


# In[54]:


# soritere daten nach Berufsgruppe und Datum
df_sorted = df.sort_values(by=["DB Berufsgruppe", "Datum"])


# In[55]:


# erste fünf Zeilen
df_sorted.head()


# In[56]:


# ALs Excel File speichern
df_sorted.to_excel("generierte Datensätze/gem_Stellen_Zeitreihe.xlsx") 


# In[ ]:




