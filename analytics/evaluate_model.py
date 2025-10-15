import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

# Config
TEMP_TH = 8.0
G_TH = 2.5
N_CONSEC = 3

df = pd.read_csv("analytics/labels.csv", parse_dates=["ts_utc"])

def rule_labels(df):
    out = []
    for pid, grp in df.sort_values("ts_utc").groupby("parcel_id"):
        consec = 0
        first_violation = None
        for _, row in grp.iterrows():
            violate = (row["temp"] > TEMP_TH) or (row["g_force"] > G_TH)
            if violate:
                consec += 1
                if first_violation is None:
                    first_violation = row["ts_utc"]
            else:
                consec = 0
                first_violation = None
            pred = "ALERT" if consec >= N_CONSEC else "NORMAL"
            out.append({**row.to_dict(), "pred": pred})
    return pd.DataFrame(out)

pred_df = rule_labels(df)
y_true = (pred_df["label"] == "ALERT").astype(int).values
y_pred = (pred_df["pred"]  == "ALERT").astype(int).values

P = precision_score(y_true, y_pred, zero_division=0)
R = recall_score(y_true, y_pred, zero_division=0)
F1 = f1_score(y_true, y_pred, zero_division=0)
cm = confusion_matrix(y_true, y_pred)

print("Precision:", round(P,3))
print("Recall:", round(R,3))
print("F1-score:", round(F1,3))
print("Confusion Matrix:\n", cm)
