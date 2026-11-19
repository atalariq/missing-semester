---
layout: lecture-id
title: "Data Wrangling"
description: >
  Pelajari cara memanipulasi dan mentransformasi data menggunakan tool command-line seperti sed, awk, dan regular expression.
thumbnail: /static/assets/thumbnails/2020/lec4.png
date: 2020-01-16
ready: true
video:
  aspect: 56.25
  id: sz_dsktIjt4
special: true
lang: id
permalink: /id/2020/data-wrangling/
---

Pernahkah Anda ingin mengambil data dalam satu format dan mengubahnya menjadi
format lain? Tentu saja pernah! Secara sangat umum, itulah
isi kuliah ini. Secara khusus, mengolah data, baik dalam
format teks atau biner, sampai Anda mendapatkan tepat apa yang Anda inginkan.

Kita telah melihat beberapa dasar data wrangling pada kuliah sebelumnya. Hampir
setiap kali Anda menggunakan operator `|`, Anda melakukan semacam
data wrangling. Perhatikan perintah seperti `journalctl | grep -i intel`. Perintah itu
menemukan semua entri log sistem yang menyebut Intel (tidak peka huruf besar-kecil). Anda
mungkin tidak menganggapnya sebagai wrangling data, tetapi perintah itu mengubah dari satu format
(seluruh log sistem Anda) menjadi format yang lebih berguna bagi Anda (hanya
entri log intel). Sebagian besar data wrangling adalah soal mengetahui tool apa
yang Anda miliki, dan bagaimana menggabungkannya.

Mari mulai dari awal. Untuk melakukan wrangling data, kita membutuhkan dua hal:
data untuk diolah, dan sesuatu untuk dilakukan dengannya. Log sering menjadi use case
yang baik, karena Anda sering ingin menyelidiki hal-hal tentangnya, dan
membaca seluruh isinya tidak layak. Mari cari tahu siapa yang mencoba
login ke server saya dengan melihat log server saya:

```bash
ssh myserver journalctl
```

Itu terlalu banyak. Mari batasi ke hal-hal ssh:

```bash
ssh myserver journalctl | grep sshd
```

Perhatikan bahwa kita menggunakan pipe untuk mengalirkan berkas _remote_ melalui `grep`
di komputer lokal kita! `ssh` itu ajaib, dan kita akan membahasnya lebih banyak
pada kuliah berikutnya tentang command-line environment. Namun ini masih jauh
lebih banyak dari yang kita inginkan. Dan cukup sulit dibaca. Mari lakukan
lebih baik:

```bash
ssh myserver 'journalctl | grep sshd | grep "Disconnected from"' | less
```

Mengapa quoting tambahan? Nah, log kita mungkin cukup besar, dan membuang-buang
waktu mengalirkannya semua ke komputer kita lalu melakukan filter di sana.
Sebagai gantinya, kita dapat melakukan filter di server jarak jauh, lalu mengolah
datanya secara lokal. `less` memberi kita "pager" yang memungkinkan kita menggulir ke atas
dan ke bawah melalui output panjang. Untuk menghemat lalu lintas tambahan saat
kita men-debug command-line kita, kita bahkan dapat menempelkan log terfilter saat ini
ke sebuah berkas sehingga kita tidak perlu mengakses jaringan saat
mengembangkan:

```console
$ ssh myserver 'journalctl | grep sshd | grep "Disconnected from"' > ssh.log
$ less ssh.log
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

(Anda mungkin mengenali sintaks ini dari bagian "Search and replace" pada [catatan
kuliah](/2020/editors/#advanced-vim) Vim kami! Memang, Vim menggunakan sintaks untuk
mencari dan mengganti yang mirip dengan perintah substitution `sed`.
Mempelajari satu tool sering membantu Anda menjadi lebih mahir dengan tool lain.)

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
string literal "Disconnected from &rdquo;. Itulah yang kita inginkan. Tetapi
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
`[preauth]`, dan kemudian akhir baris.

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

`sed` dapat melakukan berbagai hal menarik lainnya, seperti menyuntikkan teks
(dengan perintah `i`), secara eksplisit mencetak baris (dengan perintah
`p`), memilih baris berdasarkan indeks, dan banyak hal lain. Periksa `man
sed`!

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
username yang paling umum:

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

Oke, itu cukup keren, tetapi bagaimana jika kita ingin mengekstrak hanya username
sebagai daftar yang dipisahkan koma alih-alih satu per baris, mungkin untuk berkas config?

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | sort -nk1,1 | tail -n10
 | awk '{print $2}' | paste -sd,
```

