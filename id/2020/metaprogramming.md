---
layout: lecture-id
title: "Metaprogramming"
description: >
  Pelajari build system, dependency management, testing, dan continuous integration.
thumbnail: /static/assets/thumbnails/2020/lec8.png
details: build systems, dependency management, testing, CI
date: 2020-01-27
ready: true
video:
  aspect: 56.25
  id: _Ms1Z4xfqv4
lang: id
permalink: /id/2020/metaprogramming/
---

Apa yang kami maksud dengan "metaprogramming"? Nah, itu adalah istilah kolektif
terbaik yang bisa kami pikirkan untuk rangkaian hal yang lebih berkaitan dengan
_proses_ daripada dengan menulis kode atau bekerja lebih efisien.
Pada kuliah ini, kita akan melihat sistem untuk membangun dan menguji
kode Anda, serta untuk mengelola dependency. Ini mungkin tampak kurang penting
dalam keseharian Anda sebagai mahasiswa, tetapi begitu Anda
berinteraksi dengan code base yang lebih besar melalui magang atau setelah Anda memasuki
"dunia nyata", Anda akan melihatnya di mana-mana. Perlu kami catat bahwa
"metaprogramming" juga dapat berarti "[program yang beroperasi pada
program](https://en.wikipedia.org/wiki/Metaprogramming)", padahal itu
bukan persis definisi yang kami gunakan untuk keperluan
kuliah ini.

# Build systems

Jika Anda menulis makalah dengan LaTeX, perintah apa yang perlu Anda jalankan untuk
menghasilkan makalah Anda? Bagaimana dengan perintah yang digunakan untuk menjalankan benchmark Anda,
memplotnya, lalu menyisipkan plot tersebut ke makalah Anda? Atau untuk mengompilasi
kode yang disediakan di kelas yang Anda ikuti lalu menjalankan test?

Untuk sebagian besar proyek, baik yang memuat kode atau tidak, ada "proses build".
Yaitu rangkaian operasi yang perlu Anda lakukan untuk beranjak dari
input Anda ke output Anda. Sering kali, proses itu mungkin memiliki banyak langkah, dan
banyak cabang. Jalankan ini untuk menghasilkan plot ini, itu untuk menghasilkan hasil
tersebut, dan sesuatu yang lain untuk menghasilkan makalah akhir. Seperti banyak hal
yang telah kita lihat di kelas ini, Anda bukan orang pertama yang
menemui kejengkelan ini, dan untungnya ada banyak tool untuk membantu
Anda!

Tool ini biasanya disebut "build system", dan ada _banyak_ di antaranya.
Mana yang Anda gunakan bergantung pada tugas yang dihadapi, bahasa
pilihan Anda, dan ukuran proyek. Namun pada intinya, semuanya
sangat mirip. Anda mendefinisikan sejumlah _dependency_, sejumlah
_target_, dan _rule_ untuk beranjak dari satu ke yang lain. Anda memberi tahu
build system bahwa Anda menginginkan target tertentu, dan tugasnya adalah menemukan
semua dependency transitif dari target tersebut, lalu menerapkan rule
untuk menghasilkan target antara sampai target akhir
telah dihasilkan. Idealnya, build system melakukan ini tanpa perlu
mengeksekusi rule untuk target yang dependency-nya belum berubah dan
hasilnya sudah tersedia dari build sebelumnya.

`make` adalah salah satu build system paling umum di luar sana, dan Anda akan
biasanya menemukannya terpasang di hampir semua komputer berbasis UNIX. Tool ini memiliki
kekurangannya, tetapi bekerja cukup baik untuk proyek kecil sampai sedang. Ketika
Anda menjalankan `make`, tool ini mengonsultasikan berkas bernama `Makefile` di direktori
saat ini. Semua target, dependency, dan rule didefinisikan
dalam berkas itu. Mari lihat salah satunya:

```make
paper.pdf: paper.tex plot-data.png
	pdflatex paper.tex

plot-%.png: %.dat plot.py
	./plot.py -i $*.dat -o $@
```

Setiap direktif dalam berkas ini adalah rule tentang cara menghasilkan sisi kiri
menggunakan sisi kanan. Atau, dengan kata lain, hal-hal yang
disebut di sisi kanan adalah dependency, dan sisi kiri adalah
target. Blok yang diindentasi adalah rangkaian program untuk menghasilkan
target dari dependency tersebut. Di `make`, direktif pertama juga
mendefinisikan goal default. Jika Anda menjalankan `make` tanpa argumen, inilah
target yang akan dibangun. Alternatifnya, Anda dapat menjalankan sesuatu seperti
`make plot-data.png`, dan tool akan membangun target itu sebagai gantinya.

Tanda `%` pada sebuah rule adalah "pattern", dan akan mencocokkan string yang sama pada
sisi kiri dan sisi kanan. Misalnya, jika target `plot-foo.png`
diminta, `make` akan mencari dependency `foo.dat` dan
`plot.py`. Sekarang mari lihat apa yang terjadi jika kita menjalankan `make` dengan direktori
source kosong.

```console
$ make
make: *** No rule to make target 'paper.tex', needed by 'paper.pdf'.  Stop.
```

`make` dengan membantu memberi tahu kita bahwa untuk membangun `paper.pdf`, tool ini
membutuhkan `paper.tex`, dan tidak memiliki rule yang memberi tahu cara membuat berkas itu.
Mari coba membuatnya!

```console
$ touch paper.tex
$ make
make: *** No rule to make target 'plot-data.png', needed by 'paper.pdf'.  Stop.
```

Hmm, menarik, sebenarnya _ada_ rule untuk membuat `plot-data.png`, tetapi itu adalah
pattern rule. Karena berkas sumbernya tidak ada (`data.dat`), `make`
cukup menyatakan bahwa tool ini tidak dapat membuat berkas itu. Mari coba buat semua
berkas:

```console
$ cat paper.tex
\documentclass{article}
\usepackage{graphicx}
\begin{document}
\includegraphics[scale=0.65]{plot-data.png}
\end{document}
$ cat plot.py
#!/usr/bin/env python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', type=argparse.FileType('r'))
parser.add_argument('-o')
args = parser.parse_args()

data = np.loadtxt(args.i)
plt.plot(data[:, 0], data[:, 1])
plt.savefig(args.o)
$ cat data.dat
1 1
2 2
3 3
4 4
5 8
```

Sekarang apa yang terjadi jika kita menjalankan `make`?

```console
$ make
./plot.py -i data.dat -o plot-data.png
pdflatex paper.tex
... lots of output ...
```

Dan lihat, tool itu membuatkan PDF untuk kita!
Bagaimana jika kita menjalankan `make` lagi?

```console
$ make
make: 'paper.pdf' is up to date.
```

Tool itu tidak melakukan apa-apa! Mengapa tidak? Nah, karena memang tidak perlu. Tool itu
memeriksa bahwa semua target yang sebelumnya dibangun masih up to date
terhadap dependency yang tercantum. Kita dapat mengujinya dengan memodifikasi
`paper.tex` lalu menjalankan ulang `make`:

```console
$ vim paper.tex
$ make
pdflatex paper.tex
...
```

Perhatikan bahwa `make` _tidak_ menjalankan ulang `plot.py` karena itu tidak
perlu; tidak ada dependency `plot-data.png` yang berubah!

# Dependency management

Pada tingkat yang lebih makro, proyek perangkat lunak Anda kemungkinan memiliki
dependency yang merupakan proyek tersendiri. Anda mungkin bergantung pada program
yang terpasang (seperti `python`), paket sistem (seperti `openssl`), atau library
di dalam bahasa pemrograman Anda (seperti `matplotlib`). Saat ini, sebagian besar
dependency tersedia melalui _repository_ yang meng-host
banyak dependency semacam itu di satu tempat, dan menyediakan
mekanisme praktis untuk memasangnya. Beberapa contoh termasuk repositori paket
Ubuntu untuk paket sistem Ubuntu, yang Anda akses
melalui tool `apt`, RubyGems untuk library Ruby, PyPI untuk library
Python, atau Arch User Repository untuk paket kontribusi pengguna Arch Linux.

Karena mekanisme persisnya untuk berinteraksi dengan repositori ini sangat bervariasi
dari repositori ke repositori dan dari tool ke tool, kami tidak akan
terlalu membahas detail salah satu spesifiknya pada kuliah ini. Yang _akan_
kami bahas adalah sebagian terminologi umum yang semuanya gunakan. Yang pertama
di antaranya adalah _versioning_. Sebagian besar proyek yang menjadi dependency proyek lain
menerbitkan _nomor versi_ pada setiap rilis. Biasanya sesuatu seperti
8.1.3 atau 64.1.20192004. Nomor versi sering, tetapi tidak selalu, bersifat numerik.
Nomor versi memiliki banyak tujuan, dan salah satu yang paling penting
adalah memastikan perangkat lunak tetap berfungsi. Bayangkan, misalnya,
saya merilis versi baru library saya di mana saya telah mengganti nama
fungsi tertentu. Jika seseorang mencoba membangun perangkat lunak yang
bergantung pada library saya setelah saya merilis pembaruan itu, build bisa gagal
karena perangkat lunak itu memanggil fungsi yang sudah tidak ada lagi! Versioning berusaha
menyelesaikan masalah ini dengan memungkinkan sebuah proyek menyatakan bahwa ia bergantung pada
versi tertentu, atau rentang versi, dari proyek lain. Dengan begitu,
bahkan jika library di baliknya berubah, perangkat lunak yang bergantung
tetap dapat dibangun dengan menggunakan versi lama library saya.

Namun itu juga belum ideal! Bagaimana jika saya menerbitkan pembaruan keamanan yang
_tidak_ mengubah antarmuka publik library saya ("API"-nya), dan
yang seharusnya segera digunakan oleh proyek mana pun yang bergantung pada versi lama?
Di sinilah kelompok angka berbeda dalam sebuah versi berperan. Makna persis masing-masing
bervariasi antar proyek, tetapi satu standar yang relatif umum adalah [_semantic
versioning_](https://semver.org/). Dengan semantic versioning, setiap
nomor versi berbentuk: major.minor.patch. Aturannya adalah:

 - Jika rilis baru tidak mengubah API, naikkan versi patch.
 - Jika Anda _menambahkan_ ke API Anda dengan cara yang kompatibel ke belakang, naikkan
   versi minor.
 - Jika Anda mengubah API dengan cara yang tidak kompatibel ke belakang, naikkan
   versi major.

Ini sudah memberikan beberapa keuntungan besar. Sekarang, jika proyek saya bergantung
pada proyek Anda, _seharusnya_ aman menggunakan rilis terbaru dengan
major version yang sama dengan yang saya gunakan saat mengembangkan, selama
versi minor-nya setidaknya sama dengan saat itu. Dengan kata lain, jika saya bergantung pada
library Anda pada versi `1.3.7`, maka _seharusnya_ tidak masalah membangunnya
dengan `1.3.8`, `1.6.1`, atau bahkan `1.3.0`. Versi
`2.2.4` mungkin tidak akan aman, karena major version-nya
dinaikkan. Kita dapat melihat contoh semantic versioning pada nomor versi
Python. Banyak dari Anda mungkin mengetahui bahwa kode Python 2 dan Python
3 tidak dapat dicampur dengan baik, itulah sebabnya itu merupakan kenaikan versi _major_.
Demikian pula, kode yang ditulis untuk Python 3.5 mungkin berjalan baik pada Python
3.7, tetapi mungkin tidak pada 3.4.

Saat bekerja dengan sistem dependency management, Anda juga mungkin menemukan
gagasan _lock file_. Lock file hanyalah berkas yang
mencantumkan versi persis yang _saat ini_ menjadi dependency Anda untuk setiap
dependency. Biasanya, Anda perlu menjalankan program update secara eksplisit untuk
melakukan upgrade ke versi baru dependency Anda. Ada banyak alasan
untuk ini, seperti menghindari kompilasi ulang yang tidak perlu, memiliki build yang reproducible,
atau tidak memperbarui otomatis ke versi terbaru (yang mungkin
rusak). Versi ekstrem dari penguncian dependency semacam ini adalah
_vendoring_, yaitu menyalin semua kode dependency Anda
ke dalam proyek Anda sendiri. Itu memberi Anda kendali penuh atas setiap perubahan
padanya, dan memungkinkan Anda memperkenalkan perubahan sendiri, tetapi juga berarti Anda
harus secara eksplisit menarik setiap pembaruan dari maintainer upstream
seiring waktu.

# Continuous integration systems

Saat Anda mengerjakan proyek yang semakin besar, Anda akan menemukan bahwa sering
ada tugas tambahan yang harus Anda lakukan setiap kali membuat perubahan.
Anda mungkin harus mengunggah versi baru dokumentasi, mengunggah versi
terkompilasi ke suatu tempat, merilis kode ke pypi, menjalankan test suite Anda,
dan segala macam hal lainnya. Mungkin setiap kali seseorang mengirimkan
pull request di GitHub, Anda ingin kodenya diperiksa gayanya dan
Anda ingin beberapa benchmark dijalankan? Ketika kebutuhan semacam ini muncul, saatnya
melihat continuous integration.

Continuous integration, atau CI, adalah istilah payung untuk "hal yang berjalan
setiap kali kode Anda berubah", dan ada banyak perusahaan di luar sana yang
menyediakan berbagai jenis CI, sering kali gratis untuk proyek open-source.
Beberapa yang besar adalah Travis CI, Azure Pipelines, dan GitHub Actions.
Semuanya bekerja kurang lebih dengan cara yang sama: Anda menambahkan berkas ke repositori Anda
yang menjelaskan apa yang harus terjadi ketika berbagai hal terjadi pada repositori
tersebut. Yang sejauh ini paling umum adalah rule seperti "ketika seseorang
push kode, jalankan test suite". Ketika peristiwa itu terpicu, penyedia CI
menjalankan satu atau lebih virtual machine, menjalankan perintah dalam
"resep" Anda, lalu biasanya mencatat hasilnya di suatu tempat. Anda
dapat mengaturnya agar Anda diberi tahu jika test suite berhenti
lulus, atau agar badge kecil muncul di repositori Anda selama
test lulus.

Sebagai contoh sistem CI, situs kelas ini diatur menggunakan GitHub
Pages. Pages adalah aksi CI yang menjalankan perangkat lunak blog Jekyll pada setiap
push ke `master` dan menyediakan situs hasil build pada domain GitHub
tertentu. Ini membuat pembaruan situs web menjadi sangat mudah bagi kami! Kami
cukup membuat perubahan secara lokal, meng-commit dengan git, lalu push. CI
menangani sisanya.

## Sedikit catatan tentang testing

Sebagian besar proyek perangkat lunak besar dilengkapi dengan "test suite". Anda mungkin sudah
familiar dengan konsep umum testing, tetapi kami pikir kami akan
menyebutkan secara singkat beberapa pendekatan testing dan terminologi testing yang
mungkin Anda temui di lapangan:

 - Test suite: istilah kolektif untuk semua test
 - Unit test: "micro-test" yang menguji fitur tertentu secara terisolasi
 - Integration test: "macro-test" yang menjalankan bagian sistem yang lebih besar
   untuk memeriksa bahwa berbagai fitur atau komponen bekerja _bersama_.
 - Regression test: test yang mengimplementasikan pola tertentu yang
   _sebelumnya_ menyebabkan bug untuk memastikan bug tersebut tidak muncul kembali.
 - Mocking: mengganti fungsi, module, atau tipe dengan implementasi
   palsu untuk menghindari pengujian fungsionalitas yang tidak terkait. Misalnya,
   Anda mungkin "mem-mock jaringan" atau "mem-mock disk".

# Latihan

 1. Sebagian besar makefile menyediakan target bernama `clean`. Target ini tidak dimaksudkan
    untuk menghasilkan berkas bernama `clean`, tetapi untuk membersihkan berkas
    apa pun yang dapat dibangun ulang oleh make. Anggap saja sebagai cara untuk "membatalkan" semua
    langkah build. Implementasikan target `clean` untuk `Makefile` `paper.pdf`
    di atas. Anda harus membuat target tersebut
    [phony](https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html).
    Anda mungkin merasa subperintah [`git
    ls-files`](https://git-scm.com/docs/git-ls-files) berguna.
    Sejumlah target make lain yang sangat umum dicantumkan
    [di sini](https://www.gnu.org/software/make/manual/html_node/Standard-Targets.html#Standard-Targets).
 2. Lihat berbagai cara menentukan persyaratan versi untuk
    dependency di [build system
    Rust](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html).
    Sebagian besar repositori paket mendukung sintaks serupa. Untuk masing-masing
    (caret, tilde, wildcard, comparison, dan multiple), coba pikirkan
    use case di mana jenis persyaratan tersebut masuk akal.
 3. Git dapat berperan sebagai sistem CI sederhana dengan sendirinya. Di `.git/hooks`
    di dalam repositori git mana pun, Anda akan menemukan berkas (saat ini tidak aktif)
    yang dijalankan sebagai skrip ketika aksi tertentu terjadi. Tulis hook
    [`pre-commit`](https://git-scm.com/docs/githooks#_pre_commit)
    yang menjalankan `make paper.pdf` dan menolak commit jika perintah `make`
    gagal. Ini seharusnya mencegah commit apa pun yang memuat versi makalah yang tidak
    dapat dibangun.
 4. Siapkan halaman auto-published sederhana menggunakan [GitHub
    Pages](https://pages.github.com/).
    Tambahkan [GitHub Action](https://github.com/features/actions) ke
    repositori untuk menjalankan `shellcheck` pada berkas shell apa pun di
    repositori tersebut (berikut [salah satu cara
    melakukannya](https://github.com/marketplace/actions/shellcheck)). Periksa bahwa
    ini berhasil!
 5. [Bangun sendiri](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/building-actions)
    GitHub action untuk menjalankan [`proselint`](https://github.com/amperser/proselint) atau
    [`write-good`](https://github.com/btford/write-good) pada semua berkas
    `.md` di repositori. Aktifkan di repositori Anda, dan
    periksa bahwa ini berhasil dengan mengirimkan pull request yang berisi typo.
