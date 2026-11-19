---
layout: lecture-id
title: "Data Wrangling"
presenter: Jon
date: 2019-01-17
order: 2
video:
  aspect: 56.25
  id: VW2jn9Okjhw
lang: id
permalink: /id/2019/data-wrangling/
---

Pernahkah Anda memiliki sekumpulan teks dan ingin melakukan sesuatu dengannya?
Bagus. Itulah isi data wrangling!
Secara khusus, mengadaptasi data dari satu format ke format lain, sampai Anda mendapatkan
tepat apa yang Anda inginkan.

Kita sudah melihat data wrangling dasar: `journalctl | grep -i intel`.
 - menemukan semua entri log sistem yang menyebut Intel (tidak peka huruf besar-kecil)
 - sebenarnya, sebagian besar data wrangling adalah soal mengetahui tool apa yang Anda miliki,
   dan bagaimana menggabungkannya.

Mari mulai dari awal: kita membutuhkan sumber data, dan sesuatu untuk
dilakukan dengannya. Log sering menjadi use case yang baik, karena Anda sering ingin
menyelidiki hal-hal tentangnya, dan membaca seluruh isinya tidak
layak. Mari cari tahu siapa yang mencoba login ke server saya dengan melihat
log server saya:

```bash
ssh myserver journalctl
```

Itu terlalu banyak. Mari batasi ke hal-hal ssh:

```bash
ssh myserver journalctl | grep sshd
```

Perhatikan bahwa kita menggunakan pipe untuk mengalirkan berkas _remote_ melalui `grep`
di komputer lokal kita! `ssh` itu ajaib. Namun ini masih jauh lebih banyak
dari yang kita inginkan. Dan cukup sulit dibaca. Mari lakukan lebih baik:

```bash
ssh myserver journalctl | grep sshd | grep "Disconnected from"
```

Masih ada banyak kebisingan di sini. Ada _banyak_ cara untuk menyingkirkan
hal itu, tetapi mari lihat salah satu tool paling kuat di
perangkat Anda: `sed`.

