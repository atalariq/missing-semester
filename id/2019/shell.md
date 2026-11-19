---
layout: lecture-id
title: "Shell dan Scripting"
presenter: Jon
date: 2019-01-15
order: 3
video:
  aspect: 56.25
  id: dbDRfmH5uSI
lang: id
permalink: /id/2019/shell/
---

Shell adalah antarmuka tekstual yang efisien ke komputer Anda.

Prompt shell: apa yang menyambut Anda ketika membuka terminal.
Memungkinkan Anda menjalankan program dan perintah; yang umum adalah:

 - `cd` untuk mengubah direktori
 - `ls` untuk mencantumkan berkas dan direktori
 - `mv` dan `cp` untuk memindahkan dan menyalin berkas

Tetapi shell memungkinkan Anda melakukan _jauh_ lebih banyak; Anda dapat memanggil program apa pun di
komputer Anda, dan tool command-line ada untuk melakukan hampir
apa pun yang mungkin ingin Anda lakukan. Dan tool tersebut sering lebih efisien daripada
padanan grafisnya. Kita akan membahas banyak di antaranya di kelas ini.

Shell menyediakan bahasa pemrograman interaktif ("scripting").
Ada banyak shell:

 - Anda mungkin pernah menggunakan `sh` atau `bash`.
 - Juga shell yang sesuai bahasa: `csh`.
 - Atau shell yang "lebih baik": `fish`, `zsh`, `ksh`.

Di kelas ini kita akan memfokuskan pada `sh` dan `bash` yang ada di mana-mana, tetapi silakan
bermain-main dengan yang lain. Saya menyukai `fish`.

Pemrograman shell adalah tool yang *sangat* berguna di perangkat Anda.
Anda dapat menulis program langsung di prompt, atau ke dalam berkas.
`#!/bin/sh` + `chmod +x` untuk membuat shell dapat dieksekusi.

## Bekerja dengan shell

Jalankan sebuah perintah beberapa kali:

```bash
for i in $(seq 1 5); do echo hello; done
```

Ada banyak yang harus diurai:

 - `for x in list; do BODY; done`
   - `;` mengakhiri sebuah perintah -- setara dengan newline
   - pisahkan `list`, tetapkan masing-masing ke `x`, lalu jalankan body
   - pemisahan adalah "whitespace splitting", yang akan kita bahas lagi
   - tidak ada kurung kurawal di shell, sehingga `do` + `done`
 - `$(seq 1 5)`
   - jalankan program `seq` dengan argumen `1` dan `5`
   - ganti seluruh `$()` dengan output program tersebut
   - setara dengan
     ```bash
     for i in 1 2 3 4 5
     ```
 - `echo hello`
   - segala sesuatu dalam skrip shell adalah sebuah perintah
   - dalam kasus ini, jalankan perintah `echo`, yang mencetak argumennya
     dengan argumen `hello`.
   - semua perintah dicari di `$PATH` (dipisahkan titik dua)

Kita memiliki variabel:
```bash
for f in $(ls); do echo $f; done
```

Akan mencetak setiap nama berkas di direktori saat ini.
Anda juga dapat menetapkan variabel menggunakan `=` (tanpa spasi!)

```bash
foo=bar
echo $foo
```

Ada banyak variabel "khusus" juga:

 - `$1` sampai `$9`: argumen skrip
 - `$0` nama skrip itu sendiri
 - `$#` jumlah argumen
 - `$$` process ID shell saat ini

Untuk hanya mencetak direktori

```bash
for f in $(ls); do if test -d $f; then echo dir $f; fi; done
```

Ada lebih banyak yang harus diurai di sini:

 - `if CONDITION; then BODY; fi`
   - `CONDITION` adalah sebuah perintah; jika mengembalikan exit status 0
     (sukses), maka `BODY` dijalankan.
   - Anda juga dapat menyambungkan `else` atau `elif`
   - sekali lagi, tidak ada kurung kurawal, sehingga `then` + `fi`
 - `test` adalah program lain yang menyediakan berbagai pemeriksaan dan
   perbandingan, dan keluar dengan 0 jika benar (`$?`)
   - `man COMMAND` adalah teman Anda: `man test`
   - juga dapat dipanggil dengan `[` + `]`: `[ -d $f ]`
     - telaah `man test` dan `which "["`

Tetapi tunggu! Ini salah! Bagaimana jika ada berkas bernama "My Documents"?

 - `for f in $(ls)` diekspansi menjadi `for f in My Documents`
 - pertama lakukan test pada `My`, lalu pada `Documents`
 - bukan yang kita inginkan!
 - sumber bug terbesar dalam skrip shell

## Argument splitting

