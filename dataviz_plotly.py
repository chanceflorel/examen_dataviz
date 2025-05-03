import pandas as pd
import plotly.express as px
from datetime import datetime

# Charger les fichiers CSV
df_employes = pd.read_csv("Employés.csv")
df_taches = pd.read_csv("Tâches.csv")

# ----------------------------
# 1. Préparer les données
# ----------------------------

# Calculer l'âge des employés
aujourd_hui = pd.to_datetime("2025-01-01")
df_employes['date_naissance'] = pd.to_datetime(df_employes['date_naissance'])
df_employes['Âge'] = ((aujourd_hui - df_employes['date_naissance']).dt.days / 365.25).astype(int)

# Fusionner les deux tables
df = df_taches.merge(df_employes, left_on='id_employé', right_on='id')

# Extraire l’année depuis la date de début
df['date_début'] = pd.to_datetime(df['date_début'])
df['Année'] = df['date_début'].dt.year

# ----------------------------
# 1. Âge moyen des employés par département
# ----------------------------
age_moyen = df_employes.groupby('nomDepartement')['Âge'].mean().reset_index()
fig1 = px.bar(age_moyen, x='nomDepartement', y='Âge',
              title="Âge moyen des employés par département")
fig1.show()

# ----------------------------
# 2. Nombre de tâches par département pour l'année 2020
# ----------------------------
df_2020 = df[df['Année'] == 2020]
taches_par_dept = df_2020.groupby('nomDepartement').size().reset_index(name='Nombre de tâches')
fig2 = px.bar(taches_par_dept, x='nomDepartement', y='Nombre de tâches', color='nomDepartement',
              title="Nombre de tâches par département (2020)")
fig2.show()

# ----------------------------
# 3. Nombre de tâches par état selon les tranches d’âge
# ----------------------------
# Créer des tranches d'âge
bins = [19, 29, 39, 49, 59, 69]
labels = ['20-29', '30-39', '40-49', '50-59', '60-69']
df['Tranche âge'] = pd.cut(df['Âge'], bins=bins, labels=labels)

taches_etat_age = df.groupby(['Tranche âge', 'état'], observed=True).size().reset_index(name='Nombre')

fig3 = px.bar(taches_etat_age, x='Tranche âge', y='Nombre', color='état', barmode='group',
              title="Nombre de tâches par état selon les tranches d'âge")
fig3.show()

# ----------------------------
# 4. Nombre de tâches par année selon le département
# ----------------------------
taches_par_annee = df.groupby(['Année', 'nomDepartement']).size().reset_index(name='Nombre')
fig4 = px.line(taches_par_annee, x='Année', y='Nombre', color='nomDepartement',
               title="Nombre de tâches par année selon le département")
fig4.show()