`sed` adalah "stream editor" yang dibangun di atas editor lama `ed`. Di
dalamnya, Anda pada dasarnya memberikan perintah singkat tentang cara memodifikasi berkas, alih-alih
memanipulasi isinya secara langsung (meskipun Anda juga dapat melakukannya).
Ada banyak sekali perintah, tetapi salah satu yang paling umum adalah `s`:
substitution. Misalnya, kita dapat menulis:

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed 's/.*Disconnected from //'
```

Yang baru saja kita tulis adalah sebuah _regular expression_ sederhana; konstruksi
yang kuat yang memungkinkan Anda mencocokkan teks dengan pola. Perintah `s` ditulis
dalam bentuk: `s/REGEX/SUBSTITUTION/`, di mana `REGEX` adalah
regular expression yang ingin Anda cari, dan `SUBSTITUTION` adalah
teks yang ingin Anda gunakan untuk menggantikan teks yang cocok.

## Regular expressions

Regular expression cukup umum dan berguna sehingga layak untuk
meluangkan waktu memahami cara kerjanya. Mari mulai dengan melihat
yang kita gunakan di atas: `/.*Disconnected from /`. Regular expression
biasanya (meskipun tidak selalu) diapit `/`. Sebagian besar karakter ASCII
hanya membawa makna normalnya, tetapi sebagian karakter memiliki perilaku
pencocokan "khusus". Persisnya karakter mana yang melakukan apa sedikit berbeda-beda
di antara implementasi regular expression yang berbeda, yang merupakan
sumber frustrasi besar. Pola yang sangat umum adalah:

 - `.` berarti "satu karakter apa pun" kecuali newline
 - `*` nol atau lebih dari kecocokan sebelumnya
 - `+` satu atau lebih dari kecocokan sebelumnya
 - `[abc]` satu karakter apa pun di antara `a`, `b`, dan `c`
 - `(RX1|RX2)` entah sesuatu yang cocok dengan `RX1` atau `RX2`
 - `^` awal baris
 - `$` akhir baris

Regular expression `sed` agak aneh, dan akan mengharuskan Anda
menaruh `\` sebelum sebagian besar karakter ini agar makna khususnya berlaku. Atau
Anda dapat memberikan `-E`.

Jadi, melihat kembali `/.*Disconnected from /`, kita melihat bahwa pola itu cocok dengan
teks apa pun yang dimulai dengan berapa pun karakter, diikuti
string literal "Disconnected from ". Itulah yang kita inginkan. Tetapi
hati-hati, regular expression itu rumit. Bagaimana jika seseorang mencoba login
dengan username "Disconnected from"? Kita akan memiliki:

```
Jan 17 03:13:00 thesquareplanet.com sshd[2631]: Disconnected from invalid user Disconnected from 46.97.239.16 port 55920 [preauth]
```

Apa yang akan kita dapatkan? Nah, `*` dan `+` secara default bersifat "greedy".
Keduanya akan mencocokkan teks sebanyak mungkin. Jadi, pada contoh di atas, kita akan mendapatkan

```
46.97.239.16 port 55920 [preauth]
```

Yang mungkin bukan yang kita inginkan. Pada sebagian implementasi
regular expression, Anda cukup menambahkan `?` pada `*` atau `+` agar menjadi
non-greedy, tetapi sayangnya `sed` tidak mendukungnya. Kita _bisa_ beralih ke
mode command-line perl, yang _mendukung_ konstruksi tersebut:

```bash
perl -pe 's/.*?Disconnected from //'
```

Kita akan tetap menggunakan `sed` untuk sisa bagian ini, karena tool ini sejauh ini
tool yang lebih umum untuk pekerjaan semacam ini. `sed` juga dapat melakukan hal praktis
lain seperti mencetak baris setelah kecocokan tertentu, melakukan beberapa
substitusi per pemanggilan, mencari sesuatu, dsb. Tetapi kami tidak akan membahasnya
terlalu banyak di sini. `sed` pada dasarnya adalah topik tersendiri,
tetapi sering ada tool yang lebih baik.

Oke, jadi kita juga memiliki sufiks yang ingin kita singkirkan. Bagaimana kita bisa
melakukannya? Agak rumit untuk mencocokkan hanya teks yang mengikuti
username, terutama jika username bisa memiliki spasi dan sebagainya! Yang perlu
kita lakukan adalah mencocokkan _seluruh_ baris:

```bash
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user .* [^ ]+ port [0-9]+( \[preauth\])?$//'
```

Mari lihat apa yang terjadi dengan [regex
debugger](https://regex101.com/r/qqbZqh/2). Oke, jadi awalnya masih
seperti sebelumnya. Lalu, kita mencocokkan salah satu varian "user" (ada
dua prefiks di log). Lalu kita mencocokkan string karakter apa pun
tempat username berada. Lalu kita mencocokkan satu kata
(`[^ ]+`; rangkaian karakter bukan-spasi yang tidak kosong). Lalu kata
"port" diikuti rangkaian digit. Lalu mungkin sufiks
` [preauth]`, dan kemudian akhir baris.

Perhatikan bahwa dengan teknik ini, username "Disconnected from"
tidak akan membingungkan kita lagi. Dapatkah Anda melihat alasannya?

Namun ada satu masalah dengan ini, yaitu seluruh log
menjadi kosong. Kita tetap ingin _mempertahankan_ username-nya. Untuk ini, kita
dapat menggunakan "capture group". Teks apa pun yang cocok dengan regex yang diapit
tanda kurung disimpan dalam capture group bernomor. Capture group ini tersedia
dalam substitusi (dan pada sebagian mesin, bahkan dalam pola itu sendiri!)
sebagai `\1`, `\2`, `\3`, dsb. Jadi:

```bash
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