Bash memisahkan argumen berdasarkan whitespace; tidak selalu yang Anda inginkan!

 - perlu menggunakan quoting untuk menangani spasi dalam argumen
   `for f in "My Documents"` akan berfungsi dengan benar
 - masalah yang sama di tempat lain -- dapatkah Anda melihat di mana?
   `test -d $f`: jika `$f` memuat whitespace, `test` akan error!
 - `echo` kebetulan aman, karena split + join dengan spasi
   tetapi bagaimana jika nama berkas memuat newline?! berubah menjadi spasi!
 - kutip semua penggunaan variabel yang tidak ingin Anda pisahkan
 - tetapi bagaimana kita memperbaiki skrip kita di atas?
   menurut Anda apa yang dilakukan `for f in "$(ls)"`?

Globbing adalah jawabannya!

 - bash tahu cara mencari berkas menggunakan pola:
   - `*` string karakter apa pun
   - `?` satu karakter apa pun
   - `{a,b,c}` salah satu karakter ini
 - `for f in *`: semua berkas di direktori ini
 - saat melakukan globbing, setiap berkas yang cocok menjadi argumen tersendiri
   - tetap perlu memastikan quoting saat _menggunakan_: `test -d "$f"`
 - dapat membuat pola lanjutan:
   - `for f in a*`: semua berkas yang dimulai dengan `a` di direktori saat ini
   - `for f in foo/*.txt`: semua berkas `.txt` di `foo`
   - `for f in foo/*/p??.txt`
     semua berkas teks tiga huruf yang dimulai dengan p di subdirektori `foo`

Masalah whitespace tidak berhenti di situ:

 - `if [ $foo = "bar" ]; then` -- lihat masalahnya?
 - bagaimana jika `$foo` kosong? argumen `[` adalah `=` dan `bar`...
 - _dapat_ diakali dengan `[ x$foo = "xbar" ]`, tetapi meh
 - sebagai gantinya, gunakan `[[`: comparator bawaan bash yang memiliki parsing khusus
   - juga memungkinkan `&&` alih-alih `-a`, `||` alih-alih `-o`, dsb.

<!-- TODO: arrays? $@. ${array[@]} vs "${array[@]}". -->

## Composability

Shell kuat sebagian karena composability. Dapat merangkai beberapa
program bersama alih-alih memiliki satu program yang melakukan segalanya.

Karakter kuncinya adalah `|` (pipe).

 - `a | b` berarti jalankan `a` dan `b`
   kirim semua output `a` sebagai input ke `b`
   cetak output `b`

Semua program yang Anda jalankan ("proses") memiliki tiga "stream":

 - `STDIN`: ketika program membaca input, input datang dari sini
 - `STDOUT`: ketika program mencetak sesuatu, output pergi ke sini
 - `STDERR`: output ke-2 yang dapat dipilih program untuk digunakan
 - secara default, `STDIN` adalah keyboard Anda, `STDOUT` dan `STDERR` keduanya
   terminal Anda. tetapi Anda dapat mengubahnya!
   - `a | b` menjadikan `STDOUT` dari `a` sebagai `STDIN` dari `b`.
   - juga ada:
     - `a > foo` (`STDOUT` dari `a` pergi ke berkas `foo`)
     - `a 2> foo` (`STDERR` dari `a` pergi ke berkas `foo`)
     - `a < foo` (`STDIN` dari `a` dibaca dari berkas `foo`)
     - petunjuk: `tail -f` akan mencetak berkas saat sedang ditulis
 - mengapa ini berguna? memungkinkan Anda memanipulasi output sebuah program!
   - `ls | grep foo`: semua berkas yang memuat kata `foo`
   - `ps | grep foo`: semua proses yang memuat kata `foo`
   - `journalctl | grep -i intel | tail -n5`:
     lima pesan log sistem terakhir dengan kata intel (tidak peka huruf besar-kecil)
   - `who | sendmail -t me@example.com`
     kirim daftar pengguna yang login ke `me@example.com`
   - membentuk dasar bagi banyak data-wrangling, seperti akan kita bahas nanti

Bash juga menyediakan sejumlah cara lain untuk menyusun program.

Anda dapat mengelompokkan perintah dengan `(a; b) | tac`: jalankan `a`, lalu `b`, dan kirim
semua outputnya ke `tac`, yang mencetak inputnya dalam urutan terbalik.

Salah satu yang kurang dikenal tetapi sangat berguna adalah _process substitution_.
`b <(a)` akan menjalankan `a`, menghasilkan nama berkas sementara untuk stream
output-nya, dan memberikan nama berkas itu ke `b`. Misalnya:

```bash
diff <(journalctl -b -1 | head -n20) <(journalctl -b -2 | head -n20)
```
akan menunjukkan kepada Anda perbedaan antara 20 baris pertama log boot
terakhir dan log boot sebelumnya.

