import numpy as np
import matplotlib.pyplot as plt

# Диапазон расстояний (м)
d = np.linspace(100, 5000, 500)
d_km = d / 1000  # для моделей, где d в км
d_GHz = d / 1e9  # не используется, но для справки

Pt = 43  # дБм

# --- 4G (3D-UMi-NLOS) ---
fc_4g = 2.6  # ГГц
PL_4g = 36.7 * np.log10(d) + 22.7 + 26 * np.log10(fc_4g)
Pr_4g = Pt - PL_4g - 20  # минус 20 дБ на стены

# --- 3G (ITU M.1225) ---
fc_3g = 2100  # МГц
PL_3g = 40 * np.log10(d_km) + 30 * np.log10(fc_3g) + 49
Pr_3g = Pt - PL_3g

# --- 2G (Hata-Okumura) ---
fc_2g = 900
hte = 30
hre = 1.5
a_hre = (1.1 * np.log10(fc_2g) - 0.7) * hre - (1.56 * np.log10(fc_2g) - 0.8)
PL_2g = (69.55 + 26.16 * np.log10(fc_2g) - 13.82 * np.log10(hte)
         - a_hre + (44.9 - 6.55 * np.log10(hte)) * np.log10(d_km))
Pr_2g = Pt - PL_2g

# --- Построение ---
plt.figure(figsize=(10, 6))
plt.plot(d, Pr_2g, label='2G (Hata)', color='blue')
plt.plot(d, Pr_3g, label='3G (ITU M.1225)', color='green')
plt.plot(d, Pr_4g, label='4G (3D-UMi-NLOS + стены)', color='red')
plt.axhline(y=-100, color='black', linestyle='--', label='Порог −100 дБм')
plt.xlabel('Расстояние d, м')
plt.ylabel('Мощность на входе приёмника $P_r$, дБм')
plt.title('Зависимость мощности сигнала от расстояния')
plt.grid(True, which='both', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.savefig('Pr_vs_d.png', dpi=300)
plt.show()