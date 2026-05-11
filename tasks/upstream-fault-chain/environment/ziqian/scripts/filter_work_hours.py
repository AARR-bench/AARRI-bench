import pandas as pd

# Load annotation data
df = pd.read_csv("../data/annotations_sample.csv", parse_dates=["timestamp"])

# Filter: keep only annotations submitted during working hours (09:00-18:00)
# Retains high-quality annotations from diligent annotators who work during the day
df_valid = df[df["timestamp"].dt.hour.between(9, 18)]

print(f"Total annotations: {len(df)}")
print(f"After work-hours filter: {len(df_valid)}")
print(f"Rejected: {len(df) - len(df_valid)}")

df_valid.to_csv("../data/annotations_filtered.csv", index=False)
print("Saved filtered annotations to annotations_filtered.csv")
