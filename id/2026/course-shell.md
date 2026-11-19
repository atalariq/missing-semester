---
layout: lecture-id
title: "Gambaran Kursus + Pengantar Shell"
description: >
  Pelajari alasan di balik kelas ini dan mulai menggunakan shell.
thumbnail: /static/assets/thumbnails/2026/lec1.png
date: 2026-01-12
ready: true
video:
  aspect: 56.25
  id: MSgoeuMqUmU
lang: id
permalink: /id/2026/course-shell/
---

# Siapa kami?

Kelas ini diajar bersama oleh [Anish](https://anish.io/),
[Jon](https://thesquareplanet.com/), dan [Jose](http://josejg.com/). Kami
semua adalah mantan mahasiswa MIT yang memulai kelas MIT IAP ini ketika
kami masih menjadi mahasiswa. Anda dapat menghubungi kami bersama-sama di
[missing-semester@mit.edu](mailto:missing-semester@mit.edu).

Kami tidak dibayar untuk mengajar kelas ini, dan tidak memonetisasi kelas
ini dengan cara apa pun. Kami menyediakan semua [materi
kursus](https://missing.csail.mit.edu/) dan [rekaman
kuliah](https://www.youtube.com/@MissingSemester) secara bebas di
internet. Jika Anda ingin mendukung pekerjaan kami, cara terbaik adalah
dengan menyebarkan kabar tentang kelas ini. Jika Anda berasal dari
perusahaan, universitas, atau organisasi lain yang menjalankan konten ini
untuk kelompok yang lebih besar, silakan kirimkan laporan pengalaman/testimoni
kepada kami melalui email agar kami dapat mendengarnya :)

# Motivasi

Sebagai ilmuwan komputer, kita tahu bahwa komputer sangat baik dalam
membantu tugas-tugas yang berulang. Namun, terlalu sering kita lupa bahwa
hal ini juga berlaku sama besar pada _penggunaan_ komputer oleh kita,
sebagaimana pada komputasi yang ingin dijalankan program kita. Ada
berbagai macam tool yang tersedia di ujung jari kita sehingga kita dapat
lebih produktif dan menyelesaikan masalah yang lebih kompleks saat
mengerjakan masalah apa pun yang berkaitan dengan komputer. Namun banyak
dari kita hanya memanfaatkan sebagian kecil dari tool tersebut; kita hanya
mengetahui secukupnya mantra ajaib secara hafalan agar bisa bertahan, dan
menyalin-tempel perintah dari internet secara buta ketika kita macet.

Kelas ini merupakan upaya untuk [menjawab hal ini](/about/).

Kami ingin mengajarkan kepada Anda cara memanfaatkan tool yang sudah Anda
kenal sebaik mungkin, menunjukkan tool baru untuk menambah perangkat Anda,
dan semoga menumbuhkan sedikit kegembiraan dalam menjelajahi (dan mungkin
membangun) tool Anda sendiri. Inilah yang kami yakini sebagai semester
yang hilang dari sebagian besar kurikulum Ilmu Komputer.

# Struktur kelas

Kelas tanpa kredit ini terdiri dari sembilan kuliah berdurasi 1 jam, masing-masing
berpusat pada [topik tertentu](/2026/). Kuliah-kuliah tersebut sebagian besar
independen, meskipun seiring berjalannya semester kami akan menganggap Anda
sudah familiar dengan materi dari kuliah sebelumnya. Kami memiliki catatan
kuliah daring, tetapi mungkin ada materi yang dibahas di kelas (misalnya
dalam bentuk demo) yang tidak ada dalam catatan. Seperti tahun-tahun
sebelumnya, kami akan merekam kuliah dan mengunggah rekamannya
[secara daring](https://www.youtube.com/@MissingSemester).

Kami mencoba mencakup banyak materi dalam beberapa kuliah 1 jam saja,
sehingga kuliahnya cukup padat. Untuk memberi Anda waktu mengenal materinya
sesuai kecepatan Anda sendiri, setiap kuliah menyertakan serangkaian latihan
yang menuntun Anda melalui poin-poin kunci kuliah tersebut. Kami tidak akan
mengadakan office hours khusus, tetapi kami mendorong Anda untuk mengajukan
pertanyaan di [OSSU Discord](https://ossu.dev/#community), di
`#missing-semester-forum`, atau mengirim email ke kami di
[missing-semester@mit.edu](mailto:missing-semester@mit.edu).

Karena waktu kami terbatas, kami tidak akan dapat membahas semua tool
dengan tingkat detail seperti kelas berskala penuh. Bila memungkinkan, kami
akan berusaha mengarahkan Anda ke sumber daya untuk menyelami lebih jauh
suatu tool atau topik, tetapi jika ada sesuatu yang sangat menarik bagi
Anda, jangan ragu menghubungi kami dan meminta petunjuk!

Terakhir, jika Anda memiliki umpan balik tentang kelas ini, silakan kirim
melalui email ke [missing-semester@mit.edu](mailto:missing-semester@mit.edu).

# Topik 1: The Shell

{% comment %}
lecturer: Jon
{% endcomment %}

## Apa itu shell?

Komputer saat ini memiliki berbagai antarmuka untuk memberikan perintah;
antarmuka pengguna grafis yang beragam, antarmuka suara, AR/VR, dan yang
lebih baru: LLM. Semua itu bagus untuk 80% use case, tetapi sering kali
secara mendasar terbatas dalam hal yang memungkinkan Anda lakukan — Anda
tidak dapat menekan tombol yang tidak ada atau memberikan perintah suara
yang belum diprogram. Untuk memanfaatkan sepenuhnya tool yang disediakan
komputer Anda, kita harus kembali ke cara lama dan turun ke antarmuka
tekstual: The Shell.

Hampir semua platform yang dapat Anda peroleh memiliki shell dalam satu
bentuk atau lainnya, dan banyak di antaranya memiliki beberapa shell yang
dapat Anda pilih. Meskipun detailnya bisa berbeda-beda, pada intinya semua
shell kurang lebih sama: shell memungkinkan Anda menjalankan program,
memberinya input, dan memeriksa outputnya secara semi-terstruktur.

Untuk membuka _prompt_ shell (tempat Anda dapat mengetik perintah), Anda
terlebih dahulu memerlukan _terminal_, yaitu antarmuka visual ke sebuah
shell. Perangkat Anda kemungkinan sudah dilengkapi dengan terminal, atau
Anda dapat memasangnya dengan cukup mudah:

- **Linux:**
  Tekan `Ctrl + Alt + T` (berfungsi pada sebagian besar distribusi). Atau cari
  "Terminal" di menu aplikasi Anda.
- **Windows:**
  Tekan `Win + R`, ketik `cmd` atau `powershell`, lalu tekan Enter.
  Alternatifnya, cari "Terminal" atau "Command Prompt" di menu Start.
- **macOS:**
  Tekan `Cmd + Space` untuk membuka Spotlight, ketik "Terminal", lalu tekan Enter.
  Atau temukan di Applications → Utilities → Terminal.

Di Linux dan macOS, ini biasanya akan membuka Bourne Again SHell, atau
singkatnya "bash". Ini adalah salah satu shell yang paling banyak digunakan,
dan sintaksnya mirip dengan yang akan Anda lihat di banyak shell lain. Di
Windows, Anda akan disambut oleh shell "batch" atau "powershell", tergantung
perintah yang Anda jalankan. Keduanya khas Windows, dan bukan yang akan kami
fokuskan di kelas ini, meskipun ada padanannya untuk sebagian besar materi
yang akan kami ajarkan. Anda sebaiknya menggunakan [Windows Subsystem for
Linux](https://docs.microsoft.com/en-us/windows/wsl/) atau Linux virtual
machine.

Shell lain ada, sering kali dengan banyak peningkatan ergonomis dibandingkan
bash (fish dan zsh termasuk yang paling umum). Meskipun sangat populer
(semua pengajar menggunakan salah satunya), shell tersebut jauh dari
sepopuler bash, dan bertumpu pada banyak konsep yang sama, sehingga kami
tidak akan memfokuskannya pada kuliah ini.

## Mengapa Anda harus peduli dengan shell?

Shell bukan hanya (biasanya) jauh lebih cepat daripada "mengklik sana-sini",
tetapi juga hadir dengan kekuatan ekspresif yang tidak mudah Anda temukan di
satu program grafis mana pun. Seperti yang akan kita lihat, shell memberi
Anda kemampuan untuk _menggabungkan_ program secara kreatif untuk
mengotomatiskan hampir semua tugas.

Mengetahui seluk-beluk shell juga sangat berguna untuk menavigasi dunia
perangkat lunak open-source (yang sering kali menyertakan instruksi
pemasangan yang memerlukan shell), membangun continuous integration untuk
proyek perangkat lunak Anda (seperti dijelaskan pada [kuliah Code
Quality](/2026/code-quality/)), dan men-debug error ketika program lain
gagal.

## Bernavigasi di shell

Saat Anda membuka terminal, Anda akan melihat sebuah _prompt_ yang sering
kali terlihat seperti ini:

```console
missing:~$
```

Ini adalah antarmuka tekstual utama ke shell. Prompt ini memberi tahu Anda
bahwa Anda berada di mesin `missing` dan bahwa "current working directory"
Anda, atau tempat Anda saat ini, adalah `~` (singkatan dari "home"). Tanda
`$` memberi tahu bahwa Anda bukan pengguna root (lebih lanjut nanti). Pada
prompt ini Anda dapat mengetik sebuah _command_, yang kemudian akan
diinterpretasikan oleh shell. Perintah paling dasar adalah menjalankan
sebuah program:

```console
missing:~$ date
Fri 10 Jan 2020 11:49:31 AM EST
missing:~$
```

Di sini, kita menjalankan program `date`, yang (mungkin tidak mengherankan)
mencetak tanggal dan waktu saat ini. Shell lalu meminta kita memberikannya
perintah lain untuk dijalankan. Kita juga dapat menjalankan perintah dengan
_argument_:

```console
missing:~$ echo hello
hello
```

Dalam kasus ini, kita meminta shell menjalankan program `echo` dengan
argumen `hello`. Program `echo` sekadar mencetak argumennya. Shell mengurai
perintah dengan memisahkannya berdasarkan whitespace, lalu menjalankan
program yang ditunjukkan oleh kata pertama, dengan setiap kata berikutnya
diberikan sebagai argumen yang dapat diakses program. Jika Anda ingin
memberikan argumen yang memuat spasi atau karakter khusus lain (misalnya,
direktori bernama "My Photos"), Anda dapat mengapit argumen dengan `'` atau
`"` (`"My Photos"`), atau meng-escape hanya karakter yang relevan dengan `\`
(`My\ Photos`).

Mungkin perintah terpenting saat Anda memulai adalah `man`, singkatan dari
"manual". Program `man`, antara lain, memungkinkan Anda mencari informasi
lebih lanjut tentang perintah apa pun di sistem Anda. Misalnya, jika Anda
menjalankan `man date`, program itu akan menjelaskan apa itu `date`, dan
semua berbagai argumen yang dapat Anda berikan untuk mengubah perilakunya.
Anda juga biasanya dapat memperoleh versi singkat bantuan dengan memberikan
`--help` sebagai argumen pada sebagian besar perintah.

> Pertimbangkan memasang dan menggunakan [`tldr`](https://tldr.sh/) selain
> `man`, karena tool tersebut menampilkan contoh penggunaan umum langsung di
> terminal. LLM juga biasanya sangat baik dalam menjelaskan cara kerja
> perintah dan cara memanggilnya untuk mencapai tujuan Anda.

Setelah `man`, perintah terpenting untuk dipelajari adalah `cd`, atau "change
directory". Perintah ini sebenarnya dibangun ke dalam shell, dan bukan
program terpisah (yakni, `which cd` akan mengatakan "no cd found"). Anda
memberinya sebuah path, dan path tersebut menjadi current working directory
Anda. Anda juga akan melihat working directory tercermin pada prompt shell:

```console
missing:~$ cd /bin
missing:/bin$ cd /
missing:/$ cd ~
missing:~$
```

> Perhatikan bahwa shell dilengkapi auto-completion, sehingga Anda sering
> dapat melengkapi path lebih cepat dengan menekan `<TAB>`!

Banyak perintah beroperasi pada current working directory jika tidak ada
yang ditentukan. Jika Anda ragu di mana Anda berada, Anda dapat menjalankan
`pwd` atau mencetak environment variable `$PWD` (dengan `echo $PWD`),
keduanya menghasilkan current working directory.

Current working directory juga berguna karena memungkinkan kita menggunakan
path _relatif_. Semua path yang kita lihat sejauh ini bersifat
_absolut_ — path tersebut dimulai dengan `/` dan memberikan rangkaian
direktori lengkap yang diperlukan untuk menavigasi ke suatu lokasi dari root
file system (`/`). Dalam praktiknya, Anda akan lebih sering bekerja dengan
path relatif; disebut demikian karena relatif terhadap current working
directory. Pada path relatif (apa pun yang _tidak_ dimulai dengan `/`),
komponen path pertama dicari di current working directory, dan komponen
berikutnya ditelusuri seperti biasa. Contoh:

```console
missing:~$ cd /
missing:/$ cd bin
missing:/bin$
```

Ada juga dua komponen "khusus" yang ada di setiap direktori: `.` dan `..`.
`.` adalah "direktori ini", dan `..` adalah "direktori induk". Jadi:

```console
missing:~$ cd /
missing:/$ cd bin/../bin/../bin/././../bin/..
missing:/$
```

Anda biasanya dapat menggunakan path absolut dan relatif secara bergantian
untuk argumen perintah apa pun, cukup ingat current working directory Anda
saat menggunakan path relatif!

> Pertimbangkan memasang dan menggunakan
> [`zoxide`](https://github.com/ajeetdsouza/zoxide) untuk mempercepat
> `cd` Anda — `z` akan mengingat path yang sering Anda kunjungi dan
> memungkinkan Anda mengaksesnya dengan lebih sedikit pengetikan.

## Apa saja yang tersedia di shell?

Tetapi bagaimana shell mengetahui cara menemukan program seperti `date` atau
`echo`? Jika shell diminta menjalankan sebuah perintah, shell mengonsultasikan
sebuah _environment variable_ bernama `$PATH` yang mencantumkan direktori
mana yang harus dicari shell untuk program ketika diberikan sebuah perintah:

```console
missing:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
missing:~$ which echo
/bin/echo
missing:~$ /bin/echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
```

Ketika kita menjalankan perintah `echo`, shell melihat bahwa ia harus
menjalankan program `echo`, lalu menelusuri daftar direktori yang dipisahkan
`:` di `$PATH` untuk mencari berkas dengan nama tersebut. Ketika menemukannya,
shell menjalankannya (dengan asumsi berkas tersebut _executable_; lebih
lanjut nanti). Kita dapat mengetahui berkas mana yang dijalankan untuk nama
program tertentu menggunakan program `which`. Kita juga dapat melewati
`$PATH` sepenuhnya dengan memberikan _path_ ke berkas yang ingin kita
jalankan.

Ini juga memberi petunjuk bagaimana kita dapat menentukan _semua_ program
yang dapat kita jalankan di shell: dengan mencantumkan isi semua direktori
pada `$PATH`. Kita dapat melakukannya dengan memberikan path direktori
tertentu ke program `ls`, yang mencantumkan berkas:

```console
missing:~$ ls /bin
```

> Pertimbangkan memasang dan menggunakan [`eza`](https://eza.rocks/) untuk
> `ls` yang lebih ramah manusia.

Ini akan, pada sebagian besar komputer, mencetak _banyak_ program, tetapi di
sini kita hanya akan memfokuskan pada beberapa yang paling penting. Pertama,
beberapa yang sederhana:

- `cat file`, yang mencetak isi `file`.
- `sort file`, yang mencetak baris-baris `file` dalam urutan terurut.
- `uniq file`, yang menghilangkan baris duplikat berurutan dari `file`.
- `head file` dan `tail file`, yang masing-masing mencetak beberapa baris
  pertama dan terakhir `file`.

> Pertimbangkan memasang dan menggunakan [`bat`](https://github.com/sharkdp/bat)
> sebagai pengganti `cat` untuk syntax highlighting dan scrolling.

Ada juga `grep pattern file`, yang mencari baris yang cocok dengan `pattern`
di `file`. Yang ini layak mendapat perhatian sedikit lebih banyak karena
_sangat_ berguna dan menyediakan rangkaian fitur yang lebih luas daripada yang
mungkin Anda duga. `pattern` sebenarnya adalah sebuah _regular expression_
yang dapat mengekspresikan pola yang sangat kompleks — kita akan [membahasnya](/2026/code-quality/#regular-expressions)
pada kuliah code quality. Anda juga dapat menentukan sebuah direktori
sebagai pengganti berkas (atau membiarkannya kosong untuk `.`) dan
memberikan `-r` untuk mencari secara rekursif di semua berkas dalam
direktori tersebut.

> Pertimbangkan memasang dan menggunakan
> [`ripgrep`](https://github.com/BurntSushi/ripgrep) sebagai pengganti `grep`
> untuk alternatif yang lebih cepat dan lebih ramah manusia (tetapi kurang
> portabel). `ripgrep` juga akan mencari secara rekursif di current working
> directory secara default!

Ada juga beberapa tool yang sangat berguna dengan antarmuka yang sedikit
lebih rumit. Yang pertama di antaranya adalah `sed`, yaitu editor berkas
programatik. Tool ini memiliki bahasa pemrogramannya sendiri untuk membuat
pengeditan berkas secara otomatis, tetapi penggunaan paling umumnya adalah:

```console
missing:~$ sed -i 's/pattern/replacement/g' file
```

Ini mengganti semua kemunculan `pattern` dengan `replacement` di `file`.
Opsi `-i` menunjukkan bahwa kita ingin substitusi terjadi secara inline
(berbeda dengan membiarkan `file` tidak berubah dan mencetak isi hasil
substitusi). `s/` adalah cara mengekspresikan dalam bahasa pemrograman sed
bahwa kita ingin melakukan substitusi. Tanda `/` memisahkan pola dari
penggantinya. Dan `/g` di akhir menunjukkan bahwa kita ingin mengganti
_semua_ kemunculan pada setiap baris, bukan hanya yang pertama. Seperti pada
`grep`, `pattern` di sini adalah sebuah regular expression, yang memberi Anda
kekuatan ekspresif signifikan. Substitusi regular expression juga
memungkinkan `replacement` merujuk kembali ke bagian dari pola yang cocok;
kita akan melihat contohnya sebentar lagi.

Berikutnya, ada `find`, yang memungkinkan Anda menemukan berkas (secara
rekursif) yang memenuhi kondisi tertentu. Misalnya:

```console
missing:~$ find ~/Downloads -type f -name "*.zip" -mtime +30
```

Menemukan berkas ZIP di direktori unduhan yang lebih lama dari 30 hari.

```console
missing:~$ find ~ -type f -size +100M -exec ls -lh {} \;
```

Menemukan berkas yang lebih besar dari 100M di direktori home Anda dan
mencantumkannya. Perhatikan bahwa `-exec` menerima sebuah _command_ yang
diakhiri dengan `;` yang berdiri sendiri (yang perlu kita escape seperti
halnya spasi), di mana `{}` digantikan oleh setiap path berkas yang cocok
oleh `find`.

```console
missing:~$ find . -name "*.py" -exec grep -l "TODO" {} \;
```

Menemukan berkas `.py` apa pun yang memuat item TODO di dalamnya.

Sintaks `find` bisa sedikit menakutkan, tetapi semoga ini memberi Anda
gambaran betapa bergunanya tool tersebut!

> Pertimbangkan memasang dan menggunakan [`fd`](https://github.com/sharkdp/fd)
> sebagai pengganti `find` untuk pengalaman yang lebih ramah manusia (tetapi
> kurang portabel!).

Berikutnya dalam daftar adalah `awk`, yang, seperti `sed`, memiliki bahasa
pemrogramannya sendiri. Jika `sed` dirancang untuk mengedit berkas, `awk`
dirancang untuk mengurainya. Penggunaan `awk` yang paling umum sejauh ini
adalah untuk berkas data dengan sintaks teratur (seperti berkas CSV) di mana
Anda ingin mengekstrak hanya bagian tertentu dari setiap record (yakni,
baris):

```console
missing:~$ awk '{print $2}' file
```

Mencetak kolom kedua yang dipisahkan whitespace dari setiap baris `file`.
Jika Anda menambahkan `-F,`, tool ini akan mencetak kolom kedua yang
dipisahkan koma dari setiap baris. `awk` dapat melakukan jauh lebih banyak —
memfilter baris, menghitung agregat, dan lainnya — lihat latihan untuk
mencicipinya.

Dengan menggabungkan tool-tool ini, kita dapat melakukan hal-hal mewah
seperti:

```console
missing:~$ ssh myserver 'journalctl -u sshd -b-1 | grep "Disconnected from"' \
  | sed -E 's/.*Disconnected from .* user (.*) [^ ]+ port.*/\1/' \
  | sort | uniq -c \
  | sort -nk1,1 | tail -n10 \
  | awk '{print $2}' | paste -sd,
postgres,mysql,oracle,dell,ubuntu,inspur,test,admin,user,root
```

Perintah ini mengambil log SSH dari server jarak jauh (kita akan membahas
lebih banyak tentang `ssh` pada kuliah berikutnya), mencari pesan
disconnect, mengekstrak username dari setiap pesan tersebut, dan mencetak 10
username teratas yang dipisahkan koma. Semuanya dalam satu perintah! Kami
serahkan pembedahan setiap langkahnya sebagai latihan.

## Bahasa shell (bash)

Contoh sebelumnya memperkenalkan konsep baru: pipe (`|`). Pipe memungkinkan
Anda merangkai output satu program dengan input program lain. Ini berfungsi
karena sebagian besar program command-line akan beroperasi pada "standard
input"-nya (tempat ketikan Anda biasanya masuk) jika tidak ada argumen
`file` yang diberikan. `|` mengambil "standard output" (yang biasanya
dicetak ke terminal Anda) dari program sebelum `|` dan menjadikannya
standard input program setelah `|`. Ini memungkinkan Anda _menyusun_
program shell, dan inilah bagian dari alasan shell menjadi lingkungan kerja
yang sangat produktif!

Bahkan, sebagian besar shell mengimplementasikan bahasa pemrograman penuh
(seperti bash), sama seperti Python atau Ruby. Bahasa tersebut memiliki
variabel, kondisional, loop, dan fungsi. Ketika Anda menjalankan perintah di
shell Anda, Anda sebenarnya menulis sedikit kode yang diinterpretasikan oleh
shell Anda. Kami tidak akan mengajarkan seluruh bash hari ini, tetapi ada
beberapa bagian yang akan sangat berguna bagi Anda:

Pertama, redirect: `>file` memungkinkan Anda mengambil standard output
sebuah program dan menuliskannya ke `file` alih-alih ke terminal Anda. Ini
mempermudah analisis setelahnya. `>>file` akan menambahkan ke `file` alih-alih
menimpanya. Ada juga `<file` yang memberi tahu shell untuk membaca dari
`file` alih-alih dari keyboard Anda sebagai standard input sebuah program.

> Ini saat yang tepat untuk menyebutkan program `tee`. `tee` akan mencetak
> standard input ke standard output (sama seperti `cat`!), tetapi _juga_
> menuliskannya ke sebuah berkas. Jadi `verbose cmd | tee verbose.log | grep CRITICAL`
> akan menyimpan log verbose lengkap ke berkas sambil menjaga terminal Anda
> tetap bersih!

Berikutnya, kondisional: `if command1; then command2; command3; fi` akan
menjalankan `command1`, dan jika tidak menghasilkan error, akan menjalankan
`command2` dan `command3`. Anda juga dapat memiliki cabang `else` jika
diinginkan. Perintah yang paling umum digunakan sebagai `command1` adalah
perintah `test`, yang sering disingkat menjadi `[`, yang memungkinkan Anda
mengevaluasi kondisi seperti "apakah sebuah berkas ada" (`test -f file` /
`[ -f file ]`) atau "apakah sebuah string sama dengan yang lain"
(`[ "$var" = "string" ]`). Di bash, ada juga `[[ ]]`, yang merupakan versi
bawaan `test` yang "lebih aman" dan memiliki lebih sedikit perilaku aneh
terkait quoting.

Bash juga memiliki dua bentuk loop, `while` dan `for`. `while command1; do
command2; command3; done` berfungsi persis seperti perintah `if` yang setara,
kecuali bahwa loop tersebut akan mengeksekusi keseluruhan blok berulang kali
selama `command1` tidak menghasilkan error. `for varname in a b c d; do
command; done` mengeksekusi `command` empat kali, masing-masing dengan
`$varname` disetel ke salah satu dari `a`, `b`, `c`, dan `d`. Daripada
mencantumkan item secara eksplisit, Anda akan sering menggunakan "command
substitution", seperti:

```bash
for i in $(seq 1 10); do
```

Ini mengeksekusi perintah `seq 1 10` (yang mencetak angka 1 sampai 10
inklusif) lalu mengganti seluruh `$()` dengan output perintah tersebut,
sehingga Anda memperoleh loop for dengan 10 iterasi. Pada kode lama Anda
kadang akan melihat backtick literal (seperti ``for i in `seq 1 10`; do``)
sebagai pengganti `$()`, tetapi Anda sebaiknya sangat mengutamakan bentuk
`$()` karena bentuk tersebut dapat disarangkan.

Meskipun Anda _dapat_ menulis skrip shell panjang langsung di prompt Anda,
Anda biasanya ingin menuliskannya ke berkas `.sh`. Misalnya, berikut adalah
skrip yang akan menjalankan sebuah program dalam loop sampai gagal,
mencetak output hanya dari eksekusi yang gagal, sambil membebani CPU Anda di
latar belakang (berguna untuk mereproduksi flaky test, misalnya):

```bash
#!/bin/bash
set -euo pipefail

# Start CPU stress in background
stress --cpu 8 &
STRESS_PID=$!

# Setup log file
LOGFILE="test_runs_$(date +%s).log"
echo "Logging to $LOGFILE"

# Run tests until one fails
RUN=1
while cargo test my_test > "$LOGFILE" 2>&1; do
    echo "Run $RUN passed"
    ((RUN++))
done

# Cleanup and report
kill $STRESS_PID
echo "Test failed on run $RUN"
echo "Last 20 lines of output:"
tail -n 20 "$LOGFILE"
echo "Full log: $LOGFILE"
```

Di dalamnya ada sejumlah hal baru yang saya sarankan Anda luangkan waktu
untuk menyelaminya, karena hal-hal tersebut sangat berguna dalam menyusun
pemanggilan shell yang bermanfaat seperti background job (`&`) untuk
menjalankan program secara bersamaan, [shell
redirection](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)
yang lebih rumit, dan [arithmetic
expansion](https://www.gnu.org/software/bash/manual/html_node/Arithmetic-Expansion.html).

Namun ada baiknya kita membahas sejenak dua baris pertama program tersebut.
Baris pertama adalah "shebang" — Anda juga akan melihat ini di bagian atas
berkas selain skrip shell. Ketika sebuah berkas yang dimulai dengan mantra
ajaib `#!/path` dieksekusi, shell akan menjalankan program di `/path`, dan
memberikannya isi berkas sebagai input. Dalam kasus skrip shell, ini berarti
memberikan isi skrip shell ke `/bin/bash`, tetapi Anda juga dapat menulis
skrip Python dengan baris shebang `/usr/bin/python`!

Baris kedua adalah cara membuat bash "lebih ketat", dan mengurangi sejumlah
jebakan saat menulis skrip shell. `set` dapat menerima banyak argumen,
tetapi secara singkat: `-e` membuat skrip keluar lebih awal jika ada
perintah yang gagal; `-u` membuat penggunaan variabel yang tidak
terdefinisi menghentikan skrip, alih-alih hanya menggunakan string kosong;
dan `-o
pipefail` membuat skrip shell secara keseluruhan juga keluar lebih
awal jika program dalam rangkaian `|` gagal.

> Pemrograman shell adalah topik yang mendalam, sama seperti bahasa
> pemrograman apa pun, tetapi perlu diwaspadai: bash memiliki jumlah
> jebakan yang tidak biasa banyaknya, sampai-sampai ada [beberapa
> situs web](https://tldp.org/LDP/abs/html/gotchas.html) yang didedikasikan
> untuk [mencantumkannya](https://mywiki.wooledge.org/BashPitfalls). Saya
> sangat menyarankan memanfaatkan [shellcheck](https://www.shellcheck.net/)
> secara intensif saat menulisnya. LLM juga hebat dalam menulis dan
> men-debug skrip shell, serta menerjemahkannya ke bahasa pemrograman
> "sungguhan" (seperti Python) ketika skrip tersebut sudah terlalu berat
> untuk bash (100+ baris).

# Langkah selanjutnya

Pada titik ini Anda sudah cukup mengenal shell untuk menyelesaikan tugas
dasar. Anda seharusnya sudah dapat bernavigasi untuk menemukan berkas yang
diminati dan menggunakan fungsionalitas dasar sebagian besar program. Pada
kuliah berikutnya, kita akan membahas cara melakukan dan mengotomatiskan
tugas yang lebih kompleks menggunakan shell dan banyak program command-line
praktis yang tersedia.

# Latihan

Semua kelas dalam kursus ini disertai dengan serangkaian latihan. Sebagian
memberi Anda tugas spesifik untuk dikerjakan, sementara yang lain bersifat
terbuka, seperti "coba gunakan program X dan Y". Kami sangat mendorong Anda
untuk mencobanya.

Kami belum menulis solusi untuk latihan-latihan ini. Jika Anda macet pada
hal tertentu, silakan berbagi di `#missing-semester-forum` pada
[Discord](https://ossu.dev/#community) atau kirim email kepada kami yang
menjelaskan apa yang telah Anda coba sejauh ini, dan kami akan berusaha
membantu. Latihan-latihan ini juga kemungkinan akan berfungsi baik sebagai
prompt awal dalam percakapan dengan LLM di mana Anda dapat menyelami topiknya
secara interaktif. Nilai nyata dalam latihan ini adalah perjalanan menemukan
jawabannya, bukan jawabannya sendiri. Kami mendorong Anda untuk mengikuti
jalan samping dan bertanya "mengapa" saat mengerjakannya, alih-alih sekadar
mencari jalan terpendek menuju solusi.

1. Untuk kursus ini, Anda perlu menggunakan Unix shell seperti Bash atau ZSH. Jika
   Anda menggunakan Linux atau macOS, Anda tidak perlu melakukan hal khusus. Jika
   Anda menggunakan Windows, Anda perlu memastikan Anda tidak menjalankan cmd.exe atau
   PowerShell; Anda dapat menggunakan [Windows Subsystem for
   Linux](https://docs.microsoft.com/en-us/windows/wsl/) atau Linux virtual
   machine untuk menggunakan tool command-line bergaya Unix. Untuk memastikan Anda menjalankan
   shell yang sesuai, Anda dapat mencoba perintah `echo $SHELL`. Jika hasilnya
   seperti `/bin/bash` atau `/usr/bin/zsh`, itu berarti Anda menjalankan
   program yang benar.

1. Apa fungsi flag `-l` pada `ls`? Jalankan `ls -l /` dan periksa outputnya.
   Apa arti 10 karakter pertama setiap baris? (Petunjuk: `man ls`)

1. Pada perintah `find ~/Downloads -type f -name "*.zip" -mtime +30`,
   `*.zip` adalah sebuah "glob". Apa itu glob? Buat direktori uji dengan beberapa
   berkas dan bereksperimenlah dengan pola seperti `ls *.txt`, `ls file?.txt`, dan
   `ls {a,b,c}.txt`. Lihat [Pattern
   Matching](https://www.gnu.org/software/bash/manual/html_node/Pattern-Matching.html)
   di manual Bash.

1. Apa perbedaan antara `'single quotes'`, `"double quotes"`, dan
   `$'ANSI quotes'`? Tulis perintah yang mencetak string yang memuat
   `$` literal, sebuah `!`, dan karakter newline. Lihat
   [Quoting](https://www.gnu.org/software/bash/manual/html_node/Quoting.html).

1. Shell memiliki tiga standard stream: stdin (0), stdout (1), dan stderr
   (2). Jalankan `ls /nonexistent /tmp` dan redirect stdout ke satu berkas dan
   stderr ke berkas lain. Bagaimana Anda me-redirect keduanya ke berkas yang sama? Lihat
   [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html).

1. `$?` menyimpan exit status perintah terakhir (0 = sukses). `&&` menjalankan
   perintah berikutnya hanya jika perintah sebelumnya berhasil; `||` menjalankannya hanya jika
   perintah sebelumnya gagal. Tulis one-liner yang membuat `/tmp/mydir` hanya jika
   direktori itu belum ada. Lihat [Exit
   Status](https://www.gnu.org/software/bash/manual/html_node/Exit-Status.html).

1. Mengapa `cd` harus dibuat sebagai bawaan shell itu sendiri dan bukan
   program terpisah? (Petunjuk: pikirkan tentang apa yang dapat dan tidak dapat
   dipengaruhi child process pada parent-nya.)

1. Tulis skrip yang menerima nama berkas sebagai argumen (`$1`) dan memeriksa
   apakah berkas tersebut ada menggunakan `test -f` atau `[ -f ... ]`. Skrip harus mencetak
   pesan yang berbeda tergantung apakah berkas tersebut ada. Lihat [Bash
   Conditional
   Expressions](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html).

1. Simpan skrip dari latihan sebelumnya ke sebuah berkas (misalnya, `check.sh`).
   Coba jalankan dengan `./check.sh somefile`. Apa yang terjadi? Sekarang jalankan
   `chmod +x check.sh` dan coba lagi. Mengapa langkah ini diperlukan? (Petunjuk:
   lihat `ls -l check.sh` sebelum dan sesudah `chmod`.)

1. Apa yang terjadi jika Anda menambahkan `-x` pada flag `set` di sebuah skrip? Coba dengan
    skrip sederhana dan amati outputnya. Lihat [The Set
    Builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html).

1. Tulis perintah yang menyalin berkas ke cadangan dengan tanggal hari ini pada
    nama berkasnya (misalnya, `notes.txt` → `notes_2026-01-12.txt`). (Petunjuk: `$(date
    +%Y-%m-%d)`). Lihat [Command
    Substitution](https://www.gnu.org/software/bash/manual/html_node/Command-Substitution.html).

1. Ubah skrip flaky test dari kuliah agar menerima perintah test
    sebagai argumen, bukan meng-hardcode `cargo test my_test`. (Petunjuk: `$1`
    atau `$@`). Lihat [Special
    Parameters](https://www.gnu.org/software/bash/manual/html_node/Special-Parameters.html).

1. Gunakan pipe untuk menemukan 5 ekstensi berkas paling umum di direktori home
    Anda. (Petunjuk: gabungkan `find`, `grep` atau `sed` atau `awk`, `sort`,
    `uniq -c`, dan `head`.)

1. `xargs` mengonversi baris dari stdin menjadi argumen perintah. Gunakan `find` dan
    `xargs` bersamaan (bukan `find -exec`) untuk menemukan semua berkas `.sh` di
    sebuah direktori dan menghitung baris masing-masing dengan `wc -l`. Bonus: buat agar
    perintah tersebut menangani nama berkas yang memuat spasi. (Petunjuk: `-print0` dan `-0`). Lihat `man
    xargs`.

1. Gunakan `curl` untuk mengambil HTML situs web kursus
    (`https://missing.csail.mit.edu/`) dan pipe ke `grep` untuk menghitung berapa
    banyak kuliah yang tercantum. (Petunjuk: cari pola yang muncul sekali
    per kuliah; gunakan `curl -s` untuk membisukan output progres.)

1. [`jq`](https://jqlang.github.io/jq/) adalah tool yang kuat untuk memproses
    data JSON. Ambil data contoh di
    `https://microsoftedge.github.io/Demos/json-dummy-data/64KB.json` dengan
    `curl` dan gunakan `jq` untuk mengekstrak hanya nama orang yang version-nya
    lebih besar dari 6. (Petunjuk: pipe ke `jq .` terlebih dahulu untuk melihat strukturnya;
    lalu coba `jq '.[] | select(...) | .name'`)

1. `awk` dapat memfilter baris berdasarkan nilai kolom dan memanipulasi output.
    Misalnya, `awk '$3 ~ /pattern/ {$4=""; print}'` mencetak hanya baris
    di mana kolom ketiga cocok dengan `pattern`, sambil menghilangkan kolom keempat.
    Tulis perintah `awk` yang mencetak hanya baris di mana kolom kedua
    lebih besar dari 100, dan menukar kolom pertama dan ketiga. Uji
    dengan: `printf 'a 50 x\nb 150 y\nc 200 z\n'`

1. Bedah pipeline log SSH dari kuliah: apa fungsi setiap langkah?
    Lalu bangun yang serupa untuk menemukan perintah shell yang paling sering Anda gunakan dari
    `~/.bash_history` (atau `~/.zsh_history`).
