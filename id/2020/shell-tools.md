---
layout: lecture-id
title: "Tool Shell dan Scripting"
description: >
  Pelajari cara menulis shell script dan menggunakan tool command-line yang andal.
thumbnail: /static/assets/thumbnails/2020/lec2.png
date: 2020-01-14
ready: true
video:
  aspect: 56.25
  id: kgII-YWo3Zw
lang: id
permalink: /id/2020/shell-tools/
---

Pada kuliah ini, kami akan menyajikan beberapa dasar penggunaan bash sebagai bahasa scripting beserta sejumlah shell tool yang mencakup beberapa tugas paling umum yang akan terus Anda lakukan di command line.

# Shell Scripting

Sejauh ini kita telah melihat cara mengeksekusi perintah di shell dan melakukan pipe di antaranya.
Namun, dalam banyak skenario Anda akan ingin menjalankan serangkaian perintah dan memanfaatkan ekspresi control flow seperti kondisional atau loop.

Shell script adalah langkah berikutnya dalam kompleksitas.
Sebagian besar shell memiliki bahasa scriptingnya sendiri dengan variabel, control flow, dan sintaksnya sendiri.
Yang membuat shell scripting berbeda dari bahasa pemrograman scripting lain adalah bahwa bahasa ini dioptimalkan untuk melakukan tugas-tugas terkait shell.
Dengan demikian, membuat pipeline perintah, menyimpan hasil ke berkas, dan membaca dari standard input adalah primitif dalam shell scripting, yang membuatnya lebih mudah digunakan daripada bahasa scripting serbaguna.
Untuk bagian ini kami akan memfokuskan pada bash scripting karena paling umum.

Untuk menetapkan variabel di bash, gunakan sintaks `foo=bar` dan akses nilai variabel dengan `$foo`.
Perhatikan bahwa `foo = bar` tidak akan berfungsi karena diinterpretasikan sebagai pemanggilan program `foo` dengan argumen `=` dan `bar`.
Secara umum, dalam skrip shell karakter spasi melakukan pemisahan argumen. Perilaku ini bisa membingungkan pada awalnya, jadi selalu perhatikan hal itu.

String di bash dapat didefinisikan dengan pembatas `'` dan `"`, tetapi keduanya tidak setara.
String yang dibatasi `'` adalah string literal dan tidak akan melakukan substitusi nilai variabel sedangkan string yang dibatasi `"` akan melakukannya.

```bash
foo=bar
echo "$foo"
# prints bar
echo '$foo'
# prints $foo
```

Seperti pada sebagian besar bahasa pemrograman, bash mendukung teknik control flow termasuk `if`, `case`, `while` dan `for`.
Demikian pula, `bash` memiliki fungsi yang menerima argumen dan dapat beroperasi dengannya. Berikut contoh fungsi yang membuat direktori dan melakukan `cd` ke dalamnya.


```bash
mcd () {
    mkdir -p "$1"
    cd "$1"
}
```

