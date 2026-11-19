---
layout: lecture-id
title: "Command-line Environment"
description: >
  Pelajari cara kerja program command-line, termasuk input/output stream, environment variable, dan mesin jarak jauh dengan SSH.
thumbnail: /static/assets/thumbnails/2026/lec2.png
date: 2026-01-13
ready: true
video:
  aspect: 56.25
  id: ccBGsPedE9Q
lang: id
permalink: /id/2026/command-line-environment/
---

Seperti yang kita bahas pada kuliah sebelumnya, sebagian besar shell bukan sekadar peluncur untuk memulai program lain,
tetapi dalam praktiknya shell menyediakan bahasa pemrograman utuh yang penuh dengan pola dan abstraksi umum.
Namun, tidak seperti mayoritas bahasa pemrograman, dalam shell scripting segala sesuatu dirancang di sekitar menjalankan program dan membuat program-program tersebut berkomunikasi satu sama lain secara sederhana dan efisien.

Secara khusus, shell scripting terikat erat oleh _konvensi_. Agar sebuah program command line interface (CLI) dapat berperan baik di lingkungan shell yang lebih luas, ada beberapa pola umum yang perlu diikutinya.
Sekarang kita akan membahas banyak konsep yang diperlukan untuk memahami cara kerja program command line serta konvensi yang lazim tentang cara menggunakan dan mengonfigurasinya.

# Command-line Interface

Menulis sebuah fungsi pada sebagian besar bahasa pemrograman terlihat seperti:

```
def add(x: int, y: int) -> int:
    return x + y
```

Di sini kita dapat melihat secara eksplisit input dan output programnya.
Sebaliknya, skrip shell bisa terlihat cukup berbeda pada pandangan pertama.

```shell
#!/usr/bin/env bash

if [[ -f $1 ]]; then
    echo "Target file already exists"
    exit 1
else
    if $DEBUG; then
        grep 'error' - | tee $1
    else
        grep 'error' - > $1
    fi
    exit 0
fi
```

Untuk memahami dengan benar apa yang terjadi dalam skrip seperti ini, pertama-tama kita perlu memperkenalkan beberapa konsep yang sering muncul ketika program shell berkomunikasi satu sama lain atau dengan lingkungan shell:

- Arguments
- Streams
- Environment variables
- Return codes
- Signals

## Arguments

Program shell menerima daftar argumen ketika dieksekusi.
Argumen adalah string biasa di shell, dan terserah program bagaimana menafsirkannya.
Misalnya ketika kita menjalankan `ls -l folder/`, kita mengeksekusi program `/bin/ls` dengan argumen `['-l', 'folder/']`.

Dari dalam skrip shell kita mengaksesnya melalui sintaks shell khusus.
Untuk mengakses argumen pertama kita mengakses variabel `$1`, argumen kedua `$2` dan seterusnya hingga `$9`. Untuk mengakses semua argumen sebagai daftar kita menggunakan `$@` dan untuk memperoleh jumlah argumen `$#`. Selain itu kita juga dapat mengakses nama program dengan `$0`.

Untuk sebagian besar program, argumen akan terdiri dari campuran _flag_ dan string biasa.
Flag dapat dikenali karena didahului tanda dash (`-`) atau double-dash (`--`).
Flag biasanya opsional dan perannya adalah mengubah perilaku program.
Misalnya `ls -l` mengubah cara `ls` memformat outputnya.

Anda akan melihat flag double dash dengan nama panjang seperti `--all`, dan flag single dash seperti `-a`, yang paling sering diikuti satu huruf.
Opsi yang sama dapat ditentukan dalam kedua format, `ls -a` dan `ls --all` setara.
Flag single dash sering dikelompokkan, sehingga `ls -l -a` dan `ls -la` juga setara.
Urutan flag biasanya juga tidak penting, `ls -la` dan `ls -al` menghasilkan hasil yang sama.
Sebagian flag cukup lazim dan seiring Anda semakin mengenal lingkungan shell Anda akan secara intuitif menggunakannya, misalnya (`--help`, `--verbose`, `--version`).

> Flag adalah contoh pertama yang baik tentang konvensi shell. Bahasa shell tidak mewajibkan program kita menggunakan `-` atau `--` dengan cara khusus ini.
> Tidak ada yang mencegah kita menulis program dengan sintaks `myprogram +myoption myfile`, tetapi itu akan menimbulkan kebingungan karena ekspektasinya adalah kita menggunakan dash.

> Dalam praktiknya, sebagian besar bahasa pemrograman menyediakan library parsing flag CLI (misalnya `argparse` di python untuk mengurai argumen dengan sintaks dash).

Konvensi umum lain pada program CLI adalah program menerima jumlah argumen yang bervariasi dengan tipe yang sama. Ketika diberikan argumen dengan cara ini, perintah melakukan operasi yang sama pada setiap argumen tersebut.

```shell
mkdir src
mkdir docs
# is equivalent to
mkdir src docs
```

Syntactic sugar ini mungkin tampak tidak perlu pada awalnya, tetapi menjadi sangat kuat ketika digabungkan dengan _globbing_.
Globbing atau glob adalah pola khusus yang akan diekspansi oleh shell sebelum memanggil program.

Misalkan kita ingin menghapus semua berkas .py di folder saat ini secara non-rekursif. Dari yang kita pelajari pada kuliah sebelumnya kita dapat mencapainya dengan menjalankan

```shell
for file in $(ls | grep -P '\.py$'); do
    rm "$file"
done
```

Tetapi kita dapat menggantinya dengan hanya `rm *.py`!

Ketika kita mengetik `rm *.py` ke terminal, shell tidak akan memanggil program `/bin/rm` dengan argumen `['*.py']`.
Sebaliknya, shell akan mencari berkas di folder saat ini yang cocok dengan pola `*.py` di mana `*` dapat cocok dengan string apa pun yang terdiri dari nol atau lebih karakter bertipe apa pun.
Jadi jika folder kita memiliki `main.py` dan `utils.py` maka program `rm` akan menerima argumen `['main.py', 'utils.py']`.

Glob yang paling umum Anda akan temukan adalah wildcard `*` (nol atau lebih dari apa pun), `?` (tepat satu dari apa pun) dan kurung kurawal.
Kurung kurawal `{}` mengekspansi daftar pola yang dipisahkan koma menjadi beberapa argumen.

Dalam praktiknya, glob paling baik dipahami dengan contoh yang memotivasi.

```shell
touch folder/{a,b,c}.py
# Will expand to
touch folder/a.py folder/b.py folder/c.py

convert image.{png,jpg}
# Will expand to
convert image.png image.jpg

cp /path/to/project/{setup,build,deploy}.sh /newpath
# Will expand to
cp /path/to/project/setup.sh /path/to/project/build.sh /path/to/project/deploy.sh /newpath

# Globbing techniques can also be combined
mv *{.py,.sh} folder
# Will move all *.py and *.sh files
```

