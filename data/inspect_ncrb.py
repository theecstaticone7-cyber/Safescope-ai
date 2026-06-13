import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_colwidth', 50)

COL_NAMES = [
    'SL', 'City', 'Crime_2022', 'Crime_2023', 'Crime_2024',
    'Population_Lakhs', 'Crime_Rate_2024', 'Chargesheeting_Rate_2024'
]


def load_ncrb(path, label):
    df = pd.read_excel(path, header=1)
    df.columns = COL_NAMES
    df = df[pd.to_numeric(df['SL'], errors='coerce').notna()]
    df = df.dropna(subset=['City'])
    df['SL'] = df['SL'].astype(int)
    return df, label


files = [
    (r'C:\Users\bhate\safescope-ai\data\raw\ncrb_crime_against_women_2024.xlsx',
     'FILE 1 — Crime Against Women in Metro Cities (2022-2024)'),
    (r'C:\Users\bhate\safescope-ai\data\raw\ncrb_total_crimes_2024.xlsx',
     'FILE 2 — Total IPC/BNS+SLL Crimes in Metro Cities (2022-2024)'),
]

results = []
for path, label in files:
    df, lbl = load_ncrb(path, label)
    results.append(df)
    print('=' * 70)
    print(lbl)
    print('=' * 70)
    print(f'Shape: {df.shape[0]} rows x {df.shape[1]} columns')
    print()
    print('COLUMN NAMES:')
    for c in df.columns:
        print('  ' + c)
    print()
    print('FIRST 10 ROWS:')
    print(df.head(10).to_string(index=False))
    print()
    print('ALL CITIES IN THIS FILE:')
    for _, row in df.iterrows():
        sl = int(row['SL'])
        city = row['City']
        c2024 = int(row['Crime_2024'])
        rate = row['Crime_Rate_2024']
        print(f'  {sl:2d}. {city:<35s}  crimes_2024={c2024:>7,}  rate={rate}')
    print()

df1, df2 = results
cities1 = set(df1['City'])
cities2 = set(df2['City'])
print('=' * 70)
print('OVERLAP CHECK')
print('=' * 70)
common = sorted(cities1 & cities2)
print(f'Cities in BOTH files ({len(common)}):')
for c in common:
    print('  ' + c)
only1 = sorted(cities1 - cities2)
only2 = sorted(cities2 - cities1)
if only1:
    print('Only in File 1:', only1)
if only2:
    print('Only in File 2:', only2)