<!-- TODO: exit codes? -->

## Kontrol job dan proses

Bagaimana jika Anda ingin menjalankan hal jangka panjang di latar belakang?

 - sufiks `&` menjalankan program "di latar belakang"
   - program akan mengembalikan prompt Anda segera
   - berguna jika Anda ingin menjalankan dua program sekaligus
     seperti server dan client: `server & client`
   - perhatikan bahwa program yang berjalan tetap menggunakan terminal Anda sebagai `STDOUT`!
     coba: `server > server.log & client`
 - lihat semua proses semacam itu dengan `jobs`
   - perhatikan bahwa tool menampilkan "Running"
 - bawa ke foreground dengan `fg %JOB` (tanpa argumen berarti yang terakhir)
 - jika Anda ingin mem-background program saat ini: `^Z` + `bg` (Di sini `^Z` berarti menekan `Ctrl+Z`)
   - `^Z` menghentikan proses saat ini dan menjadikannya sebuah "job"
   - `bg` menjalankan job terakhir di latar belakang (seolah-olah Anda melakukan `&`)
 - job background masih terikat pada sesi Anda saat ini, dan keluar jika
   Anda logout. `disown` memungkinkan Anda memutus koneksi itu. atau gunakan `nohup`.
 - `$!` adalah pid proses background terakhir

<!-- TODO: process output control (^S and ^Q)? -->

Bagaimana dengan hal lain yang berjalan di komputer Anda?

 - `ps` adalah teman Anda: mencantumkan proses yang berjalan
   - `ps -A`: mencetak proses dari semua pengguna (juga `ps ax`)
   - `ps` memiliki *banyak* argumen: lihat `man ps`
 - `pgrep`: menemukan proses dengan pencarian (seperti `ps -A | grep`)
   - `pgrep -af`: mencari dan menampilkan beserta argumennya
 - `kill`: mengirim sebuah _signal_ ke proses berdasarkan ID (`pkill` berdasarkan pencarian + `-f`)
   - signal memberi tahu proses untuk "melakukan sesuatu"
   - paling umum: `SIGKILL` (`-9` atau `-KILL`): memberi tahu untuk keluar *sekarang*
     setara dengan `^\`
   - juga `SIGTERM` (`-15` atau `-TERM`): memberi tahu untuk keluar secara graceful
     setara dengan `^C`


## Flag

Sebagian besar utilitas command line menerima parameter menggunakan **flag**. Flag biasanya hadir dalam bentuk pendek (`-h`) dan bentuk panjang (`--help`). Biasanya menjalankan `CMD -h` atau `man CMD` akan memberi Anda daftar flag yang diterima program.
Flag pendek biasanya dapat digabungkan, menjalankan `rm -r -f` setara dengan menjalankan `rm -rf` atau `rm -fr`.
Beberapa flag umum merupakan standar de facto dan Anda akan melihatnya di banyak aplikasi:

* `-a` umumnya merujuk semua berkas (yaitu juga termasuk yang dimulai dengan titik)
* `-f` biasanya merujuk memaksa sesuatu, seperti `rm -f`
* `-h` menampilkan bantuan untuk sebagian besar perintah
* `-v` biasanya mengaktifkan output verbose
* `-V` biasanya mencetak versi perintah

Juga, double dash `--` digunakan pada perintah bawaan dan banyak perintah lain untuk menandakan akhir opsi perintah, setelah itu hanya parameter positional yang diterima. Jadi jika Anda memiliki berkas bernama `-v` (yang dapat Anda buat) dan ingin melakukan grep padanya `grep pattern -- -v` akan berfungsi sedangkan `grep pattern -v` tidak. Bahkan, salah satu cara membuat berkas semacam itu adalah melakukan `touch -- -v`.

## Latihan

1. Jika Anda benar-benar baru di shell Anda mungkin ingin membaca panduan yang lebih komprehensif tentangnya seperti [BashGuide](https://mywiki.wooledge.org/BashGuide). Jika Anda menginginkan pengantar yang lebih mendalam [The Linux Command Line](https://linuxcommand.org/tlcl.php) adalah sumber yang baik.

1. **PATH, which, type**

    Kami sempat membahas bahwa environment variable `PATH` digunakan untuk menemukan program yang Anda jalankan melalui command line. Mari jelajahi itu sedikit lebih jauh
    - Jalankan `echo $PATH` (atau `echo $PATH | tr -s ':' '\n'` untuk pencetakan yang rapi) dan periksa isinya, lokasi apa yang tercantum?
    - Perintah `which` menemukan sebuah program di PATH pengguna. Coba jalankan `which` untuk perintah umum seperti `echo`, `ls` atau `mv`. Perhatikan bahwa `which` agak terbatas karena tidak memahami alias shell. Coba jalankan `type` dan `command -v` untuk perintah yang sama. Bagaimana outputnya berbeda?
    - Jalankan `PATH=` dan coba jalankan kembali perintah sebelumnya, sebagian berfungsi dan sebagian tidak, dapatkah Anda mencari tahu alasannya?

1. **Variabel Khusus**
    - Menjadi apa variabel `~` ketika diekspansi? Bagaimana dengan `.`? Dan `..`?
    - Apa fungsi variabel `$?`?
    - Apa fungsi variabel `$_`?
    - Menjadi apa variabel `!!` ketika diekspansi? Bagaimana dengan `!!*`? Dan `!l`?
    - Cari dokumentasi untuk opsi ini dan biasakan diri dengannya

1. **xargs**

    Kadang piping tidak benar-benar berfungsi karena perintah yang menerima pipe tidak mengharapkan format yang dipisahkan newline. Misalnya perintah `file` memberi tahu Anda properti berkas.

    Coba jalankan `ls | file` dan `ls | xargs file`. Apa yang dilakukan `xargs`?


1. **Shebang**

    Ketika Anda menulis skrip Anda dapat menentukan kepada shell Anda interpreter apa yang harus digunakan untuk menafsirkan skrip dengan menggunakan baris [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)). Tulis skrip bernama `hello` dengan isi berikut lalu buat dapat dieksekusi dengan `chmod +x hello`. Lalu eksekusi dengan `./hello`. Lalu hapus baris pertama dan eksekusi lagi? Bagaimana shell menggunakan baris pertama itu?


    ```bash
      #! /usr/bin/python

      print("Hello World!")
    ```

    Anda akan sering melihat program yang memiliki shebang seperti `#! usr/bin/env bash`. Ini solusi yang lebih portabel dengan rangkaian [kelebihan dan kekurangannya](https://unix.stackexchange.com/questions/29608/why-is-it-better-to-use-usr-bin-env-name-instead-of-path-to-name-as-my) sendiri. Bagaimana `env` berbeda dari `which`? Environment variable apa yang digunakan `env` untuk menentukan program mana yang dijalankan?


