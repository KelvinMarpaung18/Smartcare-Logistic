# SmartCare Logistics: Enterprise AI Copilot Optimasi Rute Distribusi Obat & Darah Darurat

Sistem purwarupa cerdas berbasis *State-Space Search* (Uniform Cost Search & A* Search) untuk penentuan alur pengiriman dan distribusi obat serta kantong darah darurat antar-fasilitas kesehatan.

---

## 👥 Anggota Kelompok & Pembagian Peran

* **Kelompok**: 06
* **Anggota Tim**:
  * **Kelvin Yohanes Putra-12S24018** - *AI Architect & Model Lead*
  * **Amelia L.Batu-12S24031** - *Data & Integration Engineer*
  * **Nikah Suchia Panjaitan-12S24041** - *QA, Evaluation & Ethics Lead*

---

## 📌 Problem Framing & Bisnis

* **Domain Bisnis**: Logistik Rantai Pasok Kesehatan Enterprise (*Time-Critical Medical Supply Chain Logistics*).
* **Pain Points Utama**:
  1. Risiko keterlambatan pengiriman sampel darah atau obat esensial yang berdampak langsung pada keselamatan jiwa pasien.
  2. Kondisi kemacetan lalu lintas perkotaan yang tidak dapat diprediksi secara manual oleh pengemudi armada logistik.
  3. Sampel biologis dan kantong darah memiliki batas waktu ketahanan suhu (*shelf life*) saat ditranspor di luar fasilitas pendingin sentral.
* **Justifikasi Solusi AI**: Penerapan algoritma pencarian ruang keadaan (*State-Space Search*) berbasis **Uniform Cost Search (UCS)** dan **A* Search** memungkinkan kalkulasi rute distribusi terpendek dengan akumulasi waktu tempuh paling minimal secara presisi dan deterministik.

---

## 🎯 Spesifikasi Formal Agen PEAS

* **P (Performance Measure)**: Minimasi waktu tempuh pengiriman (< 20 menit), minimasi total akumulasi jarak/biaya operasional, dan ketepatan waktu pengiriman 100%.
* **E (Environment)**: Jaringan rute jalan antar-Fasilitas Kesehatan (Bank Darah Sentral $\rightarrow$ Rumah Sakit Tujuan), titik persimpangan jalan, dan kondisi tingkat kemacetan.
* **A (Actuators)**: Panel instruksi navigasi rute otomatis pada dasbor pengemudi armada medis.
* **S (Sensors)**: Sensor koordinat GPS kendaraan, sensor pemantau suhu boks medis, dan data masukan API pemantau jarak/kondisi jalan.

### Karakteristik Lingkungan Operasional
* **Partially Observable**: Agen tidak memprediksi kemacetan mendadak secara mutlak sebelum melaluinya.
* **Stochastic**: Waktu tempuh aktual dapat berubah akibat dinamika lalu lintas dan cuaca.
* **Dynamic**: Kondisi kepadatan jalan terus berubah seiring berjalannya waktu.
* **Discrete**: Jaringan lokasi dipetakan secara formal ke dalam ruang keadaan berhingga (*nodes* dan *edges*).

---

## 🧮 Formulasi Ruang Keadaan Matematika $(X, A, T, G, C)$

* **State Space ($X$)**: `{ "PMI_Pusat", "RS_A", "RS_B", "RS_C", "RS_D", "RS_E", "RS_Darurat_UAS" }`
* **Actions ($A$)**: Opsi perpindahan jalan dari lokasi $x_i$ ke lokasi tetangga $x_j$.
* **Transition Model ($T$)**: $T(x_i, a) = x_j$.
* **Goal Test ($G$)**: Agen mencapai lokasi rumah sakit tujuan darurat (`RS_Darurat_UAS`).
* **Path Cost ($C$)**: Akumulasi total waktu tempuh perjalanan $\sum \text{weight}(e)$.

### 📊 Visualisasi Graf Ruang Keadaan

```mermaid
graph LR
    PMI[PMI_Pusat] -->|10 min| RSA[RS_A]
    PMI -->|5 min| RSB[RS_B]
    RSA -->|12 min| RSC[RS_C]
    RSA -->|8 min| RSD[RS_D]
    RSB -->|18 min| RSC
    RSB -->|15 min| RSE[RS_E]
    RSC -->|10 min| Goal((RS_Darurat_UAS))
    RSD -->|14 min| Goal
    RSE -->|12 min| Goal
```

### 🧠 Nilai Heuristik $h(n)$ (Terbukti Admissible $h(n) \le h^*(n)$)

| Node ($n$) | Estimasi Waktu ke Goal $h(n)$ | Biaya Aktual Terpendek $h^*(n)$ | Status Admissible |
|---|---|---|---|
| `PMI_Pusat` | 30.0 min | 32.0 min | ✅ $30.0 \le 32.0$ |
| `RS_A` | 20.0 min | 22.0 min | ✅ $20.0 \le 22.0$ |
| `RS_B` | 26.0 min | 27.0 min | ✅ $26.0 \le 27.0$ |
| `RS_C` | 9.0 min | 10.0 min | ✅ $9.0 \le 10.0$ |
| `RS_D` | 13.0 min | 14.0 min | ✅ $13.0 \le 14.0$ |
| `RS_E` | 11.0 min | 12.0 min | ✅ $11.0 \le 12.0$ |
| `RS_Darurat_UAS` | 0.0 min | 0.0 min | ✅ $0.0 \le 0.0$ |

---

## 📁 Struktur Repositori

```text
SmartCare-Logistics/
├── .venv/                  # Virtual Environment
├── src/
│   ├── smartcare_logistics/
│   │   ├── __init__.py
│   │   └── search.py       # Algoritma UCS & A* Search (heapq)
│   └── main.py             # Skrip simulasi utama
├── tests/
│   └── test_search.py      # Pengujian otomatis pytest
├── .gitignore
├── .python-version
├── LICENSE                 # Lisensi MIT
├── pyproject.toml          # Dependensi Astral uv
├── README.md               # Dokumentasi utama
└── uv.lock
```

---

## 🚀 Instruksi Eksekusi

1. **Sinkronkan Environment & Dependensi (Astral `uv`)**:
   ```powershell
   uv sync
   ```

2. **Menjalankan Simulasi (Optimasi Rute UCS & A*)**:
   ```powershell
   uv run python src/main.py
   ```

3. **Menjalankan Pengujian Otomatis (Pytest)**:
   ```powershell
   uv run pytest
   ```
