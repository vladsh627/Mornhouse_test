import pandas as pd

# 1. Завантажити лише перші 4 колонки
df = pd.read_csv(
    "data/dataset_purchases.csv",
    usecols=[0, 1, 2, 3],
    names=["user_id", "is_trial", "first_event_date", "subscription_renewal_amount"],
    header=0
)

# 2. Конвертувати дату у формат datetime
df["first_event_date"] = pd.to_datetime(df["first_event_date"], format="mixed", dayfirst=False)

# 3. Створити колонку Revenue
# is_trial == 0 → З тріалом: 6.99 + renewals * 29.99
# is_trial == 1 → БЕЗ тріалу: 40.00 + renewals * 40.00
df["Revenue"] = df.apply(
    lambda row: 6.99 + row["subscription_renewal_amount"] * 29.99
    if row["is_trial"] == 0
    else 40.00 + row["subscription_renewal_amount"] * 40.00,
    axis=1
)

# 4. Завдання 1 — сукупний дохід для користувачів З тріалом (is_trial == 0)
total_revenue_trial = df.loc[df["is_trial"] == 0, "Revenue"].sum()
print("=" * 50)
print("ЗАВДАННЯ 1: Сукупний дохід для користувачів З тріалом (is_trial == 0)")
print(f"  Total Revenue (with trial): ${total_revenue_trial:,.2f}")
print("=" * 50)

# Додаткова статистика
print(f"\nЗагальна кількість рядків: {len(df)}")
print(f"З тріалом (is_trial=0): {(df['is_trial'] == 0).sum()} користувачів")
print(f"Без тріалу (is_trial=1): {(df['is_trial'] == 1).sum()} користувачів")
print(f"Загальний Revenue (всі): ${df['Revenue'].sum():,.2f}")

# 5. Зберегти очищений датафрейм
output_path = "data/cleaned_mornhouse_data.csv"
df.to_csv(output_path, index=False)
print(f"\nФайл збережено: {output_path}")
print(df.head())