> Sebagian shell (misalnya zsh) mendukung bentuk glob yang bahkan lebih canggih seperti `**` yang akan diekspansi untuk menyertakan path rekursif. Jadi `rm **/*.py` akan menghapus semua berkas .py secara rekursif.


## Streams

Setiap kali kita mengeksekusi pipeline program seperti

```shell
cat myfile | grep -P '\d+' | uniq -c
```

kita melihat bahwa program `grep` berkomunikasi dengan kedua program `cat` dan `uniq`.

Pengamatan penting di sini adalah ketiga program dieksekusi sekaligus.
Yakni, shell tidak memanggil cat terlebih dahulu, lalu grep, lalu uniq.
Sebaliknya, ketiga program dijalankan dan shell menghubungkan output cat ke input grep serta output grep ke input uniq.
Saat menggunakan operator pipe `|`, shell beroperasi pada aliran data yang mengalir dari satu program ke program berikutnya dalam rantai tersebut.

Kita dapat mendemonstrasikan konkurensi ini, semua perintah dalam pipeline mulai segera:

```console
$ (sleep 15 && cat numbers.txt) | grep -P '^\d$' | sort | uniq  &
[1] 12345
$ ps | grep -P '(sleep|cat|grep|sort|uniq)'
  32930 pts/1    00:00:00 sleep
  32931 pts/1    00:00:00 grep
  32932 pts/1    00:00:00 sort
  32933 pts/1    00:00:00 uniq
  32948 pts/1    00:00:00 grep
```

Kita dapat melihat bahwa semua proses kecuali `cat` berjalan segera. Shell menjalankan semua proses dan menghubungkan stream-nya sebelum ada yang selesai. `cat` baru akan dimulai setelah sleep selesai, dan output `cat` akan dikirim ke grep dan seterusnya.

Setiap program memiliki input stream, yang diberi label stdin (untuk standard input). Saat melakukan piping, stdin terhubung secara otomatis. Dalam sebuah skrip, banyak program menerima `-` sebagai nama berkas yang berarti "baca dari stdin":

```shell
# These are equivalent when data comes from a pipe
echo "hello" | grep "hello"
echo "hello" | grep "hello" -
```

Demikian pula, setiap program memiliki dua output stream: stdout dan stderr.
Standard output adalah yang paling sering ditemui dan merupakan yang digunakan untuk melakukan piping output program ke perintah berikutnya dalam pipeline.
Standard error adalah stream alternatif yang dimaksudkan agar program melaporkan peringatan dan jenis masalah lain, tanpa output tersebut diurai oleh perintah berikutnya dalam rantai.

```console
$ ls /nonexistent
ls: cannot access '/nonexistent': No such file or directory
$ ls /nonexistent | grep "pattern"
ls: cannot access '/nonexistent': No such file or directory
# The error message still appears because stderr is not piped
$ ls /nonexistent 2>/dev/null
# No output - stderr was redirected to /dev/null
```

Shell menyediakan sintaks untuk me-redirect stream ini. Berikut beberapa contoh ilustratif.

```shell
# Redirect stdout to a file (overwrite)
echo "hello" > output.txt

# Redirect stdout to a file (append)
echo "world" >> output.txt

# Redirect stderr to a file
ls foobar 2> errors.txt

# Redirect both stdout and stderr to the same file
ls foobar &> all_output.txt

# Redirect stdin from a file
grep "pattern" < input.txt

# Discard output by redirecting to /dev/null
cmd > /dev/null 2>&1
```

