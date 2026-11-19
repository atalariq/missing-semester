---
layout: page
title: "Mengapa kami mengajar kelas ini"
lang: id
permalink: /id/about/
---

Selama pendidikan Ilmu Komputer tradisional, kemungkinan besar Anda akan mengambil
banyak kelas yang mengajarkan topik lanjutan dalam CS, segalanya dari
Operating System hingga Programming Language hingga Machine Learning. Tetapi di banyak
institusi ada satu topik esensial yang jarang dibahas dan sebagai gantinya
diserahkan kepada mahasiswa untuk mempelajarinya sendiri: literasi ekosistem komputasi.

Selama bertahun-tahun, kami telah membantu mengajar beberapa kelas di MIT, dan berulang kali
kami melihat bahwa banyak mahasiswa memiliki pengetahuan terbatas tentang tool yang tersedia
bagi mereka. Komputer dibangun untuk mengotomatiskan tugas manual, tetapi mahasiswa sering
melakukan tugas berulang secara manual atau gagal memanfaatkan sepenuhnya tool yang kuat
seperti version control dan text editor. Dalam kasus terbaik, ini menghasilkan
inefisiensi dan waktu terbuang; dalam kasus terburuk, ini menghasilkan masalah seperti
kehilangan data atau ketidakmampuan menyelesaikan tugas tertentu.

Topik ini tidak diajarkan sebagai bagian dari kurikulum universitas: mahasiswa
tidak pernah ditunjukkan cara menggunakan tool ini, atau setidaknya tidak cara menggunakannya
secara efisien, sehingga membuang waktu dan usaha pada tugas yang _seharusnya_ sederhana.
Kurikulum CS standar kehilangan topik kritis tentang ekosistem
komputasi yang dapat membuat hidup mahasiswa jauh lebih mudah.

# Semester yang hilang dari pendidikan CS Anda

Untuk membantu mengatasi ini, kami membuat kelas yang mencakup semua topik yang
kami anggap krusial untuk menjadi ilmuwan komputer dan programmer yang efektif. Kelas
ini bersifat pragmatis dan praktis, serta memberikan pengantar hands-on atas
tool dan teknik yang dapat langsung Anda terapkan dalam berbagai situasi
yang akan Anda temui. Iterasi terbaru kelas ini, dengan materi yang
direvisi secara substansial, dijalankan selama "Independent
Activities Period" MIT pada Januari 2026 — semester satu bulan yang menampilkan kelas
pendek yang dijalankan mahasiswa. Meskipun kuliahnya sendiri hanya tersedia bagi komunitas
MIT, kami akan menyediakan semua materi kuliah beserta rekaman video
kuliah kepada publik.

Jika ini terdengar cocok untuk Anda, berikut beberapa contoh konkret
tentang apa yang akan diajarkan kelas ini:

## Command shell

Cara mengotomatiskan tugas umum dan berulang dengan alias, skrip,
dan build system. Tidak perlu lagi menyalin-tempel perintah dari dokumen
teks. Tidak perlu lagi "jalankan 15 perintah ini satu per satu". Tidak
perlu lagi "Anda lupa menjalankan hal ini" atau "Anda lupa memberikan
argumen ini".

Misalnya, mencari melalui riwayat Anda dengan cepat dapat sangat menghemat waktu. Pada contoh di bawah kami menunjukkan beberapa trik terkait navigasi riwayat shell Anda untuk perintah `convert`.

<video autoplay="autoplay" loop="loop" controls muted playsinline  oncontextmenu="return false;"  preload="auto"  class="demo">
  <source src="/static/media/demos/history.mp4" type="video/mp4">
</video>

## Version control

Cara menggunakan version control dengan _benar_, dan memanfaatkannya untuk
menyelamatkan Anda dari bencana, berkolaborasi dengan orang lain, dan dengan cepat menemukan serta
mengisolasi perubahan yang bermasalah. Tidak perlu lagi `rm -rf; git clone`. Tidak perlu lagi
merge conflict (baiklah, setidaknya lebih sedikit). Tidak perlu lagi blok besar
kode yang dikomentari. Tidak perlu lagi pusing mencari apa yang merusak
kode Anda. Tidak perlu lagi "oh tidak, apakah kita menghapus kode yang berfungsi?!". Kami
bahkan akan mengajarkan cara berkontribusi ke proyek orang lain dengan pull
request!

