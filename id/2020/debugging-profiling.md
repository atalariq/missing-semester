---
layout: lecture-id
title: "Debugging dan Profiling"
description: >
  Pelajari cara men-debug program menggunakan logging, debugger, dan static analysis, serta melakukan profiling kode untuk mengukur performa.
thumbnail: /static/assets/thumbnails/2020/lec7.png
date: 2020-01-23
ready: true
video:
  aspect: 56.25
  id: l812pUnKxME
lang: id
permalink: /id/2020/debugging-profiling/
---

Aturan emas dalam pemrograman adalah kode tidak melakukan apa yang Anda harapkan, tetapi melakukan apa yang Anda perintahkan.
Menjembatani kesenjangan itu kadang bisa menjadi pencapaian yang cukup sulit.
Pada kuliah ini kita akan membahas teknik berguna untuk menangani kode yang buggy dan boros sumber daya: debugging dan profiling.

# Debugging

## Printf debugging dan Logging

"Alat debugging yang paling efektif tetaplah pemikiran yang cermat, dipadukan dengan pernyataan print yang ditempatkan secara tepat" — Brian Kernighan, _Unix for Beginners_.

Pendekatan pertama untuk men-debug program adalah menambahkan pernyataan print di sekitar tempat Anda mendeteksi masalah, dan terus mengiterasi sampai Anda memperoleh cukup informasi untuk memahami apa yang bertanggung jawab atas masalah tersebut.

Pendekatan kedua adalah menggunakan logging di program Anda, alih-alih pernyataan print ad hoc. Logging lebih baik daripada pernyataan print biasa karena beberapa alasan:

- Anda dapat melakukan log ke berkas, socket, atau bahkan server jarak jauh alih-alih ke standard output.
- Logging mendukung severity level (seperti INFO, DEBUG, WARN, ERROR, &c), yang memungkinkan Anda memfilter output sesuai dengan level tersebut.
- Untuk masalah baru, ada kemungkinan besar log Anda memuat cukup informasi untuk mendeteksi apa yang salah.

[Di sini](/static/files/logger.py) ada contoh kode yang melakukan log pesan:

```bash
$ python logger.py
# Raw output as with just prints
$ python logger.py log
# Log formatted output
$ python logger.py log ERROR
# Print only ERROR levels and above
$ python logger.py color
# Color formatted output
```