1. **Pipe, process substitution, subshell**

    Buat skrip bernama `slow_seq.sh` dengan isi berikut dan lakukan `chmod +x slow_seq.sh` agar dapat dieksekusi.

    ```bash
      #! /usr/bin/env bash

      for i in $(seq 1 10); do
              echo $i;
              sleep 1;
      done
    ```

    Ada cara di mana pipe (dan process substitution) berbeda dari penggunaan eksekusi subshell, yaitu `$()`. Jalankan perintah berikut dan amati perbedaannya:

    - `./slow_seq.sh | grep -P "[3-6]"`
    - `grep -P "[3-6]" <(./slow_seq.sh)`
    - `echo $(./slow_seq.sh) | grep -P "[3-6]"`


1. **Lain-lain**
    - Coba jalankan `touch {a,b}{a,b}` lalu `ls` apa yang muncul?
    - Kadang Anda ingin mempertahankan STDIN dan tetap melakukan pipe ke sebuah berkas. Coba jalankan `echo HELLO | tee hello.txt`
    - Coba jalankan `cat hello.txt > hello.txt ` apa yang Anda harapkan terjadi? Apa yang terjadi?
    - Jalankan `echo HELLO > hello.txt` lalu jalankan `echo WORLD >> hello.txt`. Apa isi `hello.txt`? Bagaimana `>` berbeda dari `>>`?
    - Jalankan `printf "\e[38;5;81mfoo\e[0m\n"`. Bagaimana outputnya berbeda? Jika Anda ingin tahu lebih banyak, cari ANSI color escape sequence.
    - Jalankan `touch a.txt` lalu jalankan `^txt^log` apa yang bash lakukan untuk Anda? Dalam semangat yang sama, jalankan `fc`. Apa fungsinya?

{% comment %}

TODO

1. **parallel**
- set -e, set -x
- traps

{% endcomment %}

1. **Pintasan keyboard**

    Seperti aplikasi apa pun yang sering Anda gunakan, ada baiknya membiasakan diri dengan pintasan keyboard-nya. Ketik yang berikut dan coba cari tahu apa fungsinya dan dalam skenario apa mengetahuinya bisa berguna. Untuk sebagian, mungkin lebih mudah mencari daring tentang apa fungsinya. (ingat bahwa `^X` berarti menekan `Ctrl+X`)

    - `^A`, `^E`
    - `^R`
    - `^L`
    - `^C`, `^\` dan  `^D`
    - `^U` dan `^Y`