Pada contoh di bawah kami menggunakan `git bisect` untuk menemukan commit mana yang merusak unit test lalu kami memperbaikinya dengan `git revert`.
<video autoplay="autoplay" loop="loop" controls muted playsinline  oncontextmenu="return false;"  preload="auto"  class="demo">
  <source src="/static/media/demos/git.mp4" type="video/mp4">
</video>

## Penyuntingan Teks

Cara mengedit berkas secara efisien dari command-line, baik secara lokal maupun
jarak jauh, dan memanfaatkan fitur editor tingkat lanjut. Tidak perlu lagi
menyalin berkas bolak-balik. Tidak perlu lagi pengeditan berkas yang berulang.

Vim macro adalah salah satu fitur terbaiknya, pada contoh di bawah kami dengan cepat mengonversi tabel html ke format csv menggunakan macro vim bersarang.
<video autoplay="autoplay" loop="loop" controls muted playsinline  oncontextmenu="return false;"  preload="auto"  class="demo">
  <source src="/static/media/demos/vim.mp4" type="video/mp4">
</video>

## Mesin Jarak Jauh

Cara tetap waras saat bekerja dengan mesin jarak jauh menggunakan SSH key dan
terminal multiplexing. Tidak perlu lagi membuka banyak terminal hanya untuk
menjalankan dua perintah sekaligus. Tidak perlu lagi mengetik password setiap kali
terhubung. Tidak perlu lagi kehilangan segalanya hanya karena Internet Anda
terputus atau Anda harus me-reboot laptop.

Pada contoh di bawah kami menggunakan `tmux` untuk menjaga sesi tetap hidup di server jarak jauh dan `mosh` untuk mendukung roaming jaringan dan pemutusan koneksi.

<video autoplay="autoplay" loop="loop" controls muted playsinline  oncontextmenu="return false;"  preload="auto"  class="demo">
  <source src="/static/media/demos/ssh.mp4" type="video/mp4">
</video>

## Menemukan berkas

Cara dengan cepat menemukan berkas yang Anda cari. Tidak
perlu lagi mengklik berkas di proyek Anda sampai Anda menemukan yang
memiliki kode yang Anda inginkan.

Pada contoh di bawah kami dengan cepat mencari berkas dengan `fd` dan potongan kode dengan `rg`. Kami juga dengan cepat melakukan `cd` dan `vim` pada berkas/folder terbaru/sering digunakan menggunakan `fasd`.

<video autoplay="autoplay" loop="loop" controls muted playsinline  oncontextmenu="return false;"  preload="auto"  class="demo">
  <source src="/static/media/demos/find.mp4" type="video/mp4">
</video>

## Data wrangling

Cara dengan cepat dan mudah memodifikasi, melihat, mengurai, memplot, dan menghitung
data serta berkas langsung dari command-line. Tidak perlu lagi menyalin-tempel
dari berkas log. Tidak perlu lagi menghitung statistik atas data secara manual. Tidak
perlu lagi plotting dengan spreadsheet.

## Kualitas kode dan continuous integration

Cara menggunakan autoformatting, linting, testing, dan tool code coverage untuk meningkatkan
kualitas kode. Tidak perlu lagi kode jelek. Tidak perlu lagi regresi. Tidak perlu lagi kode yang berfungsi
di komputer Anda tetapi crash di komputer orang lain.

## Di Luar Kode

Cara menulis dokumentasi yang hebat, berkomunikasi dengan jelas dengan maintainer
open-source, mengirimkan issue yang dapat ditindaklanjuti, dan berkontribusi pull request yang
di-merge. Tidak perlu lagi pengguna kebingungan yang tidak dapat mulai menggunakan perangkat lunak Anda. Tidak
perlu lagi didiamkan maintainer.

# Kesimpulan

Ini, dan lebih banyak lagi, akan dibahas dalam 9 kuliah kelas, masing-masing menyertakan
latihan agar Anda lebih familiar dengan tool tersebut sendiri. Jika Anda tidak dapat
menunggu hingga Januari 2026, Anda juga dapat melihat kuliah dari
[penawaran kursus sebelumnya](/2020/), yang mencakup banyak topik yang
sama.

Kami berharap dapat bertemu Anda di bulan Januari, baik secara virtual maupun langsung!

Happy hacking,<br>
[Anish](https://anish.io/), [Jon](https://thesquareplanet.com/), dan [Jose](https://josejg.com/)