Seperti yang mungkin Anda bayangkan, Anda dapat membuat regular expression yang _sangat_
rumit. Misalnya, berikut artikel tentang bagaimana Anda mungkin
mencocokkan [alamat
e-mail](https://www.regular-expressions.info/email.html). Itu [tidak
mudah](https://web.archive.org/web/20221223174323/http://emailregex.com/). Dan ada [banyak
diskusi](https://stackoverflow.com/questions/201323/how-to-validate-an-email-address-using-a-regular-expression/1917982).
Dan orang-orang telah [menulis
test](https://fightingforalostcause.net/content/misc/2006/compare-email-regex.php).
Dan [matriks uji](https://mathiasbynens.be/demo/url-regex). Anda bahkan
dapat menulis regex untuk menentukan apakah suatu bilangan [adalah bilangan
prima](https://www.noulakaz.net/2007/03/18/a-regular-expression-to-check-for-prime-numbers/).

Regular expression terkenal sulit dibuat dengan benar, tetapi juga
sangat berguna untuk dimiliki dalam perangkat Anda!

## Kembali ke data wrangling

Oke, jadi sekarang kita memiliki

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

Kita bisa melakukannya hanya dengan `sed`, tetapi mengapa begitu? Untuk bersenang-senang, itulah alasannya.

```bash
ssh myserver journalctl
 | sed -E
   -e '/Disconnected from/!d'
   -e 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
```

Ini memamerkan sebagian kemampuan `sed`. `sed` juga dapat menyuntikkan teks
(dengan perintah `i`), secara eksplisit mencetak baris (dengan perintah `p`),
memilih baris berdasarkan indeks, dan banyak hal lain. Periksa `man sed`!

Ngomong-ngomong. Yang kita miliki sekarang memberi kita daftar semua username yang telah
mencoba login. Tetapi ini cukup tidak membantu. Mari cari yang umum:

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
```

`sort` akan, ya, mengurutkan inputnya. `uniq -c` akan meruntuhkan baris
berurutan yang sama menjadi satu baris, diberi awalan jumlah
kemunculannya. Kita mungkin ingin mengurutkan itu juga dan hanya mempertahankan
login yang paling umum:

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
```

`sort -n` akan mengurutkan dalam urutan numerik (bukan leksikografis). `-k1,1`
berarti "urutkan hanya berdasarkan kolom pertama yang dipisahkan whitespace". Bagian `,n`
menyatakan "urutkan sampai field ke-`n`, di mana defaultnya adalah akhir
baris. Pada contoh _khusus_ ini, mengurutkan berdasarkan seluruh baris
tidak akan berpengaruh, tetapi kita di sini untuk belajar!

Jika kita menginginkan yang _paling jarang_, kita dapat menggunakan `head` alih-alih
`tail`. Ada juga `sort -r`, yang mengurutkan dalam urutan terbalik.

Oke, itu cukup keren, tetapi kita agak ingin hanya memberikan
username-nya, dan mungkin bukan satu per baris?

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | awk '{print $2}' | paste -sd,
```

Mari mulai dengan `paste`: tool ini memungkinkan Anda menggabungkan baris (`-s`) dengan
pembatas satu karakter tertentu (`-d`). Tetapi apa itu `awk`?

## awk -- editor lain

`awk` adalah bahasa pemrograman yang kebetulan sangat baik dalam
memproses stream teks. Ada _banyak_ yang bisa dikatakan tentang `awk` jika Anda
mempelajarinya dengan benar, tetapi seperti banyak hal lain di sini, kita hanya akan membahas
dasar-dasarnya.

Pertama, apa yang dilakukan `{print $2}`? Nah, program `awk` berbentuk
pola opsional ditambah blok yang menyatakan apa yang harus dilakukan jika pola
cocok dengan baris tertentu. Pola default (yang kita gunakan di atas) mencocokkan
semua baris. Di dalam blok, `$0` disetel ke seluruh isi baris,
dan `$1` sampai `$n` disetel ke _field_ ke-`n` dari baris tersebut, ketika
dipisahkan oleh field separator `awk` (whitespace secara default, ubah
dengan `-F`). Dalam kasus ini, kita menyatakan bahwa, untuk setiap baris, cetak
isi field kedua, yang kebetulan adalah username!

Mari lihat apakah kita dapat melakukan sesuatu yang lebih mewah. Mari hitung jumlah
username sekali-pakai yang dimulai dengan `c` dan diakhiri dengan `e`:

```bash
 | awk '$1 == 1 && $2 ~ /^c[^ ]*e$/ { print $2 }' | wc -l
```

Ada banyak yang harus diurai di sini. Pertama, perhatikan bahwa kita sekarang memiliki pola
(hal yang berada sebelum `{...}`). Pola menyatakan bahwa field pertama
baris harus sama dengan 1 (itu adalah count dari `uniq
-c`), dan bahwa field kedua harus cocok dengan regular
expression yang diberikan. Dan bloknya hanya menyatakan untuk mencetak username. Kita kemudian menghitung
jumlah baris dalam output dengan `wc -l`.

Namun, `awk` adalah bahasa pemrograman, ingat?

```awk
BEGIN { rows = 0 }
$1 == 1 && $2 ~ /^c[^ ]*e$/ { rows += $1 }
END { print rows }
```

`BEGIN` adalah pola yang cocok dengan awal input (dan `END`
cocok dengan akhir). Sekarang, blok per-baris hanya menambahkan count dari
field pertama (meskipun dalam kasus ini akan selalu 1), lalu kita mencetaknya
di akhir. Bahkan, kita _bisa_ menyingkirkan `grep` dan `sed`
sepenuhnya, karena `awk` [dapat melakukan
semuanya](https://web.archive.org/web/20251210045942/https://backreference.org/2010/02/10/idiomatic-awk/), tetapi kami akan
menyerahkannya sebagai latihan bagi pembaca.

## Menganalisis data

Anda dapat melakukan matematika!

```bash
 | paste -sd+ | bc -l
```

```bash
echo "2*($(data | paste -sd+))" | bc -l
```

Anda dapat memperoleh statistik dengan berbagai cara.
[`st`](https://github.com/nferraz/st) cukup rapi, tetapi jika Anda sudah
memiliki R:

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | awk '{print $1}' | R --slave -e 'x <- scan(file="stdin", quiet=TRUE); summary(x)'
```

R adalah bahasa pemrograman lain (yang aneh) yang hebat dalam analisis data
dan [plotting](https://ggplot2.tidyverse.org/). Kami tidak akan membahas terlalu
detail, tetapi cukup dikatakan bahwa `summary` mencetak statistik ringkasan
tentang sebuah matriks, dan kita menghitung matriks dari aliran input
angka, sehingga R memberi kita statistik yang kita inginkan!

Jika Anda hanya ingin plotting sederhana, `gnuplot` adalah teman Anda:

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | gnuplot -p -e 'set boxwidth 0.5; plot "-" using 1:xtic(2) with boxes'
```

## Data wrangling untuk membuat argumen

Kadang Anda ingin melakukan data wrangling untuk menemukan hal yang akan dipasang atau
dihapus berdasarkan daftar yang lebih panjang. Data wrangling yang telah kita bahas
sejauh ini + `xargs` bisa menjadi kombinasi yang kuat:

```bash
rustup toolchain list | grep nightly | grep -vE "nightly-x86|01-17" | sed 's/-x86.*//' | xargs rustup toolchain uninstall
```

# Latihan

1. Jika Anda belum familiar dengan Regular Expression
   [di sini](https://regexone.com/) ada tutorial interaktif singkat yang
   mencakup sebagian besar dasarnya
1. Apa perbedaan `sed s/REGEX/SUBSTITUTION/g` dengan sed biasa?
   Bagaimana dengan `/I` atau `/m`?
1. Untuk melakukan substitusi in-place, cukup menggoda untuk melakukan sesuatu seperti
   `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`. Namun ini
   ide buruk, mengapa? Apakah ini khusus untuk `sed`?
1. Implementasikan tool padanan grep sederhana dalam bahasa yang Anda kuasai menggunakan regex. Jika Anda ingin outputnya diberi warna seperti grep, cari ANSI color escape sequence.
1. Kadang beberapa operasi seperti mengganti nama berkas bisa rumit dengan perintah mentah seperti `mv` . `rename` adalah tool rapi untuk mencapai ini dan memiliki sintaks mirip sed. Coba buat sekumpulan berkas dengan spasi di namanya dan gunakan `rename` untuk menggantinya dengan underscore.
1. Cari pesan boot yang _tidak_ sama di antara tiga reboot
   terakhir Anda (lihat flag `-b` milik `journalctl`). Anda mungkin ingin menggabungkan semua
   log boot bersama dalam satu berkas, karena itu mungkin memudahkan.
1. Hasilkan beberapa statistik waktu boot sistem Anda selama sepuluh boot
   terakhir menggunakan timestamp log dari pesan
   ```
   Logs begin at ...
   ```
   dan
   ```
   systemd[577]: Startup finished in ...
   ```
1. Temukan jumlah kata (di `/usr/share/dict/words`) yang memuat setidaknya
   tiga huruf `a` dan tidak berakhiran `'s`. Apa tiga
   dua huruf terakhir yang paling umum dari kata-kata tersebut? Perintah `y` pada `sed`, atau
   program `tr`, mungkin membantu Anda dengan ketidakpekaan huruf besar-kecil. Berapa banyak
   kombinasi dua huruf tersebut yang ada? Dan sebagai tantangan:
   kombinasi mana yang tidak muncul?
1. Temukan dataset daring seperti [ini](https://commons.wikimedia.org/wiki/Data:Wikipedia_statistics/data.tab) atau [ini](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1).
   Mungkin satu lagi [dari
   sini](https://www.springboard.com/blog/data-science/free-public-data-sets-data-science-project/).
   Ambil dengan `curl` dan ekstrak hanya dua kolom data
   numerik. Jika Anda mengambil data HTML,
   [`pup`](https://github.com/EricChiang/pup) mungkin berguna. Untuk data JSON,
   coba [`jq`](https://stedolan.github.io/jq/). Temukan min dan
   max satu kolom dalam satu perintah, dan jumlah selisih
   antara dua kolom dalam perintah lain.
