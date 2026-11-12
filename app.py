import streamlit as st
import pandas as pd

# =========================================================
# 1. KONFIGURASI APLIKASI
# =========================================================
st.set_page_config(
    page_title="Tugas 2 AUSI - Audit COBIT 5",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# 2. DESAIN APLIKASI (CSS)
# =========================================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #edf5ff, #ffffff, #e8f2ff);
    color: #17365d;
}
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(120deg, #082b59, #1266b3, #42a5f5);
    padding: 32px;
    border-radius: 18px;
    color: white;
    margin-bottom: 24px;
}
.hero h1, .hero h3, .hero p { color: white !important; margin: 4px 0; }
.section-title {
    background: linear-gradient(90deg, #d9ebff, #f1f7ff);
    border-left: 6px solid #1976d2;
    padding: 12px 18px;
    border-radius: 10px;
    margin: 24px 0 12px;
    color: #103b70;
    font-size: 18px;
    font-weight: 800;
}
.info-card {
    background: white;
    padding: 18px 22px;
    border-radius: 14px;
    border: 1px solid #d4e6fa;
    margin-bottom: 16px;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #d7e8f9;
    border-radius: 12px;
    padding: 14px;
}
.footer {
    text-align: center;
    color: #54718f;
    font-size: 13px;
    padding: 22px 0;
    border-top: 1px solid #d5e5f5;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. DATA INSTRUMEN AUDIT COBIT 5 (27 PERTANYAAN)
# =========================================================
domains = {
    "EDM": {
        "name": "Evaluate, Direct and Monitor",
        "focus": "Tata kelola: memastikan TI memberi nilai bagi bisnis, risiko terkendali, dan sumber daya digunakan optimal.",
        "questions": [
            ("EDM01", "Apakah perusahaan memiliki kerangka tata kelola TI (kebijakan, peran, wewenang) yang disetujui direksi?",
             "Piagam/kebijakan tata kelola TI, SK direksi", "W, D"),
            ("EDM02", "Apakah investasi TI dievaluasi manfaatnya (business case, ROI) sebelum dan sesudah disetujui?",
             "Business case, laporan realisasi manfaat", "D, W"),
            ("EDM03", "Apakah ada penetapan selera risiko (risk appetite) TI dan ambang toleransi oleh manajemen?",
             "Dokumen risk appetite, notulen rapat risiko", "D"),
            ("EDM04", "Apakah ketersediaan sumber daya TI (SDM, anggaran, infrastruktur) dievaluasi terhadap kebutuhan strategi bisnis?",
             "Rencana anggaran TI, laporan kapasitas SDM", "D, W"),
            ("EDM05", "Apakah direksi menerima laporan kinerja TI dan kepatuhan secara berkala, dan ada tindak lanjutnya?",
             "Laporan ke direksi, notulen, daftar tindak lanjut", "D, W")
        ]
    },
    "APO": {
        "name": "Align, Plan and Organize",
        "focus": "Perencanaan: menyelaraskan strategi TI dengan strategi bisnis dan mengatur organisasi TI.",
        "questions": [
            ("APO01", "Apakah struktur organisasi TI, uraian tugas, dan pemisahan tugas (segregation of duties) telah ditetapkan?",
             "Struktur organisasi, job description, matriks SoD", "D, W"),
            ("APO02", "Apakah ada rencana strategis TI yang selaras dengan rencana strategis bisnis dan ditinjau berkala?",
             "Renstra TI, roadmap, hasil review tahunan", "D"),
            ("APO07", "Apakah pengelolaan SDM TI (rekrutmen, pelatihan, evaluasi kompetensi) terdokumentasi dan berjalan?",
             "Rencana pelatihan, rekap kompetensi, penilaian kinerja", "D, W"),
            ("APO12", "Apakah risiko TI diidentifikasi, dinilai, dan dicatat dalam risk register beserta rencana mitigasinya?",
             "Risk register, laporan penilaian risiko", "D, W"),
            ("APO13", "Apakah ada kebijakan dan sistem manajemen keamanan informasi (misalnya mengacu ISO 27001) yang diterapkan?",
             "Kebijakan keamanan, SOP, hasil sosialisasi", "D, W, O"),
            ("APO10", "Apakah vendor TI (cloud, payment gateway, logistik) dipilih, dikontrak, dan dipantau dengan SLA yang jelas?",
             "Kontrak, SLA, laporan evaluasi vendor", "D")
        ]
    },
    "BAI": {
        "name": "Build, Acquire and Implement",
        "focus": "Pembangunan: pengadaan, pengembangan, perubahan, dan implementasi solusi TI.",
        "questions": [
            ("BAI01", "Apakah program/proyek TI dikelola dengan metodologi baku (rencana, jadwal, anggaran, pelaporan)?",
             "Dokumen proyek, project charter, laporan progres", "D, W"),
            ("BAI02", "Apakah kebutuhan pengguna didefinisikan dan disetujui sebelum pengembangan atau pembelian sistem?",
             "Dokumen kebutuhan (SRS/BRD), persetujuan pengguna", "D"),
            ("BAI03", "Apakah solusi (aplikasi) dibangun/diadakan dengan pengujian memadai (UAT, uji keamanan) sebelum rilis?",
             "Rencana dan hasil uji, berita acara UAT", "D, T"),
            ("BAI06", "Apakah perubahan sistem diajukan, disetujui, diuji, dan dicatat melalui prosedur change management?",
             "Formulir permintaan perubahan, log perubahan", "D, T"),
            ("BAI07", "Apakah ada rencana migrasi/cutover dan pelatihan pengguna sebelum sistem baru dipakai?",
             "Rencana migrasi, materi dan absensi pelatihan", "D, W"),
            ("BAI09", "Apakah aset TI (perangkat keras, perangkat lunak, lisensi) tercatat dan dikelola sepanjang siklus hidupnya?",
             "Daftar aset TI, bukti lisensi", "D, O")
        ]
    },
    "DSS": {
        "name": "Deliver, Service and Support",
        "focus": "Operasional: penyampaian layanan TI, dukungan, dan keamanan operasional.",
        "questions": [
            ("DSS01", "Apakah operasi TI harian (penjadwalan, pemantauan, backup) dijalankan sesuai prosedur?",
             "SOP operasi, log pemantauan, jadwal backup", "D, O"),
            ("DSS02", "Apakah permintaan layanan dan insiden dicatat, diprioritaskan, dan diselesaikan sesuai target waktu (help desk)?",
             "Tiket insiden, laporan SLA help desk", "D, T"),
            ("DSS03", "Apakah akar masalah dari insiden berulang dianalisis dan ditindaklanjuti (problem management)?",
             "Laporan analisis masalah, known error log", "D"),
            ("DSS04", "Apakah ada rencana kelangsungan bisnis dan pemulihan bencana (BCP/DRP) yang diuji secara berkala?",
             "Dokumen BCP/DRP, laporan uji pemulihan", "D, W"),
            ("DSS05", "Apakah keamanan layanan dikendalikan (hak akses, antivirus, firewall, enkripsi, patching)?",
             "Daftar hak akses, konfigurasi firewall, log patching", "T, O, D"),
            ("DSS06", "Apakah kontrol proses bisnis (otorisasi transaksi, validasi input, rekonsiliasi) dan perlindungan data pelanggan diterapkan?",
             "Log transaksi, prosedur rekonsiliasi, kebijakan privasi", "D, T")
        ]
    },
    "MEA": {
        "name": "Monitor, Evaluate and Assess",
        "focus": "Pemantauan: pengukuran kinerja, kepatuhan, dan kecukupan pengendalian internal.",
        "questions": [
            ("MEA01", "Apakah indikator kinerja TI (KPI) ditetapkan, diukur, dan dilaporkan secara berkala?",
             "Dokumen KPI, dashboard, laporan kinerja", "D"),
            ("MEA02", "Apakah sistem pengendalian internal TI dipantau dan hasil audit internal ditindaklanjuti?",
             "Laporan audit internal, status tindak lanjut", "D, W"),
            ("MEA03", "Apakah perusahaan mengidentifikasi dan mematuhi regulasi terkait (UU ITE, UU PDP, standar pembayaran)?",
             "Daftar regulasi, bukti kepatuhan", "D, W"),
            ("MEA04", "Apakah ada jaminan independen (audit eksternal, penetration test) atas sistem informasi?",
             "Laporan audit eksternal, hasil uji penetrasi", "D")
        ]
    }
}

level_names = {
    0: "Incomplete (Proses tidak ada atau gagal mencapai tujuannya)",
    1: "Performed (Dilaksanakan, tetapi belum terencana/terdokumentasi)",
    2: "Managed (Direncanakan, dipantau, dan hasil kerjanya terdokumentasi)",
    3: "Established (Mengikuti standar dan diterapkan secara konsisten)",
    4: "Predictable (Diukur dengan metrik kuantitatif dalam batas ditetapkan)",
    5: "Optimizing (Diperbaiki berkelanjutan berdasarkan inovasi dan analisis)"
}

level_short = {
    0: "Incomplete",
    1: "Performed",
    2: "Managed",
    3: "Established",
    4: "Predictable",
    5: "Optimizing"
}

def rekomendasi_otomatis(gap):
    if gap > 2:
        return "Prioritas Tinggi (T): Susun kebijakan/SOP formal, tetapkan PIC, dan lakukan pemantauan ketat."
    elif gap > 0:
        return "Prioritas Sedang (S): Tingkatkan konsistensi penerapan, lengkapi dokumentasi, dan evaluasi berkala."
    elif gap == 0:
        return "Prioritas Rendah (R): Pertahankan standar proses yang ada dan lakukan review berkala."
    return "Melampaui Target: Pertahankan praktik terbaik dan lakukan inovasi berkelanjutan."

# =========================================================
# 4. HEADER APLIKASI
# =========================================================
st.markdown("""
<div class="hero">
    <h1>TUGAS 2 — IMPLEMENTASI AUDIT SISTEM INFORMASI (COBIT 5)</h1>
    <h3>PT Nusantara Retail Digital</h3>
    <p>Dosen Pengampu: Dr. Ir. Arif Setiawan S.Kom., M.Cs | Program Studi Sistem Informasi - Universitas Muria Kudus</p>
    <b>Domain: EDM • APO • BAI • DSS • MEA</b>
</div>
""", unsafe_allow_html=True)

with st.expander("ℹ️ Panduan Skala Tingkat Kapabilitas COBIT (Level 0 - 5)", expanded=False):
    df_skala = pd.DataFrame([
        {"Level": k, "Nama": level_short[k], "Keterangan": v.split("(")[1].replace(")", "")}
        for k, v in level_names.items()
    ])
    st.dataframe(df_skala, hide_index=True)

# =========================================================
# 5. FORM INPUT AUDIT
# =========================================================
with st.form("form_audit_tugas2"):
    st.markdown('<div class="section-title">A. INFORMASI UMUM AUDIT</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        perusahaan = st.text_input("Nama Perusahaan", value="PT Nusantara Retail Digital")
        bidang = st.text_input("Bidang Usaha", value="Ritel dan e-commerce (toko online, marketplace, gudang, pengiriman)")
        objek = st.text_input(
            "Sistem yang Diaudit",
            value="ERP (keuangan, persediaan, pembelian), website dan aplikasi toko online, sistem POS, payment gateway, data center / cloud"
        )
        auditor = st.text_input("Auditor", value="Widyawati (202453036)")

    with col2:
        lokasi = st.text_input("Lokasi Audit", value="Kantor Pusat PT Nusantara Retail Digital, Semarang")
        periode = st.text_input("Periode Audit", value="1 Januari 2026 - 30 September 2026")
        tgl_pelaksanaan = st.text_input("Tanggal Pelaksanaan", value="19 - 23 Oktober 2026")
        auditee = st.text_input(
            "Auditee / Narasumber",
            value="Rudi Hartono (CIO), Sari Wulandari (Manajer TI), Dedi Kurniawan (Manajer Keuangan), Maya Putri (Manajer Gudang)"
        )
        metode = st.multiselect(
            "Metode Pengumpulan Bukti",
            ["Wawancara (W)", "Observasi (O)", "Telaah Dokumen (D)", "Pengujian/Inspeksi Sistem (T)"],
            default=["Wawancara (W)", "Observasi (O)", "Telaah Dokumen (D)", "Pengujian/Inspeksi Sistem (T)"]
        )

    st.markdown('<div class="section-title">B. DAFTAR PERTANYAAN AUDIT PER DOMAIN COBIT (27 ITEM)</div>', unsafe_allow_html=True)
    st.caption("Isi skor kapabilitas (0–5) dan temuan/catatan auditor untuk setiap pertanyaan.")

    skor_input = {}
    bukti_input = {}
    target_input = {}

    for domain_code, domain in domains.items():
        st.markdown(f'<div class="section-title">{domain_code} - {domain["name"]}</div>', unsafe_allow_html=True)
        st.caption(f"Fokus Domain: {domain['focus']}")

        for code, question, evidence, method in domain["questions"]:
            with st.expander(f"{code} — {question}", expanded=False):
                st.write(f"**Bukti yang Diperiksa:** {evidence}")
                st.write(f"**Metode:** {method}")
                c_skor, c_cat = st.columns([1, 2])
                with c_skor:
                    skor_input[code] = st.selectbox(
                        f"Skor {code} (0-5)",
                        options=[0, 1, 2, 3, 4, 5],
                        index=2,
                        format_func=lambda x: f"{x} - {level_short[x]}",
                        key=f"score_{code}"
                    )
                with c_cat:
                    bukti_input[code] = st.text_input(
                        f"Temuan / Catatan Auditor {code}",
                        placeholder="Masukkan temuan atau bukti hasil pemeriksaan...",
                        key=f"evidence_{code}"
                    )

        target_input[domain_code] = st.selectbox(
            f"Target Level Domain {domain_code} (Acuan Awal: Level 3)",
            options=[0, 1, 2, 3, 4, 5],
            index=3,
            format_func=lambda x: f"Level {x} - {level_short[x]}",
            key=f"target_{domain_code}"
        )

    st.markdown('<div class="section-title">C. TEMUAN UTAMA DAN REKOMENDASI (OPSIONAL / MANUAL)</div>', unsafe_allow_html=True)
    temuan_manual = []
    for i in range(1, 5):
        with st.expander(f"Temuan Utama #{i}", expanded=(i == 1)):
            tc1, tc2, tc3 = st.columns([1, 2, 1])
            with tc1:
                t_kode = st.text_input(f"Domain / Kode #{i}", placeholder="Misal: APO13", key=f"tkode_{i}")
                t_prio = st.selectbox(f"Prioritas #{i}", ["T (Tinggi)", "S (Sedang)", "R (Rendah)"], key=f"tprio_{i}")
            with tc2:
                t_temuan = st.text_input(f"Temuan #{i}", placeholder="Deskripsi temuan...", key=f"ttemuan_{i}")
                t_risiko = st.text_input(f"Risiko #{i}", placeholder="Dampak/risiko bisnis...", key=f"trisiko_{i}")
            with tc3:
                t_rekom = st.text_area(f"Rekomendasi #{i}", placeholder="Saran perbaikan...", key=f"trekom_{i}", height=100)
            temuan_manual.append({
                "No": i, "Domain / Kode": t_kode, "Temuan": t_temuan,
                "Risiko": t_risiko, "Rekomendasi": t_rekom, "Prioritas (T/S/R)": t_prio
            })

    st.markdown('<div class="section-title">D. KESIMPULAN DAN PENGESAHAN</div>', unsafe_allow_html=True)
    kesimpulan_umum = st.text_area(
        "Kesimpulan Umum Audit",
        value="Secara keseluruhan, tata kelola dan manajemen TI pada PT Nusantara Retail Digital telah berjalan namun masih memerlukan peningkatan dokumentasi dan standardisasi proses untuk mencapai Target Level 3 (Established)."
    )
    p1, p2, p3 = st.columns(3)
    with p1:
        nama_auditor_ttd = st.text_input("Nama Auditor", value="Widyawati")
        tgl_auditor_ttd = st.text_input("Tanggal (Auditor)", value="23 Oktober 2026")
    with p2:
        nama_auditee_ttd = st.text_input("Nama Auditee", value="Rudi Hartono (CIO)")
        tgl_auditee_ttd = st.text_input("Tanggal (Auditee)", value="23 Oktober 2026")
    with p3:
        nama_mengetahui_ttd = st.text_input("Mengetahui", value="Dr. Ir. Arif Setiawan S.Kom., M.Cs")
        tgl_mengetahui_ttd = st.text_input("Tanggal (Mengetahui)", value="23 Oktober 2026")

    submit = st.form_submit_button("📊 HITUNG & TAMPILKAN LAPORAN HASIL AUDIT", type="primary")

# =========================================================
# 6. OUTPUT LAPORAN HASIL AUDIT
# =========================================================
if submit:
    detail_rows = []
    domain_rows = []

    for domain_code, domain in domains.items():
        values = []
        for code, question, evidence, method in domain["questions"]:
            score = skor_input[code]
            values.append(score)
            detail_rows.append({
                "Domain": domain_code,
                "Kode": code,
                "Pertanyaan Audit": question,
                "Bukti Diperiksa": evidence,
                "Metode": method,
                "Skor (0-5)": score,
                "Level Kapabilitas": level_short[score],
                "Temuan / Catatan Auditor": bukti_input[code] if bukti_input[code] else "-"
            })

        average = sum(values) / len(values)
        target = target_input[domain_code]
        gap = target - average

        domain_rows.append({
            "Domain": f"{domain_code} - {domain['name']}",
            "Jumlah Pertanyaan": len(values),
            "Total Skor": sum(values),
            "Rata-rata": round(average, 2),
            "Target Level": target,
            "Gap (Target - Rata-rata)": round(gap, 2),
            "Rekomendasi Sistem": rekomendasi_otomatis(gap)
        })

    df_detail = pd.DataFrame(detail_rows)
    df_domain = pd.DataFrame(domain_rows)

    rata_keseluruhan = df_domain["Rata-rata"].mean()
    target_keseluruhan = df_domain["Target Level"].mean()
    gap_keseluruhan = target_keseluruhan - rata_keseluruhan

    st.success("✅ Perhitungan Audit COBIT 5 Berhasil Diproses!")

    st.markdown('<div class="section-title">E. REKAPITULASI PENILAIAN DOMAIN COBIT 5</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Pertanyaan", f"{len(df_detail)} Item")
    m2.metric("Rata-rata Keseluruhan", f"{rata_keseluruhan:.2f} / 5.00")
    m3.metric("Rata-rata Target Level", f"{target_keseluruhan:.2f}")
    m4.metric("Gap Keseluruhan", f"{gap_keseluruhan:.2f}")

    # Menambahkan baris rata-rata keseluruhan sesuai tabel di dokumen Tugas 1
    baris_total = pd.DataFrame([{
        "Domain": "Rata-rata Keseluruhan",
        "Jumlah Pertanyaan": df_domain["Jumlah Pertanyaan"].sum(),
        "Total Skor": df_domain["Total Skor"].sum(),
        "Rata-rata": round(rata_keseluruhan, 2),
        "Target Level": round(target_keseluruhan, 2),
        "Gap (Target - Rata-rata)": round(gap_keseluruhan, 2),
        "Rekomendasi Sistem": rekomendasi_otomatis(gap_keseluruhan)
    }])
    df_rekap_tampil = pd.concat([df_domain, baris_total], ignore_index=True)
    st.dataframe(df_rekap_tampil, hide_index=True)

    st.markdown("### Grafik Perbandingan Rata-rata Skor vs Target Level")
    chart_data = df_domain.set_index("Domain")[["Rata-rata", "Target Level"]]
    st.bar_chart(chart_data)

    st.markdown('<div class="section-title">F. TABEL TEMUAN UTAMA DAN REKOMENDASI</div>', unsafe_allow_html=True)
    df_temuan = pd.DataFrame([t for t in temuan_manual if t["Domain / Kode"].strip() != "" or t["Temuan"].strip() != ""])
    if not df_temuan.empty:
        st.dataframe(df_temuan, hide_index=True)
    else:
        st.info("Belum ada temuan manual yang diisi pada bagian C. Rekomendasi otomatis per domain dapat dilihat pada tabel Rekapitulasi di atas.")

    st.markdown('<div class="section-title">G. DETAIL JAWABAN SELURUH PERTANYAAN AUDIT</div>', unsafe_allow_html=True)
    st.dataframe(df_detail, hide_index=True)

    st.markdown('<div class="section-title">H. KESIMPULAN & PENGESAHAN</div>', unsafe_allow_html=True)
    st.write(f"**Kesimpulan Umum:** {kesimpulan_umum}")
    st.table(pd.DataFrame({
        "Peran": ["Auditor", "Auditee", "Mengetahui"],
        "Nama": [nama_auditor_ttd, nama_auditee_ttd, nama_mengetahui_ttd],
        "Tanggal": [tgl_auditor_ttd, tgl_auditee_ttd, tgl_mengetahui_ttd]
    }))

    st.markdown('<div class="section-title">I. UNDUH DATA HASIL AUDIT (CSV)</div>', unsafe_allow_html=True)
    dl1, dl2 = st.columns(2)
    with dl1:
        st.download_button(
            "⬇️ Download Rekapitulasi Domain (CSV)",
            data=df_rekap_tampil.to_csv(index=False).encode("utf-8-sig"),
            file_name="Tugas2_Rekap_Audit_COBIT5.csv",
            mime="text/csv"
        )
    with dl2:
        st.download_button(
            "⬇️ Download Detail 27 Pertanyaan (CSV)",
            data=df_detail.to_csv(index=False).encode("utf-8-sig"),
            file_name="Tugas2_Detail_Audit_COBIT5.csv",
            mime="text/csv"
        )

# =========================================================
# 7. FOOTER
# =========================================================
st.markdown("""
<div class="footer">
<b>Tugas 2 Audit Sistem Informasi — Implementasi COBIT 5 dengan Python Streamlit</b><br>
Widyawati (202453036) 
</div>
""", unsafe_allow_html=True)