Tool kuat lain yang menjadi contoh filosofi Unix adalah [`fzf`](https://github.com/junegunn/fzf), sebuah fuzzy finder. Tool ini membaca baris dari stdin dan menyediakan antarmuka interaktif untuk memfilter dan memilih:

```console
$ ls | fzf
$ cat ~/.bash_history | fzf
```

`fzf` dapat diintegrasikan dengan banyak operasi shell. Kita akan melihat lebih banyak penggunaannya ketika membahas kustomisasi shell.


## Environment variables

Untuk menetapkan variabel di bash kita menggunakan sintaks `foo=bar`, lalu mengakses nilai variabel tersebut dengan sintaks `$foo`.
Perhatikan bahwa `foo = bar` adalah sintaks yang tidak valid karena shell akan mengurainya sebagai pemanggilan program `foo` dengan argumen `['=', 'bar']`.
Dalam shell scripting peran karakter spasi adalah melakukan pemisahan argumen.
Perilaku ini bisa membingungkan dan sulit dibiasakan, jadi ingatlah hal ini.

Variabel shell tidak memiliki tipe, semuanya string.
Perhatikan bahwa saat menulis ekspresi string di shell, single quote dan double quote tidak dapat dipertukarkan.
String yang dibatasi `'` adalah string literal dan tidak akan mengekspansi variabel, melakukan command substitution, atau memproses escape sequence, sedangkan string yang dibatasi `"` akan melakukannya.

```shell
foo=bar
echo "$foo"
# prints bar
echo '$foo'
# prints $foo
```

Untuk menangkap output sebuah perintah ke dalam variabel kita menggunakan _command substitution_.
Ketika kita mengeksekusi
```shell
files=$(ls)
echo "$files" | grep README
echo "$files" | grep ".py"
```
output (secara konkret stdout) dari ls ditempatkan ke dalam variabel `$files` yang dapat kita akses kemudian.
Isi variabel `$files` memang menyertakan newline dari output ls, yang merupakan cara program seperti `grep` mengetahui untuk beroperasi pada setiap item secara independen.

Fitur serupa yang kurang dikenal adalah _process substitution_, `<( CMD )` akan mengeksekusi `CMD` dan menempatkan outputnya dalam berkas sementara serta mengganti `<()` dengan nama berkas tersebut.
Ini berguna ketika perintah mengharapkan nilai diberikan melalui berkas alih-alih melalui STDIN.
Misalnya, `diff <(ls src) <(ls docs)` akan menunjukkan perbedaan antara berkas di direktori `src` dan `docs`.

Setiap kali program shell memanggil program lain, program tersebut meneruskan sekumpulan variabel yang sering disebut _environment variables_.
Dari dalam shell kita dapat menemukan environment variable saat ini dengan menjalankan `printenv`.
Untuk meneruskan environment variable secara eksplisit kita dapat mengawali sebuah perintah dengan penetapan variabel

> Environment variable secara konvensi ditulis dalam ALL_CAPS (misalnya, `HOME`, `PATH`, `DEBUG`). Ini adalah konvensi, bukan persyaratan teknis, tetapi mengikutinya membantu membedakan environment variable dari variabel shell lokal yang biasanya huruf kecil.

```shell
TZ=Asia/Tokyo date  # prints the current time in Tokyo
echo $TZ  # this will be empty, since TZ was only set for the child command
```

Alternatifnya, kita dapat menggunakan fungsi bawaan `export` yang akan mengubah environment kita saat ini sehingga semua child process akan mewarisi variabel tersebut:

```shell
export DEBUG=1
# All programs from this point onwards will have DEBUG=1 in their environment
bash -c 'echo $DEBUG'
# prints 1
```

Untuk menghapus variabel gunakan perintah bawaan `unset`, misalnya `unset DEBUG`.

> Environment variable adalah konvensi shell lainnya. Variabel tersebut dapat digunakan untuk mengubah perilaku banyak program secara implisit, bukan eksplisit. Misalnya, shell menetapkan environment variable `$HOME` dengan path folder home pengguna saat ini. Kemudian program dapat mengakses variabel ini untuk memperoleh informasi tersebut, alih-alih memerlukan `--home /home/alice` yang eksplisit. Contoh umum lainnya adalah `$TZ`, yang digunakan banyak program untuk memformat tanggal dan waktu sesuai timezone yang ditentukan.

## Return codes

Seperti yang kita lihat sebelumnya, output utama sebuah program shell disampaikan melalui stream stdout/stderr dan efek samping pada file system.

Secara default skrip shell akan mengembalikan exit code nol.
Konvensinya adalah nol berarti semuanya berjalan baik sedangkan nilai bukan nol berarti ada masalah yang ditemui.
Untuk mengembalikan exit code bukan nol kita harus menggunakan perintah bawaan shell `exit NUM`.
Kita dapat mengakses return code perintah terakhir yang dijalankan dengan mengakses variabel khusus `$?`.

Shell memiliki operator boolean `&&` dan `||` untuk melakukan operasi AND dan OR masing-masing.
Tidak seperti yang ditemui pada bahasa pemrograman biasa, operator di shell beroperasi pada return code program.
Keduanya adalah operator [short-circuiting](https://en.wikipedia.org/wiki/Short-circuit_evaluation).
Ini berarti keduanya dapat digunakan untuk menjalankan perintah secara kondisional berdasarkan keberhasilan atau kegagalan perintah sebelumnya, di mana keberhasilan ditentukan berdasarkan apakah return code bernilai nol atau tidak. Beberapa contoh:

```shell
# echo will only run if grep succeeds (finds a match)
grep -q "pattern" file.txt && echo "Pattern found"

# echo will only run if grep fails (no match)
grep -q "pattern" file.txt || echo "Pattern not found"

# true is a shell program that always succeeds
true && echo "This will always print"

# and false is a shell program that always fails
false || echo "This will always print"
```

Prinsip yang sama berlaku untuk pernyataan `if` dan `while`, keduanya menggunakan return code untuk mengambil keputusan:

```shell
# if uses the return code of the condition command (0 = true, nonzero = false)
if grep -q "pattern" file.txt; then
    echo "Found"
fi

# while loops continue as long as the command returns 0
while read line; do
    echo "$line"
done < file.txt
```

## Signals

Dalam beberapa kasus Anda perlu menginterupsi program saat sedang dieksekusi, misalnya jika sebuah perintah terlalu lama selesai.
Cara paling sederhana untuk menginterupsi program adalah menekan `Ctrl-C` dan perintah tersebut mungkin akan berhenti.
Tetapi bagaimana ini sebenarnya bekerja dan mengapa kadang gagal menghentikan prosesnya?

```console
$ sleep 100
^C
$
```

> Perhatikan, di sini `^C` adalah cara `Ctrl-C` ditampilkan ketika diketik di terminal.

Di balik layar, yang terjadi di sini adalah sebagai berikut:

1. Kita menekan `Ctrl-C`
2. Shell mengidentifikasi kombinasi karakter khusus tersebut
3. Proses shell mengirim sinyal SIGINT ke proses `sleep`
4. Sinyal tersebut menginterupsi eksekusi proses `sleep`

Sinyal adalah mekanisme komunikasi khusus.
Ketika sebuah proses menerima sinyal, proses menghentikan eksekusinya, menangani sinyal tersebut dan berpotensi mengubah alur eksekusi berdasarkan informasi yang dibawa sinyal. Karena alasan ini, sinyal adalah _software interrupt_.


Dalam kasus kita, ketika mengetik `Ctrl-C` ini memicu shell untuk mengirimkan sinyal `SIGINT` ke proses.
Berikut contoh minimal program Python yang menangkap `SIGINT` dan mengabaikannya, sehingga tidak lagi berhenti. Untuk mematikan program ini kita sekarang dapat menggunakan sinyal `SIGQUIT`, dengan mengetik `Ctrl-\`.

```python
#!/usr/bin/env python
import signal, time

def handler(signum, time):
    print("\nI got a SIGINT, but I am not stopping")

signal.signal(signal.SIGINT, handler)
i = 0
while True:
    time.sleep(.1)
    print("\r{}".format(i), end="")
    i += 1
```

Berikut yang terjadi jika kita mengirim `SIGINT` dua kali ke program ini, diikuti `SIGQUIT`. Perhatikan bahwa `^` adalah cara `Ctrl` ditampilkan ketika diketik di terminal.

```console
$ python sigint.py
24^C
I got a SIGINT, but I am not stopping
26^C
I got a SIGINT, but I am not stopping
30^\[1]    39913 quit       python sigint.py
```

Meskipun `SIGINT` dan `SIGQUIT` keduanya biasanya terkait dengan permintaan yang berhubungan dengan terminal, sinyal yang lebih generik untuk meminta proses keluar secara graceful adalah sinyal `SIGTERM`.
Untuk mengirim sinyal ini kita dapat menggunakan perintah [`kill`](https://www.man7.org/linux/man-pages/man1/kill.1.html), dengan sintaks `kill -TERM <PID>`.

Sinyal dapat melakukan hal lain selain mematikan proses. Misalnya, `SIGSTOP` menjeda sebuah proses. Di terminal, mengetik `Ctrl-Z` akan memicu shell mengirim sinyal `SIGTSTP`, singkatan dari Terminal Stop (yakni versi terminal dari `SIGSTOP`).

Kita kemudian dapat melanjutkan job yang dijeda tersebut di foreground atau di background menggunakan [`fg`](https://www.man7.org/linux/man-pages/man1/fg.1p.html) atau [`bg`](https://man7.org/linux/man-pages/man1/bg.1p.html), masing-masing.

Perintah [`jobs`](https://www.man7.org/linux/man-pages/man1/jobs.1p.html) mencantumkan job yang belum selesai yang terkait dengan sesi terminal saat ini.
Anda dapat merujuk job tersebut menggunakan pid-nya (Anda dapat menggunakan [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) untuk mengetahuinya).
Lebih intuitif, Anda juga dapat merujuk sebuah proses menggunakan simbol persen diikuti nomor job-nya (ditampilkan oleh `jobs`). Untuk merujuk job terakhir yang di-background Anda dapat menggunakan parameter khusus `$!`.

Satu hal lagi yang perlu diketahui adalah sufiks `&` pada sebuah perintah akan menjalankan perintah tersebut di background, mengembalikan prompt kepada Anda, meskipun perintah itu tetap menggunakan STDOUT shell yang bisa mengganggu (gunakan shell redirection dalam kasus itu). Setara dengan itu, untuk mem-background program yang sudah berjalan Anda dapat melakukan `Ctrl-Z` diikuti `bg`.


Perhatikan bahwa proses yang di-background masih merupakan child process dari terminal Anda dan akan mati jika Anda menutup terminal (ini akan mengirim sinyal lain, `SIGHUP`).
Untuk mencegah hal itu terjadi Anda dapat menjalankan program dengan [`nohup`](https://www.man7.org/linux/man-pages/man1/nohup.1.html) (wrapper untuk mengabaikan `SIGHUP`), atau menggunakan `disown` jika proses sudah dimulai.
Alternatifnya, Anda dapat menggunakan terminal multiplexer seperti yang akan kita lihat pada bagian berikutnya.

Berikut adalah contoh sesi untuk memamerkan beberapa konsep tersebut.

```
$ sleep 1000
^Z
[1]  + 18653 suspended  sleep 1000

$ nohup sleep 2000 &
[2] 18745
appending output to nohup.out

$ jobs
[1]  + suspended  sleep 1000
[2]  - running    nohup sleep 2000

$ kill -SIGHUP %1
[1]  + 18653 hangup     sleep 1000

$ kill -SIGHUP %2   # nohup protects from SIGHUP

$ jobs
[2]  + running    nohup sleep 2000

$ kill %2
[2]  + 18745 terminated  nohup sleep 2000
```

Sinyal khusus adalah `SIGKILL` karena sinyal ini tidak dapat ditangkap oleh proses dan akan selalu menghentikannya segera. Namun, sinyal ini dapat menimbulkan efek samping buruk seperti meninggalkan child process yang yatim.

Anda dapat mempelajari lebih lanjut tentang sinyal-sinyal ini dan sinyal lainnya [di sini](https://en.wikipedia.org/wiki/Signal_(IPC)) atau dengan mengetik [`man signal`](https://www.man7.org/linux/man-pages/man7/signal.7.html) atau `kill -l`.

Di dalam skrip shell, Anda dapat menggunakan bawaan `trap` untuk mengeksekusi perintah ketika sinyal diterima. Ini berguna untuk operasi pembersihan:

```shell
#!/usr/bin/env bash
cleanup() {
    echo "Cleaning up temporary files..."
    rm -f /tmp/mytemp.*
}
trap cleanup EXIT  # Run cleanup when script exits
trap cleanup SIGINT SIGTERM  # Also on Ctrl-C or kill
```
{% comment %}
### Users, Files and Permissions

Lastly, another way programs have to indirectly communicate with each other is using files.
For a program to be able to correctly read/write/delete files and folders, the file permissions must allow the operation.

Listing a specific file will give the following output

```console
$ ls -l notes.txt
-rw-r--r--  1 alice  users  12693 Jan 11 23:05 notes.txt
```

Here `ls` is listing what is the owner of the file, user `alice`, and the group `users`. Then the `rw-r--r--` are a shorthand notation for the permissions.
In this case, the file `notes.txt` has read/write permissions for the user alice `rw-`, and only read permissions for the group and the rest of users in the file system.

```console
$ ./script.sh
# permission denied
$ chmod +x script.sh
$ ls -l script.sh
-rwxr-xr-x  1 alice  users  3125 Jan 11 23:07 script.sh
$ ./script.sh
```

For a script to be executable, the executable rights must be set, hence why we had to use the `chmod` (change mode) program.
`chmod` syntax, while intuitive, is not obvious when first encountered.
If you, like me, prefer to learn by example, this is a good usecase of the `tldr` tool (note that you need to install it first).

```console
❯ tldr chmod
  Change the access permissions of a file or directory.
  More information: <https://www.gnu.org/software/coreutils/chmod>.

  Give the [u]ser who owns a file the right to e[x]ecute it:

      chmod u+x path/to/file

  Give the [u]ser rights to [r]ead and [w]rite to a file/directory:

      chmod u+rw path/to/file_or_directory

  Give [a]ll users rights to [r]ead and e[x]ecute:

      chmod a+rx path/to/file
```

Run `tldr chmod` to see more examples, including recursive operations and group permissions.

> Your shell might show you something like `command not found: tldr`. That is because it is a more modern tool and it is not pre-installed in most systems. A good reference for how to install tools is the [https://command-not-found.com](https://command-not-found.com) website. It contains instructions for a huge collection of CLI tools for popular OS distributions.

Each program is run as a specific user in the system. We can use the `whoami` command to find our user name and `id -u` to find our UID (user id) which is the integer value that the OS associates with the user.

When running `sudo command`, the `command` is run as the root user which can bypass most permissions in the system.
Try running `sudo whoami` and `sudo id -u` to see how the output changes (you might be prompted for your password).
To change the owner of a file or folder, we use the `chown` command.

You can learn more about UNIX file permissions [here](https://en.wikipedia.org/wiki/File-system_permissions#Traditional_Unix_permissions)

So far we've focused on your local machine, but many of these skills become even more valuable when working with remote servers.

{% endcomment %}

# Mesin Jarak Jauh

Semakin umum bagi programmer untuk bekerja dengan server jarak jauh dalam pekerjaan sehari-hari mereka. Tool yang paling umum untuk tugas ini adalah SSH (Secure Shell) yang akan membantu kita terhubung ke server jarak jauh dan menyediakan antarmuka shell yang sudah familiar. Kita terhubung ke server dengan perintah seperti:

```bash
ssh alice@server.mit.edu
```

Di sini kita mencoba ssh sebagai pengguna `alice` di server `server.mit.edu`.

Fitur `ssh` yang sering terlewat adalah kemampuan menjalankan perintah secara non-interaktif. `ssh` menangani pengiriman stdin dan penerimaan stdout perintah dengan benar, sehingga kita dapat menggabungkannya dengan perintah lain

```shell
# here ls runs in the remote, and wc runs locally
ssh alice@server ls | wc -l

# here both ls and wc run in the server
ssh alice@server 'ls | wc -l'

```

> Coba pasang [Mosh](https://mosh.org/) sebagai pengganti SSH yang dapat menangani pemutusan koneksi, masuk/keluar dari sleep, pergantian jaringan dan menangani tautan dengan latency tinggi.

Agar `ssh` memungkinkan kita menjalankan perintah di server jarak jauh, kita perlu membuktikan bahwa kita berwenang melakukannya.
Kita dapat melakukannya melalui password atau ssh key.
Autentikasi berbasis key memanfaatkan public-key cryptography untuk membuktikan kepada server bahwa klien memiliki private key rahasia tanpa mengungkapkan key tersebut.
Autentikasi berbasis key lebih praktis sekaligus lebih aman, sehingga sebaiknya Anda memilihnya.
Perhatikan bahwa private key (sering `~/.ssh/id_rsa` dan lebih baru `~/.ssh/id_ed25519`) secara efektif adalah password Anda, jadi perlakukan seperti itu dan jangan pernah membagikan isinya.

Untuk menghasilkan pasangan key Anda dapat menjalankan [`ssh-keygen`](https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html).
```bash
ssh-keygen -a 100 -t ed25519 -f ~/.ssh/id_ed25519
```

Jika Anda pernah mengonfigurasi push ke GitHub menggunakan SSH key, maka Anda mungkin pernah melakukan langkah-langkah yang diuraikan [di sini](https://help.github.com/articles/connecting-to-github-with-ssh/) dan sudah memiliki pasangan key yang valid. Untuk memeriksa apakah Anda memiliki passphrase dan memvalidasinya Anda dapat menjalankan `ssh-keygen -y -f /path/to/key`.

Di sisi server `ssh` akan memeriksa `.ssh/authorized_keys` untuk menentukan klien mana yang boleh masuk. Untuk menyalin public key Anda dapat menggunakan:

```bash
cat .ssh/id_ed25519.pub | ssh alice@remote 'cat >> ~/.ssh/authorized_keys'

# or more simply (if ssh-copy-id is available)

ssh-copy-id -i .ssh/id_ed25519 alice@remote
```

Selain menjalankan perintah, koneksi yang dibangun ssh dapat digunakan untuk mentransfer berkas dari dan ke server secara aman. [`scp`](https://www.man7.org/linux/man-pages/man1/scp.1.html) adalah tool paling tradisional dan sintaksnya adalah `scp path/to/local_file remote_host:path/to/remote_file`. [`rsync`](https://www.man7.org/linux/man-pages/man1/rsync.1.html) meningkatkan `scp` dengan mendeteksi berkas identik di lokal dan remote, serta mencegah penyalinan ulang berkas tersebut. Tool ini juga memberikan kendali lebih terperinci atas symlink, permission dan memiliki fitur tambahan seperti flag `--partial` yang dapat melanjutkan dari penyalinan yang sebelumnya terinterupsi. `rsync` memiliki sintaks yang mirip dengan `scp`.

Konfigurasi klien SSH berada di `~/.ssh/config` dan memungkinkan kita mendeklarasikan host serta menetapkan pengaturan default untuknya. Berkas konfigurasi ini tidak hanya dibaca oleh `ssh` tetapi juga program lain seperti `scp`, `rsync`, `mosh`, &c.

```bash
Host vm
    User alice
    HostName 172.16.174.141
    Port 2222
    IdentityFile ~/.ssh/id_ed25519

# Configs can also take wildcards
Host *.mit.edu
    User alice
```




# Terminal Multiplexers

Saat menggunakan command line interface Anda akan sering ingin menjalankan lebih dari satu hal sekaligus.
Misalnya, Anda mungkin ingin menjalankan editor dan program Anda secara berdampingan.
Meskipun hal ini dapat dicapai dengan membuka jendela terminal baru, menggunakan terminal multiplexer adalah solusi yang lebih serbaguna.

Terminal multiplexer seperti [`tmux`](https://www.man7.org/linux/man-pages/man1/tmux.1.html) memungkinkan Anda memultipleks jendela terminal menggunakan pane dan tab sehingga Anda dapat berinteraksi dengan beberapa sesi shell secara efisien.
Selain itu, terminal multiplexer memungkinkan Anda melepas sesi terminal saat ini dan menghubungkannya kembali di waktu lain.
Karena itu, terminal multiplexer sangat praktis saat bekerja dengan mesin jarak jauh, karena menghindari kebutuhan menggunakan `nohup` dan trik serupa.

Terminal multiplexer paling populer saat ini adalah [`tmux`](https://www.man7.org/linux/man-pages/man1/tmux.1.html). `tmux` sangat dapat dikonfigurasi dan dengan menggunakan keybinding terkait Anda dapat membuat beberapa tab dan pane serta bernavigasi di antaranya dengan cepat.

`tmux` mengharapkan Anda mengetahui keybinding-nya, dan semuanya berbentuk `<C-b> x` yang berarti (1) tekan `Ctrl+b`, (2) lepaskan `Ctrl+b`, lalu (3) tekan `x`. `tmux` memiliki hierarki objek berikut:
- **Sessions** - sebuah session adalah workspace independen dengan satu atau lebih window
    + `tmux` memulai session baru.
    + `tmux new -s NAME` memulainya dengan nama tersebut.
    + `tmux ls` mencantumkan session saat ini
    + Di dalam `tmux` mengetik `<C-b> d` melepas session saat ini
    + `tmux a` menghubungkan session terakhir. Anda dapat menggunakan flag `-t` untuk menentukan yang mana

- **Windows** - Setara dengan tab di editor atau browser, window adalah bagian yang terpisah secara visual dari session yang sama
    + `<C-b> c` Membuat window baru. Untuk menutupnya Anda cukup mengakhiri shell dengan `<C-d>`
    + `<C-b> N` Pindah ke window ke-_N_. Perhatikan window diberi nomor
    + `<C-b> p` Pindah ke window sebelumnya
    + `<C-b> n` Pindah ke window berikutnya
    + `<C-b> ,` Mengganti nama window saat ini
    + `<C-b> w` Mencantumkan window saat ini

- **Panes** - Seperti split di vim, pane memungkinkan Anda memiliki beberapa shell dalam tampilan visual yang sama.
    + `<C-b> "` Membagi pane saat ini secara horizontal
    + `<C-b> %` Membagi pane saat ini secara vertikal
    + `<C-b> <direction>` Pindah ke pane pada _direction_ yang ditentukan. Direction di sini berarti tombol panah.
    + `<C-b> z` Mengaktifkan/mematikan zoom untuk pane saat ini
    + `<C-b> [` Mulai scrollback. Anda kemudian dapat menekan `<space>` untuk memulai seleksi dan `<enter>` untuk menyalin seleksi tersebut.
    + `<C-b> <space>` Berputar melalui pengaturan pane.

> Untuk mempelajari lebih lanjut tentang tmux, pertimbangkan membaca [ini](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) tutorial singkat dan [ini](https://linuxcommand.org/lc3_adv_termmux.php) penjelasan yang lebih terperinci.

Dengan tmux dan SSH di perangkat Anda, Anda akan ingin membuat environment Anda terasa seperti di rumah di mesin mana pun. Di sinilah kustomisasi shell berperan.

# Menyesuaikan Shell

Berbagai macam program command line dikonfigurasi menggunakan berkas teks biasa yang dikenal sebagai _dotfiles_
(karena nama berkasnya dimulai dengan `.`, misalnya `~/.vimrc`, sehingga berkas tersebut
tersembunyi dari pencantuman direktori `ls` secara default).

> Dotfiles adalah juga merupakan konvensi shell. Titik di depan dimaksudkan untuk "menyembunyikan" berkas tersebut saat pencantuman (ya, konvensi lagi).

Shell adalah salah satu contoh program yang dikonfigurasi dengan berkas semacam itu. Saat startup, shell Anda akan membaca banyak berkas untuk memuat konfigurasinya.
Bergantung pada shell-nya dan apakah Anda memulai sesi login dan/atau interaktif, keseluruhan proses bisa cukup kompleks.
[Di sini](https://web.archive.org/web/20260329133158/https://blog.flowblok.id.au/2013-02/shell-startup-scripts.html) ada sumber yang sangat baik tentang topik ini.

Untuk `bash`, mengedit `.bashrc` atau `.bash_profile` Anda akan berfungsi di sebagian besar sistem.
Beberapa contoh lain tool yang dapat dikonfigurasi melalui dotfiles adalah:

- `bash` - `~/.bashrc`, `~/.bash_profile`
- `git` - `~/.gitconfig`
- `vim` - `~/.vimrc` dan folder `~/.vim`
- `ssh` - `~/.ssh/config`
- `tmux` - `~/.tmux.conf`

Perubahan konfigurasi yang umum adalah menambahkan lokasi baru bagi shell untuk menemukan program. Anda akan menemui pola ini saat memasang perangkat lunak:

```shell
export PATH="$PATH:path/to/append"
```

Di sini, kita memberi tahu shell untuk menetapkan nilai variabel $PATH ke nilai saat ini ditambah path baru, dan membuat semua child process mewarisi nilai PATH yang baru ini.
Ini akan memungkinkan child process menemukan program yang berada di bawah `path/to/append`.


Menyesuaikan shell Anda sering kali berarti memasang tool command-line baru. Package manager mempermudah hal ini. Package manager menangani pengunduhan, pemasangan, dan pembaruan perangkat lunak. Sistem operasi yang berbeda memiliki package manager berbeda: macOS menggunakan [Homebrew](https://brew.sh/), Ubuntu/Debian menggunakan `apt`, Fedora menggunakan `dnf`, dan Arch menggunakan `pacman`. Kita akan membahas package manager lebih mendalam pada kuliah shipping code.

Berikut cara memasang dua tool berguna menggunakan Homebrew di macOS:

```shell
# ripgrep: a faster grep with better defaults
brew install ripgrep

# fd: a faster, user-friendly find
brew install fd
```

Dengan ini terpasang, Anda dapat menggunakan `rg` sebagai pengganti `grep` dan `fd` sebagai pengganti `find`.

> **Peringatan tentang `curl | bash`**: Anda akan sering melihat instruksi pemasangan seperti `curl -fsSL https://example.com/install.sh | bash`. Pola ini mengunduh sebuah skrip lalu langsung menjalankannya, yang praktis tetapi berisiko; Anda menjalankan kode yang belum Anda periksa. Pendekatan yang lebih aman adalah mengunduh terlebih dahulu, meninjau, lalu mengeksekusi:
> ```shell
> curl -fsSL https://example.com/install.sh -o install.sh
> less install.sh  # review the script
> bash install.sh
> ```
> Sebagian installer menggunakan varian yang sedikit lebih aman: `/bin/bash -c "$(curl -fsSL https://url)"` yang setidaknya memastikan bash yang menafsirkan skrip, bukan shell Anda saat ini.

Ketika Anda mencoba menjalankan perintah yang tidak terpasang, shell Anda akan menampilkan `command not found`. Situs web [command-not-found.com](https://command-not-found.com) adalah sumber yang membantu yang dapat Anda gunakan untuk mencari perintah apa pun guna mengetahui cara memasangnya di berbagai package manager dan distribusi.

Tool berguna lainnya adalah [`tldr`](https://tldr.sh/), yang menyediakan man page yang disederhanakan dan berfokus pada contoh. Daripada membaca dokumentasi yang panjang, Anda dapat melihat pola penggunaan umum dengan cepat:

```console
$ tldr fd
  An alternative to find.
  Aims to be faster and easier to use than find.

  Recursively find files matching a pattern in the current directory:
      fd "pattern"

  Find files that begin with "foo":
      fd "^foo"

  Find files with a specific extension:
      fd --extension txt
```

Kadang Anda tidak memerlukan program baru seutuhnya, melainkan hanya shortcut untuk perintah yang sudah ada dengan flag tertentu. Di sinilah alias berperan.

Kita juga dapat membuat alias perintah kita sendiri menggunakan bawaan shell `alias`.
Shell alias adalah bentuk singkat untuk perintah lain yang akan diganti otomatis oleh shell Anda sebelum mengevaluasi ekspresi tersebut.
Misalnya, alias di bash memiliki struktur berikut:

```bash
alias alias_name="command_to_alias arg1 arg2"
```

> Perhatikan bahwa tidak ada spasi di sekitar tanda sama dengan `=`, karena [`alias`](https://www.man7.org/linux/man-pages/man1/alias.1p.html) adalah perintah shell yang menerima satu argumen.

Alias memiliki banyak fitur praktis:

```bash
# Make shorthands for common flags
alias ll="ls -lh"

# Save a lot of typing for common commands
alias gs="git status"
alias gc="git commit"

# Save you from mistyping
alias sl=ls

# Overwrite existing commands for better defaults
alias mv="mv -i"           # -i prompts before overwrite
alias mkdir="mkdir -p"     # -p make parent dirs as needed
alias df="df -h"           # -h prints human readable format

# Alias can be composed
alias la="ls -A"
alias lla="la -l"

# To ignore an alias run it prepended with \
\ls
# Or disable an alias altogether with unalias
unalias la

# To get an alias definition just call it with alias
alias ll
# Will print ll='ls -lh'
```

Alias memiliki keterbatasan: alias tidak dapat menerima argumen di tengah perintah. Untuk perilaku yang lebih kompleks, Anda sebaiknya menggunakan fungsi shell.

Sebagian besar shell mendukung `Ctrl-R` untuk pencarian riwayat terbalik. Ketik `Ctrl-R` dan mulai mengetik untuk mencari melalui perintah sebelumnya. Sebelumnya kita memperkenalkan `fzf` sebagai fuzzy finder; dengan integrasi shell fzf dikonfigurasi, `Ctrl-R` menjadi pencarian fuzzy interaktif melalui seluruh riwayat Anda, jauh lebih kuat daripada default.

Bagaimana Anda sebaiknya mengorganisasi dotfiles Anda? Dotfiles sebaiknya berada di foldernya sendiri,
di bawah version control, dan **symlink** ke tempatnya menggunakan sebuah skrip. Ini memiliki
manfaat:

- **Pemasangan mudah**: jika Anda login ke mesin baru, menerapkan
kustomisasi Anda hanya akan memakan waktu satu menit.
- **Portabilitas**: tool Anda akan bekerja dengan cara yang sama di mana pun.
- **Sinkronisasi**: Anda dapat memperbarui dotfiles Anda di mana saja dan menjaga semuanya
tetap sinkron.
- **Pelacakan perubahan**: Anda mungkin akan memelihara dotfiles Anda
sepanjang karier pemrograman Anda, dan riwayat versi berguna untuk
proyek yang berumur panjang.

Apa yang sebaiknya Anda letakkan di dotfiles Anda?
Anda dapat mempelajari pengaturan tool Anda dengan membaca dokumentasi daring atau
[man page](https://en.wikipedia.org/wiki/Man_page). Cara hebat lainnya adalah
mencari di internet posting blog tentang program tertentu, di mana penulisnya akan
memberi tahu Anda tentang kustomisasi yang mereka sukai. Cara lain lagi untuk mempelajari
kustomisasi adalah dengan melihat dotfiles orang lain: Anda dapat menemukan banyak
[repositori
dotfiles](https://github.com/search?o=desc&q=dotfiles&s=stars&type=Repositories)
di GitHub --- lihat yang paling populer
[di sini](https://github.com/mathiasbynens/dotfiles) (kami menyarankan Anda untuk tidak menyalin
konfigurasi secara buta).
[Di sini](https://dotfiles.github.io/) ada sumber lain yang baik tentang topik ini.

Semua pengajar kelas memiliki dotfiles yang dapat diakses publik di GitHub: [Anish](https://github.com/anishathalye/dotfiles),
[Jon](https://github.com/jonhoo/configs),
[Jose](https://github.com/jjgo/dotfiles).

**Framework dan plugin** juga dapat meningkatkan shell Anda. Beberapa framework umum yang populer adalah [prezto](https://github.com/sorin-ionescu/prezto) atau [oh-my-zsh](https://ohmyz.sh/), dan plugin yang lebih kecil yang berfokus pada fitur tertentu:

- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) - mewarnai perintah valid/tidak valid saat Anda mengetik
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) - menyarankan perintah dari riwayat saat Anda mengetik
- [zsh-completions](https://github.com/zsh-users/zsh-completions) - definisi completion tambahan
- [zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search) - pencarian riwayat seperti fish
- [powerlevel10k](https://github.com/romkatv/powerlevel10k) - tema prompt yang cepat dan dapat disesuaikan

Shell seperti [fish](https://fishshell.com/) menyertakan banyak fitur ini secara default.

> Anda tidak memerlukan framework besar seperti oh-my-zsh untuk mendapatkan fitur ini. Memasang plugin satu per satu sering lebih cepat dan memberi Anda kendali lebih banyak. Framework besar dapat secara signifikan memperlambat waktu startup shell, jadi pertimbangkan memasang hanya yang benar-benar Anda gunakan.


# AI di Shell

Ada banyak cara untuk memasukkan tooling AI ke dalam shell. Berikut beberapa contoh pada tingkat integrasi yang berbeda:

**Command generation**: Tool seperti [`simonw/llm`](https://github.com/simonw/llm) dapat membantu menghasilkan perintah shell dari deskripsi bahasa alami:

```console
$ llm cmd "find all python files modified in the last week"
find . -name "*.py" -mtime -7
```

**Pipeline integration**: LLM dapat diintegrasikan ke dalam pipeline shell untuk memproses dan mentransformasi data. LLM sangat berguna ketika Anda perlu mengekstrak informasi dari format yang tidak konsisten di mana regex akan menyulitkan:

```console
$ cat users.txt
Contact: john.doe@example.com
User 'alice_smith' logged in at 3pm
Posted by: @bob_jones on Twitter
Author: Jane Doe (jdoe)
Message from mike_wilson yesterday
Submitted by user: sarah.connor
$ INSTRUCTIONS="Extract just the username from each line, one per line, nothing else"
$ llm "$INSTRUCTIONS" < users.txt
john.doe
alice_smith
bob_jones
jdoe
mike_wilson
sarah.connor
```

Perhatikan bagaimana kita menggunakan `"$INSTRUCTIONS"` (diberi quote) karena variabel tersebut memuat spasi, dan `< users.txt` untuk me-redirect isi berkas ke stdin.

**AI shells**: Tool seperti [Claude Code](https://docs.anthropic.com/en/docs/claude-code) berperan sebagai meta-shell yang menerima perintah bahasa Inggris dan menerjemahkannya menjadi operasi shell, pengeditan berkas, dan tugas multi-langkah yang lebih kompleks.

# Terminal Emulators

Selain menyesuaikan shell Anda, ada baiknya meluangkan waktu untuk memikirkan pilihan **terminal emulator** dan pengaturannya.
Terminal emulator adalah program GUI yang menyediakan antarmuka berbasis teks tempat shell Anda berjalan.
Ada banyak terminal emulator di luar sana.

Karena Anda mungkin menghabiskan ratusan hingga ribuan jam di terminal Anda, menelaah pengaturannya akan terbayar. Beberapa aspek yang mungkin ingin Anda ubah pada terminal Anda meliputi:

- Pilihan font
- Skema warna
- Pintasan keyboard
- Dukungan Tab/Pane
- Konfigurasi scrollback
- Performa (sebagian terminal yang lebih baru seperti [Alacritty](https://github.com/alacritty/alacritty) atau [Ghostty](https://ghostty.org/) menawarkan akselerasi GPU).



# Latihan

## Argument dan Glob

1. Anda mungkin melihat perintah seperti `cmd --flag -- --notaflag`. `--` adalah argumen khusus yang memberi tahu program untuk berhenti mengurai flag. Semua yang setelah `--` diperlakukan sebagai argumen positional. Mengapa ini bisa berguna? Coba jalankan `touch -- -myfile` lalu hapus berkas tersebut tanpa `--`.

1. Baca [`man ls`](https://www.man7.org/linux/man-pages/man1/ls.1.html) dan tulis perintah `ls` yang mencantumkan berkas dengan cara berikut:
    - Menyertakan semua berkas, termasuk berkas tersembunyi
    - Ukuran dicantumkan dalam format yang mudah dibaca manusia (misalnya 454M alih-alih 454279954)
    - Berkas diurutkan berdasarkan kebaruan
    - Output diberi warna

    Contoh output akan terlihat seperti ini:

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

1. Process substitution `<(command)` memungkinkan Anda menggunakan output sebuah perintah seolah-olah itu adalah berkas. Gunakan `diff` dengan process substitution untuk membandingkan output `printenv` dan `export`. Mengapa keduanya berbeda? (Petunjuk: coba `diff <(printenv | sort) <(export | sort)`).

## Environment Variables

1. Tulis fungsi bash `marco` dan `polo` yang melakukan hal berikut: setiap kali Anda mengeksekusi `marco` current working directory harus disimpan dengan cara tertentu, lalu ketika Anda mengeksekusi `polo`, di direktori mana pun Anda berada, `polo` harus melakukan `cd` kembali ke direktori tempat Anda mengeksekusi `marco`. Untuk memudahkan debugging Anda dapat menulis kodenya di berkas `marco.sh` dan (memuat ulang) definisinya ke shell Anda dengan mengeksekusi `source marco.sh`.

{% comment %}
marco() {
    export MARCO=$(pwd)
}

polo() {
    cd "$MARCO"
}
{% endcomment %}

## Return Codes

1. Misalkan Anda memiliki perintah yang jarang gagal. Untuk men-debug-nya Anda perlu menangkap outputnya tetapi mendapatkan eksekusi yang gagal bisa memakan waktu. Tulis skrip bash yang menjalankan skrip berikut sampai gagal dan menangkap stream standard output serta error-nya ke berkas dan mencetak semuanya di akhir. Poin bonus jika Anda juga dapat melaporkan berapa banyak eksekusi yang diperlukan hingga skrip gagal.

    ```bash
    #!/usr/bin/env bash

    n=$(( RANDOM % 100 ))

    if [[ $n -eq 42 ]]; then
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

## Signal dan Job Control

1. Mulai job `sleep 10000` di terminal, background-kan dengan `Ctrl-Z` dan lanjutkan eksekusinya dengan `bg`. Sekarang gunakan [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) untuk menemukan pid-nya dan [`pkill`](https://man7.org/linux/man-pages/man1/pgrep.1.html) untuk mematikannya tanpa pernah mengetik pid itu sendiri. (Petunjuk: gunakan flag `-lf`).

1. Misalkan Anda tidak ingin memulai sebuah proses sampai proses lain selesai. Bagaimana Anda melakukannya? Pada latihan ini, proses pembatas kita akan selalu `sleep 60 &`. Salah satu cara untuk mencapainya adalah menggunakan perintah [`wait`](https://www.man7.org/linux/man-pages/man1/wait.1p.html). Coba jalankan perintah sleep dan buat `ls` menunggu sampai proses background selesai.

    Namun, strategi ini akan gagal jika kita memulai di sesi bash yang berbeda, karena `wait` hanya berfungsi untuk child process. Satu fitur yang tidak kita bahas di catatan adalah bahwa exit status perintah `kill` akan bernilai nol jika berhasil dan bukan nol jika sebaliknya. `kill -0` tidak mengirim sinyal tetapi akan memberikan exit status bukan nol jika proses tidak ada. Tulis fungsi bash bernama `pidwait` yang menerima sebuah pid dan menunggu sampai proses yang diberikan selesai. Anda sebaiknya menggunakan `sleep` agar tidak membuang CPU secara tidak perlu.

## Berkas dan Permission

1. (Advanced) Tulis perintah atau skrip untuk menemukan berkas yang paling baru dimodifikasi di sebuah direktori secara rekursif. Lebih umum, dapatkah Anda mencantumkan semua berkas berdasarkan kebaruan?

## Terminal Multiplexers

1. Ikuti [tutorial](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) `tmux` ini lalu pelajari cara melakukan beberapa kustomisasi dasar mengikuti [langkah-langkah ini](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/).

## Alias dan Dotfiles

1. Buat alias `dc` yang bermuara ke `cd` untuk saat Anda salah mengetiknya.

1. Jalankan `history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10` untuk mendapatkan 10 perintah paling sering Anda gunakan dan pertimbangkan menulis alias yang lebih pendek untuk perintah tersebut. Catatan: ini berfungsi untuk Bash; jika Anda menggunakan ZSH, gunakan `history 1` alih-alih hanya `history`.

1. Buat folder untuk dotfiles Anda dan siapkan version control.

1. Tambahkan konfigurasi untuk setidaknya satu program, misalnya shell Anda, dengan sedikit kustomisasi (untuk memulai, bisa sesuatu yang sesederhana menyesuaikan prompt shell Anda dengan menetapkan `$PS1`).

1. Siapkan metode untuk memasang dotfiles Anda dengan cepat (dan tanpa usaha manual) di mesin baru. Ini bisa sesederhana skrip shell yang memanggil `ln -s` untuk setiap berkas, atau Anda dapat menggunakan [utility khusus](https://dotfiles.github.io/utilities/).

1. Uji skrip pemasangan Anda pada virtual machine yang baru.

1. Migrasikan semua konfigurasi tool Anda saat ini ke repositori dotfiles Anda.

1. Publikasikan dotfiles Anda di GitHub.

## Mesin Jarak Jauh (SSH)

Pasang Linux virtual machine (atau gunakan yang sudah ada) untuk latihan-latihan ini. Jika Anda belum familiar dengan virtual machine, lihat [ini](https://hibbard.eu/install-ubuntu-virtual-box/) tutorial untuk memasangnya.

1. Buka `~/.ssh/` dan periksa apakah Anda memiliki pasangan SSH key di sana. Jika tidak, hasilkan dengan `ssh-keygen -a 100 -t ed25519`. Disarankan Anda menggunakan password dan menggunakan `ssh-agent`, info lebih lanjut [di sini](https://www.ssh.com/ssh/agent).

1. Edit `.ssh/config` agar memiliki entri sebagai berikut:

    ```bash
    Host vm
        User username_goes_here
        HostName ip_goes_here
        IdentityFile ~/.ssh/id_ed25519
        LocalForward 9999 localhost:8888
    ```

1. Gunakan `ssh-copy-id vm` untuk menyalin ssh key Anda ke server.

1. Mulai webserver di VM Anda dengan mengeksekusi `python -m http.server 8888`. Akses webserver VM dengan bernavigasi ke `http://localhost:9999` di mesin Anda.

1. Edit konfigurasi server SSH Anda dengan melakukan `sudo vim /etc/ssh/sshd_config` dan nonaktifkan autentikasi password dengan mengedit nilai `PasswordAuthentication`. Nonaktifkan login root dengan mengedit nilai `PermitRootLogin`. Restart layanan `ssh` dengan `sudo service sshd restart`. Coba ssh masuk lagi.

1. (Challenge) Pasang [`mosh`](https://mosh.org/) di VM dan bangun koneksi. Lalu putuskan network adapter server/VM tersebut. Dapatkah mosh pulih dengan benar?

1. (Challenge) Telaah apa fungsi flag `-N` dan `-f` pada `ssh` dan cari tahu perintah untuk mencapai background port forwarding.
