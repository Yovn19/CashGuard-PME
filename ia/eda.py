import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# CHARGEMENT DU DATASET
# ============================================
df = pd.read_csv("../data/tresorerie_pharmacie_v2.csv")
print("✅ Dataset chargé avec succès !")

# ============================================
# 1. INFORMATIONS GÉNÉRALES
# ============================================
print("\n📊 INFORMATIONS GÉNÉRALES")
print(f"Nombre de lignes : {len(df)}")
print(f"Nombre de colonnes : {len(df.columns)}")
print(f"Colonnes : {list(df.columns)}")
print(f"\nPériode : {df['date'].min()} → {df['date'].max()}")

# ============================================
# 2. QUALITÉ DES DONNÉES
# ============================================
print("\n🔍 QUALITÉ DES DONNÉES")
print("Valeurs manquantes par colonne :")
print(df.isnull().sum())
print(f"\nDoublons : {df.duplicated().sum()}")
print(f"\nTypes de données :")
print(df.dtypes)

# ============================================
# 3. STATISTIQUES DESCRIPTIVES
# ============================================
print("\n📈 STATISTIQUES DES MONTANTS")
print(df['montant'].describe())
print(f"\nMontant minimum : {df['montant'].min():,.0f} FCFA")
print(f"Montant maximum : {df['montant'].max():,.0f} FCFA")
print(f"Montant moyen   : {df['montant'].mean():,.0f} FCFA")

# ============================================
# 4. RÉPARTITION DES TRANSACTIONS
# ============================================
print("\n💼 RÉPARTITION DES TYPES DE TRANSACTIONS")
print(df['type_transaction'].value_counts())

print("\n💳 RÉPARTITION DES MOYENS DE PAIEMENT")
print(df['moyen_paiement'].value_counts())

print("\n🚨 RÉPARTITION FRAUDES / NORMALES")
print(df['est_fraude'].value_counts())
print(f"Taux de fraude : {df['est_fraude'].mean()*100:.4f}%")

# ============================================
# 5. GRAPHIQUE 1 — Revenus par jour
# ============================================
print("\n📊 Génération des graphiques...")

df['date'] = pd.to_datetime(df['date'])
revenus_jour = df[df['sens'] == 'entree'].groupby('date')['montant'].sum()

plt.figure(figsize=(14, 4))
plt.plot(revenus_jour.index, revenus_jour.values, color='#1a1a2e', linewidth=0.8)
plt.title("Revenus journaliers de la pharmacie — 2024", fontsize=14)
plt.xlabel("Date")
plt.ylabel("Montant (FCFA)")
plt.tight_layout()
plt.savefig("../data/graphique_revenus.png")
plt.close()
print("✅ Graphique 1 sauvegardé")

# ============================================
# 6. GRAPHIQUE 2 — Répartition des types
# ============================================
types_counts = df['type_transaction'].value_counts()

plt.figure(figsize=(8, 8))
plt.pie(types_counts.values,
        labels=types_counts.index,
        autopct='%1.1f%%',
        colors=['#1a1a2e','#4a4a8a','#7a7aaa','#aaaacc','#ccccee','#eeeeff','#f0f0f8'])
plt.title("Répartition des types de transactions", fontsize=14)
plt.tight_layout()
plt.savefig("../data/graphique_types.png")
plt.close()
print("✅ Graphique 2 sauvegardé")

# ============================================
# 7. GRAPHIQUE 3 — Fraudes vs Normales
# ============================================
fraudes = df[df['est_fraude'] == 1]['montant']
normales = df[df['est_fraude'] == 0]['montant']

plt.figure(figsize=(10, 5))
plt.hist(normales, bins=50, color='#1a1a2e', alpha=0.7, label='Transactions normales')
plt.hist(fraudes, bins=10, color='red', alpha=0.7, label='Fraudes')
plt.title("Distribution des montants — Fraudes vs Normales", fontsize=14)
plt.xlabel("Montant (FCFA)")
plt.ylabel("Nombre de transactions")
plt.legend()
plt.tight_layout()
plt.savefig("../data/graphique_fraudes.png")
plt.close()
print("✅ Graphique 3 sauvegardé")

# ============================================
# 8. GRAPHIQUE 4 — Transactions par heure
# ============================================
df['heure_int'] = df['heure'].str.split(':').str[0].astype(int)
transactions_heure = df.groupby('heure_int').size()

plt.figure(figsize=(10, 4))
plt.bar(transactions_heure.index, transactions_heure.values, color='#4a4a8a')
plt.title("Nombre de transactions par heure", fontsize=14)
plt.xlabel("Heure de la journée")
plt.ylabel("Nombre de transactions")
plt.tight_layout()
plt.savefig("../data/graphique_heures.png")
plt.close()
print("✅ Graphique 4 sauvegardé")

# ============================================
# RÉSUMÉ FINAL
# ============================================
print("\n" + "="*50)
print("✅ EDA TERMINÉE AVEC SUCCÈS !")
print("="*50)
print(f"📊 {len(df)} transactions analysées")
print(f"🚨 {df['est_fraude'].sum()} fraudes détectées")
print(f"📈 4 graphiques sauvegardés dans data/")
print("="*50)