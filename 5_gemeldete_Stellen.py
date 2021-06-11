#!/usr/bin/env python
# coding: utf-8

# ## gemeldete Stellen



# Bibliotheken
import numpy as np
import pandas as pd




# Daten einlesen
df = pd.read_excel("generierte Datensätze/Datensatz_komplett.xlsx", index_col=0)




# erste fünf Zeilen
df.head()




# definiere technische Berufe
Technische_Berufe  = df.Berufsgruppe.isin(["24 Metallerzeugung,-bearbeitung, Metallbau", 
                                "25 Maschinen- und Fahrzeugtechnikberufe", 
                                "26 Mechatronik-, Energie- u. Elektroberufe"])




# definiere Verkehrsberufe
Verkehr_Logistikberufe = df.Berufsgruppe.isin(["51 Verkehr, Logistik (außer Fahrzeugführ.)", 
                                                  "52 Führer von Fahrzeug- u. Transportgeräten"])




# definiere Gastgewerbeberufe
Gastgewerbeberufe = df.Berufsgruppe.isin(["632 Hotellerie", "633 Gastronomie"])




# definiere Elektroberufe
Elektroberufe = df.Berufsgruppe.isin(["262 Energietechnik", "263 Elektrotechnik"])




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




# Elektroberufe
df_elektro = get_stellen(df, Elektroberufe, "Elektroberufe")




# technische Berufe
df_tech = get_stellen(df, Technische_Berufe, "Technische Berufe")




# Verkehr und Logistik
df_verkehr = get_stellen(df, Verkehr_Logistikberufe, "Verkehr -/ Logistikberufe")




# Gastgewerberufe
df_gg = get_stellen(df, Gastgewerbeberufe, "Gastgewerbeberufe")




# Zusammenführung
df = pd.concat([df_elektro, df_tech, df_verkehr, df_gg])




# Missings entfernen
df = df.dropna()




# erste fünf Zeilen
df.head()




# Monat
df["Monat"] = df.Zeitpunkt.str[:3]




# Jahr
df["Jahr"] = df.Zeitpunkt.str[4:8]




# kreiere neue Spalte: Monat als Zahl
df["Monat Zahl"] = df.Monat.replace(
                     ["Jan", "Feb", "Mrz", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez",],
                     ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
)




# Kreeire neue Datum Spalte
df["Datum"] = df["Jahr"] + "-" + df["Monat Zahl"] + "-" + "1"




# konvertiere Strinf zu Datum
df["Datum"] = pd.to_datetime(df.Datum, format="%Y-%m-%d")




# Filter dataframe
df = df[["Datum", "DB Berufsgruppe", "gemeldete Stellen"]]




# soritere daten nach Berufsgruppe und Datum
df_sorted = df.sort_values(by=["DB Berufsgruppe", "Datum"])




# erste fünf Zeilen
df_sorted.head()




# ALs Excel File speichern
df_sorted.to_excel("generierte Datensätze/gem_Stellen_Zeitreihe.xlsx") 

