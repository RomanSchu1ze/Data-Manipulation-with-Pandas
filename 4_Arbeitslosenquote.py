#!/usr/bin/env python
# coding: utf-8

# ## Berechnung der Arbeitslosenquote

# In[29]:


# Bibliotheken laden
import numpy as np
import pandas as pd


# In[30]:


# Daten einlesen
df = pd.read_excel("generierte Datensätze/Datensatz_komplett.xlsx", index_col=0)


# In[31]:


# erste fünf Zeilen
df.head()


# In[4]:


# Format dataframe
df.shape


# In[5]:


# definiere technische Berufe
Technische_Berufe  = df.Berufsgruppe.isin(["24 Metallerzeugung,-bearbeitung, Metallbau", 
                                "25 Maschinen- und Fahrzeugtechnikberufe", 
                                "26 Mechatronik-, Energie- u. Elektroberufe"])


# In[6]:


# definiere Verkehrsberufe
Verkehr_Logistikberufe = df.Berufsgruppe.isin(["51 Verkehr, Logistik (außer Fahrzeugführ.)", 
                                                  "52 Führer von Fahrzeug- u. Transportgeräten"])


# In[7]:


# definiere Gastgewerbeberufe
Gastgewerbeberufe = df.Berufsgruppe.isin(["632 Hotellerie", "633 Gastronomie"])


# In[8]:


# definiere Elektroberufe
Elektroberufe = df.Berufsgruppe.isin(["262 Energietechnik", "263 Elektrotechnik"])


# In[9]:


# Berechne Arbeitslosenquote nach Berufsgruppe und Zeitpunkt
def get_alo(data, Berufsgruppe, label):
    alo_liste = []
    Jahre = []
    for element in data.Jahr.unique():
        sub = data[Berufsgruppe]
        sub = sub.loc[sub.Jahr==element, :]
        if label == "Gastgewerbeberufe":
                    alo = (sub.Fachkraft.sum() + sub.Helfer.sum())  / (sub.Fachkraft.sum() + sub.Helfer.sum() + 
                            sub.Fachkraft_svB.sum() + sub.Helfer_svB.sum() + 
                            sub.Fachkraft_agB.sum() + sub.Helfer_agB.sum()) * 100
        else:
            alo = sub.Fachkraft.sum() / (sub.Fachkraft.sum() + sub.Fachkraft_svB.sum() + sub.Fachkraft_agB.sum()) * 100      
        alo_liste.append(alo)
        Jahre.append(element)    
    df_alo = pd.DataFrame({"Zeitpunkt":Jahre, "DB Berufsgruppe":label, "Arbeitslosenquote":alo_liste})
    return df_alo


# In[10]:


# Elektroberufe
df_elektro = get_alo(df, Elektroberufe, "Elektroberufe")


# In[11]:


# technische Berufe
df_tech = get_alo(df, Technische_Berufe, "Technische Berufe")


# In[12]:


# Verkehr und Logistik
df_verkehr = get_alo(df, Verkehr_Logistikberufe, "Verkehr -/ Logistikberufe")


# In[13]:


# Gastgewerberufe
df_gg = get_alo(df, Gastgewerbeberufe, "Gastgewerbeberufe")


# In[14]:


# Zusammenführung der Dataframes in eine Gesamtübersicht
df = pd.concat([df_elektro, df_tech, df_verkehr, df_gg])


# In[15]:


# Missings entfernen
df = df.dropna()


# In[16]:


# erste fünf Zeilen
df.head()


# In[17]:


# Monat
df["Monat"] = df.Zeitpunkt.str[:3]


# In[18]:


# Jahr
df["Jahr"] = df.Zeitpunkt.str[4:8]


# In[19]:


# kreiere neue Spalte: Monat als Zahl
df["Monat Zahl"] = df.Monat.replace(
                     ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",],
                     ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
)


# In[20]:


# Kreeire neue Datum Spalte
df["Datum"] = df["Jahr"] + "-" + df["Monat Zahl"] + "-" + "1"


# In[21]:


# konvertiere Strinf zu Datum
df["Datum"] = pd.to_datetime(df.Datum, format="%Y-%m-%d")


# In[22]:


# Filter dataframe
df = df[["Datum", "DB Berufsgruppe", "Arbeitslosenquote"]]


# In[23]:


# soritere daten nach Berufsgruppe und Datum
df_sorted = df.sort_values(by=["DB Berufsgruppe", "Datum"])


# In[24]:


# erste fünf Zeilen
df_sorted.head()


# In[25]:


# ALs Excel File speichern
df_sorted.to_excel("generierte Datensätze/Arbeitslosezahlen_Zeitreihe.xlsx") 