Di sini `$1` adalah argumen pertama skrip/fungsi.
Tidak seperti bahasa scripting lain, bash menggunakan berbagai variabel khusus untuk merujuk argumen, kode error, dan variabel relevan lainnya. Berikut daftar beberapa di antaranya. Daftar yang lebih komprehensif dapat ditemukan [di sini](https://tldp.org/LDP/abs/html/special-chars.html).
- `$0` - Nama skrip
- `$1` sampai `$9` - Argumen skrip. `$1` adalah argumen pertama dan seterusnya.
- `$@` - Semua argumen
- `$#` - Jumlah argumen
- `$?` - Return code perintah sebelumnya
- `$$` - Process identification number (PID) untuk skrip saat ini
- `!!` - Seluruh perintah terakhir, termasuk argumennya. Pola umum adalah menjalankan sebuah perintah yang kemudian gagal karena permission yang kurang; Anda dapat dengan cepat mengeksekusi ulang perintah tersebut dengan sudo dengan melakukan `sudo !!`
- `$_` - Argumen terakhir dari perintah terakhir. Jika Anda berada di shell interaktif, Anda juga dapat dengan cepat memperoleh nilai ini dengan mengetik `Esc` diikuti `.` atau `Alt+.`

Perintah sering mengembalikan output melalui `STDOUT`, error melalui `STDERR`, dan sebuah Return Code untuk melaporkan error dengan cara yang lebih ramah skrip.
Return code atau exit status adalah cara skrip/perintah berkomunikasi tentang bagaimana eksekusinya berjalan.
Nilai 0 biasanya berarti semuanya berjalan OK; apa pun yang berbeda dari 0 berarti terjadi error.

Exit code dapat digunakan untuk mengeksekusi perintah secara kondisional menggunakan `&&` (operator and) dan `||` (operator or), keduanya merupakan operator [short-circuiting](https://en.wikipedia.org/wiki/Short-circuit_evaluation). Perintah juga dapat dipisahkan dalam baris yang sama menggunakan titik koma `;`.
Program `true` akan selalu memiliki return code 0 dan perintah `false` akan selalu memiliki return code 1.
Mari lihat beberapa contoh

```bash
false || echo "Oops, fail"
# Oops, fail

true || echo "Will not be printed"
#

true && echo "Things went well"
# Things went well

false && echo "Will not be printed"
#

true ; echo "This will always run"
# This will always run

false ; echo "This will always run"
# This will always run
```

Pola umum lain adalah ingin memperoleh output sebuah perintah sebagai variabel. Ini dapat dilakukan dengan _command substitution_.
Setiap kali Anda menempatkan `$( CMD )` ia akan mengeksekusi `CMD`, memperoleh output perintah dan menggantikannya di tempat tersebut.
Misalnya, jika Anda melakukan `for file in $(ls)`, shell akan terlebih dahulu memanggil `ls` lalu mengiterasi nilai-nilai tersebut.
Fitur serupa yang kurang dikenal adalah _process substitution_, `<( CMD )` akan mengeksekusi `CMD` dan menempatkan outputnya dalam berkas sementara serta mengganti `<()` dengan nama berkas tersebut. Ini berguna ketika perintah mengharapkan nilai diberikan melalui berkas alih-alih melalui STDIN. Misalnya, `diff <(ls foo) <(ls bar)` akan menunjukkan perbedaan antara berkas di direktori `foo` dan `bar`.


Karena itu adalah curahan informasi yang besar, mari lihat contoh yang memamerkan beberapa fitur tersebut. Skrip ini akan mengiterasi argumen yang kami berikan, melakukan `grep` untuk string `foobar`, dan menambahkannya ke berkas sebagai komentar jika tidak ditemukan.

```bash
#!/bin/bash

echo "Starting program at $(date)" # Date will be substituted

echo "Running program $0 with $# arguments with pid $$"

for file in "$@"; do
    grep foobar "$file" > /dev/null 2> /dev/null
    # When pattern is not found, grep has exit status 1
    # We redirect STDOUT and STDERR to a null register since we do not care about them
    if [[ $? -ne 0 ]]; then
        echo "File $file does not have any foobar, adding one"
        echo "# foobar" >> "$file"
    fi
done
```

Pada perbandingan tersebut kami menguji apakah `$?` tidak sama dengan 0.
Bash mengimplementasikan banyak perbandingan semacam ini - Anda dapat menemukan daftar terperincinya di manpage untuk [`test`](https://www.man7.org/linux/man-pages/man1/test.1.html).
Saat melakukan perbandingan di bash, coba gunakan kurung siku ganda `[[ ]]` sebagai pengganti kurung siku sederhana `[ ]`. Kemungkinan membuat kesalahan lebih rendah meskipun tidak portabel ke `sh`. Penjelasan lebih terperinci dapat ditemukan [di sini](https://mywiki.wooledge.org/BashFAQ/031).

Saat menjalankan skrip, Anda akan sering ingin memberikan argumen yang serupa. Bash memiliki cara untuk mempermudahnya, mengekspansi ekspresi dengan melakukan filename expansion. Teknik ini sering disebut shell _globbing_.
- Wildcard - Setiap kali Anda ingin melakukan semacam wildcard matching, Anda dapat menggunakan `?` untuk mencocokkan satu karakter dan `*` untuk mencocokkan berapa pun karakter. Misalnya, diberikan berkas `foo`, `foo1`, `foo2`, `foo10` dan `bar`, perintah `rm foo?` akan menghapus `foo1` dan `foo2` sedangkan `rm foo*` akan menghapus semuanya kecuali `bar`.
- Kurung kurawal `{}` - Setiap kali Anda memiliki substring yang sama pada serangkaian perintah, Anda dapat menggunakan kurung kurawal agar bash mengekspansinya secara otomatis. Ini sangat berguna saat memindahkan atau mengonversi berkas.

```bash
convert image.{png,jpg}
# Will expand to
convert image.png image.jpg

cp /path/to/project/{foo,bar,baz}.sh /newpath
# Will expand to
cp /path/to/project/foo.sh /path/to/project/bar.sh /path/to/project/baz.sh /newpath

# Globbing techniques can also be combined
mv *{.py,.sh} folder
# Will move all *.py and *.sh files


mkdir foo bar
# This creates files foo/a, foo/b, ... foo/h, bar/a, bar/b, ... bar/h
touch {foo,bar}/{a..h}
touch foo/x bar/y
# Show differences between files in foo and bar
diff <(ls foo) <(ls bar)
# Outputs
# < x
# ---
# > y
```

<!-- Lastly, pipes `|` are a core feature of scripting. Pipes connect one program's output to the next program's input. We will cover them more in detail in the data wrangling lecture. -->

Menulis skrip `bash` bisa rumit dan tidak intuitif. Ada tool seperti [shellcheck](https://github.com/koalaman/shellcheck) yang akan membantu Anda menemukan error di skrip sh/bash Anda.

Perhatikan bahwa skrip tidak harus ditulis dalam bash agar dapat dipanggil dari terminal. Misalnya, berikut skrip Python sederhana yang mengeluarkan argumennya dalam urutan terbalik:

```python
#!/usr/local/bin/python
import sys
for arg in reversed(sys.argv[1:]):
    print(arg)
```

Kernel mengetahui cara mengeksekusi skrip ini dengan interpreter python alih-alih perintah shell karena kami menyertakan baris [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) di bagian atas skrip.
Praktik yang baik adalah menulis baris shebang menggunakan perintah [`env`](https://www.man7.org/linux/man-pages/man1/env.1.html) yang akan mencari di mana perintah itu berada di sistem, sehingga meningkatkan portabilitas skrip Anda. Untuk mencari lokasinya, `env` akan memanfaatkan environment variable `PATH` yang kami perkenalkan pada kuliah pertama.
Untuk contoh ini baris shebang akan terlihat seperti `#!/usr/bin/env python`.

Beberapa perbedaan antara fungsi shell dan skrip yang perlu Anda ingat adalah:
- Fungsi harus berada dalam bahasa yang sama dengan shell, sedangkan skrip dapat ditulis dalam bahasa apa pun. Inilah sebabnya menyertakan shebang untuk skrip itu penting.
- Fungsi dimuat sekali ketika definisinya dibaca. Skrip dimuat setiap kali dieksekusi. Ini membuat fungsi sedikit lebih cepat dimuat, tetapi setiap kali Anda mengubahnya Anda harus memuat ulang definisinya.
- Fungsi dieksekusi di environment shell saat ini sedangkan skrip dieksekusi di prosesnya sendiri. Dengan demikian, fungsi dapat memodifikasi environment variable, misalnya mengubah current directory Anda, sedangkan skrip tidak dapat. Environment variable yang telah di-export menggunakan [`export`](https://www.man7.org/linux/man-pages/man1/export.1p.html) diteruskan berdasarkan nilai ke skrip.
- Seperti pada bahasa pemrograman apa pun, fungsi adalah konstruksi yang kuat untuk mencapai modularitas, code reuse, dan kejelasan kode shell. Sering kali skrip shell menyertakan definisi fungsi mereka sendiri.

# Shell Tools

## Menemukan cara menggunakan perintah

Pada titik ini, Anda mungkin bertanya-tanya bagaimana menemukan flag untuk perintah di bagian aliasing seperti `ls -l`, `mv -i` dan `mkdir -p`.
Lebih umum, diberikan sebuah perintah, bagaimana Anda mencari tahu apa yang dilakukannya dan berbagai opsinya?
Anda selalu dapat mulai mencari di Google, tetapi karena UNIX lebih tua dari StackOverflow, ada cara bawaan untuk memperoleh informasi ini.

Seperti yang kita lihat pada kuliah shell, pendekatan tingkat pertama adalah memanggil perintah tersebut dengan flag `-h` atau `--help`. Pendekatan yang lebih terperinci adalah menggunakan perintah `man`.
Singkatan dari manual, [`man`](https://www.man7.org/linux/man-pages/man1/man.1.html) menyediakan manual page (disebut manpage) untuk perintah yang Anda tentukan.
Misalnya, `man rm` akan mengeluarkan perilaku perintah `rm` beserta flag yang diterimanya, termasuk flag `-i` yang kami tunjukkan sebelumnya.
Bahkan, yang telah saya tautkan sejauh ini untuk setiap perintah adalah versi daring dari manpage Linux untuk perintah tersebut.
Bahkan perintah non-native yang Anda pasang akan memiliki entri manpage jika pengembangnya menuliskannya dan menyertakannya sebagai bagian dari proses pemasangan.
Untuk tool interaktif seperti yang berbasis ncurses, bantuan untuk perintah sering dapat diakses di dalam program menggunakan perintah `:help` atau mengetik `?`.

Kadang manpage memberikan deskripsi perintah yang terlalu detail, sehingga sulit mengurai flag/sintaks mana yang digunakan untuk use case umum.
[TLDR pages](https://tldr.sh/) adalah solusi pelengkap yang rapi yang berfokus pada pemberian contoh use case sebuah perintah sehingga Anda dapat dengan cepat mencari tahu opsi mana yang digunakan.
Misalnya, saya mendapati diri saya merujuk kembali ke halaman tldr untuk [`tar`](https://tldr.inbrowser.app/pages/common/tar) dan [`ffmpeg`](https://tldr.inbrowser.app/pages/common/ffmpeg) jauh lebih sering daripada manpage.


## Menemukan berkas

Salah satu tugas berulang yang paling umum dihadapi setiap programmer adalah menemukan berkas atau direktori.
Semua sistem mirip UNIX hadir dengan [`find`](https://www.man7.org/linux/man-pages/man1/find.1.html), sebuah shell tool yang hebat untuk menemukan berkas. `find` akan mencari berkas yang cocok dengan beberapa kriteria secara rekursif. Beberapa contoh:

```bash
# Find all directories named src
find . -name src -type d
# Find all python files that have a folder named test in their path
find . -path '*/test/*.py' -type f
# Find all files modified in the last day
find . -mtime -1
# Find all zip files with size in range 500k to 10M
find . -size +500k -size -10M -name '*.tar.gz'
```
Selain mencantumkan berkas, find juga dapat melakukan aksi pada berkas yang cocok dengan kueri Anda.
Properti ini bisa sangat membantu menyederhanakan tugas yang mungkin cukup monoton.
```bash
# Delete all files with .tmp extension
find . -name '*.tmp' -exec rm {} \;

# Find all PNG files and convert them to JPG
find . -name '*.png' -exec magick {} {}.jpg \;
```

Meskipun `find` ada di mana-mana, sintaksnya kadang sulit diingat.
Misalnya, untuk sekadar menemukan berkas yang cocok dengan pola `PATTERN` Anda harus mengeksekusi `find -name '*PATTERN*'` (atau `-iname` jika Anda ingin pencocokan pola tidak peka huruf besar-kecil).
Anda dapat mulai membuat alias untuk skenario tersebut, tetapi bagian dari filosofi shell adalah bahwa menjelajahi alternatif itu baik.
Ingat, salah satu properti terbaik shell adalah Anda hanya memanggil program, sehingga Anda dapat menemukan (bahkan menulis sendiri) pengganti untuk sebagian program.
Misalnya, [`fd`](https://github.com/sharkdp/fd) adalah alternatif `find` yang sederhana, cepat, dan ramah pengguna.
Tool ini menawarkan beberapa default yang bagus seperti output berwarna, regex matching default, dan dukungan Unicode. Menurut saya, sintaksnya juga lebih intuitif.
Misalnya, sintaks untuk menemukan pola `PATTERN` adalah `fd PATTERN`.

Sebagian besar akan setuju bahwa `find` dan `fd` itu bagus, tetapi sebagian dari Anda mungkin bertanya-tanya tentang efisiensi mencari berkas setiap kali versus mengompilasi semacam indeks atau database untuk pencarian cepat.
Itulah kegunaan [`locate`](https://www.man7.org/linux/man-pages/man1/locate.1.html).
`locate` menggunakan database yang diperbarui menggunakan [`updatedb`](https://www.man7.org/linux/man-pages/man1/updatedb.1.html).
Pada sebagian besar sistem, `updatedb` diperbarui setiap hari melalui [`cron`](https://www.man7.org/linux/man-pages/man8/cron.8.html).
Oleh karena itu salah satu trade-off antara keduanya adalah kecepatan versus kebaruan.
Lebih jauh lagi `find` dan tool serupa juga dapat menemukan berkas menggunakan atribut seperti ukuran berkas, waktu modifikasi, atau permission berkas, sedangkan `locate` hanya menggunakan nama berkas.
Perbandingan yang lebih mendalam dapat ditemukan [di sini](https://unix.stackexchange.com/questions/60205/locate-vs-find-usage-pros-and-cons-of-each-other).

## Menemukan kode

Menemukan berkas berdasarkan nama itu berguna, tetapi cukup sering Anda ingin mencari berdasarkan *isi* berkas.
Skenario umum adalah ingin mencari semua berkas yang memuat suatu pola, beserta di mana pola tersebut muncul di berkas tersebut.
Untuk mencapainya, sebagian besar sistem mirip UNIX menyediakan [`grep`](https://www.man7.org/linux/man-pages/man1/grep.1.html), tool generik untuk mencocokkan pola dari teks input.
`grep` adalah shell tool yang luar biasa berharga yang akan kami bahas lebih detail selama kuliah data wrangling.

Untuk sekarang, ketahuilah bahwa `grep` memiliki banyak flag yang membuatnya menjadi tool yang sangat serbaguna.
Beberapa yang sering saya gunakan adalah `-C` untuk memperoleh **C**ontext di sekitar baris yang cocok dan `-v` untuk mem**b**alik kecocokan, yaitu mencetak semua baris yang **tidak** cocok dengan pola. Misalnya, `grep -C 5` akan mencetak 5 baris sebelum dan sesudah kecocokan.
Ketika ingin mencari dengan cepat melalui banyak berkas, Anda ingin menggunakan `-R` karena ia akan **R**ecursively masuk ke direktori dan mencari berkas untuk string yang cocok.

Tetapi `grep -R` dapat ditingkatkan dengan banyak cara, seperti mengabaikan folder `.git`, menggunakan dukungan multi CPU, dsb.
Banyak alternatif `grep` telah dikembangkan, termasuk [ack](https://github.com/beyondgrep/ack3), [ag](https://github.com/ggreer/the_silver_searcher) dan [rg](https://github.com/BurntSushi/ripgrep).
Semuanya fantastis dan kurang lebih menyediakan fungsionalitas yang sama.
Untuk sekarang saya tetap menggunakan ripgrep (`rg`), mengingat betapa cepat dan intuitifnya. Beberapa contoh:
```bash
# Find all python files where I used the requests library
rg -t py 'import requests'
# Find all files (including hidden files) without a shebang line
rg -u --files-without-match "^#\!"
# Find all matches of foo and print the following 5 lines
rg foo -A 5
# Print statistics of matches (# of matched lines and files )
rg --stats PATTERN
```

Perhatikan bahwa seperti pada `find`/`fd`, penting bagi Anda untuk mengetahui bahwa masalah-masalah ini dapat diselesaikan dengan cepat menggunakan salah satu tool tersebut, sedangkan tool spesifik yang Anda gunakan tidak begitu penting.

## Menemukan perintah shell

Sejauh ini kita telah melihat cara menemukan berkas dan kode, tetapi saat Anda mulai menghabiskan lebih banyak waktu di shell, Anda mungkin ingin menemukan perintah tertentu yang pernah Anda ketik.
Hal pertama yang perlu diketahui adalah menekan tombol panah atas akan mengembalikan perintah terakhir Anda, dan jika Anda terus menekannya Anda akan perlahan menelusuri riwayat shell Anda.

Perintah `history` memungkinkan Anda mengakses riwayat shell secara programatik.
Perintah ini akan mencetak riwayat shell Anda ke standard output.
Jika kita ingin mencari di sana kita dapat melakukan pipe output tersebut ke `grep` dan mencari pola.
`history | grep find` akan mencetak perintah yang memuat substring "find".

Pada sebagian besar shell, Anda dapat memanfaatkan `Ctrl+R` untuk melakukan pencarian terbalik melalui riwayat Anda.
Setelah menekan `Ctrl+R`, Anda dapat mengetik substring yang ingin Anda cocokkan untuk perintah di riwayat Anda.
Seiring Anda terus menekannya, Anda akan berputar melalui kecocokan di riwayat Anda.
Ini juga dapat diaktifkan dengan tombol panah UP/DOWN di [zsh](https://github.com/zsh-users/zsh-history-substring-search).
Tambahan bagus di atas `Ctrl+R` datang dengan menggunakan binding [fzf](https://github.com/junegunn/fzf/wiki/Configuring-shell-key-bindings#ctrl-r).
`fzf` adalah fuzzy finder serbaguna yang dapat digunakan dengan banyak perintah.
Di sini ia digunakan untuk mencocokkan secara fuzzy melalui riwayat Anda dan menyajikan hasil dengan cara yang praktis dan enak dilihat.

Trik lain terkait riwayat yang sangat saya nikmati adalah **history-based autosuggestion**.
Pertama diperkenalkan oleh shell [fish](https://fishshell.com/), fitur ini secara dinamis melengkapi perintah shell Anda saat ini dengan perintah terbaru yang Anda ketik yang memiliki prefiks sama dengannya.
Fitur ini dapat diaktifkan di [zsh](https://github.com/zsh-users/zsh-autosuggestions) dan merupakan trik kualitas hidup yang hebat untuk shell Anda.

Anda dapat memodifikasi perilaku riwayat shell Anda, seperti mencegah perintah dengan spasi di depan disertakan. Ini berguna ketika Anda mengetik perintah dengan password atau bagian informasi sensitif lainnya.
Untuk melakukannya, tambahkan `HISTCONTROL=ignorespace` ke `.bashrc` Anda atau `setopt HIST_IGNORE_SPACE` ke `.zshrc` Anda.
Jika Anda membuat kesalahan karena tidak menambahkan spasi di depan, Anda selalu dapat menghapus entri secara manual dengan mengedit `.bash_history` atau `.zsh_history` Anda.

## Navigasi Direktori

Sejauh ini, kita menganggap Anda sudah berada di tempat yang Anda butuhkan untuk melakukan aksi tersebut. Tetapi bagaimana Anda melakukan navigasi direktori dengan cepat?
Ada banyak cara sederhana untuk melakukannya, seperti menulis alias shell atau membuat symlink dengan [ln -s](https://www.man7.org/linux/man-pages/man1/ln.1.html), tetapi kenyataannya para pengembang telah menemukan solusi yang cukup cerdik dan canggih saat ini.

Seperti tema kursus ini, Anda sering ingin mengoptimalkan untuk kasus umum.
Menemukan berkas dan direktori yang sering dan/atau baru-baru ini digunakan dapat dilakukan melalui tool seperti [`fasd`](https://github.com/clvv/fasd) dan [`autojump`](https://github.com/wting/autojump).
Fasd memeringkat berkas dan direktori berdasarkan [_frecency_](https://web.archive.org/web/20210421120120/https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Frecency_algorithm), yaitu berdasarkan _frequency_ dan _recency_ sekaligus.
Secara default, `fasd` menambahkan perintah `z` yang dapat Anda gunakan untuk `cd` dengan cepat menggunakan substring dari direktori yang _frecent_. Misalnya, jika Anda sering pergi ke `/home/user/files/cool_project` Anda cukup menggunakan `z cool` untuk melompat ke sana. Dengan autojump, perubahan direktori yang sama dapat dilakukan menggunakan `j cool`.

Tool yang lebih kompleks ada untuk dengan cepat memperoleh gambaran struktur direktori: [`tree`](https://linux.die.net/man/1/tree), [`broot`](https://github.com/Canop/broot) atau bahkan file manager lengkap seperti [`nnn`](https://github.com/jarun/nnn) atau [`ranger`](https://github.com/ranger/ranger).

<a id="exercises"></a>
# Latihan

1. Baca [`man ls`](https://www.man7.org/linux/man-pages/man1/ls.1.html) dan tulis perintah `ls` yang mencantumkan berkas dengan cara berikut

    - Menyertakan semua berkas, termasuk berkas tersembunyi
    - Ukuran dicantumkan dalam format yang mudah dibaca manusia (misalnya 454M alih-alih 454279954)
    - Berkas diurutkan berdasarkan kebaruan
    - Output diberi warna

    Contoh output akan terlihat seperti ini

    ```
    -rw-r--r--   1 user group 1.1M Jan 14 09:53 baz
    drwxr-xr-x   5 user group  160 Jan 14 09:53 .
    -rw-r--r--   1 user group  514 Jan 14 06:42 bar
    -rw-r--r--   1 user group 106M Jan 13 12:12 foo
    drwx------+ 47 user group 1.5K Jan 12 18:08 ..
    ```

{% comment %}
ls -lath --color=auto
{% endcomment %}

1. Tulis fungsi bash `marco` dan `polo` yang melakukan hal berikut.
Setiap kali Anda mengeksekusi `marco` current working directory seharusnya disimpan dengan cara tertentu, lalu ketika Anda mengeksekusi `polo`, di direktori mana pun Anda berada, `polo` seharusnya melakukan `cd` kembali ke direktori tempat Anda mengeksekusi `marco`.
Untuk memudahkan debugging Anda dapat menulis kodenya di berkas `marco.sh` dan (memuat ulang) definisinya ke shell Anda dengan mengeksekusi `source marco.sh`.

{% comment %}
marco() {
    export MARCO=$(pwd)
}

polo() {
    cd "$MARCO"
}
{% endcomment %}

1. Misalkan Anda memiliki perintah yang jarang gagal. Untuk men-debug-nya Anda perlu menangkap outputnya tetapi mendapatkan eksekusi yang gagal bisa memakan waktu.
Tulis skrip bash yang menjalankan skrip berikut sampai gagal dan menangkap stream standard output serta error-nya ke berkas dan mencetak semuanya di akhir.
Poin bonus jika Anda juga dapat melaporkan berapa banyak eksekusi yang diperlukan hingga skrip gagal.

    ```bash
    #!/usr/bin/env bash

    n=$(( RANDOM % 100 ))

    if [[ n -eq 42 ]]; then
       echo "Something went wrong"
       >&2 echo "The error was using magic numbers"
       exit 1
    fi

    echo "Everything went according to plan"
    ```

{% comment %}
#!/usr/bin/env bash

count=0
until [[ "$?" -ne 0 ]];
do
  count=$((count+1))
  ./random.sh &> out.txt
done

echo "found error after $count runs"
cat out.txt
{% endcomment %}

1. Seperti yang kita bahas pada kuliah, `-exec` milik `find` bisa sangat kuat untuk melakukan operasi pada berkas yang kita cari.
Namun, bagaimana jika kita ingin melakukan sesuatu dengan **semua** berkas, seperti membuat berkas zip?
Seperti yang telah Anda lihat sejauh ini, perintah akan menerima input dari argumen dan STDIN sekaligus.
Saat melakukan pipe perintah, kita menghubungkan STDOUT ke STDIN, tetapi sebagian perintah seperti `tar` menerima input dari argumen.
Untuk menjembatani ketidaksesuaian ini ada perintah [`xargs`](https://www.man7.org/linux/man-pages/man1/xargs.1.html) yang akan mengeksekusi perintah menggunakan STDIN sebagai argumen.
Misalnya `ls | xargs rm` akan menghapus berkas di direktori saat ini.

    Tugas Anda adalah menulis perintah yang menemukan semua berkas HTML di folder secara rekursif dan membuat zip dengannya. Perhatikan bahwa perintah Anda harus bekerja bahkan jika berkas memiliki spasi (petunjuk: periksa flag `-d` untuk `xargs`).
    {% comment %}
    find . -type f -name "*.html" | xargs -d '\n'  tar -cvzf archive.tar.gz
    {% endcomment %}

    Jika Anda menggunakan macOS, perhatikan bahwa `find` BSD default berbeda dari yang disertakan dalam [GNU coreutils](https://en.wikipedia.org/wiki/List_of_GNU_Core_Utilities_commands). Anda dapat menggunakan `-print0` pada `find` dan flag `-0` pada `xargs`. Sebagai pengguna macOS, Anda harus menyadari bahwa utilitas command-line yang disertakan dengan macOS mungkin berbeda dari padanan GNU-nya; Anda dapat memasang versi GNU jika mau dengan [menggunakan brew](https://formulae.brew.sh/formula/coreutils).

1. (Advanced) Tulis perintah atau skrip untuk menemukan berkas yang paling baru dimodifikasi di sebuah direktori secara rekursif. Lebih umum, dapatkah Anda mencantumkan semua berkas berdasarkan kebaruan?
