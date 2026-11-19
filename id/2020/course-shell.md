---
layout: lecture-id
title: "Gambaran Kursus + Shell"
description: >
  Pelajari alasan di balik kelas ini dan mulai menggunakan shell.
thumbnail: /static/assets/thumbnails/2020/lec1.png
date: 2020-01-13
ready: true
video:
  aspect: 56.25
  id: Z56Jmr9Z34Q
lang: id
permalink: /id/2020/course-shell/
---

# Motivasi

Sebagai ilmuwan komputer, kita tahu bahwa komputer sangat baik dalam membantu tugas-tugas yang
berulang. Namun, terlalu sering kita lupa bahwa hal ini juga berlaku sama besar pada
_penggunaan_ komputer oleh kita, sebagaimana pada komputasi
yang ingin dijalankan program kita. Ada berbagai macam tool
yang tersedia di ujung jari kita sehingga kita dapat lebih produktif dan
menyelesaikan masalah yang lebih kompleks saat mengerjakan masalah apa pun yang berkaitan dengan
komputer. Namun banyak dari kita hanya memanfaatkan sebagian kecil dari tool tersebut; kita
hanya mengetahui secukupnya mantra ajaib secara hafalan agar bisa bertahan, dan
menyalin-tempel perintah dari internet secara buta ketika kita macet.

Kelas ini merupakan upaya untuk menjawab hal ini.

Kami ingin mengajarkan kepada Anda cara memanfaatkan tool yang sudah Anda
kenal sebaik mungkin, menunjukkan tool baru untuk menambah perangkat Anda,
dan semoga menumbuhkan sedikit kegembiraan dalam menjelajahi (dan mungkin membangun) lebih banyak tool sendiri.
Inilah yang kami yakini sebagai semester yang hilang dari sebagian besar kurikulum Ilmu
Komputer.

# Struktur kelas

Kelas ini terdiri dari 11 kuliah berdurasi 1 jam, masing-masing berpusat pada
[topik tertentu](/2020/). Kuliah-kuliah tersebut sebagian besar independen,
meskipun seiring berjalannya semester kami akan menganggap Anda sudah familiar
dengan materi dari kuliah sebelumnya. Kami memiliki catatan kuliah
daring, tetapi akan ada banyak materi yang dibahas di kelas (misalnya dalam
bentuk demo) yang mungkin tidak ada dalam catatan. Kami akan merekam
kuliah dan mengunggah rekamannya secara daring.

Kami mencoba mencakup banyak materi dalam 11 kuliah 1 jam saja,
sehingga kuliahnya cukup padat. Untuk memberi Anda waktu mengenal materinya
sesuai kecepatan Anda sendiri, setiap kuliah menyertakan
serangkaian latihan yang menuntun Anda melalui poin-poin kunci kuliah tersebut. Setelah
setiap kuliah, kami mengadakan office hours di mana kami akan hadir untuk
membantu menjawab pertanyaan apa pun yang Anda miliki. Jika Anda mengikuti kelas
secara daring, Anda dapat mengirim pertanyaan ke kami di
[missing-semester@mit.edu](mailto:missing-semester@mit.edu).

Karena waktu kami terbatas, kami tidak akan dapat membahas semua tool
dengan tingkat detail seperti kelas berskala penuh. Bila memungkinkan, kami
akan berusaha mengarahkan Anda ke sumber daya untuk menyelami lebih jauh suatu tool
atau topik, tetapi jika ada sesuatu yang sangat menarik bagi
Anda, jangan ragu menghubungi kami dan meminta petunjuk!

# Topik 1: The Shell

## Apa itu shell?

Komputer saat ini memiliki berbagai antarmuka untuk memberikan perintah;
antarmuka pengguna grafis yang beragam, antarmuka suara, dan
bahkan AR/VR ada di mana-mana. Semua itu bagus untuk 80% use case, tetapi
sering kali secara mendasar terbatas dalam hal yang memungkinkan Anda lakukan —
Anda tidak dapat menekan tombol yang tidak ada atau memberikan perintah suara yang
belum diprogram. Untuk memanfaatkan sepenuhnya tool yang disediakan komputer
Anda, kita harus kembali ke cara lama dan turun ke antarmuka
tekstual: The Shell.

Hampir semua platform yang dapat Anda peroleh memiliki shell dalam satu bentuk atau
lainnya, dan banyak di antaranya memiliki beberapa shell yang dapat Anda pilih.
Meskipun detailnya bisa berbeda-beda, pada intinya semuanya kurang lebih
sama: shell memungkinkan Anda menjalankan program, memberinya input, dan memeriksa
outputnya secara semi-terstruktur.

