---
layout: lecture-id
title: "Mesin Jarak Jauh"
presenter: Jose
date: 2019-01-29
order: 4
video:
  aspect: 62.5
  id: X5c2Y8BCowM
lang: id
permalink: /id/2019/remote-machines/
---

Semakin umum bagi programmer untuk menggunakan server jarak jauh dalam pekerjaan sehari-hari mereka. Jika Anda perlu menggunakan server jarak jauh untuk men-deploy perangkat lunak backend atau Anda membutuhkan server dengan kemampuan komputasi lebih tinggi, pada akhirnya Anda akan menggunakan Secure Shell (SSH). Seperti pada sebagian besar tool yang dibahas, SSH sangat dapat dikonfigurasi sehingga layak untuk dipelajari.


## Mengeksekusi perintah

Fitur `ssh` yang sering terlewat adalah kemampuan menjalankan perintah secara langsung.

- `ssh foobar@server ls` akan mengeksekusi ls di folder home foobar
- Ini bekerja dengan pipe, sehingga `ssh foobar@server ls | grep PATTERN` akan melakukan grep secara lokal pada output remote `ls` dan `ls | ssh foobar@server grep PATTERN` akan melakukan grep secara remote pada output lokal `ls`.

## SSH Keys

Autentikasi berbasis key memanfaatkan public-key cryptography untuk membuktikan kepada server bahwa klien memiliki private key rahasia tanpa mengungkapkan key tersebut. Dengan cara ini Anda tidak perlu memasukkan ulang password setiap kali. Meskipun demikian private key (misalnya `~/.ssh/id_rsa`) secara efektif adalah password Anda jadi perlakukan seperti itu.

- Pembuatan key. Untuk menghasilkan pasangan key Anda cukup menjalankan `ssh-keygen -t rsa -b 4096`. Jika Anda tidak memilih passphrase siapa pun yang memperoleh private key Anda akan dapat mengakses server yang berwenang sehingga disarankan memilih passphrase dan menggunakan `ssh-agent` untuk mengelola sesi shell.

