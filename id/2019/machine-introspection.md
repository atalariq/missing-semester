---
layout: lecture-id
title: "Machine Introspection"
presenter: Jon
date: 2019-01-24
order: 4
video:
  aspect: 56.25
  id: eNYT2Oq3PF8
special: true
lang: id
permalink: /id/2019/machine-introspection/
---

Kadang, komputer berperilaku tidak semestinya. Dan sangat sering, Anda ingin tahu mengapa.
Mari lihat beberapa tool yang membantu Anda melakukannya!

Tetapi pertama, mari pastikan Anda dapat melakukan introspection. Sering kali,
system introspection mengharuskan Anda memiliki hak istimewa tertentu, seperti
menjadi anggota sebuah grup (seperti `power` untuk shutdown). Pengguna `root`
memiliki hak istimewa tertinggi; mereka dapat melakukan hampir apa pun. Anda dapat menjalankan
perintah sebagai `root` (tetapi hati-hati!) menggunakan `sudo`.

## Apa yang terjadi?

Jika sesuatu salah, tempat pertama untuk memulai adalah melihat apa yang
terjadi di sekitar waktu ketika masalah itu muncul. Untuk ini, kita perlu
melihat log.

Secara tradisional, semua log disimpan di `/var/log`, dan banyak yang masih begitu.
Biasanya ada satu berkas atau folder per program. Gunakan `grep` atau `less` untuk
menemukan jalan Anda di antaranya.

Ada juga log kernel yang dapat Anda lihat menggunakan perintah `dmesg`.
Dulu ini tersedia sebagai berkas teks biasa, tetapi saat ini Anda sering
harus melalui `dmesg` untuk mengaksesnya.

Terakhir, ada "system log", yang semakin menjadi tempat semua
pesan log Anda pergi. Pada _sebagian besar_, meskipun tidak semua, sistem Linux, log itu
dikelola oleh `systemd`, "system daemon", yang mengendalikan semua
layanan yang berjalan di latar belakang (dan banyak sekali hal lain pada titik ini).
Log itu dapat diakses melalui tool `journalctl` yang agak tidak praktis
jika Anda root, atau bagian dari grup `admin` atau `wheel`.

Untuk `journalctl`, Anda sebaiknya menyadari flag berikut secara khusus:

 - `-u UNIT`: hanya tampilkan pesan yang terkait dengan layanan systemd yang diberikan
 - `--full`: jangan potong baris panjang (fitur paling bodoh)
 - `-b`: hanya tampilkan pesan dari boot terakhir (lihat juga `-b -2`)
 - `-n100`: hanya tampilkan 100 entri terakhir

## Apa yang sedang terjadi?

Jika ada sesuatu yang _salah_, atau Anda hanya ingin merasakan apa yang sedang terjadi
di sistem Anda, Anda memiliki sejumlah tool untuk
memeriksa sistem yang sedang berjalan:

Pertama, ada `top`, dan versi yang ditingkatkan `htop`, yang menampilkan berbagai
statistik untuk proses yang sedang berjalan di sistem.
Penggunaan CPU, penggunaan memori, process tree, dsb. Ada banyak shortcut,
tetapi `t` sangat berguna untuk mengaktifkan tampilan tree. Anda juga dapat
melihat process tree dengan `pstree` (+ `-p` untuk menyertakan PID). Jika Anda ingin
mengetahui apa yang dilakukan program tersebut, Anda sering ingin melakukan tail pada berkas
log-nya. `journalctl -f`, `dmesg -w`, dan `tail -f` adalah teman Anda
di sini.