Pada kuliah ini, kami akan memfokuskan pada Bourne Again SHell, atau "bash" secara
singkat. Ini adalah salah satu shell yang paling banyak digunakan, dan sintaksnya
mirip dengan yang akan Anda lihat di banyak shell lain. Untuk membuka
_prompt_ shell (tempat Anda dapat mengetik perintah), Anda terlebih dahulu memerlukan sebuah _terminal_.
Perangkat Anda kemungkinan sudah dilengkapi dengan terminal, atau Anda dapat memasangnya
dengan cukup mudah.

## Menggunakan shell

Saat Anda membuka terminal, Anda akan melihat sebuah _prompt_ yang sering kali terlihat
sedikit seperti ini:

```console
missing:~$
```

Ini adalah antarmuka tekstual utama ke shell. Prompt ini memberi tahu Anda
bahwa Anda berada di mesin `missing` dan bahwa "current working directory" Anda,
atau tempat Anda saat ini, adalah `~` (singkatan dari "home"). Tanda `$` memberi tahu
Anda bahwa Anda bukan pengguna root (lebih lanjut nanti). Pada prompt ini Anda
dapat mengetik sebuah _command_, yang kemudian akan diinterpretasikan oleh shell. Perintah
paling dasar adalah menjalankan sebuah program:

```console
missing:~$ date
Fri 10 Jan 2020 11:49:31 AM EST
missing:~$
```

Di sini, kita menjalankan program `date`, yang (mungkin tidak mengherankan)
mencetak tanggal dan waktu saat ini. Shell lalu meminta kita memberikannya
perintah lain untuk dijalankan. Kita juga dapat menjalankan perintah dengan _argument_:

```console
missing:~$ echo hello
hello
```

Dalam kasus ini, kita meminta shell menjalankan program `echo` dengan
argumen `hello`. Program `echo` sekadar mencetak argumennya.
Shell mengurai perintah dengan memisahkannya berdasarkan whitespace, lalu
menjalankan program yang ditunjukkan oleh kata pertama, dengan setiap kata berikutnya
diberikan sebagai argumen yang dapat diakses program. Jika Anda ingin memberikan
argumen yang memuat spasi atau karakter khusus lain (misalnya, sebuah
direktori bernama "My Photos"), Anda dapat mengapit argumen dengan `'`
atau `"` (`"My Photos"`), atau meng-escape hanya karakter yang relevan dengan `\`
(`My\ Photos`).

Tetapi bagaimana shell mengetahui cara menemukan program `date` atau `echo`?
Nah, shell adalah lingkungan pemrograman, sama seperti Python atau Ruby,
sehingga shell memiliki variabel, kondisional, loop, dan fungsi (kuliah
berikutnya!). Ketika Anda menjalankan perintah di shell Anda, Anda sebenarnya menulis
sedikit kode yang diinterpretasikan shell Anda. Jika shell diminta
menjalankan sebuah perintah yang tidak cocok dengan salah satu kata kunci pemrogramannya, shell
mengonsultasikan sebuah _environment variable_ bernama `$PATH` yang mencantumkan direktori
mana yang harus dicari shell untuk program ketika diberikan sebuah
perintah:


```console
missing:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
missing:~$ which echo
/bin/echo
missing:~$ /bin/echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Ketika kita menjalankan perintah `echo`, shell melihat bahwa ia harus menjalankan
program `echo`, lalu menelusuri daftar direktori yang dipisahkan `:` di `$PATH` untuk mencari berkas
dengan nama tersebut. Ketika menemukannya, shell menjalankannya (dengan asumsi berkas tersebut
_executable_; lebih lanjut nanti). Kita dapat mengetahui berkas mana yang dijalankan untuk
nama program tertentu menggunakan program `which`. Kita juga dapat melewati `$PATH`
sepenuhnya dengan memberikan _path_ ke berkas yang ingin kita jalankan.

## Bernavigasi di shell

