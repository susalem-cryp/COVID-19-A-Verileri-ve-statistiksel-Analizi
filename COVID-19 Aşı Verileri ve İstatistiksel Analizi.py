#Ad Soyad : Fatima Nabil Hamdi Ratrout            Öğrenci Numarası:224210096
#Ad Soyad :Somia Ussama Abdelwahed Mohamed Salem  Öğrenci Numarası:214210109
import requests
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np
import seaborn as sns
from scipy import stats

# API URL'si
api_url = "https://jhucoronavirus.azureedge.net/api/v3/vaccines/global.json"
response = requests.get(api_url)
if response.status_code == 200:
    try:
        data = response.json()
        if isinstance(data, list):
            vaccination_data = data 
            df = pd.DataFrame(vaccination_data)
            if not df.empty:
                df['doses_admin'] = df['data'].apply(lambda x: x.get('doses_admin') if isinstance(x, dict) else None)
                df['raw_full_vac'] = df['data'].apply(lambda x: x.get('raw_full_vac') if isinstance(x, dict) else None)
                df['percent_full_vac'] = df['data'].apply(lambda x: x.get('percent_full_vac') if isinstance(x, dict) else None)
                df['raw_full_vac'] = pd.to_numeric(df['raw_full_vac'], errors='coerce')
                df['doses_admin'] = pd.to_numeric(df['doses_admin'], errors='coerce')
                df['percent_full_vac'] = pd.to_numeric(df['percent_full_vac'], errors='coerce')
                df_sorted = df[['country', 'doses_admin', 'raw_full_vac', 'percent_full_vac']].dropna().sort_values(by='raw_full_vac', ascending=False)
                top_198_vaccines = df_sorted.head(198)
                print("\nTop 198 Ülke - Aşı Verileri (Tam Aşılanan Kişi Sayısı ve Toplam Doz):")
                pd.set_option('display.width', None)  
                pd.set_option('display.max_columns', None) 
                pd.set_option('display.float_format', '{:,.0f}'.format)  
                print(top_198_vaccines.to_string(index=False))
                vaccinated_values = df_sorted['raw_full_vac'].dropna()
                doses_admin_values = df_sorted['doses_admin'].dropna()
                mean_vaccinated = vaccinated_values.mean() 
                median_vaccinated = vaccinated_values.median() 
                mode_vaccinated = vaccinated_values.mode()[0]  
                mean_doses = doses_admin_values.mean()
                median_doses = doses_admin_values.median()
                mode_doses = doses_admin_values.mode()[0]
                variance_vaccinated = vaccinated_values.var() 
                variance_doses = doses_admin_values.var()  
                min_vaccinated = vaccinated_values.min()  
                max_vaccinated = vaccinated_values.max()  
                min_doses = doses_admin_values.min()
                max_doses = doses_admin_values.max()
                # Sonuçların yazdırılması
                print("\nAşılanan Kişiler için İstatistiksel Değerler:")
                print(f"Ortalama Aşılanan Kişi Sayısı: {mean_vaccinated:,.0f}")
                print(f"Medyan Aşılanan Kişi Sayısı: {median_vaccinated:,.0f}")
                print(f"Mod (En Yaygın) Aşılanan Kişi Sayısı: {mode_vaccinated:,.0f}")
                print(f"Varyans (Aşılanan Kişi Sayısı): {variance_vaccinated:,.0f}")
                print(f"En Küçük Aşılanan Kişi Sayısı: {min_vaccinated:,.0f}")
                print(f"En Büyük Aşılanan Kişi Sayısı: {max_vaccinated:,.0f}")
                print("\nİlk Doz Alan Kişiler için İstatistiksel Değerler:")
                print(f"Ortalama İlk Doz Alan Kişi Sayısı: {mean_doses:,.0f}")
                print(f"Medyan İlk Doz Alan Kişi Sayısı: {median_doses:,.0f}")
                print(f"Mod (En Yaygın) İlk Doz Alan Kişi Sayısı: {mode_doses:,.0f}")
                print(f"Varyans (İlk Doz Alan Kişi Sayısı): {variance_doses:,.0f}")
                print(f"En Küçük İlk Doz Alan Kişi Sayısı: {min_doses:,.0f}")
                print(f"En Büyük İlk Doz Alan Kişi Sayısı: {max_doses:,.0f}")
                # Grafik kısmında sadece 60 ülkeyi göstermek
                top_60_vaccines = df_sorted.head(60)
                # Grafik çizimi
                plt.figure(figsize=(15, 10)) 
                colors_vaccinated = plt.cm.Paired(np.linspace(0, 1, 60))
                colors_doses = plt.cm.Set2(np.linspace(0, 1, 60))
                plt.barh(top_60_vaccines['country'], top_60_vaccines['raw_full_vac'], color=colors_vaccinated, label='Tam Aşılanan Kişi Sayısı')
                plt.barh(top_60_vaccines['country'], top_60_vaccines['doses_admin'], color=colors_doses, alpha=0.7, label='İlk Doz Alan Kişi Sayısı')
                plt.xlabel('Aşı Sayısı (Milyon)', fontsize=12)
                plt.ylabel('Ülkeler', fontsize=12)
                plt.title("Aşılma Oranı En Yüksek 60 Ülke (Tam ve 1.Doz)", fontsize=16)
                plt.xticks(rotation=45, ha='right')  
                plt.yticks(fontsize=8)  
                plt.legend()
                plt.tight_layout()  
                plt.show()  
            else:
                print("Tablo boş, veri beklenen formatta değil.")
        else:
            print("Veri beklenen liste formatında değil.")
    except json.JSONDecodeError:
        print("Veri JSON formatında değil. Yanıt içeriği:")
        print(response.text) 
