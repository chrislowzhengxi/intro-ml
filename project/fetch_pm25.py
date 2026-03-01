import requests
import pandas as pd
import time

START_YEAR = 2008
END_YEAR = 2020

COUNTRIES = [
    "USA","CAN","GBR","DEU","FRA","ITA","ESP","JPN","KOR","IND",
    "BRA","MEX","AUS","NLD","SWE","NOR","ZAF","ARG","TUR","IDN",
    "CHE","POL","BEL","AUT","DNK","FIN","IRL","PRT","GRC","NZL",
    "CHN","THA","MYS","PHL","VNM","EGY","SAU","ARE","ISR","COL",
    "PER","CHL","CZE","HUN","ROU","UKR","PAK","BGD","NGA","KEN"
]

INDICATORS = {
    "EN.ATM.PM25.MC.M3": "pm25",
    "EG.EGY.PRIM.PP.KD": "primary_energy_per_capita",
    "EG.FEC.RNEW.ZS": "renewable_energy_pct",
    "AG.LND.FRST.ZS": "forest_area_pct",
    "EG.USE.PCAP.KG.OE": "energy_use_per_capita",
    "AG.LND.AGRI.ZS": "agricultural_land_pct",
    "NY.GDP.PCAP.KD": "gdp_per_capita",
    "NV.IND.TOTL.ZS": "industry_pct_gdp",
    "NE.TRD.GNFS.ZS": "trade_pct_gdp",
    "NE.GDI.TOTL.ZS": "gross_capital_formation_pct",
    "SP.URB.TOTL.IN.ZS": "urban_population_pct",
    "SP.DYN.LE00.IN": "life_expectancy",
    "EN.POP.DNST": "population_density",
    "SH.H2O.BASW.ZS": "basic_drinking_water_pct",
}

BASE = "https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}"

def fetch_indicator(indicator_code, countries_iso3):
    countries_str = ";".join(countries_iso3)
    params = {
        "format": "json",
        "per_page": 20000,
        "date": f"{START_YEAR}:{END_YEAR}"
    }

    url = BASE.format(countries=countries_str, indicator=indicator_code)
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    payload = r.json()

    if not isinstance(payload, list) or payload[1] is None:
        return pd.DataFrame(columns=["country", "year", "value"])

    rows = []
    for item in payload[1]:
        rows.append({
            "country": item["countryiso3code"],
            "year": int(item["date"]),
            "value": item["value"]
        })

    return pd.DataFrame(rows)

dfs = []

for code, name in INDICATORS.items():
    print(f"Fetching {code}")
    dfi = fetch_indicator(code, COUNTRIES)
    dfi = dfi.rename(columns={"value": name})
    dfs.append(dfi)
    time.sleep(0.5)

df = dfs[0]
for dfi in dfs[1:]:
    df = df.merge(dfi, on=["country","year"], how="outer")

df = df.sort_values(["country","year"]).reset_index(drop=True)

print(df.head())
print("\nMissing values:")
print(df.isna().sum())

df.to_csv("clean_8_variable_panel.csv", index=False)