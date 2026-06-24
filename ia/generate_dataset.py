import pandas as pd
import numpy as np

# ---- PARAMÈTRES DE BASE ----
np.random.seed(42)
dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
n = len(dates)

# ---- REVENUS DE BASE ----
# Une pharmacie à Dakar gagne environ 800 000 FCFA par jour
revenus_base = 800_000

# ---- SAISONNALITÉ ----
# On crée des multiplicateurs selon les périodes
multiplicateurs = np.ones(n)

for i, date in enumerate(dates):
    mois = date.month
    jour = date.day

    # Hivernage (Août - Septembre) : paludisme = plus de clients
    if mois in [8, 9]:
        multiplicateurs[i] = 1.5

    # Ramadan (Mars 2024) : moins de clients le jour
    if mois == 3:
        multiplicateurs[i] = 0.8

    # Tabaski (Juin 2024) : pic de ventes
    if mois == 6 and jour in [15, 16, 17]:
        multiplicateurs[i] = 2.0

    # Fin d'année : pic
    if mois == 12 and jour >= 20:
        multiplicateurs[i] = 1.4

# ---- REVENUS FINAUX ----
# Revenus de base x saisonnalité + bruit aléatoire réaliste
revenus = (revenus_base * multiplicateurs +
           np.random.normal(0, 50_000, n))

# Les revenus ne peuvent pas être négatifs
revenus = np.clip(revenus, 0, None)

# ---- CHARGES FIXES ----
# Payées le 1er de chaque mois
charges = np.zeros(n)
for i, date in enumerate(dates):
    if date.day == 1:
        charges[i] = 1_500_000  # loyer + salaires + fournisseurs

# ---- TRANSACTIONS FRAUDULEUSES ----
# On cache 5 fraudes dans les données
fraudes = np.zeros(n)
indices_fraude = [45, 112, 178, 234, 301]  # jours choisis au hasard
for idx in indices_fraude:
    fraudes[idx] = np.random.uniform(2_000_000, 5_000_000)  # montant anormal

# ---- CONSTRUCTION DU DATASET ----
df = pd.DataFrame({
    "date": dates,
    "revenus": revenus.round(0),
    "charges": charges,
    "transaction_suspecte": fraudes,
    "est_fraude": (fraudes > 0).astype(int)  # 1 = fraude, 0 = normal
})

# ---- CALCUL DU SOLDE ----
df["flux_net"] = df["revenus"] - df["charges"] - df["transaction_suspecte"]
df["solde_cumule"] = df["flux_net"].cumsum()

# ---- SAUVEGARDE ----
df.to_csv("../data/tresorerie_pharmacie.csv", index=False)
print("✅ Dataset généré avec succès !")
print(f"📊 Nombre de lignes : {len(df)}")
print(f"🚨 Nombre de fraudes cachées : {df['est_fraude'].sum()}")
print(df.head(10))