Sebuah path di shell adalah daftar direktori yang dibatasi; dipisahkan oleh `/`
di Linux dan macOS serta `\` di Windows. Di Linux dan macOS, path `/`
adalah "root" dari file system, di bawahnya semua direktori dan berkas
berada, sedangkan di Windows ada satu root untuk setiap partisi disk (misalnya,
`C:\`). Kami umumnya akan menganggap Anda menggunakan file system Linux
di kelas ini. Path yang dimulai dengan `/` disebut path _absolut_.
Path lainnya adalah path _relatif_. Path relatif bersifat relatif terhadap
current working directory, yang dapat kita lihat dengan perintah `pwd` dan
ubah dengan perintah `cd`. Dalam sebuah path, `.` merujuk pada direktori saat ini,
dan `..` pada direktori induknya:

```console
missing:~$ pwd
/home/missing
missing:~$ cd /home
missing:/home$ pwd
/home
missing:/home$ cd ..
missing:/$ pwd
/
missing:/$ cd ./home
missing:/home$ pwd
/home
missing:/home$ cd missing
missing:~$ pwd
/home/missing
missing:~$ ../../bin/echo hello
hello
```

Perhatikan bahwa prompt shell kita terus memberi tahu kita apa
current working directory kita. Anda dapat mengonfigurasi prompt Anda untuk menampilkan berbagai
informasi berguna, yang akan kami bahas pada kuliah berikutnya.

Secara umum, ketika kita menjalankan sebuah program, program akan beroperasi di direktori
saat ini kecuali kita memberi tahu sebaliknya. Misalnya, program biasanya akan
mencari berkas di sana, dan membuat berkas baru di sana jika perlu.

Untuk melihat apa yang ada di sebuah direktori, kita menggunakan perintah `ls`:

```console
missing:~$ ls
missing:~$ cd ..
missing:/home$ ls
missing
missing:/home$ cd ..
missing:/$ ls
bin
boot
dev
etc
home
...
```

Kecuali sebuah direktori diberikan sebagai argumen pertamanya, `ls` akan mencetak
isi direktori saat ini. Sebagian besar perintah menerima flag dan
opsi (flag dengan nilai) yang dimulai dengan `-` untuk mengubah
perilakunya. Biasanya, menjalankan program dengan flag `-h` atau `--help`
akan mencetak beberapa teks bantuan yang memberi tahu Anda flag
dan opsi apa yang tersedia. Misalnya, `ls --help` memberi tahu kita:

```
  -l                         use a long listing format
