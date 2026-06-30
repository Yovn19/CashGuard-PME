import pandas as pd
import numpy as np

# ============================================
# PARAMÈTRES GÉNÉRAUX
# ============================================
np.random.seed(42)
dates = pd.date_range("2024-01-01", "2024-12-31", freq="D")
TRANSACTIONS_PAR_JOUR = 274  # 274 x 366 jours = ~100 000 lignes

# ============================================
# TYPES DE TRANSACTIONS
# ============================================
types_transactions = [
    "vente_medicament",      # Client achète un médicament
    "vente_parapharmacie",   # Client achète cosmétique/hygiène
    "paiement_fournisseur",  # On paie un fournisseur
    "charge_loyer",          # Loyer mensuel
    "charge_electricite",    # Facture électricité
    "charge_salaire",        # Salaires employés
    "remboursement_client",  # Client retourne un médicament
]

# ============================================
# MOYENS DE PAIEMENT
# ============================================
moyens_paiement = ["cash", "wave", "orange_money", "carte_bancaire", "virement"]

# ============================================
# FOURNISSEURS
# ============================================
fournisseurs = [
    "Laborex Sénégal",
    "SODIPHARM",
    "COPHASE",
    "Mama Pharma",
    "MedAfrique Distribution",
]

# ============================================
# MULTIPLICATEURS DE SAISONNALITÉ
# ============================================
def get_multiplicateur(date):
    mois = date.month
    jour = date.day

    # Hivernage — paludisme = boom des ventes
    if mois in [8, 9]:
        return 1.6

    # Ramadan — moins de clients la journée
    if mois == 3:
        return 0.75

    # Tabaski — pic maximum
    if mois == 6 and jour in [15, 16, 17]:
        return 2.2

    # Korité
    if mois == 4 and jour in [9, 10]:
        return 1.8

    # Rentrée scolaire
    if mois == 9 and jour <= 15:
        return 1.3

    # Fin d'année
    if mois == 12 and jour >= 20:
        return 1.4

    # Jours normaux
    return 1.0

# ============================================
# GÉNÉRATION DES TRANSACTIONS
# ============================================
toutes_transactions = []

for date in dates:
    multiplicateur = get_multiplicateur(date)
    nb_transactions = int(TRANSACTIONS_PAR_JOUR * multiplicateur)

    for _ in range(nb_transactions):

        # Choisir le type de transaction
        type_tx = np.random.choice(types_transactions, p=[
    0.55,   # vente médicament
    0.20,   # vente parapharmacie
    0.10,   # paiement fournisseur
    0.003,  # loyer ← était 0.03
    0.003,  # électricité ← était 0.03
    0.004,  # salaires ← était 0.04
    0.14,   # remboursement ← complète à 1.0
])
        # Calculer le montant selon le type
        if type_tx == "vente_medicament":
            montant = np.random.uniform(500, 85_000) * multiplicateur
            sens = "entree"
            fournisseur = None
            moyen = np.random.choice(moyens_paiement, p=[0.4, 0.3, 0.2, 0.07, 0.03])

        elif type_tx == "vente_parapharmacie":
            montant = np.random.uniform(1_000, 35_000) * multiplicateur
            sens = "entree"
            fournisseur = None
            moyen = np.random.choice(moyens_paiement, p=[0.35, 0.35, 0.2, 0.07, 0.03])

        elif type_tx == "paiement_fournisseur":
            montant = np.random.uniform(50_000, 300_000)
            sens = "sortie"
            fournisseur = np.random.choice(fournisseurs)
            moyen = np.random.choice(["virement", "cheque"], p=[0.7, 0.3])

        elif type_tx == "charge_loyer":
            montant = 850_000
            sens = "sortie"
            fournisseur = "Propriétaire Immeuble"
            moyen = "virement"

        elif type_tx == "charge_electricite":
            montant = np.random.uniform(120_000, 280_000)
            sens = "sortie"
            fournisseur = "SENELEC"
            moyen = "virement"

        elif type_tx == "charge_salaire":
            montant = np.random.uniform(180_000, 450_000)
            sens = "sortie"
            fournisseur = None
            moyen = "virement"

        elif type_tx == "remboursement_client":
            montant = np.random.uniform(500, 25_000)
            sens = "sortie"
            fournisseur = None
            moyen = np.random.choice(["cash", "wave", "orange_money"])

        # Heure de la transaction (pharmacie ouverte 8h-22h)
        heure = np.random.randint(8, 22)
        minute = np.random.randint(0, 59)

        toutes_transactions.append({
            "date": date.strftime("%Y-%m-%d"),
            "heure": f"{heure:02d}:{minute:02d}",
            "type_transaction": type_tx,
            "montant": round(montant, 0),
            "sens": sens,
            "moyen_paiement": moyen if 'moyen' in locals() else "cash",
            "fournisseur": fournisseur,
            "est_fraude": 0
        })

# ============================================
# AJOUTER LES FRAUDES
# ============================================
# 50 fraudes variées et réalistes
nb_fraudes = 50
indices_fraudes = np.random.choice(len(toutes_transactions), nb_fraudes, replace=False)

for idx in indices_fraudes:
    type_fraude = np.random.choice([
        "montant_gonfle",       # Montant anormalement élevé
        "fournisseur_inconnu",  # Fournisseur jamais vu
        "heure_suspecte",       # Transaction à 3h du matin
        "doublon",              # Même transaction deux fois
    ])

    if type_fraude == "montant_gonfle":
        toutes_transactions[idx]["montant"] = np.random.uniform(8_000_000, 15_000_000)
        toutes_transactions[idx]["type_fraude"] = "montant_gonfle"

    elif type_fraude == "fournisseur_inconnu":
        toutes_transactions[idx]["fournisseur"] = "Fournisseur Inconnu SARL"
        toutes_transactions[idx]["montant"] = np.random.uniform(3_000_000, 7_000_000)
        toutes_transactions[idx]["type_fraude"] = "fournisseur_inconnu"

    elif type_fraude == "heure_suspecte":
        toutes_transactions[idx]["heure"] = f"0{np.random.randint(1,4)}:{np.random.randint(0,59):02d}"
        toutes_transactions[idx]["montant"] = np.random.uniform(2_000_000, 6_000_000)
        toutes_transactions[idx]["type_fraude"] = "heure_suspecte"

    elif type_fraude == "doublon":
        toutes_transactions[idx]["montant"] = toutes_transactions[idx-1]["montant"]
        toutes_transactions[idx]["type_fraude"] = "doublon"

    toutes_transactions[idx]["est_fraude"] = 1

# ============================================
# CONSTRUCTION DU DATAFRAME
# ============================================
df = pd.DataFrame(toutes_transactions)

# Remplir les valeurs manquantes
df["fournisseur"] = df["fournisseur"].fillna("Client direct")
df["type_fraude"] = df.get("type_fraude", pd.Series(["normal"] * len(df)))
df["type_fraude"] = df["type_fraude"].fillna("normal")

# Trier par date et heure
df = df.sort_values(["date", "heure"]).reset_index(drop=True)

# ============================================
# SAUVEGARDE
# ============================================
df.to_csv("../data/tresorerie_pharmacie_v2.csv", index=False)

print("✅ Dataset v2 généré avec succès !")
print(f"📊 Nombre de transactions : {len(df)}")
print(f"🚨 Nombre de fraudes : {df['est_fraude'].sum()}")
print(f"📅 Période : {df['date'].min()} → {df['date'].max()}")
print("\n--- Aperçu ---")
print(df.head(10))
print("\n--- Répartition des types ---")
print(df['type_transaction'].value_counts())