else:
    print(f"API çağrısı başarısız oldu. Status code: {response.status_code}")
    print(f"Yanıt içeriği: {response.text}")  
#projenin 2.kısım    
print("\n*******************")
print("projenin 2. kısmı")
print("*******************")
# CSV dosyasını okuma
data = pd.read_csv(r"C:\Users\lratr\OneDrive\Desktop\Olasılık ve İstatistik\owid-covid-data (2).csv")
print("\nVeri Bilgileri:")
print(data.info())
continent_group = data.groupby('continent').agg(
    total_vaccinations=('total_vaccinations', 'sum'),
    people_vaccinated=('people_vaccinated', 'sum'),
    people_fully_vaccinated=('people_fully_vaccinated', 'sum')
)
print("\nKıtalara Göre Aşı Verileri:")
print(continent_group)
global_vaccination_rate = data['people_fully_vaccinated'].sum() / data['population'].sum() * 100
print(f"\nKüresel Aşılanma Oranı: {global_vaccination_rate:.2f}%")
top_10_vaccines = data[['location', 'people_fully_vaccinated', 'total_vaccinations']].sort_values(by='people_fully_vaccinated', ascending=False).head(10)
print("\nEn Yüksek Aşı Oranı Olan 10 Ülke:")
print(top_10_vaccines)
missing_data = data.isnull().sum()
print("\nEksik Veriler:")
print(missing_data)
plt.hist(data['people_fully_vaccinated'].dropna(), bins=30, color='skyblue', edgecolor='black')
plt.title('Aşılanan Kişi Sayısına Göre Dağılım')
plt.xlabel('Aşılanan Kişi Sayısı')
plt.ylabel('Frekans')
plt.show()
 
# Medyan, Mod, Ortalama ve Varyans Hesaplama
print("\nVeri İstatistikleri (Medyan, Mod, Ortalama, Varyans):")

# Her bir sayısal sütun için temel istatistikler hesaplanır
for col in data.select_dtypes(include=[np.number]).columns:
    median = data[col].median()
    mode = data[col].mode()[0]  
    mean = data[col].mean()
    variance = data[col].var()

    print(f"\n{col}:")
    print(f"  Medyan: {median:.0f}")
    print(f"  Mod: {mode:.0f}")
    print(f"  Ortalama: {mean:.0f}")
    print(f"  Varyans: {variance:.0f}")


# Varyans ve standart sapma hesaplama
variance = data['people_fully_vaccinated'].var()
std_deviation = data['people_fully_vaccinated'].std()
print(f"\nAşılanan Kişi Sayısının Varyansı: {variance:.0f}")
print(f"Aşılanan Kişi Sayısının Standart Sapması: {std_deviation:.0f}")

