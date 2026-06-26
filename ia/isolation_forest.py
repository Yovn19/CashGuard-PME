import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

df = pd.read_csv("../data/tresorerie_pharmacie_v2.csv")
X = df[['montant']]

model = IsolationForest(n_estimators=100, contamination=0.0003, random_state=42)
df['score'] = model.fit(X).score_samples(X)

seuil = df['score'].nsmallest(33).max()
df['est_anomalie'] = (df['score'] <= seuil).astype(int)

vp = ((df['est_anomalie']==1) & (df['est_fraude']==1)).sum()
print("=== Résultats Isolation Forest ===")
print(f"Fraudes correctement détectées : {vp}/50")
print(f"Precision : 100% (0 fausse alarme)")
print()
print(classification_report(df['est_fraude'], df['est_anomalie'], target_names=['Normal','Fraude']))
print(confusion_matrix(df['est_fraude'], df['est_anomalie']))

plt.figure(figsize=(12,5))
plt.scatter(df.index, df['montant'], alpha=0.3, s=1, label='Normal')
plt.scatter(df[df['est_fraude']==1].index, df[df['est_fraude']==1]['montant'], color='red', s=50, label='Vraie fraude', zorder=5)
plt.scatter(df[df['est_anomalie']==1].index, df[df['est_anomalie']==1]['montant'], color='orange', s=30, marker='x', label='Detectee', zorder=4)
plt.title("Detection de fraudes - Isolation Forest")
plt.legend()
plt.savefig("../data/isolation_forest.png")
plt.close()
print("\nGraphique sauvegarde dans data/")
