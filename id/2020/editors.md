---
layout: lecture-id
title: "Editors (Vim)"
description: >
  Pelajari cara menggunakan Vim, text editor andal yang dirancang untuk menyunting kode secara efisien.
thumbnail: /static/assets/thumbnails/2020/lec3.png
date: 2020-01-15
ready: true
video:
  aspect: 56.25
  id: a6Q8Na575qc
lang: id
permalink: /id/2020/editors/
---

Menulis kata-kata bahasa Inggris dan menulis kode adalah aktivitas yang sangat berbeda. Saat
memprogram, Anda lebih banyak menghabiskan waktu berpindah berkas, membaca, bernavigasi, dan
mengedit kode dibandingkan menulis aliran panjang. Masuk akal bahwa ada
jenis program berbeda untuk menulis kata-kata bahasa Inggris versus kode (misalnya
Microsoft Word versus Visual Studio Code).

Sebagai programmer, kita menghabiskan sebagian besar waktu kita mengedit kode, jadi layak menginvestasikan
waktu untuk menguasai editor yang sesuai kebutuhan Anda. Berikut cara Anda mempelajari editor
baru:

- Mulai dengan tutorial (yaitu kuliah ini, ditambah sumber daya yang kami tunjukkan)
- Konsisten menggunakan editor tersebut untuk semua kebutuhan text editing Anda (bahkan jika itu memperlambat
Anda pada awalnya)
- Cari tahu seiring berjalan: jika tampaknya ada cara yang lebih baik untuk melakukan
sesuatu, kemungkinan besar memang ada

Jika Anda mengikuti metode di atas, sepenuhnya berkomitmen menggunakan program baru untuk
semua keperluan text editing, garis waktu untuk mempelajari text editor
canggih terlihat seperti ini. Dalam satu atau dua jam, Anda akan mempelajari fungsi dasar editor
seperti membuka dan mengedit berkas, save/quit, dan bernavigasi antar buffer. Setelah
Anda mencapai 20 jam, Anda seharusnya sudah secepat dengan editor lama Anda.
Setelah itu, manfaatnya mulai: Anda akan memiliki cukup pengetahuan dan muscle
memory sehingga menggunakan editor baru menghemat waktu Anda. Text editor modern adalah tool
yang canggih dan kuat, jadi pembelajaran tidak pernah berhenti: Anda akan menjadi bahkan lebih cepat saat Anda
belajar lebih banyak.

# Editor mana yang harus dipelajari?

