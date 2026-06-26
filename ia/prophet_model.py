import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# ── 1. Chargement ─────────────────────────────────────────
df = pd.read_csv("../data/tresorerie_pharmacie_v2.csv")
df['date'] = pd.to_datetime(df['date'])

# ── 2. Flux net journalier ────────────────────────────────
entrees = df[df['sens'] == 'entree'].groupby('date')['montant'].sum()
sorties = df[df['sens'] == 'sortie'].groupby('date')['montant'].sum()
flux_net = (entrees - sorties).fillna(0).reset_index()
flux_net.columns = ['ds', 'y']

# ── 3. Entraînement Prophet ───────────────────────────────
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    changepoint_prior_scale=0.05
)
model.fit(flux_net)

# ── 4. Prévisions J+15 et J+30 ───────────────────────────
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

j15 = forecast.iloc[-16]
j30 = forecast.iloc[-1]

print("=== Prévision J+15 ===")
print(f"Date : {j15['ds'].date()}")
print(f"Flux net prévu : {j15['yhat']:,.0f} FCFA")
print(f"Intervalle : [{j15['yhat_lower']:,.0f} – {j15['yhat_upper']:,.0f}] FCFA")

print("\n=== Prévision J+30 ===")
print(f"Date : {j30['ds'].date()}")
print(f"Flux net prévu : {j30['yhat']:,.0f} FCFA")
print(f"Intervalle : [{j30['yhat_lower']:,.0f} – {j30['yhat_upper']:,.0f}] FCFA")

# ── 5. Graphiques ─────────────────────────────────────────
fig1 = model.plot(forecast)
plt.title("Prévision flux net - CashGuard PME")
plt.savefig("../data/prophet_forecast.png")
plt.close()

fig2 = model.plot_components(forecast)
plt.savefig("../data/prophet_components.png")
plt.close()

print("\nGraphiques sauvegardés dans data/")