Kadang, Anda ingin mengetahui lebih banyak tentang sumber daya yang digunakan secara keseluruhan
di sistem Anda. [`dool`](https://github.com/scottchiefbaker/dool) sangat baik
untuk itu. Tool ini memberi Anda metrik sumber daya real-time untuk banyak
subsistem berbeda seperti I/O, networking, penggunaan CPU, context
switch, dan sejenisnya. `man dool` adalah tempat untuk memulai.

Jika ruang disk Anda habis, ada dua utilitas utama
yang ingin Anda ketahui: `df` dan `du`. Yang pertama menunjukkan kepada Anda
status semua partisi di sistem Anda (coba dengan `-h`), sedangkan
yang kedua mengukur ukuran semua folder yang Anda berikan, termasuk
isinya (lihat juga `-h` dan `-s`).

Untuk mencari tahu koneksi jaringan apa yang terbuka, `ss` adalah pilihannya.
`ss -t` akan menampilkan semua koneksi TCP yang terbuka. `ss -tl` akan menampilkan semua
port yang mendengarkan (yakni port server) di sistem Anda. `-p` juga akan menyertakan
proses mana yang menggunakan koneksi itu, dan `-n` akan memberi Anda nomor
port mentah.


## Konfigurasi sistem

Ada _banyak_ cara mengonfigurasi sistem Anda, tetapi kita akan membahas
dua yang sangat umum: networking dan layanan. Sebagian besar aplikasi di sistem
Anda memberi tahu cara mengonfigurasinya di manpage-nya, dan biasanya itu
melibatkan pengeditan berkas di `/etc`; direktori konfigurasi
sistem.

Jika Anda ingin mengonfigurasi jaringan Anda, perintah `ip` memungkinkan Anda melakukannya.
Argumennya berbentuk sedikit aneh, tetapi `ip help command`
akan membawa Anda cukup jauh. `ip addr` menunjukkan kepada Anda informasi tentang
antarmuka jaringan Anda dan bagaimana konfigurasinya (alamat IP dan sebagainya),
dan `ip route` menunjukkan kepada Anda bagaimana lalu lintas jaringan dirutekan ke berbagai
host jaringan. Masalah jaringan sering dapat diselesaikan murni melalui
tool `ip`. Ada juga `iw` untuk mengelola antarmuka jaringan nirkabel.
`ping` adalah tool praktis untuk memeriksa seberapa parah kerusakannya. Coba
ping sebuah hostname (google.com), alamat IP eksternal (1.1.1.1), dan
alamat IP internal (192.168.1.1 atau default gw). Anda mungkin juga ingin
mengutak-atik `/etc/resolv.conf` untuk memeriksa pengaturan DNS Anda (bagaimana hostname
diselesaikan menjadi alamat IP).

Untuk mengonfigurasi layanan, saat ini Anda hampir harus berinteraksi dengan `systemd`,
untung atau rugi. Sebagian besar layanan di sistem Anda akan
memiliki berkas layanan systemd yang mendefinisikan sebuah _unit_ systemd. Berkas ini
mendefinisikan perintah apa yang dijalankan ketika layanan itu dimulai, cara menghentikannya,
di mana mencatat log, dsb. Biasanya berkas ini tidak terlalu sulit dibaca, dan
Anda dapat menemukan sebagian besarnya di `/usr/lib/systemd/system/`. Anda juga dapat
mendefinisikan milik Anda sendiri di `/etc/systemd/system` .

Setelah Anda memiliki layanan systemd yang dimaksud, Anda menggunakan perintah `systemctl`
untuk berinteraksi dengannya. `systemctl enable UNIT` akan mengatur layanan agar
mulai saat boot (`disable` menghapusnya lagi), dan `start`, `stop`, dan
`restart` akan melakukan seperti yang Anda harapkan. Jika sesuatu salah, systemd akan
memberi tahu Anda, dan Anda dapat menggunakan `journalctl -u UNIT` untuk melihat
log aplikasi. Anda juga dapat menggunakan `systemctl status` untuk melihat bagaimana semua
layanan sistem Anda berjalan. Jika boot Anda terasa lambat, itu mungkin
disebabkan beberapa layanan yang lambat, dan Anda dapat menggunakan `systemd-analyze` (coba
dengan `blame`) untuk mencari tahu yang mana.
