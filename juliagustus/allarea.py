import pandas as pd
import matplotlib.pyplot as plt

data = {
    'Area Sales': [
        'JAKARTA','DEPOK','CENGKARENG','TANGGERANG SELATAN (CIPUTAT)','KOTA TANGGERANG (PORIS)',
        'KAB TANGGERANG (LEGOK CIKASUNGKA)','KLAPANUNGGAL','CILEUNGSI','CIANJUR','PARUNG BOGOR',
        'TAMBUN','SERANG','KAB PANDEGLANG','CILEGON','CIREBON','SUBANG','KARAWANG','PURWAKARTA',
        'CISOLOK','TASIKMALAYA','KAB. TASIK','CIAMIS','CIAWI','BANDUNG','GARUT','BANJAR',
        'SEMARANG','KUDUS','KENDAL','DEMAK','SOLO','PURWOKERTO','JOGJA','KLATEN','KEBUMEN',
        'CILACAP','TEGAL','KEDIRI','MALANG','PONOROGO','BADUNG','TABANAN','DENPASAR','NEGARA',
        'BANGKA BELITUNG','MEDAN','SURABAYA'
    ],
    'Target': [
        640,570,25,380,230,230,190,150,150,190,190,340,150,150,530,380,150,150,150,490,
        150,300,190,190,490,490,1360,100,340,300,640,150,570,230,225,340,240,420,150,150,
        640,150,530,300,450,300,190
    ],
    'CA': [
        370,315,0,247,102,100,143,152,78,21,156,201,100,103,454,231,82,26,56,471,
        126,250,160,237,434,371,1346,50,312,175,283,58,269,80,87,241,206,147,16,16,
        426,42,230,157,218,282,20
    ],
    'MinusPlus': [
        -270,-255,-25,-133,-128,-130,-47,2,-72,-169,-34,-139,-50,-47,-76,-149,-68,-124,
        -94,-19,-24,-50,-30,47,-56,-119,-14,-50,-28,-125,-357,-92,-301,-150,-138,-99,
        -34,-273,-134,-134,-214,-108,-300,-143,-232,-18,-170
    ],
    'Persen': [
        58,55,0,65,44,43,75,101,52,11,82,59,67,69,86,61,55,17,37,96,
        84,83,84,125,89,76,99,50,92,58,44,39,47,35,39,71,86,35,11,11,
        67,28,43,52,48,94,11
    ]
}

df = pd.DataFrame(data)

# rumus
total_target = df['Target'].sum()
total_ca = df['CA'].sum()
total_minusplus = df['MinusPlus'].sum()
total_persen = round((total_ca / total_target) * 100, 2)


# plot kurva
plt.figure(figsize=(15,7))

plt.plot(df['Area Sales'], df['Target'], marker='o', label='Target')
plt.plot(df['Area Sales'], df['CA'], marker='s', label='CA (Sales)')
plt.plot(df['Area Sales'], df['MinusPlus'], marker='^', label='Minus/Plus')
plt.plot(df['Area Sales'], df['Persen'], marker='d', label='Persen (%)')

plt.xticks(rotation=90)
plt.ylabel("Nilai")
plt.title("Kurva Data Sales per Area")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.show()

# terminal
print("=== RINGKASAN TOTAL ===")
print(f"Total Target     : {total_target}")
print(f"Total CA         : {total_ca}")
print(f"Total MinusPlus  : {total_minusplus}")
print(f"Rata-rata Persen : {total_persen}%")