Programmer memiliki [pendapat yang kuat](https://en.wikipedia.org/wiki/Editor_war)
tentang text editor mereka.

Editor mana yang populer saat ini? Lihat [survei Stack Overflow
ini](https://insights.stackoverflow.com/survey/2019/#development-environments-and-tools)
(mungkin ada bias karena pengguna Stack Overflow mungkin tidak representatif
bagi programmer secara keseluruhan). [Visual Studio
Code](https://code.visualstudio.com/) adalah editor paling populer.
[Vim](https://www.vim.org/) adalah editor berbasis command-line paling populer.

## Vim

Semua pengajar kelas ini menggunakan Vim sebagai editor mereka. Vim memiliki
sejarah yang kaya; ia berasal dari editor Vi (1976), dan masih
dikembangkan hingga hari ini. Vim memiliki beberapa gagasan yang sangat rapi di baliknya, dan karena alasan ini,
banyak tool mendukung mode emulasi Vim (misalnya, 1,4 juta orang
telah memasang [emulasi Vim untuk VS code](https://github.com/VSCodeVim/Vim)).
Vim mungkin layak dipelajari bahkan jika pada akhirnya Anda beralih ke text editor
lain.

Tidak mungkin mengajarkan seluruh fungsionalitas Vim dalam 50 menit, jadi kami
akan memfokuskan pada menjelaskan filosofi Vim, mengajarkan dasar-dasarnya,
menunjukkan beberapa fungsionalitas yang lebih canggih, dan memberi Anda
sumber daya untuk menguasai tool tersebut.

# Filosofi Vim

Saat memprogram, Anda menghabiskan sebagian besar waktu membaca/mengedit, bukan menulis. Karena
alasan ini, Vim adalah editor _modal_: ia memiliki mode berbeda untuk menyisipkan teks
versus memanipulasi teks. Vim dapat diprogram (dengan Vimscript dan juga bahasa lain
seperti Python), dan antarmuka Vim itu sendiri adalah bahasa pemrograman:
ketukan tombol (dengan nama mnemonik) adalah perintah, dan perintah-perintah ini
dapat dikomposisikan. Vim menghindari penggunaan mouse, karena terlalu lambat; Vim bahkan
menghindari penggunaan tombol panah karena memerlukan terlalu banyak gerakan.

Hasil akhirnya adalah sebuah editor yang dapat menyamai kecepatan berpikir Anda.

# Modal editing

Desain Vim didasarkan pada gagasan bahwa banyak waktu programmer dihabiskan untuk
membaca, bernavigasi, dan membuat edit kecil, bukan menulis aliran panjang
teks. Karena alasan ini, Vim memiliki beberapa mode operasi.

- **Normal**: untuk bergerak di dalam berkas dan membuat edit
- **Insert**: untuk menyisipkan teks
- **Replace**: untuk mengganti teks
- **Visual** (biasa, baris, atau blok): untuk memilih blok teks
- **Command-line**: untuk menjalankan sebuah perintah

Ketukan tombol memiliki arti berbeda pada mode operasi berbeda. Misalnya,
huruf `x` pada mode Insert hanya akan menyisipkan karakter literal 'x', tetapi pada
mode Normal, huruf itu akan menghapus karakter di bawah kursor, dan pada mode Visual,
huruf itu akan menghapus seleksi.

Dalam konfigurasi defaultnya, Vim menampilkan mode saat ini di kiri bawah.
Mode awal/default adalah mode Normal. Anda umumnya akan menghabiskan sebagian besar waktu Anda
antara mode Normal dan mode Insert.

Anda mengubah mode dengan menekan `<ESC>` (tombol escape) untuk beralih dari mode apa pun
kembali ke mode Normal. Dari mode Normal, masuk ke mode Insert dengan `i`, mode Replace
dengan `R`, mode Visual dengan `v`, mode Visual Line dengan `V`, mode Visual Block
dengan `<C-v>` (Ctrl-V, kadang juga ditulis `^V`), dan mode Command-line dengan
`:`.

Anda menggunakan tombol `<ESC>` cukup sering saat menggunakan Vim: pertimbangkan memetakan ulang Caps Lock ke
Escape ([instruksi
macOS](https://vim.fandom.com/wiki/Map_caps_lock_to_escape_in_macOS))
atau membuat [pemetaan
alternatif](https://vim.fandom.com/wiki/Avoid_the_escape_key#Mappings) untuk `<ESC>`
dengan rangkaian tombol yang sederhana.

# Dasar-dasar

## Menyisipkan teks

Dari mode Normal, tekan `i` untuk masuk ke mode Insert. Sekarang, Vim berperilaku seperti
text editor lain, sampai Anda menekan `<ESC>` untuk kembali ke mode Normal. Ini,
beserta dasar-dasar yang dijelaskan di atas, adalah semua yang Anda butuhkan untuk mulai mengedit berkas
menggunakan Vim (meskipun tidak terlalu efisien, jika Anda menghabiskan seluruh waktu Anda
mengedit dari mode Insert).

## Buffer, tab, dan window

Vim memelihara sekumpulan berkas yang terbuka, yang disebut "buffer". Sebuah sesi Vim memiliki sejumlah
tab, masing-masing memiliki sejumlah window (pane terbagi). Setiap window menampilkan
satu buffer. Berbeda dengan program lain yang Anda kenal, seperti web
browser, tidak ada korespondensi 1-ke-1 antara buffer dan window;
window hanyalah tampilan. Buffer tertentu dapat terbuka di _beberapa_ window,
bahkan dalam tab yang sama. Ini bisa sangat berguna, misalnya, untuk melihat dua
bagian berbeda sebuah berkas pada saat yang sama.

Secara default, Vim terbuka dengan satu tab, yang berisi satu window.

## Command-line

Mode command dapat dimasuki dengan mengetik `:` pada mode Normal. Kursor Anda akan melompat
ke command line di bagian bawah layar saat menekan `:`. Mode ini
memiliki banyak fungsionalitas, termasuk membuka, menyimpan, dan menutup berkas, serta
[keluar dari Vim](https://twitter.com/iamdevloper/status/435555976687923200).

- `:q` quit (tutup window)
- `:w` save ("write")
- `:wq` save dan quit
- `:e {name of file}` buka berkas untuk diedit
- `:ls` tampilkan buffer yang terbuka
- `:help {topic}` buka bantuan
    - `:help :w` membuka bantuan untuk perintah `:w`
    - `:help w` membuka bantuan untuk movement `w`

# Antarmuka Vim adalah sebuah bahasa pemrograman

Gagasan terpenting dalam Vim adalah bahwa antarmuka Vim itu sendiri adalah bahasa
pemrograman. Ketukan tombol (dengan nama mnemonik) adalah perintah, dan perintah-perintah ini
_dapat dikomposisikan_. Ini memungkinkan pergerakan dan edit yang efisien, terutama setelah
perintah-perintah tersebut menjadi muscle memory.

## Berpindah Posisi

Anda sebaiknya menghabiskan sebagian besar waktu Anda di mode Normal, menggunakan perintah movement untuk
bernavagasi di buffer. Movement di Vim juga disebut "noun", karena movement
merujuk pada potongan-potongan teks.

- Movement dasar: `hjkl` (kiri, bawah, atas, kanan)
- Kata: `w` (kata berikutnya), `b` (awal kata), `e` (akhir kata)
- Baris: `0` (awal baris), `^` (karakter pertama yang bukan whitespace), `$` (akhir baris)
- Layar: `H` (bagian atas layar), `M` (bagian tengah layar), `L` (bagian bawah layar)
- Scroll: `Ctrl-u` (ke atas), `Ctrl-d` (ke bawah)
- Berkas: `gg` (awal berkas), `G` (akhir berkas)
- Line numbers: `:{number}<CR>` atau `{number}G` (baris {number})
- Misc: `%` (item yang bersesuaian)
- Find: `f{character}`, `t{character}`, `F{character}`, `T{character}`
    - mencari/menuju {character} ke depan/ke belakang pada baris saat ini
    - `,` / `;` untuk bernavigasi antar kecocokan
- Search: `/{regex}`, `n` / `N` untuk bernavigasi antar kecocokan

## Memilih Teks

Mode visual:

- Visual: `v`
- Visual Line: `V`
- Visual Block: `Ctrl-v`

Anda dapat menggunakan tombol movement untuk membuat seleksi.

## Penyuntingan

Segala sesuatu yang dulu Anda lakukan dengan mouse, sekarang Anda lakukan dengan keyboard
menggunakan perintah editing yang dapat dikomposisikan dengan perintah movement. Di sinilah antarmuka Vim
mulai terlihat seperti bahasa pemrograman. Perintah editing Vim
juga disebut "verb", karena verb bekerja pada noun.

- `i` masuk ke mode Insert
    - tetapi untuk memanipulasi/menghapus teks, Anda ingin menggunakan sesuatu yang lebih dari
    backspace
- `o` / `O` menyisipkan baris di bawah / di atas
- `d{motion}` menghapus {motion}
    - misalnya `dw` adalah menghapus kata, `d$` adalah menghapus hingga akhir baris, `d0` adalah menghapus
    hingga awal baris
- `c{motion}` mengubah {motion}
    - misalnya `cw` adalah mengubah kata
    - seperti `d{motion}` diikuti `i`
- `x` menghapus karakter (sama dengan `dl`)
- `s` mengganti karakter (sama dengan `cl`)
- Mode Visual + manipulasi
    - pilih teks, `d` untuk menghapusnya atau `c` untuk mengubahnya
- `u` untuk undo, `<C-r>` untuk redo
- `y` untuk menyalin / "yank" (beberapa perintah lain seperti `d` juga menyalin)
- `p` untuk paste
- Masih banyak yang bisa dipelajari: misalnya `~` membalik kapitalisasi sebuah karakter

## Count dan Jumlah Pengulangan

Anda dapat menggabungkan noun dan verb dengan sebuah count, yang akan melakukan aksi tertentu
sejumlah kali.

- `3w` bergerak maju 3 kata
- `5j` bergerak turun 5 baris
- `7dw` menghapus 7 kata

## Modifiers

Anda dapat menggunakan modifier untuk mengubah makna sebuah noun. Beberapa modifier adalah `i`,
yang berarti "inner" atau "inside", dan `a`, yang berarti "around".

- `ci(` ubah isi di dalam pasangan tanda kurung saat ini
- `ci[` ubah isi di dalam pasangan tanda kurung siku saat ini
- `da'` hapus string berkutip tunggal, termasuk tanda kutip tunggal di sekelilingnya

<a id="demo"></a>
# Demo

Berikut implementasi [fizz buzz](https://en.wikipedia.org/wiki/Fizz_buzz) yang rusak:

```python
def fizz_buzz(limit):
    for i in range(limit):
        if i % 3 == 0:
            print('fizz')
        if i % 5 == 0:
            print('fizz')
        if i % 3 and i % 5:
            print(i)

def main():
    fizz_buzz(10)
```

Kami akan memperbaiki masalah-masalah berikut:

- Main tidak pernah dipanggil
- Dimulai dari 0 alih-alih 1
- Mencetak "fizz" dan "buzz" pada baris terpisah untuk kelipatan 15
- Mencetak "fizz" untuk kelipatan 5
- Menggunakan argumen hard-code 10 alih-alih menerima argumen command-line

{% comment %}
- main is never called
  - `G` akhir berkas
  - `o` open new line below
  - type in "if __name__ ..." thing
- starts at 0 instead of 1
  - search for `/range`
  - `ww` to move forward 2 words
  - `i` to insert text, "1, "
  - `ea` to insert after limit, "+1"
- newline for "fizzbuzz"
  - `jj$i` untuk menyisipkan teks di akhir baris
  - add ", end=''"
  - `jj.` to repeat for second print
  - `jjo` to open line below if
  - add "else: print()"
- fizz fizz
  - `ci'` to change fizz
- command-line argument
  - `ggO` to open above
  - "import sys"
  - `/10`
  - `ci(` to "int(sys.argv[1])"
{% endcomment %}

Lihat video kuliah untuk demonstrasinya. Bandingkan bagaimana perubahan di atas
dilakukan menggunakan Vim dengan bagaimana Anda mungkin membuat edit yang sama menggunakan program lain.
Perhatikan betapa sedikit ketukan tombol yang diperlukan di Vim, memungkinkan Anda mengedit secepat
pikiran Anda.

# Kustomisasi Vim

Vim dikustomisasi melalui berkas konfigurasi teks biasa di `~/.vimrc`
(memuat perintah Vimscript). Mungkin ada banyak pengaturan dasar yang
ingin Anda aktifkan.

Kami menyediakan config dasar yang terdokumentasi dengan baik yang dapat Anda gunakan sebagai titik
awal. Kami menyarankan menggunakan config ini karena ia memperbaiki beberapa perilaku default Vim yang aneh. **Unduh config kami [di sini](/2020/files/vimrc) dan simpan ke
`~/.vimrc`.**

Vim sangat dapat dikustomisasi, dan ada baiknya meluangkan waktu menjelajahi
opsi kustomisasi. Anda dapat melihat dotfiles orang lain di GitHub untuk
inspirasi, misalnya config Vim pengajar Anda
([Anish](https://github.com/anishathalye/dotfiles/blob/master/vimrc),
[Jon](https://github.com/jonhoo/configs/blob/master/editor/.config/nvim/init.lua) (menggunakan [neovim](https://neovim.io/)),
[Jose](https://github.com/JJGO/dotfiles/blob/master/vim/.vimrc)). Ada
banyak posting blog yang bagus tentang topik ini juga. Usahakan untuk tidak menyalin-tempel
konfigurasi lengkap orang, tetapi bacalah, pahami, dan ambil yang Anda butuhkan.

# Memperluas Vim

Ada banyak sekali plugin untuk memperluas Vim. Berlawanan dengan nasihat usang yang
mungkin Anda temukan di internet, Anda _tidak_ perlu menggunakan plugin manager untuk
Vim (sejak Vim 8.0). Sebaliknya, Anda dapat menggunakan sistem package management
bawaannya. Cukup buat direktori `~/.vim/pack/vendor/start/`, dan letakkan
plugin di sana (misalnya melalui `git clone`).

Berikut beberapa plugin favorit kami:

- [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim): fuzzy file finder
- [ack.vim](https://github.com/mileszs/ack.vim): code search
- [nerdtree](https://github.com/scrooloose/nerdtree): file explorer
- [vim-easymotion](https://github.com/easymotion/vim-easymotion): magic motions

Kami berusaha menghindari memberikan daftar plugin yang sangat panjang di sini. Anda
dapat memeriksa dotfiles pengajar
([Anish](https://github.com/anishathalye/dotfiles),
[Jon](https://github.com/jonhoo/configs),
[Jose](https://github.com/JJGO/dotfiles)) untuk melihat plugin lain yang kami gunakan.
Lihat [Vim Awesome](https://vimawesome.com/) untuk plugin Vim yang lebih hebat.
Ada juga banyak posting blog tentang topik ini: cukup cari "best Vim
plugins".

# Vim-mode di program lain

Banyak tool mendukung emulasi Vim. Kualitasnya bervariasi dari bagus hingga hebat;
bergantung pada tool-nya, mungkin tidak mendukung fitur Vim yang lebih canggih, tetapi sebagian besar
mencakup dasar-dasarnya dengan cukup baik.

## Shell

Jika Anda pengguna Bash, gunakan `set -o vi`. Jika Anda menggunakan Zsh, `bindkey -v`. Untuk Fish,
`fish_vi_key_bindings`. Selain itu, apa pun shell yang Anda gunakan, Anda dapat
`export EDITOR=vim`. Ini adalah environment variable yang digunakan untuk menentukan editor
mana yang diluncurkan ketika sebuah program ingin memulai editor. Misalnya, `git`
akan menggunakan editor ini untuk pesan commit.

## Readline

Banyak program menggunakan library [GNU
Readline](https://tiswww.case.edu/php/chet/readline/rltop.html) untuk
command-line interface mereka. Readline juga mendukung emulasi Vim (dasar),
yang dapat diaktifkan dengan menambahkan baris berikut ke berkas `~/.inputrc`:

```
set editing-mode vi
```

Dengan pengaturan ini, misalnya, REPL Python akan mendukung binding Vim.

## Lainnya

Bahkan ada ekstensi keybinding vim untuk web
[browser](https://vim.fandom.com/wiki/Vim_key_bindings_for_web_browsers) - beberapa
yang populer adalah
[Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en)
untuk Google Chrome dan [Tridactyl](https://github.com/tridactyl/tridactyl) untuk
Firefox. Anda bahkan dapat memperoleh binding Vim di [Jupyter
notebook](https://github.com/jupyterlab-contrib/jupyterlab-vim).
Berikut [daftar panjang](https://reversed.top/2016-08-13/big-list-of-vim-like-software) perangkat lunak dengan keybinding mirip vim.

<a id="advanced-vim"></a>
# Vim tingkat lanjut

Berikut beberapa contoh untuk menunjukkan kekuatan editor ini. Kami tidak dapat mengajarkan
semua hal semacam ini, tetapi Anda akan mempelajarinya seiring berjalan. Heuristik
yang baik: setiap kali Anda menggunakan editor dan berpikir "pasti ada
cara yang lebih baik untuk melakukan ini", kemungkinan besar memang ada: carilah daring.

## Mencari dan Mengganti Teks

Perintah `:s` (substitute) ([dokumentasi](https://vim.fandom.com/wiki/Search_and_replace)).

- `%s/foo/bar/g`
    - ganti foo dengan bar secara global di berkas
- `%s/\[.*\](\(.*\))/\1/g`
    - ganti tautan Markdown bernama dengan URL biasa

## Banyak window

- `:sp` / `:vsp` untuk membagi window
- Dapat memiliki beberapa tampilan dari buffer yang sama.

<a id="macros"></a>
## Macros

- `q{character}` untuk mulai merekam macro di register `{character}`
- `q` untuk berhenti merekam
- `@{character}` memutar ulang macro
- Eksekusi macro berhenti saat terjadi error
- `{number}@{character}` mengeksekusi macro {number} kali
- Macro dapat rekursif
    - bersihkan macro terlebih dahulu dengan `q{character}q`
    - rekam macro, dengan `@{character}` untuk memanggil macro secara rekursif
    (akan menjadi no-op sampai perekaman selesai)
- Contoh: konversi xml ke json ([berkas](/2020/files/example-data.xml))
    - Array objek dengan key "name" / "email"
    - Gunakan program Python?
    - Gunakan sed / regex
        - `g/people/d`
        - `%s/<person>/{/g`
        - `%s/<name>\(.*\)<\/name>/"name": "\1",/g`
        - ...
    - Perintah / macro Vim
        - `Gdd`, `ggdd` hapus baris pertama dan terakhir
        - Macro untuk memformat satu elemen (register `e`)
            - Pergi ke baris dengan `<name>`
            - `qe^r"f>s": "<ESC>f<C"<ESC>q`
        - Macro untuk memformat satu person
            - Pergi ke baris dengan `<person>`
            - `qpS{<ESC>j@eA,<ESC>j@ejS},<ESC>q`
        - Macro untuk memformat satu person dan pergi ke person berikutnya
            - Pergi ke baris dengan `<person>`
            - `qq@pjq`
        - Eksekusi macro sampai akhir berkas
            - `999@q`
        - Hapus `,` terakhir secara manual dan tambahkan pembatas `[` dan `]`

# Sumber daya

- `vimtutor` adalah tutorial yang terpasang bersama Vim - jika Vim terpasang, Anda seharusnya dapat menjalankan `vimtutor` dari shell Anda
- [Vim Adventures](https://vim-adventures.com/) adalah game untuk mempelajari Vim
- [Vim Tips Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2019/) memiliki berbagai tip Vim
- [Vim Golf](https://www.vimgolf.com/) adalah [code golf](https://en.wikipedia.org/wiki/Code_golf), tetapi bahasa pemrogramannya adalah UI Vim
- [Vi/Vim Stack Exchange](https://vi.stackexchange.com/)
- [Vim Screencasts](http://vimcasts.org/)
- [Practical Vim](https://pragprog.com/titles/dnvim2/) (buku)

# Latihan

1. Selesaikan `vimtutor`. Catatan: tutorial ini paling baik ditampilkan di
   jendela terminal
   [80x24](https://en.wikipedia.org/wiki/VT100) (80 kolom kali 24 baris).
1. Unduh [vimrc dasar](/2020/files/vimrc) kami dan simpan ke `~/.vimrc`. Baca
   berkas yang dikomentari dengan baik itu (menggunakan Vim!), dan amati bagaimana Vim terlihat dan
   berperilaku sedikit berbeda dengan config baru.
1. Pasang dan konfigurasikan sebuah plugin:
   [ctrlp.vim](https://github.com/ctrlpvim/ctrlp.vim).
   1. Buat direktori plugin dengan `mkdir -p ~/.vim/pack/vendor/start`
   1. Unduh plugin: `cd ~/.vim/pack/vendor/start; git clone
      https://github.com/ctrlpvim/ctrlp.vim`
   1. Baca
      [dokumentasi](https://github.com/ctrlpvim/ctrlp.vim/blob/master/readme.md)
      untuk plugin tersebut. Coba gunakan CtrlP untuk menemukan berkas dengan bernavigasi ke
      direktori proyek, membuka Vim, dan menggunakan command-line Vim untuk memulai
      `:CtrlP`.
    1. Kustomisasi CtrlP dengan menambahkan
       [konfigurasi](https://github.com/ctrlpvim/ctrlp.vim/blob/master/readme.md#basic-options)
       ke `~/.vimrc` Anda agar membuka CtrlP dengan menekan Ctrl-P.
1. Untuk berlatih menggunakan Vim, kerjakan ulang [Demo](#demo) dari kuliah di mesin
   Anda sendiri.
1. Gunakan Vim untuk _semua_ text editing Anda selama bulan berikutnya. Setiap kali sesuatu
   terasa tidak efisien, atau ketika Anda berpikir "pasti ada cara yang lebih baik", coba
   cari di Google, kemungkinan besar memang ada. Jika Anda macet, datang ke office hours atau
   kirim email kepada kami.
1. Konfigurasikan tool lain Anda untuk menggunakan binding Vim (lihat instruksi di atas).
1. Kustomisasi lebih lanjut `~/.vimrc` Anda dan pasang lebih banyak plugin.
1. (Advanced) Konversi XML ke JSON ([contoh berkas](/2020/files/example-data.xml))
   menggunakan macro Vim. Coba lakukan sendiri, tetapi Anda dapat melihat bagian
   [macro](#macros) di atas jika Anda macet.