Jika Anda pernah mengonfigurasi push ke Github menggunakan SSH key Anda mungkin pernah melakukan langkah-langkah yang diuraikan [di sini](https://help.github.com/articles/connecting-to-github-with-ssh/) dan sudah memiliki pasangan key yang valid. Untuk memeriksa apakah Anda memiliki passphrase dan memvalidasinya Anda dapat menjalankan `ssh-keygen -y -f /path/to/key`.

- Autentikasi berbasis key. `ssh` akan memeriksa `.ssh/authorized_keys` untuk menentukan klien mana yang boleh masuk. Untuk menyalin public key Anda dapat menggunakan

```bash
cat .ssh/id_dsa.pub | ssh foobar@remote 'cat >> ~/.ssh/authorized_keys'
```

Solusi yang lebih sederhana dapat dicapai dengan `ssh-copy-id` bila tersedia.

```bash
ssh-copy-id -i .ssh/id_dsa.pub foobar@remote
```

## Menyalin berkas melalui ssh

Ada banyak cara menyalin berkas melalui ssh

- `ssh+tee`, yang paling sederhana adalah menggunakan eksekusi perintah `ssh` dan input stdin dengan melakukan `cat localfile | ssh remote_server tee serverfile`
- `scp` saat menyalin berkas/direktori dalam jumlah besar, perintah secure copy `scp` lebih praktis karena dapat dengan mudah melakukan rekursi pada path. Sintaksnya adalah `scp path/to/local_file remote_host:path/to/remote_file`
- `rsync` meningkatkan `scp` dengan mendeteksi berkas identik di lokal dan remote serta mencegah penyalinan ulang berkas tersebut. Tool ini juga memberikan kendali lebih terperinci atas symlink, permission dan memiliki fitur tambahan seperti flag `--partial` yang dapat melanjutkan dari penyalinan yang sebelumnya terinterupsi. `rsync` memiliki sintaks yang mirip dengan `scp`.


## Mem-background proses

Secara default ketika koneksi ssh terputus, child process dari shell induk ikut dihentikan. Ada beberapa alternatif

- `nohup` - tool `nohup` secara efektif memungkinkan sebuah proses tetap hidup ketika terminal dihentikan. Meskipun ini kadang dapat dicapai dengan `&` dan `disown`, nohup adalah default yang lebih baik. Detail lebih lanjut dapat ditemukan [di sini](https://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and).

- `tmux`, `screen` - meskipun `nohup` secara efektif mem-background proses, tool itu tidak praktis untuk sesi shell interaktif. Dalam kasus itu menggunakan terminal multiplexer seperti `screen` atau `tmux` adalah pilihan yang praktis karena seseorang dapat dengan mudah melepas dan menghubungkan kembali shell terkait.

Terakhir, jika Anda melakukan disown pada sebuah program dan ingin menghubungkannya kembali ke terminal saat ini, Anda dapat menelaah [reptyr](https://github.com/nelhage/reptyr). `reptyr PID` akan mengambil proses dengan id PID dan menghubungkannya ke terminal Anda saat ini.

## Port Forwarding

Dalam banyak skenario Anda akan menemui perangkat lunak yang bekerja dengan mendengarkan port di mesin. Ketika ini terjadi di mesin lokal Anda, Anda cukup melakukan `localhost:PORT` atau `127.0.0.1:PORT`, tetapi apa yang Anda lakukan dengan server jarak jauh yang port-nya tidak tersedia langsung melalui jaringan/internet?. Ini disebut port forwarding dan hadir
dalam dua rasa: Local Port Forwarding dan Remote Port Forwarding (lihat gambar untuk detail lebih lanjut, kredit gambar dari [posting SO ini](https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot)).


**Local Port Forwarding**
![Local Port Forwarding](https://i.stack.imgur.com/a28N8.png)

**Remote Port Forwarding**
![Remote Port Forwarding](https://i.stack.imgur.com/4iK3b.png)


Skenario paling umum adalah local port forwarding di mana sebuah layanan di mesin remote mendengarkan di sebuah port dan Anda ingin menautkan port di mesin lokal Anda untuk meneruskan ke port remote tersebut. Misalnya jika kita mengeksekusi `jupyter notebook` di server jarak jauh yang mendengarkan port `8888`. Jadi untuk meneruskannya ke port lokal `9999` kita akan melakukan `ssh -L 9999:localhost:8888 foobar@remote_server` lalu bernavigasi ke `localhost:9999` di mesin lokal kita.

## Graphics Forwarding

Kadang melakukan port forwarding tidak cukup karena kita ingin menjalankan program berbasis GUI di server. Anda selalu dapat menggunakan Remote Desktop Software yang mengirim seluruh Desktop Environment (yaitu opsi seperti RealVNC, Teamviewer, &c). Namun untuk satu tool GUI, SSH menyediakan alternatif yang baik: Graphics Forwarding.

Menggunakan flag `-X` memberi tahu SSH untuk meneruskan

 Untuk trusted X11 forwarding flag `-Y` dapat digunakan.

Catatan terakhir adalah agar ini berfungsi `sshd_config` di server harus memiliki opsi berikut

```bash
X11Forwarding yes
X11DisplayOffset 10
```

## Roaming

Masalah umum saat terhubung ke server jarak jauh adalah pemutusan karena mematikan/menidurkan komputer Anda atau mengganti jaringan. Lebih jauh lagi jika seseorang memiliki koneksi dengan lag signifikan, menggunakan ssh bisa menjadi sangat menjengkelkan. [Mosh](https://mosh.org/), mobile shell, meningkatkan ssh, memungkinkan koneksi roaming, konektivitas intermiten dan menyediakan intelligent local echo.

Mosh tersedia di semua distribusi dan package manager umum. Mosh memerlukan ssh server yang berfungsi di server. Anda tidak perlu menjadi superuser untuk memasang mosh tetapi mosh memerlukan port 60000 sampai 60010 terbuka di server (biasanya memang terbuka karena tidak berada di rentang privileged).

Kekurangan `mosh` adalah tool ini tidak mendukung roaming port/graphics forwarding sehingga jika Anda sering menggunakan hal itu `mosh` tidak akan banyak membantu.

## Konfigurasi SSH

### Klien

Kita telah membahas banyak argumen yang dapat kita berikan. Alternatif yang menggoda adalah membuat alias shell seperti `alias my_server="ssh -X -i ~/.ssh/id_rsa -L 9999:localhost:8888 foobar@remote_server"`, namun ada alternatif yang lebih baik, menggunakan `~/.ssh/config`.

```bash
Host vm
    User foobar
    HostName 172.16.174.141
    Port 22
    IdentityFile ~/.ssh/id_rsa
    RemoteForward 9999 localhost:8888

# Configs can also take wildcards
Host *.mit.edu
    User foobaz
```


Keuntungan tambahan menggunakan berkas `~/.ssh/config` dibandingkan alias adalah bahwa program lain seperti `scp`, `rsync`, `mosh`, &c juga dapat membacanya dan mengonversi pengaturannya menjadi flag yang sesuai.


Perhatikan bahwa berkas `~/.ssh/config` dapat dianggap sebagai dotfile, dan secara umum tidak masalah menyertakannya bersama dotfiles Anda lainnya. Namun jika Anda mempublikasikannya, pikirkan informasi yang berpotensi Anda berikan kepada orang asing di internet: alamat server Anda, pengguna yang Anda gunakan, port terbuka, &c. Ini dapat memudahkan beberapa jenis serangan sehingga pertimbangkan dengan matang sebelum membagikan konfigurasi SSH Anda.

Peringatan: Jangan pernah menyertakan RSA key Anda ( `~/.ssh/id_rsa*` ) di repositori publik!

### Sisi server

Konfigurasi sisi server biasanya ditentukan di `/etc/ssh/sshd_config`. Di sini Anda dapat membuat perubahan seperti menonaktifkan autentikasi password, mengubah port ssh, mengaktifkan X11 forwarding, &c. Anda dapat menentukan pengaturan config per pengguna.

## Filesystem Remote

Kadang praktis untuk me-mount folder remote. [sshfs](https://github.com/libfuse/sshfs) dapat me-mount folder di server jarak jauh
secara lokal, lalu Anda dapat menggunakan editor lokal.

## Latihan

1. Agar SSH berfungsi host perlu menjalankan SSH server. Pasang SSH server (seperti OpenSSH) di virtual machine agar Anda dapat mengerjakan sisa latihan. Untuk mencari tahu berapa ip mesinnya jalankan perintah `ip addr` dan cari field inet (abaikan entri `127.0.0.1`, yang bersesuaian dengan antarmuka loopback).

1. Buka `~/.ssh/` dan periksa apakah Anda memiliki pasangan SSH key di sana. Jika tidak, hasilkan dengan `ssh-keygen -t rsa -b 4096`. Disarankan Anda menggunakan password dan menggunakan `ssh-agent` , info lebih lanjut [di sini](https://www.ssh.com/ssh/agent).

1. Gunakan `ssh-copy-id` untuk menyalin key ke virtual machine Anda. Uji bahwa Anda dapat ssh tanpa password. Lalu, edit `sshd_config` Anda di server untuk menonaktifkan autentikasi password dengan mengedit nilai `PasswordAuthentication`. Nonaktifkan login root dengan mengedit nilai `PermitRootLogin`.

1. Edit `sshd_config` di server untuk mengubah port ssh dan periksa bahwa Anda masih dapat ssh. Jika Anda memiliki server yang menghadap publik, port non-default dan login hanya dengan key akan memperlambat sejumlah besar serangan berbahaya.

1. Pasang mosh di server/VM Anda, bangun koneksi lalu putuskan network adapter server/VM tersebut. Dapatkah mosh pulih dengan benar?

1. Penggunaan lain local port forwarding adalah menyalurkan (tunnel) host tertentu ke server. Jika jaringan Anda memfilter beberapa situs web seperti misalnya `reddit.com` Anda dapat menyalurkannya melalui server sebagai berikut:

    - Jalankan `ssh remote_server -L 80:reddit.com:80`
    - Setel `reddit.com` dan `www.reddit.com` ke `127.0.0.1` di `/etc/hosts`
    - Periksa bahwa Anda mengakses situs web itu melalui server
    - Jika tidak jelas gunakan situs web seperti [ipinfo.io](https://ipinfo.io/) yang akan berubah tergantung ip publik host Anda.


1. Background port forwarding dapat dengan mudah dicapai dengan beberapa flag tambahan. Telaah apa fungsi flag `-N` dan `-f` pada `ssh` dan cari tahu apa yang dilakukan perintah seperti ini `ssh -N -f -L 9999:localhost:8888 foobar@remote_server`.


## Referensi

- [SSH Hacks](https://matt.might.net/articles/ssh-hacks/)
- [Secure Secure Shell](https://stribika.github.io/2015/01/04/secure-secure-shell.html)

{% comment %}
Lecture notes will be available by the start of lecture.
{% endcomment %}