Jika Anda menggunakan macOS: perhatikan bahwa perintah seperti yang ditampilkan tidak akan berfungsi dengan
`paste` BSD yang disertakan dengan macOS. Lihat [latihan 4 dari kuliah shell
tools](/2020/shell-tools/#exercises) untuk lebih lanjut tentang perbedaan antara BSD
dan GNU coreutils serta instruksi cara memasang GNU coreutils di macOS.

Mari mulai dengan `paste`: tool ini memungkinkan Anda menggabungkan baris (`-s`) dengan
pembatas satu karakter tertentu (`-d`; `,` dalam kasus ini). Tetapi apa itu `awk`?

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

Anda dapat melakukan matematika langsung di shell Anda menggunakan `bc`, kalkulator yang dapat membaca
dari STDIN! Misalnya, jumlahkan angka pada setiap baris dengan menggabungkan
mereka, dipisahkan `+`:

```bash
 | paste -sd+ | bc -l
```

Atau menghasilkan ekspresi yang lebih rumit:

```bash
echo "2*($(data | paste -sd+))" | bc -l
```

Anda dapat memperoleh statistik dengan berbagai cara.
[`st`](https://github.com/nferraz/st) cukup rapi, tetapi jika Anda sudah
memiliki [R](https://www.r-project.org/):

```bash
ssh myserver journalctl
 | grep sshd
 | grep "Disconnected from"
 | sed -E 's/.*Disconnected from (invalid |authenticating )?user (.*) [^ ]+ port [0-9]+( \[preauth\])?$/\2/'
 | sort | uniq -c
 | awk '{print $1}' | R --no-echo -e 'x <- scan(file="stdin", quiet=TRUE); summary(x)'
```

R adalah bahasa pemrograman lain (yang aneh) yang hebat dalam analisis data
dan [plotting](https://ggplot2.tidyverse.org/). Kami tidak akan membahas terlalu
detail, tetapi cukup dikatakan bahwa `summary` mencetak statistik ringkasan
untuk sebuah vektor, dan kita membuat vektor yang memuat aliran input
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
sejauh ini + `xargs` bisa menjadi kombinasi yang kuat.

Misalnya, seperti yang terlihat di kuliah, saya dapat menggunakan perintah berikut untuk meng-uninstall
build nightly lama Rust dari sistem saya dengan mengekstrak nama build lama
menggunakan tool data wrangling lalu meneruskannya melalui `xargs` ke
uninstaller:

```bash
rustup toolchain list | grep nightly | grep -vE "nightly-x86" | sed 's/-x86.*//' | xargs rustup toolchain uninstall
```

## Wrangling data biner

Sejauh ini, kita sebagian besar membahas wrangling data tekstual, tetapi pipe
sama bergunanya untuk data biner. Misalnya, kita dapat menggunakan ffmpeg untuk
mengambil gambar dari kamera, mengonversinya ke grayscale, mengompresnya,
mengirimnya ke mesin jarak jauh melalui SSH, mendekompresnya di sana, membuat salinan,
dan kemudian menampilkannya.

```bash
ffmpeg -loglevel panic -i /dev/video0 -frames 1 -f image2 -
 | convert - -colorspace gray -
 | gzip
 | ssh mymachine 'gzip -d | tee copy.jpg | env DISPLAY=:0 feh -'
```

# Latihan

1. Ikuti [tutorial regex interaktif singkat](https://regexone.com/) ini.
2. Temukan jumlah kata (di `/usr/share/dict/words`) yang memuat setidaknya
   tiga huruf `a` dan tidak berakhiran `'s`. Apa tiga
   dua huruf terakhir yang paling umum dari kata-kata tersebut? Perintah `y` pada `sed`, atau
   program `tr`, mungkin membantu Anda dengan ketidakpekaan huruf besar-kecil. Berapa banyak
   kombinasi dua huruf tersebut yang ada? Dan sebagai tantangan:
   kombinasi mana yang tidak muncul?
3. Untuk melakukan substitusi in-place, cukup menggoda untuk melakukan sesuatu seperti
   `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`. Namun ini
   ide buruk, mengapa? Apakah ini khusus untuk `sed`? Gunakan `man sed` untuk mencari tahu
   cara melakukannya.
4. Temukan rata-rata, median, dan waktu boot sistem maksimum Anda selama sepuluh
   boot terakhir. Gunakan `journalctl` di Linux dan `log show` di macOS, dan cari
   timestamp log di dekat awal dan akhir setiap boot. Di Linux,
   mungkin terlihat seperti:
   ```
   Logs begin at ...
   ```
   dan
   ```
   systemd[577]: Startup finished in ...
   ```
   Di macOS, [cari
   ini](https://eclecticlight.co/2018/03/21/macos-unified-log-3-finding-your-way/):
   ```
   === system boot:
   ```
   dan
   ```
   Previous shutdown cause: 5
   ```
5. Cari pesan boot yang _tidak_ sama di antara tiga
   reboot terakhir Anda (lihat flag `-b` milik `journalctl`). Pecah tugas ini menjadi
   beberapa langkah. Pertama, temukan cara untuk memperoleh hanya log dari tiga
   boot terakhir. Mungkin ada flag yang berlaku pada tool yang Anda gunakan untuk
   mengekstrak log boot, atau Anda dapat menggunakan `sed '0,/STRING/d'` untuk menghapus
   semua baris sebelum baris yang cocok dengan `STRING`. Selanjutnya, hapus bagian
   baris yang _selalu_ berubah (seperti timestamp). Lalu,
   de-duplikasi baris input dan simpan hitungan masing-masing (`uniq` adalah
   teman Anda). Dan akhirnya, hilangkan baris yang hitungannya 3 (karena
   baris itu _memang_ sama di semua boot).
6. Temukan dataset daring seperti [ini](https://commons.wikimedia.org/wiki/Data:Wikipedia_statistics/data.tab), [ini](https://ucr.fbi.gov/crime-in-the-u.s/2016/crime-in-the-u.s.-2016/topic-pages/tables/table-1),
   atau mungkin satu [dari
   sini](https://www.springboard.com/blog/data-science/free-public-data-sets-data-science-project/).
   Ambil dengan `curl` dan ekstrak hanya dua kolom data
   numerik. Jika Anda mengambil data HTML,
   [`pup`](https://github.com/EricChiang/pup) mungkin berguna. Untuk data JSON,
   coba [`jq`](https://stedolan.github.io/jq/). Temukan min dan
   max satu kolom dalam satu perintah, dan selisih jumlah
   setiap kolom dalam perintah lain.