Salah satu tip favorit saya untuk membuat log lebih mudah dibaca adalah memberinya color code.
Saat ini Anda mungkin telah menyadari bahwa terminal Anda menggunakan warna agar lebih mudah dibaca. Tetapi bagaimana caranya?
Program seperti `ls` atau `grep` menggunakan [ANSI escape code](https://en.wikipedia.org/wiki/ANSI_escape_code), yaitu rangkaian karakter khusus untuk memberi tahu shell Anda mengubah warna output. Misalnya, mengeksekusi `echo -e "\e[38;2;255;0;0mThis is red\e[0m"` mencetak pesan `This is red` dalam warna merah di terminal Anda, selama terminal mendukung [true color](https://github.com/termstandard/colors#truecolor-support-in-output-devices). Jika terminal Anda tidak mendukungnya (misalnya Terminal.app di macOS), Anda dapat menggunakan escape code yang lebih universal untuk 16 pilihan warna, misalnya `echo -e "\e[31;1mThis is red\e[0m"`.

Skrip berikut menunjukkan cara mencetak banyak warna RGB ke terminal Anda (lagi-lagi, selama terminal mendukung true color).

```bash
#!/usr/bin/env bash
for R in $(seq 0 20 255); do
    for G in $(seq 0 20 255); do
        for B in $(seq 0 20 255); do
            printf "\e[38;2;${R};${G};${B}m█\e[0m";
        done
    done
done
```

## Log pihak ketiga

Saat Anda mulai membangun sistem perangkat lunak yang lebih besar, kemungkinan besar Anda akan menemui dependency yang berjalan sebagai program terpisah.
Web server, database, atau message broker adalah contoh umum dependency semacam ini.
Saat berinteraksi dengan sistem tersebut sering kali perlu membaca log-nya, karena pesan error di sisi klien mungkin tidak memadai.

Untungnya, sebagian besar program menulis log-nya sendiri di suatu tempat di sistem Anda.
Pada sistem UNIX, adalah hal umum bagi program menulis log-nya di bawah `/var/log`.
Misalnya, webserver [NGINX](https://www.nginx.com/) menempatkan log-nya di bawah `/var/log/nginx`.
Belakangan ini, sistem mulai menggunakan **system log**, yang semakin menjadi tempat semua pesan log Anda pergi.
Sebagian besar (tetapi tidak semua) sistem Linux menggunakan `systemd`, daemon sistem yang mengendalikan banyak hal di sistem Anda seperti layanan mana yang diaktifkan dan berjalan.
`systemd` menempatkan log di bawah `/var/log/journal` dalam format khusus dan Anda dapat menggunakan perintah [`journalctl`](https://www.man7.org/linux/man-pages/man1/journalctl.1.html) untuk menampilkan pesannya.
Demikian pula, di macOS masih ada `/var/log/system.log` tetapi semakin banyak tool menggunakan system log, yang dapat ditampilkan dengan [`log show`](https://www.manpagez.com/man/1/log/).
Pada sebagian besar sistem UNIX Anda juga dapat menggunakan perintah [`dmesg`](https://www.man7.org/linux/man-pages/man1/dmesg.1.html) untuk mengakses log kernel.

Untuk melakukan logging di bawah system log Anda dapat menggunakan program shell [`logger`](https://www.man7.org/linux/man-pages/man1/logger.1.html).
Berikut contoh penggunaan `logger` dan cara memeriksa bahwa entri tersebut sampai ke system log.
Lebih jauh lagi, sebagian besar bahasa pemrograman memiliki binding untuk melakukan logging ke system log.

```bash
logger "Hello Logs"
# On macOS
log show --last 1m | grep Hello
# On Linux
journalctl --since "1m ago" | grep Hello
```

Seperti yang kita lihat pada kuliah data wrangling, log bisa cukup verbose dan memerlukan beberapa tingkat pemrosesan serta filter untuk memperoleh informasi yang Anda inginkan.
Jika Anda mendapati diri Anda melakukan filter berat melalui `journalctl` dan `log show`, Anda dapat mempertimbangkan menggunakan flag-nya, yang dapat melakukan pemeriksaan filter pertama pada outputnya.
Ada juga beberapa tool seperti  [`lnav`](https://lnav.org/), yang menyediakan penyajian dan navigasi log yang lebih baik.

## Debuggers

Ketika printf debugging tidak cukup, Anda sebaiknya menggunakan debugger.
Debugger adalah program yang memungkinkan Anda berinteraksi dengan eksekusi sebuah program, memungkinkan hal berikut:

- Menghentikan eksekusi program ketika mencapai baris tertentu.
- Melangkah melalui program satu instruksi sekaligus.
- Memeriksa nilai variabel setelah program crash.
- Menghentikan eksekusi secara kondisional ketika kondisi tertentu terpenuhi.
- Dan banyak fitur lanjutan lainnya

Banyak bahasa pemrograman dilengkapi dengan semacam debugger.
Di Python ini adalah Python Debugger [`pdb`](https://docs.python.org/3/library/pdb.html).

Berikut deskripsi singkat beberapa perintah yang didukung `pdb`:

- **l**(ist) - Menampilkan 11 baris di sekitar baris saat ini atau melanjutkan pencantuman sebelumnya.
- **s**(tep) - Mengeksekusi baris saat ini, berhenti pada kesempatan pertama yang memungkinkan.
- **n**(ext) - Melanjutkan eksekusi sampai baris berikutnya dalam fungsi saat ini tercapai atau fungsi kembali.
- **b**(reak) - Menetapkan breakpoint (tergantung argumen yang diberikan).
- **p**(rint) - Mengevaluasi ekspresi dalam konteks saat ini dan mencetak nilainya. Ada juga **pp** untuk menampilkan menggunakan [`pprint`](https://docs.python.org/3/library/pprint.html) sebagai gantinya.
- **r**(eturn) - Melanjutkan eksekusi sampai fungsi saat ini kembali.
- **q**(uit) - Keluar dari debugger.

Mari telusuri contoh penggunaan `pdb` untuk memperbaiki kode python buggy berikut. (Lihat video kuliah).

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n):
            if arr[j] > arr[j+1]:
                arr[j] = arr[j+1]
                arr[j+1] = arr[j]
    return arr

print(bubble_sort([4, 2, 1, 8, 7, 6]))
```


Perhatikan bahwa karena Python adalah bahasa terinterpretasi kita dapat menggunakan shell `pdb` untuk mengeksekusi perintah dan mengeksekusi instruksi.
[`ipdb`](https://pypi.org/project/ipdb/) adalah `pdb` yang ditingkatkan yang menggunakan REPL [`IPython`](https://ipython.org) sehingga memungkinkan tab completion, syntax highlighting, traceback yang lebih baik, dan introspeksi yang lebih baik sambil mempertahankan antarmuka yang sama dengan module `pdb`.

Untuk pemrograman yang lebih low level Anda mungkin ingin menelaah [`gdb`](https://www.gnu.org/software/gdb/) (dan modifikasi kualitas hidupnya [`pwndbg`](https://github.com/pwndbg/pwndbg)) serta [`lldb`](https://lldb.llvm.org/).
Keduanya dioptimalkan untuk debugging bahasa mirip C tetapi akan memungkinkan Anda menyelidiki hampir semua proses dan memperoleh state mesin saat ini: register, stack, program counter, &c.


## Tool Khusus

Bahkan jika yang Anda coba debug adalah binary black box, ada tool yang dapat membantu Anda.
Setiap kali program perlu melakukan aksi yang hanya dapat dilakukan kernel, program menggunakan [System Call](https://en.wikipedia.org/wiki/System_call).
Ada perintah yang memungkinkan Anda melacak syscall yang dilakukan program Anda. Di Linux ada [`strace`](https://www.man7.org/linux/man-pages/man1/strace.1.html) dan macOS serta BSD memiliki [`dtrace`](https://dtrace.org/about/). `dtrace` bisa rumit digunakan karena menggunakan bahasa `D`-nya sendiri, tetapi ada wrapper bernama [`dtruss`](https://www.manpagez.com/man/1/dtruss/) yang menyediakan antarmuka lebih mirip `strace` (detail lebih lanjut [di sini](https://8thlight.com/blog/colin-jones/2015/11/06/dtrace-even-better-than-strace-for-osx.html)).

Berikut beberapa contoh penggunaan `strace` atau `dtruss` untuk menampilkan jejak syscall [`stat`](https://www.man7.org/linux/man-pages/man2/stat.2.html) untuk eksekusi `ls`. Untuk menyelami `strace` lebih dalam, [artikel ini](https://blogs.oracle.com/linux/strace-the-sysadmins-microscope-v2) dan [zine ini](https://jvns.ca/strace-zine-unfolded.pdf) adalah bacaan yang baik.

```bash
# On Linux
sudo strace -e lstat ls -l > /dev/null
# On macOS
sudo dtruss -t lstat64_extended ls -l > /dev/null
```

Dalam beberapa keadaan, Anda mungkin perlu melihat paket jaringan untuk mencari tahu masalah di program Anda.
Tool seperti [`tcpdump`](https://www.man7.org/linux/man-pages/man1/tcpdump.1.html) dan [Wireshark](https://www.wireshark.org/) adalah penganalisis paket jaringan yang memungkinkan Anda membaca isi paket jaringan dan memfilternya berdasarkan kriteria berbeda.

Untuk pengembangan web, developer tool Chrome/Firefox cukup berguna. Tool tersebut memiliki banyak fitur, termasuk:
- Source code - Memeriksa kode sumber HTML/CSS/JS situs web apa pun.
- Live HTML, CSS, JS modification - Mengubah konten, gaya, dan perilaku situs web untuk pengujian (Anda dapat melihat sendiri bahwa tangkapan layar situs web bukan bukti yang sah).
- Javascript shell - Mengeksekusi perintah di REPL JS.
- Network - Menganalisis timeline permintaan.
- Storage - Memeriksa Cookie dan penyimpanan aplikasi lokal.

## Static Analysis

Untuk sebagian masalah Anda tidak perlu menjalankan kode apa pun.
Misalnya, hanya dengan melihat sebuah potongan kode dengan cermat Anda dapat menyadari bahwa variabel loop Anda menutupi (shadowing) nama variabel atau fungsi yang sudah ada; atau bahwa sebuah program membaca variabel sebelum mendefinisikannya.
Di sinilah tool [static analysis](https://en.wikipedia.org/wiki/Static_program_analysis) berperan.
Program static analysis menerima kode sumber sebagai input dan menganalisisnya menggunakan aturan pengkodean untuk menalar kebenarannya.

Pada potongan Python berikut ada beberapa kesalahan.
Pertama, variabel loop kita `foo` menutupi definisi sebelumnya dari fungsi `foo`. Kita juga menulis `baz` alih-alih `bar` pada baris terakhir, sehingga program akan crash setelah menyelesaikan pemanggilan `sleep` (yang akan memakan waktu satu menit).

```python
import time

def foo():
    return 42

for foo in range(5):
    print(foo)
bar = 1
bar *= 0.2
time.sleep(60)
print(baz)
```

Tool static analysis dapat mengidentifikasi masalah semacam ini. Ketika kita menjalankan [`pyflakes`](https://pypi.org/project/pyflakes) pada kode tersebut kita mendapatkan error yang terkait dengan kedua bug tersebut. [`mypy`](https://mypy-lang.org/) adalah tool lain yang dapat mendeteksi masalah type checking. Di sini, `mypy` akan memperingatkan kita bahwa `bar` awalnya bertipe `int` lalu di-cast menjadi `float`.
Sekali lagi, perhatikan bahwa semua masalah ini terdeteksi tanpa perlu menjalankan kodenya.

```bash
$ pyflakes foobar.py
foobar.py:6: redefinition of unused 'foo' from line 3
foobar.py:11: undefined name 'baz'

$ mypy foobar.py
foobar.py:6: error: Incompatible types in assignment (expression has type "int", variable has type "Callable[[], Any]")
foobar.py:9: error: Incompatible types in assignment (expression has type "float", variable has type "int")
foobar.py:11: error: Name 'baz' is not defined
Found 3 errors in 1 file (checked 1 source file)
```

Pada kuliah shell tools kita membahas [`shellcheck`](https://www.shellcheck.net/), yang merupakan tool serupa untuk skrip shell.

Sebagian besar editor dan IDE mendukung penampilan output tool ini di dalam editor itu sendiri, menyorot lokasi peringatan dan error.
Ini sering disebut **code linting** dan juga dapat digunakan untuk menampilkan jenis masalah lain seperti pelanggaran gaya atau konstruksi yang tidak aman.

Di vim, plugin [`ale`](https://vimawesome.com/plugin/ale) atau [`syntastic`](https://vimawesome.com/plugin/syntastic) memungkinkan Anda melakukan itu.
Untuk Python, [`pylint`](https://github.com/PyCQA/pylint) dan [`pep8`](https://pypi.org/project/pep8/) adalah contoh linter gaya dan [`bandit`](https://pypi.org/project/bandit/) adalah tool yang dirancang untuk menemukan masalah keamanan umum.
Untuk bahasa lain orang telah menyusun daftar komprehensif tool static analysis yang berguna, seperti [Awesome Static Analysis](https://github.com/mre/awesome-static-analysis) (Anda mungkin ingin melihat bagian _Writing_) dan untuk linter ada [Awesome Linters](https://github.com/caramelomartins/awesome-linters).

Tool pelengkap untuk linting gaya adalah code formatter seperti [`black`](https://github.com/psf/black) untuk Python, `gofmt` untuk Go, `rustfmt` untuk Rust atau [`prettier`](https://prettier.io/) untuk JavaScript, HTML dan CSS.
Tool ini memformat kode Anda secara otomatis agar konsisten dengan pola gaya umum untuk bahasa pemrograman tersebut.
Meskipun Anda mungkin enggan menyerahkan kendali gaya atas kode Anda, menstandarkan format kode akan membantu orang lain membaca kode Anda dan akan membuat Anda lebih baik dalam membaca kode orang lain (yang distandarkan secara gaya).

# Profiling

Bahkan jika kode Anda berperilaku secara fungsional seperti yang Anda harapkan, itu mungkin belum cukup baik jika kode tersebut menghabiskan seluruh CPU atau memori Anda dalam prosesnya.
Kelas algoritma sering mengajarkan notasi big _O_ tetapi tidak mengajarkan cara menemukan hot spot pada program Anda.
Karena [optimasi yang terlalu dini adalah akar segala masalah](https://wiki.c2.com/?PrematureOptimization), Anda sebaiknya mempelajari profiler dan tool monitoring. Tool tersebut akan membantu Anda memahami bagian program mana yang menghabiskan sebagian besar waktu dan/atau sumber daya sehingga Anda dapat memfokuskan upaya mengoptimalkan bagian tersebut.

<a id="timing"></a>
## Pengukuran Waktu

Serupa dengan kasus debugging, dalam banyak skenario cukup dengan mencetak waktu yang dibutuhkan kode Anda antara dua titik.
Berikut contoh di Python menggunakan module [`time`](https://docs.python.org/3/library/time.html).

```python
import time, random
n = random.randint(1, 10) * 100

# Get current time
start = time.time()

# Do some work
print("Sleeping for {} ms".format(n))
time.sleep(n/1000)

# Compute time between start and now
print(time.time() - start)

# Output
# Sleeping for 500 ms
# 0.5713930130004883
```

Namun, wall clock time bisa menyesatkan karena komputer Anda mungkin menjalankan proses lain pada waktu yang sama atau menunggu peristiwa terjadi. Adalah hal umum bagi tool untuk membedakan antara waktu _Real_, _User_ dan _Sys_. Secara umum, _User_ + _Sys_ memberi tahu Anda berapa banyak waktu yang sebenarnya dihabiskan proses Anda di CPU (penjelasan lebih detail [di sini](https://stackoverflow.com/questions/556405/what-do-real-user-and-sys-mean-in-the-output-of-time1)).

- _Real_ - Waktu wall clock yang berlalu dari awal sampai selesai program, termasuk waktu yang diambil proses lain dan waktu saat terblokir (misalnya menunggu I/O atau jaringan)
- _User_ - Jumlah waktu yang dihabiskan di CPU untuk menjalankan kode pengguna
- _Sys_ - Jumlah waktu yang dihabiskan di CPU untuk menjalankan kode kernel

Misalnya, coba jalankan perintah yang melakukan permintaan HTTP dan awali dengan [`time`](https://www.man7.org/linux/man-pages/man1/time.1.html). Pada koneksi lambat Anda mungkin mendapatkan output seperti di bawah ini. Di sini dibutuhkan lebih dari 2 detik untuk menyelesaikan permintaan tetapi prosesnya hanya memakan 15ms waktu CPU user dan 12ms waktu CPU kernel.

```bash
$ time curl https://missing.csail.mit.edu &> /dev/null
real    0m2.561s
user    0m0.015s
sys     0m0.012s
```

## Profilers

### CPU

Sebagian besar waktu ketika orang menyebut _profiler_ yang mereka maksud sebenarnya adalah _CPU profiler_, yang paling umum.
Ada dua jenis utama CPU profiler: profiler _tracing_ dan _sampling_.
Tracing profiler menyimpan catatan setiap pemanggilan fungsi yang dilakukan program Anda sedangkan sampling profiler menyelidiki program Anda secara berkala (umumnya setiap milidetik) dan mencatat stack program.
Profiler menggunakan catatan ini untuk menyajikan statistik agregat tentang apa yang paling banyak menghabiskan waktu program Anda.
[Di sini](https://jvns.ca/blog/2017/12/17/how-do-ruby---python-profilers-work-) ada artikel pengantar yang baik jika Anda ingin detail lebih lanjut tentang topik ini.

Sebagian besar bahasa pemrograman memiliki semacam profiler command line yang dapat Anda gunakan untuk menganalisis kode Anda.
Profiler sering terintegrasi dengan IDE lengkap tetapi untuk kuliah ini kami akan memfokuskan pada tool command line itu sendiri.

Di Python kita dapat menggunakan module `cProfile` untuk memprofil waktu per pemanggilan fungsi. Berikut contoh sederhana yang mengimplementasikan grep sederhana di Python:

```python
#!/usr/bin/env python

import sys, re

def grep(pattern, file):
    with open(file, 'r') as f:
        print(file)
        for i, line in enumerate(f.readlines()):
            pattern = re.compile(pattern)
            match = pattern.search(line)
            if match is not None:
                print("{}: {}".format(i, line), end="")

if __name__ == '__main__':
    times = int(sys.argv[1])
    pattern = sys.argv[2]
    for i in range(times):
        for file in sys.argv[3:]:
            grep(pattern, file)
```

Kita dapat memprofil kode ini menggunakan perintah berikut. Menganalisis outputnya kita dapat melihat bahwa IO menghabiskan sebagian besar waktu dan bahwa mengompilasi regex juga memakan waktu cukup banyak. Karena regex hanya perlu dikompilasi sekali, kita dapat memfaktorkannya keluar dari loop for.

```
$ python -m cProfile -s tottime grep.py 1000 '^(import|\s*def)[^,]*$' *.py

[omitted program output]

 ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     8000    0.266    0.000    0.292    0.000 {built-in method io.open}
     8000    0.153    0.000    0.894    0.000 grep.py:5(grep)
    17000    0.101    0.000    0.101    0.000 {built-in method builtins.print}
     8000    0.100    0.000    0.129    0.000 {method 'readlines' of '_io._IOBase' objects}
    93000    0.097    0.000    0.111    0.000 re.py:286(_compile)
    93000    0.069    0.000    0.069    0.000 {method 'search' of '_sre.SRE_Pattern' objects}
    93000    0.030    0.000    0.141    0.000 re.py:231(compile)
    17000    0.019    0.000    0.029    0.000 codecs.py:318(decode)
        1    0.017    0.017    0.911    0.911 grep.py:3(<module>)

[omitted lines]
```


Satu catatan penting tentang profiler `cProfile` Python (dan banyak profiler serupa) adalah mereka menampilkan waktu per pemanggilan fungsi. Itu bisa menjadi tidak intuitif dengan sangat cepat, terutama jika Anda menggunakan library pihak ketiga dalam kode Anda karena pemanggilan fungsi internal juga diperhitungkan.
Cara yang lebih intuitif untuk menampilkan informasi profiling adalah dengan menyertakan waktu yang dihabiskan per baris kode, yang merupakan apa yang dilakukan _line profiler_.

Misalnya, potongan kode Python berikut melakukan permintaan ke situs kelas dan mengurai respons untuk mendapatkan semua URL di halaman:

```python
#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

# This is a decorator that tells line_profiler
# that we want to analyze this function
@profile
def get_urls():
    response = requests.get('https://missing.csail.mit.edu')
    s = BeautifulSoup(response.content, 'lxml')
    urls = []
    for url in s.find_all('a'):
        urls.append(url['href'])

if __name__ == '__main__':
    get_urls()
```

Jika kita menggunakan profiler `cProfile` Python kita akan mendapatkan lebih dari 2500 baris output, dan bahkan dengan pengurutan akan sulit memahami di mana waktu dihabiskan. Sekali jalan dengan [`line_profiler`](https://github.com/pyutils/line_profiler) menunjukkan waktu yang diambil per baris:

```bash
$ kernprof -l -v a.py
Wrote profile results to urls.py.lprof
Timer unit: 1e-06 s

Total time: 0.636188 s
File: a.py
Function: get_urls at line 5

Line #  Hits         Time  Per Hit   % Time  Line Contents
==============================================================
 5                                           @profile
 6                                           def get_urls():
 7         1     613909.0 613909.0     96.5      response = requests.get('https://missing.csail.mit.edu')
 8         1      21559.0  21559.0      3.4      s = BeautifulSoup(response.content, 'lxml')
 9         1          2.0      2.0      0.0      urls = []
10        25        685.0     27.4      0.1      for url in s.find_all('a'):
11        24         33.0      1.4      0.0          urls.append(url['href'])
```

### Memori

Pada bahasa seperti C atau C++ memory leak dapat menyebabkan program Anda tidak pernah melepaskan memori yang tidak dibutuhkannya lagi.
Untuk membantu proses memory debugging Anda dapat menggunakan tool seperti [Valgrind](https://valgrind.org/) yang akan membantu Anda mengidentifikasi memory leak.

Pada bahasa dengan garbage collection seperti Python masih berguna menggunakan memory profiler karena selama Anda memiliki pointer ke objek di memori, objek tersebut tidak akan di-garbage collect.
Berikut contoh program dan output terkait saat menjalankannya dengan [memory-profiler](https://pypi.org/project/memory-profiler/) (perhatikan decorator seperti pada `line-profiler`).

```python
@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    my_func()
```

```bash
$ python -m memory_profiler example.py
Line #    Mem usage  Increment   Line Contents
==============================================
     3                           @profile
     4      5.97 MB    0.00 MB   def my_func():
     5     13.61 MB    7.64 MB       a = [1] * (10 ** 6)
     6    166.20 MB  152.59 MB       b = [2] * (2 * 10 ** 7)
     7     13.61 MB -152.59 MB       del b
     8     13.61 MB    0.00 MB       return a
```

### Event Profiling

Seperti halnya `strace` untuk debugging, Anda mungkin ingin mengabaikan detail kode yang Anda jalankan dan memperlakukannya seperti black box saat melakukan profiling.
Perintah [`perf`](https://www.man7.org/linux/man-pages/man1/perf.1.html) mengabstraksi perbedaan CPU dan tidak melaporkan waktu atau memori, tetapi melaporkan peristiwa sistem yang terkait dengan program Anda.
Misalnya, `perf` dapat dengan mudah melaporkan locality cache yang buruk, jumlah page fault yang tinggi atau livelock. Berikut gambaran umum perintahnya:

- `perf list` - Mencantumkan peristiwa yang dapat dilacak dengan perf
- `perf stat COMMAND ARG1 ARG2` - Mendapatkan hitungan berbagai peristiwa yang terkait dengan sebuah proses atau perintah
- `perf record COMMAND ARG1 ARG2` - Merekam eksekusi sebuah perintah dan menyimpan data statistik ke berkas bernama `perf.data`
- `perf report` - Memformat dan mencetak data yang dikumpulkan di `perf.data`


### Visualisasi

Output profiler untuk program dunia nyata akan memuat informasi dalam jumlah besar karena kompleksitas proyek perangkat lunak yang melekat.
Manusia adalah makhluk visual dan cukup buruk dalam membaca angka dalam jumlah besar dan memahaminya.
Dengan demikian ada banyak tool untuk menampilkan output profiler dengan cara yang lebih mudah diurai.

Salah satu cara umum menampilkan informasi CPU profiling untuk sampling profiler adalah menggunakan [Flame Graph](https://www.brendangregg.com/flamegraphs.html), yang akan menampilkan hierarki pemanggilan fungsi pada sumbu Y dan waktu yang dihabiskan secara proporsional pada sumbu X. Grafik ini juga interaktif, memungkinkan Anda memperbesar bagian tertentu dari program dan memperoleh stack trace-nya (coba klik pada gambar di bawah).

[![FlameGraph](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)

Call graph atau control flow graph menampilkan hubungan antara subroutine di dalam sebuah program dengan menyertakan fungsi sebagai node dan pemanggilan fungsi di antaranya sebagai edge berarah. Ketika digabungkan dengan informasi profiling seperti jumlah pemanggilan dan waktu yang diambil, call graph bisa sangat berguna untuk menafsirkan alur sebuah program.
Di Python Anda dapat menggunakan library [`pycallgraph`](https://pycallgraph.readthedocs.io/) untuk menghasilkannya.

![Call Graph](https://upload.wikimedia.org/wikipedia/commons/2/2f/A_Call_Graph_generated_by_pycallgraph.png)


## Resource Monitoring

Kadang, langkah pertama menuju analisis performa program Anda adalah memahami konsumsi sumber daya aktualnya.
Program sering berjalan lambat ketika sumber dayanya terbatas, misalnya tanpa memori yang cukup atau pada koneksi jaringan yang lambat.
Ada banyak sekali tool command line untuk menyelidiki dan menampilkan berbagai sumber daya sistem seperti penggunaan CPU, penggunaan memori, jaringan, penggunaan disk, dan sebagainya.

- **Monitoring umum** - Mungkin yang paling populer adalah [`htop`](https://htop.dev/), yang merupakan versi [`top`](https://www.man7.org/linux/man-pages/man1/top.1.html) yang ditingkatkan.
`htop` menyajikan berbagai statistik untuk proses yang sedang berjalan di sistem. `htop` memiliki banyak sekali opsi dan keybind, beberapa yang berguna adalah: `<F6>` untuk mengurutkan proses, `t` untuk menampilkan hierarki tree dan `h` untuk menampilkan/menyembunyikan thread.
Lihat juga [`glances`](https://nicolargo.github.io/glances/) untuk implementasi serupa dengan UI yang hebat. Untuk memperoleh ukuran agregat di semua proses, [`dool`](https://github.com/scottchiefbaker/dool) adalah tool rapi lain yang menghitung metrik sumber daya real-time untuk banyak subsistem berbeda seperti I/O, networking, penggunaan CPU, context switch, &c.
- **Operasi I/O** - [`iotop`](https://www.man7.org/linux/man-pages/man8/iotop.8.html) menampilkan informasi penggunaan I/O secara langsung dan berguna untuk memeriksa apakah sebuah proses melakukan operasi disk I/O yang berat
- **Penggunaan Disk** - [`df`](https://www.man7.org/linux/man-pages/man1/df.1.html) menampilkan metrik per partisi dan [`du`](https://man7.org/linux/man-pages/man1/du.1.html) menampilkan **d**isk **u**sage per berkas untuk direktori saat ini. Pada tool ini flag `-h` memberi tahu program untuk mencetak dengan format yang mudah dibaca **h**uman.
Versi `du` yang lebih interaktif adalah [`ncdu`](https://dev.yorhel.nl/ncdu) yang memungkinkan Anda bernavigasi antar folder dan menghapus berkas serta folder saat bernavigasi.
- **Penggunaan Memori** - [`free`](https://www.man7.org/linux/man-pages/man1/free.1.html) menampilkan jumlah total memori bebas dan terpakai di sistem. Memori juga ditampilkan pada tool seperti `htop`.
- **Berkas terbuka** - [`lsof`](https://www.man7.org/linux/man-pages/man8/lsof.8.html)  mencantumkan informasi berkas tentang berkas yang dibuka oleh proses. Ini bisa sangat berguna untuk memeriksa proses mana yang membuka berkas tertentu.
- **Koneksi dan Konfigurasi Jaringan** - [`ss`](https://www.man7.org/linux/man-pages/man8/ss.8.html) memungkinkan Anda memantau statistik paket jaringan masuk dan keluar serta statistik antarmuka. Use case umum `ss` adalah mencari tahu proses apa yang menggunakan port tertentu di mesin. Untuk menampilkan routing, perangkat jaringan dan antarmuka Anda dapat menggunakan [`ip`](https://man7.org/linux/man-pages/man8/ip.8.html). Perhatikan bahwa `netstat` dan `ifconfig` telah deprecated dan digantikan oleh tool tersebut masing-masing.
- **Penggunaan Jaringan** -  [`nethogs`](https://github.com/raboof/nethogs) dan [`iftop`](https://pdw.ex-parrot.com/iftop/) adalah tool CLI interaktif yang baik untuk memantau penggunaan jaringan.

Jika Anda ingin menguji tool ini Anda juga dapat secara artifisial membebani mesin menggunakan perintah [`stress`](https://linux.die.net/man/1/stress).


### Tool khusus

Kadang, black box benchmarking adalah semua yang Anda butuhkan untuk menentukan perangkat lunak mana yang digunakan.
Tool seperti [`hyperfine`](https://github.com/sharkdp/hyperfine) memungkinkan Anda melakukan benchmark program command line dengan cepat.
Misalnya, pada kuliah shell tools dan scripting kami merekomendasikan `fd` alih-alih `find`. Kita dapat menggunakan `hyperfine` untuk membandingkannya pada tugas yang sering kita jalankan.
Misalnya pada contoh di bawah `fd` 20x lebih cepat daripada `find` di mesin saya.

```bash
$ hyperfine --warmup 3 'fd -e jpg' 'find . -iname "*.jpg"'
Benchmark #1: fd -e jpg
  Time (mean ± σ):      51.4 ms ±   2.9 ms    [User: 121.0 ms, System: 160.5 ms]
  Range (min … max):    44.2 ms …  60.1 ms    56 runs

Benchmark #2: find . -iname "*.jpg"
  Time (mean ± σ):      1.126 s ±  0.101 s    [User: 141.1 ms, System: 956.1 ms]
  Range (min … max):    0.975 s …  1.287 s    10 runs

Summary
  'fd -e jpg' ran
   21.89 ± 2.33 times faster than 'find . -iname "*.jpg"'
```

Seperti halnya debugging, browser juga dilengkapi seperangkat tool fantastis untuk memprofil pemuatan halaman web, memungkinkan Anda mencari tahu di mana waktu dihabiskan (loading, rendering, scripting, &c).
Info lebih lanjut untuk [Firefox](https://profiler.firefox.com/docs/) dan [Chrome](https://developers.google.com/web/tools/chrome-devtools/rendering-tools).

# Latihan

## Debugging
1. Gunakan `journalctl` di Linux atau `log show` di macOS untuk memperoleh akses dan perintah super user dalam sehari terakhir.
Jika tidak ada, Anda dapat mengeksekusi beberapa perintah tidak berbahaya seperti `sudo ls` dan memeriksa lagi.

1. Kerjakan [ini](https://github.com/spiside/pdb-tutorial) tutorial hands on `pdb` untuk membiasakan diri dengan perintahnya. Untuk tutorial yang lebih mendalam baca [ini](https://realpython.com/python-debugging-pdb).

1. Pasang [`shellcheck`](https://www.shellcheck.net/) dan coba periksa skrip berikut. Apa yang salah dengan kodenya? Perbaiki. Pasang plugin linter di editor Anda agar peringatan Anda muncul secara otomatis.

   ```bash
   #!/bin/sh
   ## Example: a typical script with several problems
   for f in $(ls *.m3u)
   do
     grep -qi hq.*mp3 $f \
       && echo -e 'Playlist $f contains a HQ file in mp3 format'
   done
   ```

1. (Advanced) Baca tentang [reversible debugging](https://undo.io/resources/reverse-debugging-whitepaper/) dan buat contoh sederhana berfungsi menggunakan [`rr`](https://rr-project.org/) atau [`RevPDB`](https://morepypy.blogspot.com/2016/07/reverse-debugging-for-python.html).
## Profiling

1. [Di sini](/static/files/sorts.py) ada beberapa implementasi algoritma pengurutan. Gunakan [`cProfile`](https://docs.python.org/3/library/profile.html) dan [`line_profiler`](https://github.com/pyutils/line_profiler) untuk membandingkan runtime insertion sort dan quicksort. Apa bottleneck masing-masing algoritma? Lalu gunakan `memory_profiler` untuk memeriksa konsumsi memorinya, mengapa insertion sort lebih baik? Sekarang periksa versi inplace quicksort. Tantangan: Gunakan `perf` untuk melihat jumlah cycle dan cache hit serta miss dari masing-masing algoritma.

1. Berikut beberapa kode Python (bisa dibilang berbelit) untuk menghitung bilangan Fibonacci menggunakan satu fungsi untuk setiap bilangan.

   ```python
   #!/usr/bin/env python
   def fib0(): return 0

   def fib1(): return 1

   s = """def fib{}(): return fib{}() + fib{}()"""

   if __name__ == '__main__':

       for n in range(2, 10):
           exec(s.format(n, n-1, n-2))
       # from functools import lru_cache
       # for n in range(10):
       #     exec("fib{} = lru_cache(1)(fib{})".format(n, n))
       print(eval("fib9()"))
   ```

   Letakkan kode tersebut ke sebuah berkas dan buat dapat dieksekusi. Pasang prasyarat: [`pycallgraph`](https://lewiscowles1986.github.io/py-call-graph/) dan [`graphviz`](https://graphviz.org/). (Jika Anda dapat menjalankan `dot`, Anda sudah memiliki GraphViz.) Jalankan kode apa adanya dengan `pycallgraph graphviz -- ./fib.py` dan periksa berkas `pycallgraph.png`. Berapa kali `fib0` dipanggil?. Kita dapat melakukan lebih baik dengan memoizing fungsinya. Buka komentar pada baris yang dikomentari dan hasilkan ulang gambarnya. Berapa kali kita memanggil setiap fungsi `fibN` sekarang?

1. Masalah umum adalah port yang ingin Anda dengarkan sudah dipakai proses lain. Mari pelajari cara menemukan pid proses tersebut. Pertama jalankan `python -m http.server 4444` untuk memulai web server minimal yang mendengarkan port `4444`. Di terminal terpisah jalankan `lsof | grep LISTEN` untuk mencetak semua proses dan port yang mendengarkan. Temukan pid proses itu dan hentikan dengan menjalankan `kill <PID>`.

1. Membatasi sumber daya sebuah proses bisa menjadi tool berguna lain di perangkat Anda.
Coba jalankan `stress -c 3` dan visualisasikan konsumsi CPU dengan `htop`. Sekarang, jalankan `taskset --cpu-list 0,2 stress -c 3` dan visualisasikan. Apakah `stress` menggunakan tiga CPU? Mengapa tidak? Baca [`man taskset`](https://www.man7.org/linux/man-pages/man1/taskset.1.html).
Tantangan: capai hal yang sama menggunakan [`cgroups`](https://www.man7.org/linux/man-pages/man7/cgroups.7.html). Coba batasi konsumsi memori `stress -m`.

1. (Advanced) Perintah `curl ipinfo.io` melakukan permintaan HTTP dan mengambil informasi tentang IP publik Anda. Buka [Wireshark](https://www.wireshark.org/) dan coba sadap paket permintaan dan balasan yang dikirim serta diterima `curl`. (Petunjuk: Gunakan filter `http` untuk hanya melihat paket HTTP).
