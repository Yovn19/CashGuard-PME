import pandas as pd

# ============================================
# CHARGEMENT DES DONNÉES
# ============================================
df = pd.read_csv("../data/tresorerie_pharmacie_v2.csv")
print("Nombre de transactions chargées :", len(df))


# ============================================
# RÈGLE 1 — MONTANT ANORMAL (par type de transaction)
# ============================================
def detect_montant_anormal(df, seuil_ecarts_type=3):
    """
    Détecte les transactions dont le montant est anormal
    PAR RAPPORT À SON PROPRE TYPE de transaction.
    """
    resultats = []

    for type_tx in df["type_transaction"].unique():
        sous_df = df[df["type_transaction"] == type_tx]
        moyenne = sous_df["montant"].mean()
        ecart_type = sous_df["montant"].std()
        seuil = moyenne + seuil_ecarts_type * ecart_type

        suspects = sous_df[sous_df["montant"] > seuil]
        resultats.append(suspects)

    return pd.concat(resultats)


# ============================================
# RÈGLE 2 — FOURNISSEUR / BÉNÉFICIAIRE INCONNU
# ============================================
FOURNISSEURS_CONNUS = [
    "Laborex Sénégal",
    "SODIPHARM",
    "COPHASE",
    "Mama Pharma",
    "MedAfrique Distribution",
    "SENELEC",
    "Propriétaire Immeuble",
    "Client direct",
]


def detect_fournisseur_inconnu(df):
    """
    Détecte les transactions dont le fournisseur/bénéficiaire
    n'est pas dans la liste des fournisseurs connus et validés.
    """
    suspects = df[~df["fournisseur"].isin(FOURNISSEURS_CONNUS)]
    return suspects


# ============================================
# RÈGLE 3 — HORAIRE SUSPECT
# ============================================
def detect_heure_suspecte(df, heure_ouverture=8, heure_fermeture=22):
    """
    Détecte les transactions effectuées en dehors des horaires
    d'ouverture habituels de la pharmacie.
    """
    heures = df["heure"].str.split(":").str[0].astype(int)
    suspects = df[(heures < heure_ouverture) | (heures >= heure_fermeture)]
    return suspects


# ============================================
# RÈGLE 4 — DOUBLON (deux transactions très rapprochées avec
# exactement le même montant, le même jour)
# ============================================
def detect_doublons(df):
    """
    Détecte les transactions potentiellement dupliquées :
    deux transactions le même jour avec un montant identique
    qui ne fait pas partie des montants "ronds" très courants
    (ex: charges fixes comme le loyer).
    On exclut les montants typiques de charges fixes pour limiter
    les coïncidences normales (loyer, électricité).
    """
    # On exclut les transactions de type "charge" qui ont des montants
    # récurrents et donc naturellement dupliqués (ex: loyer = 850000 chaque mois)
    df_filtre = df[~df["type_transaction"].isin(
        ["charge_loyer", "charge_electricite", "charge_salaire"]
    )]

    doublons_mask = df_filtre.duplicated(
        subset=["date", "montant"], keep=False
    )
    suspects = df_filtre[doublons_mask]
    return suspects


# ============================================
# TESTS
# ============================================
if __name__ == "__main__":
    resultats_montant = detect_montant_anormal(df)
    print("\n🚨 Règle 1 - Montant anormal :", len(resultats_montant), "détectées")
    print("   Dont vraies fraudes :", resultats_montant["est_fraude"].sum())

    resultats_fournisseur = detect_fournisseur_inconnu(df)
    print("\n🚨 Règle 2 - Fournisseur inconnu :", len(resultats_fournisseur), "détectées")
    print("   Dont vraies fraudes :", resultats_fournisseur["est_fraude"].sum())

    resultats_heure = detect_heure_suspecte(df)
    print("\n🚨 Règle 3 - Heure suspecte :", len(resultats_heure), "détectées")
    print("   Dont vraies fraudes :", resultats_heure["est_fraude"].sum())

    resultats_doublons = detect_doublons(df)
    print("\n🚨 Règle 4 - Doublons :", len(resultats_doublons), "détectées")
    print("   Dont vraies fraudes :", resultats_doublons["est_fraude"].sum())