```

```console
missing:~$ ls -l /home
drwxr-xr-x 1 missing  users  4096 Jun 15  2019 missing
```

Ini memberi kita banyak informasi tambahan tentang setiap berkas atau direktori
yang ada. Pertama, `d` di awal baris memberi tahu kita bahwa
`missing` adalah sebuah direktori. Lalu mengikuti tiga kelompok tiga karakter
(`rwx`). Ini menunjukkan permission apa yang dimiliki pemilik berkas
(`missing`), grup pemilik (`users`), dan semua orang lain secara berurutan
pada item terkait. Tanda `-` menunjukkan bahwa principal tertentu tidak
memiliki permission tersebut. Di atas, hanya pemilik yang diizinkan
memodifikasi (`w`) direktori `missing` (yakni, menambah/menghapus berkas di dalamnya). Untuk
masuk ke sebuah direktori, pengguna harus memiliki permission "search" (direpresentasikan oleh "execute":
`x`) pada direktori tersebut (dan induk-induknya). Untuk mencantumkan isinya,
pengguna harus memiliki permission read (`r`) pada direktori tersebut. Untuk
berkas, permission-nya seperti yang Anda duga. Perhatikan bahwa hampir semua
berkas di `/bin` memiliki permission `x` yang disetel untuk grup terakhir,
"everyone else", sehingga siapa pun dapat mengeksekusi program tersebut.

Beberapa program praktis lain yang perlu diketahui pada titik ini adalah `mv` (untuk
mengganti nama/memindahkan berkas), `cp` (untuk menyalin berkas), dan `mkdir` (untuk membuat
direktori baru).

Jika Anda ingin informasi _lebih_ tentang argumen, input,
output sebuah program, atau cara kerjanya secara umum, coba program `man`. Program ini
menerima sebagai argumen nama sebuah program, dan menampilkan _manual
page_-nya. Tekan `q` untuk keluar.

```console
missing:~$ man ls
```

## Menghubungkan program

Di shell, program memiliki dua "stream" utama yang terkait dengannya:
input stream dan output stream-nya. Ketika program mencoba
membaca input, program membaca dari input stream, dan ketika program mencetak
sesuatu, program mencetak ke output stream-nya. Biasanya, input
dan output sebuah program keduanya adalah terminal Anda. Yakni, keyboard Anda sebagai input dan
layar Anda sebagai output. Namun, kita juga dapat mengalihkan stream tersebut!

Bentuk redirection paling sederhana adalah `< file` dan `> file`. Yang pertama mengalihkan input dari berkas, sedangkan yang kedua mengalihkan output ke berkas:

```console
missing:~$ echo hello > hello.txt
missing:~$ cat hello.txt
hello
missing:~$ cat < hello.txt
hello
missing:~$ cat < hello.txt > hello2.txt
missing:~$ cat hello2.txt
hello
```

Seperti ditunjukkan pada contoh di atas, `cat` adalah program yang mengon`cat`enasi
berkas. Ketika diberikan nama berkas sebagai argumen, program mencetak isi masing-masing
berkas secara berurutan ke output stream-nya. Tetapi ketika `cat` tidak diberikan argumen
apa pun, program mencetak isi dari input stream ke output stream-nya (seperti
pada contoh ketiga di atas).

Anda juga dapat menggunakan `>>` untuk menambahkan ke sebuah berkas. Tempat redirection
input/output semacam ini benar-benar bersinar adalah dalam penggunaan _pipe_. Operator `|`
memungkinkan Anda "merangkai" program sehingga output satu program menjadi
input program lain:

```console
missing:~$ ls -l / | tail -n1
drwxr-xr-x 1 root  root  4096 Jun 20  2019 var
missing:~$ curl --head --silent google.com | grep --ignore-case content-length | cut --delimiter=' ' -f2
219
```

Kami akan membahas jauh lebih detail tentang cara memanfaatkan pipe
pada kuliah data wrangling.

## Tool yang serbaguna dan kuat

Pada sebagian besar sistem mirip Unix, satu pengguna bersifat khusus: pengguna "root". Anda mungkin
telah melihatnya pada pencantuman berkas di atas. Pengguna root berada di atas (hampir)
semua pembatasan akses, dan dapat membuat, membaca, memperbarui, dan menghapus berkas
apa pun di sistem. Anda biasanya tidak akan login ke sistem Anda sebagai
pengguna root, karena terlalu mudah untuk tanpa sengaja merusak sesuatu.
Sebagai gantinya, Anda akan menggunakan perintah `sudo`. Seperti namanya, perintah ini
memungkinkan Anda "melakukan" sesuatu "sebagai su" (singkatan dari "super user", atau "root").
Ketika Anda mendapatkan error permission denied, biasanya itu karena Anda perlu
melakukan sesuatu sebagai root. Meskipun begitu, pastikan Anda memeriksa ulang terlebih dahulu bahwa Anda
benar-benar ingin melakukannya dengan cara itu!

Satu hal yang Anda perlukan sebagai root untuk melakukannya adalah menulis ke file
system `sysfs` yang di-mount di bawah `/sys`. `sysfs` mengekspos sejumlah parameter kernel sebagai
berkas, sehingga Anda dapat dengan mudah mengonfigurasi ulang kernel secara langsung tanpa
tool khusus. **Perhatikan bahwa sysfs tidak ada di Windows atau macOS.**

Misalnya, kecerahan layar laptop Anda diekspos melalui berkas
bernama `brightness` di bawah

```
/sys/class/backlight
```

Dengan menuliskan sebuah nilai ke berkas tersebut, kita dapat mengubah kecerahan layar.
Naluri pertama Anda mungkin melakukan sesuatu seperti:

```console
$ sudo find -L /sys/class/backlight -maxdepth 2 -name '*brightness*'
/sys/class/backlight/thinkpad_screen/brightness
$ cd /sys/class/backlight/thinkpad_screen
$ sudo echo 3 > brightness
An error occurred while redirecting file 'brightness'
open: Permission denied
```

Error ini mungkin mengejutkan. Bagaimanapun juga, kita menjalankan perintah dengan
`sudo`! Ini hal penting yang perlu diketahui tentang shell. Operasi
seperti `|`, `>`, dan `<` dilakukan _oleh shell_, bukan oleh masing-masing
program. `echo` dan kawan-kawan tidak "mengetahui" tentang `|`. Program hanya membaca dari
input dan menulis ke output-nya, apa pun itu. Dalam kasus
di atas, _shell_ (yang terautentikasi sebagai pengguna Anda) mencoba
membuka berkas brightness untuk ditulis, sebelum menetapkannya sebagai output `sudo
echo`, tetapi dicegah melakukannya karena shell tidak
berjalan sebagai root. Dengan pengetahuan ini, kita dapat mengakalinya:

```console
$ echo 3 | sudo tee brightness
```

Karena program `tee` yang membuka berkas `/sys` untuk ditulis,
dan _program itu_ berjalan sebagai `root`, permission-nya berhasil. Anda dapat
mengendalikan berbagai hal menyenangkan dan berguna melalui `/sys`, seperti
status berbagai LED sistem (path Anda mungkin berbeda):

```console
$ echo 1 | sudo tee /sys/class/leds/input6::scrolllock/brightness
```

# Langkah selanjutnya

Pada titik ini Anda sudah cukup mengenal shell untuk menyelesaikan
tugas dasar. Anda seharusnya sudah dapat bernavigasi untuk menemukan berkas yang
diminati dan menggunakan fungsionalitas dasar sebagian besar program. Pada kuliah
berikutnya, kita akan membahas cara melakukan dan mengotomatiskan tugas yang lebih kompleks
menggunakan shell dan banyak program command-line praktis yang
tersedia.

# Latihan

Semua kelas dalam kursus ini disertai dengan serangkaian latihan. Sebagian memberi
Anda tugas spesifik untuk dikerjakan, sementara yang lain bersifat terbuka, seperti "coba gunakan program X dan Y".
Kami sangat mendorong Anda untuk mencobanya.

Kami belum menulis solusi untuk latihan-latihan ini. Jika Anda macet pada hal tertentu,
silakan kirim email kepada kami yang menjelaskan apa yang telah Anda coba
sejauh ini, dan kami akan berusaha membantu.

 1. Untuk kursus ini, Anda perlu menggunakan Unix shell seperti Bash atau ZSH. Jika Anda
    menggunakan Linux atau macOS, Anda tidak perlu melakukan hal khusus. Jika Anda menggunakan
    Windows, Anda perlu memastikan Anda tidak menjalankan cmd.exe atau PowerShell;
    Anda dapat menggunakan [Windows Subsystem for
    Linux](https://docs.microsoft.com/en-us/windows/wsl/) atau Linux virtual
    machine untuk menggunakan tool command-line bergaya Unix. Untuk memastikan Anda menjalankan
    shell yang sesuai, Anda dapat mencoba perintah `echo $SHELL`. Jika hasilnya
    seperti `/bin/bash` atau `/usr/bin/zsh`, itu berarti Anda menjalankan
    program yang benar.
 1. Buat direktori baru bernama `missing` di bawah `/tmp`.
 1. Cari program `touch`. Program `man` adalah teman Anda.
 1. Gunakan `touch` untuk membuat berkas baru bernama `semester` di dalam `missing`.
 1. Tuliskan berikut ini ke dalam berkas tersebut, satu baris setiap kali:
    ```
    #!/bin/sh
    curl --head --silent https://missing.csail.mit.edu
    ```
    Baris pertama mungkin sulit dibuat berfungsi. Berguna untuk mengetahui bahwa
    `#` memulai komentar di Bash, dan `!` memiliki makna khusus bahkan di dalam
    string berkutip ganda (`"`). Bash memperlakukan string berkutip tunggal (`'`)
    secara berbeda: string tersebut akan berhasil dalam kasus ini. Lihat halaman manual
    [quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html) Bash
    untuk informasi lebih lanjut.
 1. Coba eksekusi berkas tersebut, yaitu ketik path ke skrip (`./semester`)
    ke shell Anda dan tekan enter. Pahami mengapa itu tidak berfungsi dengan
    mengonsultasikan output `ls` (petunjuk: lihat bit permission pada
    berkas tersebut).
 1. Jalankan perintah dengan secara eksplisit memulai interpreter `sh`, dan memberikannya
    berkas `semester` sebagai argumen pertama, yaitu `sh semester`. Mengapa
    ini berfungsi, sedangkan `./semester` tidak?
 1. Cari program `chmod` (misalnya gunakan `man chmod`).
 1. Gunakan `chmod` agar memungkinkan menjalankan perintah `./semester` alih-alih
    harus mengetik `sh semester`. Bagaimana shell Anda mengetahui bahwa berkas tersebut
    seharusnya diinterpretasikan menggunakan `sh`? Lihat halaman ini tentang baris
    [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) untuk informasi lebih
    lanjut.
 1. Gunakan `|` dan `>` untuk menuliskan output tanggal "last modified" yang dihasilkan oleh
    `semester` ke berkas bernama `last-modified.txt` di direktori home
    Anda.
 1. Tulis perintah yang membaca tingkat daya baterai laptop Anda atau
    suhu CPU mesin desktop Anda dari `/sys`. Catatan: jika Anda pengguna macOS,
    OS Anda tidak memiliki sysfs, sehingga Anda dapat melewati latihan ini.
