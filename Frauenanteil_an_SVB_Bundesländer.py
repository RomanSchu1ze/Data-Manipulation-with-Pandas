#!/usr/bin/env python
# coding: utf-8

# ### Frauenquote von DB Fokusberufen im Bundesland Bayern

# In[1]:


# Bibliotheken
import pandas as pd
import numpy as np


###### 1. Daten einlesen



# daten laden
df = pd.read_csv("Daten/202009_Besch_Laender.csv", sep=";")




# erste fünf Zeilen
df.head()




# Datentypen
df.dtypes




# Bereinigung der Daten
def clean_data(df):
    df.replace("*", np.nan, inplace=True)
    for col in df.columns:
        if col in ["SVB ohne Azubis", "AGB"]:
            df[col] = df[col].astype("float64")
    return df




# Anwendung der Funktion
df = clean_data(df)




# erste fünf Zeilen
df.head()


###### 2. Berufe Matching



# Auflistung der DB Berufe und deren zugehöriger ID´s
Berufe = {
    "Planungsingenieure_LST_TK_OLA_ETCS" : [59],
    "Planungsingenieure_KIB_Oberbau" : [113, 114],
    "Projektingenieure KIB/Projektingenieure Oberbau/Projektingenieure Verkehrsanlagen" : [47, 113, 114, 115, 116, 117, 118, 119],
    "Bauleiter" : [119],
    "Recruiter/HR-Partner/Personalreferent/Spezialisten und Berater HR/Change Management" : [81],
    "Controller (Finance)" : [82],
    "Projektkaufmann / -leiter, Berater" : [80],
    "IT_Service/Betriebsführung" : [68],
    "IT_Entwicklung" : [69],
    "IT-Anwendungs- / Anforderungsmanagement, IT-Beratung" : [67],
    "IT-Strategie, -Projektmanagement, -Security" : [66],
    "Zugbegleiter/KiN/(1. Klasse) Steward" : [78, 79, 133],
    "Reiseberater" : [132],
    "Call Center Agent" : [134],
    "Arbeiter KIB" : [137],
    "Gleisbauer/beiter Oberbau" : [62],
    "Schweißer" : [88],
    "(Qual.) Instandhalter/Schienenfahrzeugmechaniker/Industriemechaniker/Weichenmechaniker" : [57, 91, 92, 162, 163],
    "Elektroniker/Elektriker/Arbeiter LST/Arbeiter Oberleitung/Signalmechaniker" : [58, 60],
    "Mechatroniker" : [138],
    "Servicetechniker Elektrotechnik/Telekommunikation" : [107],
    "Servicetechniker Maschinen- / Fördertechnik" : [92],
    "Servicetechniker Heizung/Klima/Lüftung/Sanitär" : [124],
    "Hausinspektor/Objektbetreuer": [123],
    "Polier/Meister Bau" : [120, 121, 122],
    "Industriemeister & Fertigungsmeister FZI/Instandhaltung": [85, 86, 87, 89, 90, 93, 95],
    "Meister Elektrotechnik" : [98, 105, 112],
    "Elektrotechniker" : [96, 97, 99, 100, 101, 102, 103, 104, 106, 108, 109, 110, 111],
    "Sicherungsdienst/Ordnungsdienst" : [130], 
    "Sicherungsdienst/Ordnungsdienst (einfach)" : [131],
    "Fahrwegpfleger/Landschaftspfleger" : [84],
    "Gebäudereiniger/Fahrzeugreiniger" : [76],
    "Gebäudereiniger/Fahrzeugreiniger (einfach)" : [77],
    "Busfahrer (fertig/qual.)" : [128],
    "Busfahrer (Quer.)" : [126, 127, 129],
    "Triebfahrzeugführer (Quer.)/Lokrangierführer (Quer.)" : [56, 57, 125, 126, 127, 128, 129],
    "Triebfahrzeugführer (fertig/qual.)/Lokrangierführer (fertig/qual.)" : [73],
    "Fahrdienstleiter (Quer.)" : [56, 57, 50, 150, 149, 151, 152, 153, 155, 157, 156],
    "Wagenmeister (Quer.)" : [37, 56, 57],
    "Rangierbegleiter/Rangierarbeiter (Quer.)" : [39, 70]
}


###### 3. Frauenquote für jeden Beruf berechnen


# Definiere BL Bayern
Bundesländer = {
    "Schleswig-Holstein" : [1],
    "Hamburg" : [2],
    "Niedersachsen" : [3],
    "Bremen" : [4],
    "Nordrhein-Westfalen" : [5],
    "Hessen" : [6],
    "Rheinland-Pfalz" : [7],
    "Baden-Württemberg" : [8],
    "Bayern" : [9],
    "Saarland" : [10],
    "Berlin" : [11],
    "Brandenburg" : [12],
    "Mecklenburg-Vorp." : [13],
    "Sachsen" : [14],
    "Sachsen-Anhalt" : [15],
    "Thüringen" : [16]
}




# Frauen ID
Frauen_ID = [2]




# Berechnung der Frauenquote für jeden DB Fokusberuf
def calc_fem_share(df, Bundesland):
    # leere liste um Ergebnisse zu speichern
    liste = []
    for key, value in Berufe.items():
        # Definiere welche Zeilen bleiben sollen
        keep_gesamt = {"Berufe ID": value, "Bundesland": Bundesland}
        # Definiere welche Zeilen bleiben sollen
        keep_frauen = {"Berufe ID": value, "Bundesland": Bundesland, "Geschlecht":Frauen_ID}
        # filtere Dataframe für alle SVB´s
        df_ges = df[df[list(keep_gesamt)].isin(keep_gesamt).all(axis=1)]
        # filtere Dataframe für alle SVB´s
        df_fem = df[df[list(keep_frauen)].isin(keep_frauen).all(axis=1)]
        # Summiere SVB´s & AGB´s
        ges = df_ges["SVB ohne Azubis"].sum() + df_ges["AGB"].sum()
        # Summiere weibliche SVB´s & AGB´s
        fem = df_fem["SVB ohne Azubis"].sum() + df_fem["AGB"].sum()
        # berechne Frauenquote 
        fem_share = fem / ges 
        # erstelle liste mit allen relevanten Inhalten
        liste.append([key, ges, fem, fem_share])
        # Konvertierung in Dataframe
        data = pd.DataFrame(liste)
        # Anpassung der Spaltennamen
        data.columns = ["DB Fokusberuf", "SVB Gesamt", "Frauenanteil", "Frauenquote"]
    # liste leeren
    liste.clear()
    # ausgabe Df
    return data




# leere Liste um Ergebnisse zu speichern
list_of_df = []
# Frauenquote für jedes Bundesland und jeden Beruf
for key, value in Bundesländer.items():
    # Berechnung der Frauenquote für jeden Beruf 
    df_new = calc_fem_share(df, value)
    # Bundesland als Spalte ergänzen 
    df_new["Bundesland"] = key
    # Daten nach Frauenqote sortieren
    df_sorted = df_new[df_new["Bundesland"] == key].sort_values(by=["Frauenquote"], ascending=False)
    # index aktualisieren
    df_sorted = df_sorted.set_index(np.arange(1, len(df_sorted) + 1))
    # liste mit dataframe füllen
    list_of_df.append(df_sorted)




# Zusammenführung der Dataframes 
df_all = pd.concat(list_of_df)




# erste fünf Zeilen für das Bundesland Bayern ausgeben
df_all[df_all["Bundesland"] == "Bayern"].head()




# ALs Excel File speichern
df_all.to_excel("Frauenanteil.xlsx")






