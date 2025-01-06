import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import folium
from streamlit_folium import folium_static
import time

# Setup page config
st.set_page_config(page_title="Optimasi Rute Ambulans", layout="wide")

# Tambahkan CSS untuk mempercantik tampilan
st.markdown(
    """
    <style>
    body {
        background-color: #f4f7fc;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 38px;
        color: #9efbff;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .title_rs {
        text-align: left;
        font-size: 30px;
        color: #9efbff;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .description {
        text-align: center;
        font-size: 20px;
        color: white;
        margin-bottom: 20px;
    }
    .main-title_menuRS {
        text-align: left;
        font-size: 40px;
        color: blue;
        font-weight: bold;
        margin-bottom: 0px;
    }
    .description_menuRS {
        text-align: left;
        font-size: 20px;
        color: white;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Data Rumah Sakit
rs_data = {
    "Rumah Sakit Bhayangkara": {
        "code": "Rumah Sakit Bhayangkara",
        "file": "Data Set/1 dataset_Rumah Sakit Bhayangkara.csv",
        "desc": "Rumah Sakit Bhayangkara terletak di Jl. Ahmad Yani No.116, Ketintang, Kec. Gayungan, Surabaya, Jawa Timur. Sebagai salah satu rumah sakit utama di wilayah tersebut, fasilitas ini menawarkan berbagai layanan kesehatan, termasuk pemeriksaan umum, bedah, dan layanan darurat 24 jam. Dengan lokasi strategis dan dukungan tenaga medis yang profesional, rumah sakit ini menjadi pilihan utama bagi masyarakat sekitar. Untuk informasi lebih lanjut, Anda dapat menghubungi telepon (031) 8292227.",
        "image": "Tampilan Aplikasi/1 RS bhayangkara.jpg"
    },
    "Rumah Sakit Ramelan": {
        "code": "Rumah Sakit Ramelan",
        "file": "Data Set/2 dataset_Rumah Sakit Ramelan.csv",
        "desc": "Berlokasi di Jl. Gadung No.1, Jagir, Kec. Wonokromo, Surabaya, Rumah Sakit Ramelan adalah salah satu rumah sakit rujukan dengan layanan kesehatan lengkap. Rumah sakit ini dilengkapi dengan teknologi medis terkini, fasilitas perawatan intensif, dan berbagai poliklinik spesialis untuk memenuhi kebutuhan masyarakat. Untuk informasi atau pertanyaan, Anda dapat menghubungi (031) 8438153.",
        "image": "Tampilan Aplikasi/2 RS Ramelan.png"
    },
    "Rumah Sakit Islam": {
        "code": "Rumah Sakit Islam",
        "file": "Data Set/3 dataset_Rumah Sakit Islam.csv",
        "desc": "Rumah Sakit Islam berada di Jl. Achmad Yani No.2-4, Wonokromo, Kec. Wonokromo, Surabaya, Jawa Timur. Rumah sakit ini dikenal dengan pelayanan berbasis syariah yang mencakup layanan kesehatan umum, spesialis, dan rawat inap. Dengan motto pelayanan sepenuh hati, Rumah Sakit Islam memberikan perhatian khusus pada kenyamanan pasien. Telepon yang dapat dihubungi adalah (031) 8284505",
        "image": "Tampilan Aplikasi/3 RS Islam Surabaya.jpg"
    },
    "RSU Bakti Rahayu": {
        "code": "RSU Bakti Rahayu",
        "file": "Data Set/4 dataset_RSU Bakti Rahayu.csv",
        "desc": "RSU Bakti Rahayu, beralamat di Jl. Ketintang Madya I No.16, Ketintang, Kec. Gayungan, Surabaya, adalah rumah sakit yang fokus pada pelayanan kesehatan komprehensif untuk semua kalangan. Rumah sakit ini memiliki layanan gawat darurat, poliklinik spesialis, serta fasilitas diagnostik lengkap. Untuk informasi lebih lanjut, hubungi (031) 8295922.",
        "image": "Tampilan Aplikasi/4 RSU Bhakti Rahayu.jpg"
    },
    "RS Cempaka Putih": {
        "code": "RS Cempaka Putih",
        "file": "Data Set/20 Data RS Cempaka Putih.csv",
        "desc": "Rumah Sakit Cempaka Putih adalah salah satu fasilitas kesehatan di Surabaya yang menawarkan layanan medis berkualitas untuk masyarakat. Dengan fasilitas yang memadai dan tenaga medis profesional, rumah sakit ini menjadi pilihan masyarakat untuk memenuhi kebutuhan kesehatan dengan layanan yang ramah dan efisien.",
        "image": "Tampilan Aplikasi/10 RS Cempaka Putih.jpeg"
    },
    "RS Wiyung Sejahtera":{
        "code": "RS Wiyung Sejahtera",
        "file": "Data Set/5 dataset_RS Wiyung Sejahtera.csv",
        "desc": "RS Wiyung Sejahtera berlokasi di Jl. Karangan Pdam No.1-3, Babatan, Kec. Wiyung, Surabaya. Rumah sakit ini menyediakan layanan kesehatan berkualitas dengan fasilitas lengkap, termasuk rawat inap, rawat jalan, dan pelayanan gawat darurat 24 jam. Rumah sakit ini dikenal dengan staf medisnya yang ramah dan berpengalaman. Hubungi (031) 7532653 untuk informasi lebih lanjut.",
        "image": "Tampilan Aplikasi/5 RS Wiyung Sejahtera.png"
    },
    "RSUD Soetomo":{
        "code": "RSUD Soetomo",
        "file": "Data Set/6 dataset RSUD Soetomo.csv",
        "desc": "RSUD Dr. Soetomo adalah rumah sakit rujukan nasional yang terletak di Jl. Prof. DR. Moestopo No.6-8, Airlangga, Surabaya. Sebagai rumah sakit pendidikan, fasilitas ini menawarkan layanan kesehatan super spesialistik dan dilengkapi teknologi medis terkini. Dengan kapasitas besar dan dokter ahli di berbagai bidang, RSUD Dr. Soetomo melayani pasien dari seluruh Indonesia.",
        "image": "Tampilan Aplikasi/6 RSUD Soetomo.jpeg"
    },
    "RS RSIA Pura Raharja":{
        "code": "RS RSIA Pura Raharja",
        "file": "Data Set/7 dataset_RS RSIA Pura Raharja.csv",
        "desc": "Rumah Sakit Ibu dan Anak (RSIA) Pura Raharja menawarkan layanan kesehatan ibu dan anak yang komprehensif. Terletak di Jl. Pucang Adi No.12-14, rumah sakit ini memiliki fasilitas unggulan untuk perawatan kehamilan, persalinan, dan kesehatan anak. Dengan suasana nyaman dan dukungan tenaga medis ahli, rumah sakit ini menjadi pilihan keluarga.",
        "image": "Tampilan Aplikasi/7 RS RSIA Pura Raharja.jpg"
    },
    "RS PHC Surabaya":{
        "code": "RS PHC Surabaya",
        "file": "Data Set/8 dataset_RS PHC Surabaya.csv",
        "desc": "Rumah Sakit PHC Surabaya berada di Jl. Prapat Kurung Selatan No.1. Rumah sakit ini dikenal dengan layanan kesehatan industri, selain juga melayani kebutuhan kesehatan umum. Dengan lokasi strategis di dekat pelabuhan, rumah sakit ini menjadi andalan para pekerja di sektor maritim dan industri.",
        "image": "Tampilan Aplikasi/8 RS PHC Surabaya.jpg"
    },
    "Mitra Keluarga Kenjeran":{
        "code": "Mitra Keluarga Kenjeran",
        "file": "Data Set/9 dataset_RS Mitra Keluarga Kenjeran.csv",
        "desc": "Rumah Sakit Mitra Keluarga Kenjeran menyediakan berbagai layanan kesehatan untuk masyarakat Surabaya Timur. Rumah sakit ini memiliki fasilitas modern untuk perawatan rawat inap, rawat jalan, dan pemeriksaan kesehatan preventif. Berlokasi di Jl. Kenjeran No.506, rumah sakit ini mengedepankan pelayanan ramah dan profesional.",
        "image": "Tampilan Aplikasi/9 Mitra Keluarga Kenjeren.jpg"
    },
    "Rumah Sakit Royal":{
        "code": "Rumah Sakit Royal",
        "file": "Data Set/10 dataset Rumah Sakit Royal.csv",
        "desc": "Rumah Sakit Royal terletak di kawasan strategis Surabaya Timur, berdekatan dengan area industri Rungkut. Rumah sakit ini menawarkan layanan medis lengkap yang meliputi rawat jalan, rawat inap, layanan darurat 24 jam, serta fasilitas diagnostik modern. Dengan tim dokter spesialis yang berpengalaman dan peralatan medis canggih, Rumah Sakit Royal berkomitmen memberikan pelayanan kesehatan terbaik untuk masyarakat. Selain itu, lokasinya yang mudah diakses menjadikannya pilihan utama bagi pasien yang membutuhkan perawatan medis segera.",
        "image": "Tampilan Aplikasi/11 rs royal.jpg"
    },
    "RSGM Nala Husada":{
        "code": "RSGM Nala Husada",
        "file": "Data Set/11 dataset_RSGM Nala Husada.csv",
        "desc": "RSGM Nala Husada adalah rumah sakit yang berfokus pada kesehatan gigi dan mulut, berlokasi di pusat pendidikan dan teknologi Surabaya. Rumah sakit ini dilengkapi dengan fasilitas perawatan gigi terkini, seperti radiografi digital, perawatan ortodonti, hingga bedah mulut. Selain melayani pasien umum, RSGM Nala Husada juga menjadi pusat pelatihan dan pendidikan bagi mahasiswa kedokteran gigi. Pelayanan profesional yang didukung dengan standar internasional menjadikan RSGM Nala Husada tempat yang ideal untuk pengobatan dan pencegahan masalah kesehatan gigi dan mulut.",
        "image": "Tampilan Aplikasi/12 rsgm nala husada.jpg"
    },
    "Rumah Sakit Manyar":{
        "code": "Rumah Sakit Manyar",
        "file": "Data Set/12 dataset_ Rumah Sakit Manyar.csv",
        "desc": "Rumah Sakit Manyar merupakan fasilitas kesehatan yang melayani masyarakat Surabaya Timur, khususnya di kawasan Mulyorejo. Dengan layanan seperti poliklinik spesialis, instalasi gawat darurat, dan laboratorium diagnostik, rumah sakit ini menawarkan solusi medis yang terjangkau dan berkualitas. Rumah Sakit Manyar juga dikenal dengan program promosi kesehatannya yang sering melibatkan masyarakat sekitar, seperti pemeriksaan kesehatan gratis dan seminar kesehatan.",
        "image": "Tampilan Aplikasi/13 manyar.jpeg"
    },
    "Rumah Sakit UBAYA":{
        "code": "Rumah Sakit UBAYA",
        "file": "Data Set/13 dataset_Rumah Sakit UBAYA.csv",
        "desc": "Sebagai bagian dari Universitas Surabaya (UBAYA), Rumah Sakit UBAYA menggabungkan pendidikan, penelitian, dan pelayanan kesehatan. Rumah sakit ini dilengkapi dengan berbagai fasilitas unggulan, seperti pusat rehabilitasi, ruang operasi modern, dan laboratorium diagnostik canggih. Selain melayani kebutuhan medis umum, RS UBAYA juga aktif dalam program kesehatan masyarakat dan menjadi tempat praktik mahasiswa kedokteran UBAYA. Dengan pendekatan berbasis riset, rumah sakit ini terus berinovasi dalam memberikan layanan yang efektif dan efisien.",
        "image": "Tampilan Aplikasi/14 rs ubaya.jpg"
    },
    "Premier Hospital Suarabaya": {
        "code": "Premier Hospital Suarabaya",
        "file": "Data Set/14 dataset_Premier Hospital Surabaya.csv",
        "desc": "Premier Hospital Surabaya adalah rumah sakit dengan layanan kesehatan premium yang melayani pasien lokal dan internasional. Dikenal dengan lingkungan yang bersih dan nyaman, rumah sakit ini menyediakan fasilitas seperti suite eksklusif untuk pasien VIP, pusat diagnostik lengkap, serta layanan kesehatan holistik. Premier Hospital juga memiliki tim medis multidisiplin yang selalu siap memberikan perawatan individual sesuai kebutuhan pasien.",
        "image": "Tampilan Aplikasi/15 premier hospital.png"
    },
    "RSI Darus Syifa":{
        "code": "RSI Darus Syifa",
        "file": "Data Set/15 dataset_RS DARUS SYIFA.csv",
        "desc": "RSI Darus Syifa adalah rumah sakit berbasis syariah yang mengintegrasikan pelayanan kesehatan modern dengan nilai-nilai Islam. Rumah sakit ini memiliki fasilitas yang mencakup layanan maternitas, kesehatan anak, dan perawatan penyakit kronis. Selain itu, RSI Darus Syifa juga mengadakan kegiatan sosial seperti pengobatan gratis dan edukasi kesehatan berbasis komunitas. Dengan suasana yang nyaman dan layanan penuh kasih, rumah sakit ini menjadi pilihan bagi mereka yang mencari pengobatan sesuai syariat Islam.",
        "image": "Tampilan Aplikasi/16 RSI Darus Syifa.png"
    },
    "RS Bhakti Dharma Husada":{
        "code": "RS Bhakti Dharma Husada",
        "file": "Data Set/16 dataset_RS BDH.csv",
        "desc": "Terletak di kawasan Benowo, RS Bhakti Dharma Husada melayani kebutuhan kesehatan masyarakat dengan fasilitas yang lengkap dan modern. Rumah sakit ini menyediakan layanan unggulan seperti poliklinik spesialis, ICU, dan fasilitas rawat inap yang nyaman. Sebagai bagian dari komunitas, RS BDH sering terlibat dalam program kesehatan masyarakat, seperti penyuluhan kesehatan dan pemeriksaan gratis.",
        "image": "Tampilan Aplikasi/17 RS BDH.jpg"
    },
    "Rumah Sakit Bunda":{
        "code": "Rumah Sakit Bunda",
        "file": "Data Set/17 dataset RS BUNDA.csv",
        "desc": "Rumah Sakit Bunda adalah fasilitas kesehatan yang terkenal dengan layanan kesehatan ibu dan anak. Dengan fasilitas seperti ruang bersalin modern, perawatan neonatal intensif (NICU), dan layanan konsultasi kesehatan keluarga, RS Bunda menjadi pilihan utama bagi keluarga di kawasan Kandangan. Rumah sakit ini juga menawarkan layanan imunisasi dan program edukasi kesehatan untuk mendukung kesejahteraan ibu dan anak.",
        "image": "Tampilan Aplikasi/18 RS BUNDA.jpg"
    },
    "RS Mitra Keluarga Darmo": {
        "code": "RS Mitra Keluarga Darmo",
        "file": "Data Set/18 dataset RS MKD.csv",
        "desc": "RS Mitra Keluarga Darmo dikenal dengan pelayanannya yang ramah, efisien, dan berkualitas. Berlokasi di kawasan Darmo Satelit, rumah sakit ini menawarkan berbagai layanan, termasuk pusat radiologi, farmasi 24 jam, dan unit rawat inap dengan fasilitas hotel. RS Mitra Keluarga Darmo juga memiliki program pencegahan kesehatan, seperti pemeriksaan kesehatan berkala dan konsultasi gizi.",
        "image": "Tampilan Aplikasi/19 RS MKD.jpg"
    },
    "RS Muji Rahayu": {
        "code": "RS Muji Rahayu",
        "file": "Data Set/19 dataset RS MUJI RAHAYU.csv",
        "desc": "RS Muji Rahayu berkomitmen memberikan pelayanan kesehatan yang terjangkau bagi masyarakat Surabaya Barat. Rumah sakit ini menawarkan layanan seperti rawat jalan, unit gawat darurat 24 jam, dan poliklinik spesialis. Dilengkapi dengan laboratorium diagnostik dan apotek onsite, RS Muji Rahayu memastikan pasien mendapatkan perawatan yang cepat dan efektif.",
        "image": "Tampilan Aplikasi/20 RS MUJI RAHAYU.jpg"
    }
}
# Node positions (menggunakan definisi yang ada di kode kedua)
node_positions = {
    "Rumah Sakit Bhayangkara": {
        "Klinik Unesa": (0, 3.6),
        "A1": (0.1, 4),
        "A2": (1.3, 3.8),
        "A3": (0.5, 1.5),
        "A4": (1.5, 1.38),
        "A5": (1.63, 1.87),
        "A6": (1.45, 0),
        "A7": (1.38, 0),
        "B1": (0.2, 1.48),
        "B2": (-0.5, -0.5),
        "B3": (1.3, -0.7),
        "Rumah Sakit Bhayangkara": (1.5, 1)
    },
    "Rumah Sakit Ramelan": {
        "Klinik Unesa": (2, 0),      
        "A1": (2.3, 0.8),                
        "A2": (5.2, 2),              
        "A3": (6.5, 1.7),             
        "A4": (7.4, 2.8),                
        "A5": (9.67, 5.8),               
        "A6": (9.2, 6),             
        "A7": (8.6, 2.7),              
        "B1": (5, 0.4),              
        "B2": (7.4, 0),              
        "B3": (7.87, 2),               
        "B4": (10.45, 6.9),              
        "B5": (9.4, 7),               
        "Rumah Sakit Ramelan": (11, 1.32)
    },
    "Rumah Sakit Islam": {
        "Klinik Unesa": (3, 0),     
        "A1": (3.5, 0.5),             
        "A2": (7, 0.5),          
        "A3": (7.5, 1),  
        "A4": (8.7, 0.95),           
        "B1": (9.4, 0.35),            
        "B2": (9.8, 1),       
        "Rumah Sakit Islam": (9.7, 1.3)          
    },
    "RSU Bakti Rahayu": {
        "Klinik Unesa": (12,12),
        "A1": (12.2,13),
        "A2": (8,14),
        "A3": (7.2,11),
        "A4": (6.2,11.2),
        "B1": (11.4,10.1),
        "B2": (9.4,10.8),
        "B3": (11.2,8.5),
        "B4": (9,9),
        "B5": (9.6,8),
        "B6": (9.8,8.8),
        "B7": (11,7),
        "B8": (9.5,7.3),
        "B9": (9.3,5.7),
        "B10": (9.3,5.3),
        "B11": (6,6),
        "B12": (6.1,6.4),
        "B13": (7.3,6.1),
        "B14": (7.6,7.5),
        "B15": (6.4,7.7),
        "B16": (6.9,9.5),
        "B18": (6.1,9.6),
        "RSU Bakti Rahayu": (6.2,10.5)
    },
    "RS Wiyung Sejahtera":{
        "Klinik Unesa": (10.2,7),
        "A1": (10.4,7.8),
        "F1": (8,8.2),
        "F2": (7,8.5),
        "F6": (5.2,7.7),
        "V1": (10,6),
        "V2": (9.8,5),
        "V3": (9,5.2),
        "V5": (8.9,2.2),
        "V6": (7.2,2.4),
        "V9": (5.6,2.6),
        "V10": (4.8,2.8),
        "Fv1": (5.2,9),
        "Fv2": (4,8.5),
        "Fv3": (3.5,7.5),
        "Fv6": (1,7.8),
        "RS Wiyung Sejahtera": (1.3,8)
    },
    "RS Cempaka Putih": {
        "Klinik Unesa": (190, 88),
        "A1": (201, 119),
        "A2": (86, 168),
        "A3": (48, 185),
        "A4": (-79, 146),
        "A5": (-114, -14),
        "A6": (-126, -62),
        "A7": (-155, -67),
        "RS Cempaka Putih": (-210, -181),
        "B1": (166, 47),
        "B2": (150, 6),
        "B3": (117, 17),
        "B4": (77, -80),
        "B5": (5, -53),
        "B6": (-10, -152),
        "B7": (-108, -126),
        "C1": (-83, -30)
    },
    "RSUD Soetomo": {
        "Klinik Unesa": (0,0),
        "A1": (0.3,0.5),
        "A6": (1.5,0.5),
        "A9": (1.6,0.8),
        "A7": (1.7,1+0.4),
        "A10": (2+0.3,0.9+0.4),
        "A11": (2.5+0.3,2.2),
        "B1": (3+0.3,2.1+0.4),
        "C1": (6.8,1.7+0.4),
        "C2": (6.8,3+0.4),
        "C3": (5.5,3+0.4),
        "B2": (3.4+0.3,4+0.4),
        "B3": (4.6,4.3),
        "B4": (4.6,4),
        "BC1": (5.6,3.7+0.4),
        "A12": (3+0.3,4.8+0.4),
        "A13": (2.8+0.3,6.5),
        "A14": (3.4+0.3,6.3),
        "A15": (3.7,6.8),
        "A16": (5.7,6),
        "RSUD Soetomo": (5.7,5.5)
    },
    "RS RSIA Pura Raharja": {
        "Klinik Unesa": (-1,0),
        "A1": (-0.8,0.5),
        "A2": (0.1,0.7),
        "A3": (0.8,0.6),
        "A4": (0.2,1.7),
        "A5": (1,1.6),
        "A6": (0.9,1),
        "A7": (1.5,1.5),
        "A8": (2.5,2),
        "B1": (2.4,3),
        "B2": (2.7,4),
        "B3": (2.5,5),
        "C1": (3.6,3),
        "BC1": (3.6,4.8),
        "BC2": (3.7,5.4),
        "BC3": (7,4.5),
        "BC4": (3.6,7),
        "BC5": (4.3,6.8),
        "BC6": (4.3,6.4),
        "BC7": (5,6.4),
        "BC8": (7,7.2),
        "BC9": (5,7.2),
        "RS RSIA Pura Raharja": (5.7,7.2)
    },
    "Mitra Keluarga Kenjeran":{
        "Klinik Unesa": (0,0),
        "A1": (0.1,0.5),
        "A6": (1,0.5),
        "A9": (1.1,1),
        "A7": (1.2,1.7),
        "A10": (1.7,1.5),
        "A11": (2.5,3),
        "C3": (6,2),
        "B1": (2.7,4),
        "B2": (2.7,5),
        "B3": (2.9,5.4),
        "B4": (3.5,5.3),
        "B5": (3.5,5),
        "C1": (4.2,3.8),
        "C2": (4.3,4.9),
        "C4": (6,4.8),
        "C5": (6.1,7),
        "C6": (7,7),
        "Mitra Keluarga Kenjeran": (6.7,6.7)
    },
    "RS PHC Surabaya": {
        "Klinik Unesa": (0,-3),
        "A1": (0.1,-2),
        "A2": (1.4,-2),
        "A3": (1.4,-1),
        "A4": (2.4,-2.2),
        "A10": (1.9,0),
        "Z11": (2.2,1),
        "A11": (2.6,2.5),
        "A12": (2.9,4.3),
        "X1": (4,7),
        "X2": (3.2,8.3),
        "X3": (4.4,8.2),
        "X4": (3.8,11),
        "X7": (3.5,12),
        "X8": (3.1,15),
        "Y1": (-1,7),
        "Y2": (0,8.7),
        "Y3": (0.7,10),
        "Y4": (-2,11),
        "Y5": (-2,11.5),
        "Y6": (0.7,11.3),
        "Y10": (0.5,12.5),
        "Y11": (-1,12.5),
        "YX1": (1,15),
        "RS PHC Surabaya": (1.2,20)
    },
    "Rumah Sakit Royal": {
        "Klinik Unesa": (0, 2),
        "A1": (0.2, 2.5),
        "A2": (0.8, 2.5),
        "A3": (1, 3),
        "A4": (1.2, 2.8),
        "A5": (3.2, 5),
        "A6": (2.8, 5.2),
        "A7": (1.8, 0.8),
        "A8": (1.36, -1.5),
        "B1": (1.2, 2.4),
        "B2": (0.3, 0.6),
        "B3": (1.4, 0.2),
        "Rumah Sakit Royal": (9, -2.5)
    },
    "RSGM Nala Husada": {
        "Klinik Unesa": (-0.2, 0),
        "A1": (0.1, 0.5),
        "A2": (0.6, 0.5),
        "A3": (0.63, 0.8),
        "A4": (0.88, 0.8),
        "A5": (1.2, 2),
        "A6": (8.9, 0.7),
        "A7": (8.8, 4.3),
        "A8": (11.1, 4.34),
        "B1": (2, 4),
        "B2": (5.7, 3.5),
        "B3": (5.9, 4.35),
        "RSGM Nala Husada": (11, 4)
    },
    "Rumah Sakit Manyar": {
        "Klinik Unesa": (-0.2, 0),
        "A1": (0.1, 0.5),
        "A2": (0.6, 0.5),
        "A3": (0.63, 0.8),
        "A4": (0.88, 0.8),
        "A5": (1.6, 2),
        "A6": (2.8, 4),
        "A7": (7, 3.5),
        "A8": (7.15, 5),
        "B1": (7.1, 1.2),
        "Rumah Sakit Manyar": (7.2, 4.5)
    },
    "Rumah Sakit UBAYA": {
        "Klinik Unesa": (0.8, 0),
        "A1": (1.1, 0.5),
        "A2": (1.6, 0.5),
        "A3": (1.63, 0.8),
        "A4": (1.88, 0.8),
        "A5": (2.8, 3),
        "A6": (8.35, 1.15),
        "A7": (8.3, 1.05),
        "A8": (8.2, 0.95),
        "A9": (8.15, 1),
        "B1": (1.7, 0.5),
        "B2": (1.3, -0.5),
        "B3": (2, -0.8),
        "B4": (2.05, -0.6),
        "B5": (2.15, -0.4),
        "B6": (2.5, 0.85),
        "B7": (1.8, -2),
        "B8": (5, -2.1),
        "B9": (4.6, -2.5),
        "B10": (4.8, -3),
        "B11": (5.05, -2.8),
        "B12": (7.5, -2.85),
        "Rumah Sakit UBAYA": (8, 0.2)
    },
    "Premier Hospital Suarabaya": {
        "Klinik Unesa": (0.8, 0),
        "A1": (1.1, 0.5),
        "A2": (1.6, 0.5),
        "A3": (1.63, 0.8),
        "A4": (1.88, 0.8),
        "A5": (3.4, 2.8),
        "A6": (8.5, 1.5),
        "A7": (9.5, 1.23),
        "A8": (9.48, 1.7),
        "A9": (8.67, 1.8),
        "B1": (4.3, 3.8),
        "B2": (4.5, 3.82),
        "B3": (4.7, 3.9),
        "B4": (7.84, 3),
        "B5": (7.8, 1.85),
        "B6": (8.48, 1.7),
        "B7": (8.49, 2.4),
        "Premier Hospital Suarabaya":(8.8,2)
    },
    "RSI Darus Syifa": {
        "Klinik Unesa": (830, -580),
        "A1": (810, -570),
        "A2": (780, -560),
        "A3": (750, -580),
        "A4": (730, -560),
        "A5": (710, -590),
        "A6": (700, -200),
        "A7": (700, -100),
        "A8": (400, -90),
        "A9": (380, -40),
        "A10": (250, -30),
        "A11": (120, -170),
        "A12": (100, -160),
        "A13": (90, -200),
        "RSI Darus Syifa": (110, -220),
        "B1": (650, -270),
    },
    "RS Bhakti Dharma Husada": {
        "Klinik Unesa": (201, -746),
        "A1": (206, -730),
        "A2": (173, -717),
        "A3": (142, -725),
        "A4": (139, -713),
        "A5": (91, -731),
        "A6": (85, -747),
        "A7": (-126, -723),
        "A8": (-120, -662),
        "A9": (-259, -650),
        "A10": (-276, -640),
        "A11": (-301, -519),
        "A12": (-330, -519),
        "A13": (-340, -510),
        "A14": (-327, -469),
        "A15": (-366, -436),
        "RS Bhakti Dharma Husada": (-359, -403),
        "B1": (80, -434),
        "B2": (68, -468),
        "B3": (-351, -349)
    },
    "Rumah Sakit Bunda": {
        "Klinik Unesa": (13.75, -136.75),
        "A1": (17, -129),
        "A2": (35, -129.25),
        "A3": (43.75, -114.75), 
        "A4": (55.75, -116.25),
        "A5": (68.75, -95.75),
        "A6": (81.25, -43.25),
        "A7": (16.75, 18.75),
        "A8": (-10.25, 25.75),
        "Rumah Sakit Bunda": (-92.75, 45.75),
        "B1": (-7.25, -110.75),
        "B2": (-20.75, -112.75),
        "B3": (-22.75, -105.25),
        "B4": (-28.25, -104.25),
        "B5": (-39.25, -81.75),
        "B6": (-12.25, -40.5),
        "B7": (-20.25, -36.25),
        "B8": (-5.75, -15.25),
        "B9": (-18.75, -4.75),
        "B10": (-26.25, 6.75),
        "B11": (-19.25, 18.25)
    },
    "RS Mitra Keluarga Darmo": {
        "Klinik Unesa": (243, -373),
        "A1": (256, -345),
        "A2": (191, -320),
        "A3": (135, -334),
        "A4": (126, -318),
        "A5": (107, -323),
        "A6": (38, -350),
        "A7": (-19, -325),
        "A8": (-106, -158),
        "A9": (10, -109),
        "A10": (50, 84),
        "A11": (-103, 109),
        "A12": (-185, 183),
        "A13": (-183, 213),
        "RS Mitra Keluarga Darmo": (-220, 215),
        "B1": (6, -299),
        "B2": (12, -234),
        "B3": (26, -235),
        "B4": (31, -111)
    },
    "RS Muji Rahayu": {
        "Klinik Unesa": (27.5, -297.5),
        "A1": (34, -282),
        "A2": (79.5, -282.5),
        "A3": (87.5, -253.5),
        "A4": (111.5, -256.5),
        "A5": (137.5, -215.5),
        "A6": (162.5, -110.5),
        "A7": (33.5, 13.5),
        "A8": (-20.5, 27.5),
        "A9": (-170, 65),
        "RS Muji Rahayu": (-149, 63),
        "B1": (-14.5, -245.5),
        "B2": (-41.5, -249.5),
        "B3": (-45.5, -234.5),
        "B4": (-56.5, -232.5),
        "B5": (-78.5, -187.5),
        "B6": (-24.5, -105),
        "B7": (-40.5, -96.5),
        "B8": (-11.5, -54.5),
        "B9": (-37.5, -33.5),
        "B10": (-52.5, -10.5),
        "B11": (-38.5, 12.5)
    }
}

def load_graph_from_file(file_path):
    try:
        df = pd.read_csv(file_path)
        graph = {}

        all_nodes = pd.concat([df['Node Awal'], df['Node Tujuan']]).unique()
        for node in all_nodes:
            graph[node] = {}

        for _, row in df.iterrows():
            source, target, jarak = row['Node Awal'], row['Node Tujuan'], float(row['Jarak']) * 10
            graph[source][target] = jarak
            graph[target][source] = jarak

        return graph
    except Exception as e:
        st.error(f"Error loading graph: {str(e)}")
        return None


def dijkstra(graph, start, target):
    distances = {node: float('inf') for node in graph}
    previous_nodes = {node: None for node in graph}
    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])
        if distances[current_node] == float('inf'):
            break

        for neighbor, jarak in graph[current_node].items():
            distance = distances[current_node] + jarak
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node

        unvisited.remove(current_node)

    return distances, previous_nodes

def shortest_path(previous_nodes, start, target):
    path = []
    current_node = target

    while current_node:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]
        if current_node == start:
            path.insert(0, start)
            break

    return path

def draw_graph(graph, path, hospital_name):
    # Create figure
    plt.figure(figsize=(15, 10))
    
    # Get node positions for the selected hospital
    pos = node_positions[hospital_name]
    
    # Draw edges first (so they appear behind nodes)
    for source, targets in graph.items():
        for target, jarak in targets.items():
            # Get positions for source and target nodes
            source_pos = pos[source]
            target_pos = pos[target]
            
            # Determine if this edge is part of the shortest path
            is_path_edge = False
            if path:
                if any((source == p1 and target == p2) or (target == p1 and source == p2) 
                       for p1, p2 in zip(path[:-1], path[1:])):
                    is_path_edge = True
            
            # Draw the edge
            color = 'red' if is_path_edge else 'gray'
            width = 3 if is_path_edge else 1
            plt.plot([source_pos[0], target_pos[0]], 
                    [source_pos[1], target_pos[1]], 
                    color=color, 
                    linewidth=width,
                    zorder=1)
            
            # Add edge jarak label
            mid_x = (source_pos[0] + target_pos[0]) / 2
            mid_y = (source_pos[1] + target_pos[1]) / 2
            plt.text(mid_x, mid_y, f"{int(graph[source][target])}m",
                    fontsize=6, 
                    horizontalalignment='center',
                    verticalalignment='center',
                    bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    # Draw nodes
    for node, (x, y) in pos.items():
        # Determine node color
        if node == 'Klinik Unesa':
            color = 'green'
        elif node == rs_data[hospital_name]["code"]:
            color = 'red'
        else:
            color = 'lightblue'
        
        # Draw the node
        circle = plt.Circle((x, y), 0.2, 
                          color=color, 
                          alpha=0.6, 
                          zorder=2)
        plt.gca().add_patch(circle)
        
        # Add node label
        plt.text(x, y, node,
                fontsize=8,
                horizontalalignment='center',
                verticalalignment='center',
                zorder=3)
    
    # Set plot limits with some padding
    all_x = [x for x, y in pos.values()]
    all_y = [y for x, y in pos.values()]
    plt.xlim(min(all_x) - 1, max(all_x) + 1)
    plt.ylim(min(all_y) - 1, max(all_y) + 1)
    
    # Set title and remove axes
    plt.title(f"Peta Rute ke {hospital_name}", pad=20, size=16)
    plt.gca().set_aspect('equal')
    plt.axis('off')
    
    return plt

def format_distance(meters):
    km = meters / 1000
    return f"{meters:.1f} meter ({km:.2f} km)"

# Halaman Utama
def halaman_utama():
    image = Image.open("Tampilan Aplikasi/ICON Tampilan Awal.png")
    st.image(image, use_container_width=True)

    st.markdown('<h1 class="main-title">Selamat Datang di Aplikasi Navigasi Darurat</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="description">Saat keadaan darurat kesehatan terjadi, '
        'waktu menjadi faktor yang sangat penting dalam proses penjemputan pasien oleh ambulans menuju rumah sakit. Lalu lintas yang padat dan jarak tempuh yang tidak '
        'optimal dapat memperlambat respons, yang dapat berdampak pada keselamatan pasien. Menggunakan pendekatan berbasis algoritma Dijkstra, sistem penjemputan pasien ini bertujuan untuk '
        'memastikan ambulans mengambil rute tercepat dari titik Klinik Unesa lokasi pasien menuju rumah sakit terdekat. Sistem ini mengambil jarak terpendek, mempercepat waktu respon untuk penjemputan darurat.</p>',
        unsafe_allow_html=True,
    )
    if st.button("Mulai", use_container_width=True):
        st.session_state["page"] = "menu_rs"

# Menu Pilihan Rumah Sakit
def menu_rs():
    st.markdown('<h2 class="title_menuRS">Pilih Rumah Sakit Tujuan</h2>', unsafe_allow_html=True)
    st.markdown('<p class="description_menuRS">Silakan pilih tujuan rumah sakit di bawah ini:</p>', unsafe_allow_html=True)

    for title, data in rs_data.items():
        col1, col2 = st.columns([1, 2])

        with col1:
            try:
                image = Image.open(data["image"])
                st.image(image, use_container_width=True, caption=title)
            except FileNotFoundError:
                st.error("Gambar tidak ditemukan")

        with col2:
            st.markdown(f'<h2 class="title_rs">{title}</h2>', unsafe_allow_html=True)

            st.markdown(data["desc"])
            if st.button(f"Pilih {title}", key=title):
                st.session_state["selected_rs"] = title
                st.session_state["page"] = "halaman_rs"

    if st.button("Kembali"):
        st.session_state["page"] = "halaman_utama"

# Halaman Hasil Rute
def halaman_rs():
    title = st.session_state["selected_rs"]
    col1, col2 = st.columns([2, 3])

    # Column 1 for displaying hospital info
    with col1:
        st.markdown(f'<h1>{title}</h1>', unsafe_allow_html=True)
        st.markdown('<p><b>Mulai:</b> Klinik Unesa Ketintang</p>', unsafe_allow_html=True)
        st.markdown(f'<p><b>Tujuan Akhir:</b> {title}</p>', unsafe_allow_html=True)
        st.markdown('<hr>', unsafe_allow_html=True)

        graph = load_graph_from_file(rs_data[title]["file"])
        if graph:
            # start_time = time.time() 
            distances, previous_nodes = dijkstra(graph, "Klinik Unesa", rs_data[title]["code"])
            print('distances: ', distances)
            print('previous: ', previous_nodes)
            # end_time = time.time()
            # execution_time = end_time + start_time
            # print(f"Waktu eksekusi algoritma DijkstraCempaka: {execution_time:.50f} detik")
            path = shortest_path(previous_nodes, "Klinik Unesa", rs_data[title]["code"])
            print(path)

            if rs_data[title]["code"] in distances and distances[rs_data[title]["code"]] != float('inf'):
                st.success(f"Rute Terpendek:\n{' → '.join(path)}")
                st.info(f"Total Jarak: {format_distance(distances[rs_data[title]['code']])}")

                # Calculate estimated time (assuming average speed of 40 km/h)
                speed = 40  # km/h
                time_hours = (distances[rs_data[title]["code"]] / 1000) / speed
                time_minutes = time_hours * 60
                st.info(f"Estimasi Waktu: {time_minutes:.1f} menit")

        # Create buttons for navigating
        col1_buttons = st.columns([1, 1])  # creates two columns for buttons
        with col1_buttons[0]:
            if st.button("Kembali ke Menu Rumah Sakit"):
                st.session_state["page"] = "menu_rs"
        with col1_buttons[1]:
            if "view_mode" not in st.session_state:
                st.session_state["view_mode"] = "graph"
            if st.button(
                "Lihat dalam bentuk Graph" if st.session_state["view_mode"] == "route" else "Lihat dalam bentuk Rute"
            ):
                # Toggle view_mode between 'route' and 'graph'
                st.session_state["view_mode"] = "route" if st.session_state["view_mode"] == "graph" else "graph"

    # Column 2 for showing the route or graph
    with col2:
        if st.session_state.get("view_mode") == "route":
            # Membaca data koordinat dari CSV
            csv_file = "Data Set/TITIK KOORDINAT.csv"  # Pastikan path file CSV sesuai
            node_coordinates = read_coordinates_from_csv(csv_file)

            hospital_name = title  # Nama rumah sakit yang dipilih

            # Tentukan path dan hospital_name dari rute
            if title == "Rumah Sakit Bhayangkara":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "Rumah Sakit Bhayangkara"]
            elif title == "Rumah Sakit Ramelan":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "Rumah Sakit Ramelan"]
            elif title == "Rumah Sakit Islam":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "Rumah Sakit Islam"]
            elif title == "RSU Bakti Rahayu":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5","6","7","8","RSU Bakti Rahayu"]
            elif title == "RS Wiyung Sejahtera":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "RS Wiyung Sejahtera"]
            elif title == "RS Cempaka Putih":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "RS Cempaka Putih"]
            elif title == "RSUD Soetomo":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24","RSUD Soetomo"]
            elif title == "RS RSIA Pura Raharja":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24", "25", "26" ,"RS RSIA Pura Raharja"]
            elif title == "RS PHC Surabaya":
                path = ["Klinik Unesa","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "21", "22", "23", "24","25","26","27","28","29","30","31","32","33","34","35","36","37","38", "39", "40", "41", "42","43","44", "45","46","47","48","49","50","51","52","RS PHC Surabaya"]
            elif title == "Mitra Keluarga Kenjeran":
                path = ["Klinik Unesa","1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "12", "13", "14", "15", "16", "17", "19", "21", "22", "23", "24","25","26","27","28","29","30","31","32","33","34","35","36","37","38", "39", "40", "41", "42", "Mitra Keluarga Kenjeran"]
            elif title == "Rumah Sakit Royal":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "Rumah Sakit Royal"]
            elif title == "RSGM Nala Husada":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "RSGM Nala Husada"]
            elif title == "Rumah Sakit Manyar":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "Rumah Sakit Manyar"]
            elif title == "Rumah Sakit UBAYA":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "Rumah Sakit UBAYA"]
            elif title == "Premier Hospital Suarabaya":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Premier Hospital Suarabaya"]
            elif title == "RSI Darus Syifa":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "RS Darus Syifa"]
            elif title == "Rumah Sakit Bunda":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "Rumah Sakit Bunda"]
            elif title == "RS Bhakti Dharma Husada":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "RS Bhakti Dharma Husada"]
            elif title == "RS Mitra Keluarga Darmo":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "RS Mitra Keluarga Darmo"]
            elif title == "RS Muji Rahayu":
                path = ["Klinik Unesa", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "RS Muji Rahayu"]

            map_object = create_map_with_manual_route(path, hospital_name, node_coordinates)
            folium_static(map_object)
        elif st.session_state.get("view_mode") == "graph":
            # If view mode is 'graph', draw the graph
            if graph:
                fig = draw_graph(graph, path, title)
                st.pyplot(fig)
                plt.close()

def read_coordinates_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    node_coordinates = {}

    # Proses setiap baris untuk membuat dictionary berdasarkan rumah sakit dan node
    for _, row in df.iterrows():
        hospital_name = row["hospital_name"]
        node_name = row["node_name"]
        latitude = row["latitude"]
        longitude = row["longitude"]

        if hospital_name not in node_coordinates:
            node_coordinates[hospital_name] = {}

        node_coordinates[hospital_name][node_name] = (latitude, longitude)

    return node_coordinates

def create_map_with_manual_route(path, hospital_name, node_coordinates):
    if hospital_name not in node_coordinates:
        raise ValueError(f"Koordinat untuk {hospital_name} tidak ditemukan.")
    
    if "Klinik Unesa" not in node_coordinates[hospital_name]:
        raise ValueError("Koordinat Klinik Unesa tidak ditemukan.")
    
    start_location = node_coordinates[hospital_name]["Klinik Unesa"]
    m = folium.Map(location=start_location, zoom_start=15)

    if path:
        start_node = path[0]
        folium.Marker(
            location=node_coordinates[hospital_name][start_node],
            popup=f"Mulai: {start_node}",
            icon=folium.Icon(color="green")
        ).add_to(m)

        end_node = path[-1]
        folium.Marker(
            location=node_coordinates[hospital_name][end_node],
            popup=f"Tujuan Akhir: {end_node}",
            icon=folium.Icon(color="red")
        ).add_to(m)

        # Menambahkan PolyLine untuk menggambarkan jalur
        path_coords = [node_coordinates[hospital_name][node] for node in path]
        folium.PolyLine(
            locations=path_coords,
            color="blue",
            weight=5,
            opacity=0.8
        ).add_to(m)
    else:
        folium.Marker(
            location=start_location,
            popup="Tidak ada rute yang ditemukan.",
            icon=folium.Icon(color="gray")
        ).add_to(m)

    return m

# Routing halaman
if "page" not in st.session_state:
    st.session_state["page"] = "halaman_utama"
if st.session_state["page"] == "halaman_utama":
    halaman_utama()
elif st.session_state["page"] == "menu_rs":
    menu_rs()
elif st.session_state["page"] == "halaman_rs":
    halaman_rs()