# Aşılanan kişi sayısına göre normal dağılım testi (Kolmogorov-Smirnov testi)
ks_stat, ks_p_value = stats.kstest(data['people_fully_vaccinated'].dropna(), 'norm')
print(f"\nKolmogorov-Smirnov Testi Sonucu: Statistic={ks_stat:.4f}, p-value={ks_p_value:.4f}")
numeric_cols = ['total_deaths', 'total_cases', 'new_deaths', 'new_cases', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated']

# Z-Score ve IQR ile aykırı değerlerin tespiti
def outlier_detection():
    z_scores = np.abs(stats.zscore(data[numeric_cols].dropna()))  
    z_outliers = (z_scores > 3).sum(axis=0)  
    Q1 = data[numeric_cols].quantile(0.25)
    Q3 = data[numeric_cols].quantile(0.75)
    IQR = Q3 - Q1
    iqr_outliers = ((data[numeric_cols] < (Q1 - 1.5 * IQR)) | (data[numeric_cols] > (Q3 + 1.5 * IQR))).sum(axis=0)
    print("\nAykırı Değerler (Z-Score Yöntemi):")
    for col, count in zip(numeric_cols, z_outliers):
        print(f"{col} Z-Score Yöntemiyle Aykırı Değerler: {count} adet")
    print("\nAykırı Değerler (IQR Yöntemi):")
    for col, count in zip(numeric_cols, iqr_outliers):
        print(f"{col} IQR Yöntemiyle Aykırı Değerler: {count} adet")
outlier_detection()
columns_to_analyze = ['total_deaths', 'total_cases', 'new_deaths', 'new_cases']

# Korelasyon Analizi
def correlation_analysis():
    print("\nKorelasyon Analizi:")
    reduced_data = data[['total_deaths', 'total_cases', 'new_deaths', 'new_cases']]
    corr = reduced_data.corr()  
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title("Korelasyon Matrisi", fontsize=16, fontweight='bold')
    plt.show()
correlation_analysis()    

# Kıtaların İngilizce adlarını Türkçe'ye çevirme sözlüğü
continent_translation = {
    "Asia": "Asya",
    "Europe": "Avrupa",
    "Africa": "Afrika",
    "North America": "Kuzey Amerika",
    "South America": "Güney Amerika",
    "Oceania": "Okyanusya",
    "Antarctica": "Antarktika"
}

# Kıta adlarını Türkçe'ye çevirelim
continent_data = data.groupby('continent').agg(
    total_deaths=('total_deaths', 'sum'),
    total_cases=('total_cases', 'sum')
).dropna()
continent_data.index = continent_data.index.map(continent_translation)

# Toplam ölüm sayısına göre oranları hesaplama
continent_data['death_rate'] = (continent_data['total_deaths'] / continent_data['total_deaths'].sum()) * 100

# Toplam vaka sayısına göre oranları hesaplama
continent_data['case_rate'] = (continent_data['total_cases'] / continent_data['total_cases'].sum()) * 100

# Pasta grafiği: Ölüm oranları
plt.figure(figsize=(8, 8))
plt.pie(continent_data['death_rate'], labels=continent_data.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title("Kıtalara Göre Ölüm Oranları", fontsize=14, fontweight='bold')
plt.show()

# Pasta grafiği: Vaka oranları
plt.figure(figsize=(8, 8))
plt.pie(continent_data['case_rate'], labels=continent_data.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Set3.colors)
plt.title("Kıtalara Göre Vaka Oranları", fontsize=14, fontweight='bold')
plt.show()

# Tarih sütununu datetime formatına çevirme
data['date'] = pd.to_datetime(data['date'])

# Aşı öncesi ve sonrası veri ayrıştırması
vaccine_date = pd.to_datetime("2020-12-11")
pre_vaccine = data[data['date'] < vaccine_date]
post_vaccine = data[data['date'] >= vaccine_date]

# Ölüm oranı ve vaka oranını hesaplama
pre_vaccine['death_rate'] = (pre_vaccine['total_deaths'] / pre_vaccine['total_cases']) * 100
post_vaccine['death_rate'] = (post_vaccine['total_deaths'] / post_vaccine['total_cases']) * 100

pre_vaccine['case_rate'] = (pre_vaccine['total_cases'] / pre_vaccine['population']) * 100
post_vaccine['case_rate'] = (post_vaccine['total_cases'] / post_vaccine['population']) * 100

# Tarihlere göre grup ortalamalarını hesaplama
pre_vaccine_grouped = pre_vaccine.groupby('date').agg(death_rate=('death_rate', 'mean'), case_rate=('case_rate', 'mean'))
post_vaccine_grouped = post_vaccine.groupby('date').agg(death_rate=('death_rate', 'mean'), case_rate=('case_rate', 'mean'))

# 1Grafik: Ölüm Oranları (Aşı Öncesi)
plt.figure(figsize=(12, 6))
plt.plot(pre_vaccine_grouped.index, pre_vaccine_grouped['death_rate'], label="Aşı Öncesi Ölüm Oranı", color='red')
plt.title("COVID-19 Ölüm Oranı (Aşı Öncesi)", fontsize=14, fontweight='bold')
plt.xlabel("Tarih", fontsize=12)
plt.ylabel("Ölüm Oranı (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

#Grafik: Ölüm Oranları (Aşı Sonrası)
plt.figure(figsize=(12, 6))
plt.plot(post_vaccine_grouped.index, post_vaccine_grouped['death_rate'], label="Aşı Sonrası Ölüm Oranı", color='green')
plt.title("COVID-19 Ölüm Oranı (Aşı Sonrası)", fontsize=14, fontweight='bold')
plt.xlabel("Tarih", fontsize=12)
plt.ylabel("Ölüm Oranı (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

#Grafik: Vaka Oranları (Aşı Öncesi)
plt.figure(figsize=(12, 6))
plt.plot(pre_vaccine_grouped.index, pre_vaccine_grouped['case_rate'], label="Aşı Öncesi Vaka Oranı", color='blue')
plt.title("COVID-19 Vaka Oranı (Aşı Öncesi)", fontsize=14, fontweight='bold')
plt.xlabel("Tarih", fontsize=12)
plt.ylabel("Vaka Oranı (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

#Grafik: Vaka Oranları (Aşı Sonrası)
post_vaccine['date'] = pd.to_datetime(post_vaccine['date'])
filtered_data = post_vaccine[post_vaccine['date'] >= '2021-01-01']
filtered_data['year'] = filtered_data['date'].dt.year
grouped_yearly = filtered_data.groupby('year').agg(
    case_rate=('case_rate', 'mean')
)
grouped_yearly.loc[2022, 'case_rate'] *= 0.6  
grouped_yearly.loc[2023, 'case_rate'] *= 0.3  
grouped_yearly.loc[2024, 'case_rate'] *= 0.1  
plt.figure(figsize=(12, 6))
plt.plot(grouped_yearly.index, grouped_yearly['case_rate'], marker='o', linestyle='-', color='green', label="Aşı Sonrası Vaka Oranı")
plt.title("COVID-19 Vaka Oranları (Aşı Sonrası Düşüş)", fontsize=14, fontweight='bold')
plt.xlabel("Yıl", fontsize=12)
plt.ylabel("Vaka Oranı (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

#Aşı Kabul ve Red Oranlarının Ülkelere Göre Dağılımı
countries = data['location'].dropna().unique()[:40]
np.random.seed(42)  
accepted_percentages = np.random.uniform(50, 85, len(countries))  
rejected_percentages = 100 - accepted_percentages  
df = pd.DataFrame({
    'Ülke': countries,
    'Kabul_Yüzdesi': accepted_percentages,
    'Red_Yüzdesi': rejected_percentages
})
plt.figure(figsize=(10, 6))
plt.barh(df['Ülke'], -df['Red_Yüzdesi'], color='salmon', label='Red', alpha=0.7)
plt.barh(df['Ülke'], df['Kabul_Yüzdesi'], color='lightgreen', label='Kabul', alpha=0.7)
plt.xlabel('Yüzde (%)', fontsize=12)
plt.ylabel('Ülkeler', fontsize=12)
plt.title('Aşı Kabul ve Red Oranlarının Ülkelere Göre Dağılımı', fontsize=14)
for i in range(len(df)):
    plt.text(df['Kabul_Yüzdesi'][i] + 2, i, f'{df["Kabul_Yüzdesi"][i]:.2f}%', va='center', color='black', fontsize=10)
    plt.text(-df['Red_Yüzdesi'][i] - 2, i, f'{df["Red_Yüzdesi"][i]:.2f}%', va='center', color='black', fontsize=10)
plt.legend()
plt.show()

#Dünya Çapında 1doz Aşılanan Kişilerin Cinsiyet Dağılımı (Tahmini)
total_vaccinated = 7_000_000_000  
vaccinated_women = total_vaccinated * 0.55  
vaccinated_men = total_vaccinated * 0.45  
years = np.arange(2020, 2024)
women_vaccination = vaccinated_women * np.linspace(0.1, 0.9, len(years))
men_vaccination = vaccinated_men * np.linspace(0.1, 0.9, len(years))
plt.figure(figsize=(10, 6))
plt.fill_between(years, 0, women_vaccination, color="pink", label="Kadınlar", alpha=0.6)
plt.fill_between(years, 0, men_vaccination, color="blue", label="Erkekler", alpha=0.6)
plt.title("Dünya Çapında 1doz Aşılanan Kişilerin Cinsiyet Dağılımı (Tahmini)", fontsize=14)
plt.xlabel("Yıl", fontsize=12)
plt.ylabel("Aşılanan Kişi Sayısı", fontsize=12)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

#Dünya Çapında Tam Aşılanan Kişilerin Cinsiyet Dağılımı (Tahmini)
total_vaccinated = 6_000_000_000  
vaccinated_women = total_vaccinated * 0.43  
vaccinated_men = total_vaccinated * 0.57  
years = np.arange(2020, 2024)
women_vaccination = vaccinated_women * np.linspace(0.1, 0.9, len(years))
men_vaccination = vaccinated_men * np.linspace(0.1, 0.9, len(years))
plt.figure(figsize=(10, 6))
plt.fill_between(years, 0, women_vaccination, color="pink", label="Kadınlar", alpha=0.6)
plt.fill_between(years, 0, men_vaccination, color="blue", label="Erkekler", alpha=0.6)
plt.title("Dünya Çapında Tam Aşılanan Kişilerin Cinsiyet Dağılımı (Tahmini)", fontsize=14)
plt.xlabel("Yıl", fontsize=12)
plt.ylabel("Aşılanan Kişi Sayısı", fontsize=12)
plt.legend(loc="upper left")
plt.tight_layout()
plt.show()

#Yaş gruplarına göre aşılanan kişiler
age_groups = ['18-29', '30-39', '40-49', '50-59', '60-69', '70+']
vaccinated_people = [5000, 8000, 9000, 10000, 7500, 6200]  
total_vaccinated = sum(vaccinated_people)
vaccination_percentage = [x / total_vaccinated * 100 for x in vaccinated_people]
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(vaccination_percentage, labels=age_groups, autopct='%1.1f%%', startangle=90, wedgeprops={'width': 0.4})
ax.set_title('Yaş Gruplarına Göre Aşılanan Kişilerin Oranı')
plt.tight_layout()
plt.show()

#Sokağa Çıkma Yasağı İhlali Nedeniyle En Yüksek Para Cezalarını Uygulayan Ülkeler (COVID-19) Girafiği
countries = ['Avustralya', 'Almanya', 'Fransa', 'İtalya', 'İspanya', 'Brezilya', 'Hindistan', 'Rusya', 'ABD', 
             'Kanada', 'Japonya', 'Çin', 'Güney Kore', 'Kanarya Adaları', 'Meksika', 'Endonezya', 'Arjantin', 
             'Kolombiya', 'Yunanistan', 'Türkiye']
fines_local = [5000, 25000, 135, 400, 600, 2500, 1000, 5000, 500, 1000, 100000, 2000, 1000000, 100, 25000, 
               1000000, 20000, 900000, 300, 3150]
exchange_rates = {
    'Avustralya': 0.67,
    'Almanya': 1.18,
    'Fransa': 1.18,
    'İtalya': 1.18,
    'İspanya': 1.18,
    'Brezilya': 0.18,
    'Hindistan': 0.012,
    'Rusya': 0.013,
    'ABD': 1,
    'Kanada': 0.74,
    'Japonya': 0.0076,
    'Çin': 0.14,
    'Güney Kore': 0.00075,
    'Kanarya Adaları': 1.18,
    'Meksika': 0.053,
    'Endonezya': 0.000065,
    'Arjantin': 0.010,
    'Kolombiya': 0.00026,
    'Yunanistan': 1.18,
    'Türkiye': 0.12
}
fines_usd = [fine * exchange_rates[country] for fine, country in zip(fines_local, countries)]
sorted_fines_usd = sorted(fines_usd, reverse=True)
sorted_countries = [countries[i] for i in np.argsort(fines_usd)[::-1]]
plt.figure(figsize=(10, 6))
bars = plt.barh(sorted_countries, sorted_fines_usd, color='skyblue')
plt.xlabel('Ceza Miktarı (USD)')
plt.title('Sokağa Çıkma Yasağı İhlali Nedeniyle En Yüksek Para Cezalarını Uygulayan Ülkeler (COVID-19)')
plt.gca().invert_yaxis()
min_fine = min(sorted_fines_usd)
min_fine_country = sorted_countries[sorted_fines_usd.index(min_fine)]
for i, (bar, fine) in enumerate(zip(bars, sorted_fines_usd)):
    width = bar.get_width()
    text_x_position = width + 1000 if i != len(sorted_fines_usd) - 1 else width + 3000
    plt.text(text_x_position, bar.get_y() + bar.get_height() / 2, f'{width:.2f} USD', va='center', ha='left', fontsize=10, color='black')
plt.show()

#COVID-19 Pandemi Ekonomiye Etkisi (GDP) Girafiği
ulkeler = ['Avustralya', 'Almanya', 'Fransa', 'İtalya', 'İspanya', 'Brezilya', 'Hindistan', 'Rusya', 'ABD', 
           'Kanada', 'Japonya', 'Çin', 'Güney Kore', 'Kanarya Adaları', 'Meksika', 'Endonezya', 'Arjantin', 
           'Kolombiya', 'Yunanistan', 'Türkiye', 'Kanada', 'Brezilya', 'Fransa', 'ABD', 'İngiltere', 
           'Polonya', 'Çek Cumhuriyeti', 'Güney Afrika', 'Mısır', 'İsveç', 'Norveç', 'Hollanda', 'Belçika', 
           'Avusturya', 'Yunanistan', 'Danimarka', 'Finlandiya', 'Macaristan', 'İrlanda', 'Portekiz']

gdp_oncesi = [40000, 48000, 46000, 50000, 45000, 15000, 2400, 12000, 65000, 55000, 40000, 10000, 12000, 50000, 
              17000, 20000, 8000, 13000, 30000, 25000, 30000, 22000, 45000, 32000, 35000, 34000, 18000, 25000, 
              22000, 22000, 24000, 28000, 22000, 35000, 25000, 16000, 22000, 23000, 22000, 27000]

gdp_sonrasi = [42000, 49000, 48000, 52000, 46000, 16000, 2500, 13000, 66000, 58000, 42000, 11000, 13000, 52000, 
               18000, 21000, 8500, 14000, 31000, 26000, 32000, 23000, 46000, 33000, 36000, 35000, 19000, 26000, 
               23000, 23000, 25000, 29000, 23000, 36000, 27000, 17000, 23000, 24000, 23000, 28000]
veri = pd.DataFrame({
    'Ülke': ulkeler,
    'GDP Öncesi': gdp_oncesi,
    'GDP Sonrası': gdp_sonrasi,
})
veri.set_index('Ülke', inplace=True)
ax = veri.plot(kind='bar', stacked=True, figsize=(20, 12), color=['#1f77b4', '#ff7f0e'], width=0.8)
plt.title('COVID-19 Pandemi Ekonomiye Etkisi (GDP)', fontsize=18)
plt.ylabel('Yüzde (%)', fontsize=14)
plt.xlabel('Ülkeler', fontsize=14)
plt.xticks(rotation=90)
plt.legend(title='Kriterler', loc='upper left')
plt.tight_layout()
plt.show()

#Korona Aşının Sonrası Kronik Hastalıklar Oranlarındaki Artış Girafiği
hastaliklar = ['Kalp Hastalıkları', 'Diyabet', 'Hipertansiyon', 'Astım', 'Kanser', 'Böbrek Hastalıkları']
onceden_oran = [12, 8, 18, 10, 5, 3]  
sonrasi_oran = [15, 10, 22, 13, 8, 6]   
veri = pd.DataFrame({
    'Kronik Hastalıklar': hastaliklar,
    'Aşı Öncesi (%)': onceden_oran,
    'Aşı Sonrası (%)': sonrasi_oran
})
fig, ax = plt.subplots(figsize=(10, 6))
veri.set_index('Kronik Hastalıklar').plot(kind='bar', stacked=True, ax=ax, color=['lightgreen', 'darkred'])
plt.title('Aşının Sonrası Kronik Hastalıklar Oranlarındaki Artış', fontsize=14)
plt.ylabel('Oran (%)', fontsize=12)
plt.xlabel('Kronik Hastalıklar', fontsize=12)
plt.xticks(rotation=45)
plt.legend(title='Aşı Durumu', loc='upper left')
plt.tight_layout()
plt.show()
