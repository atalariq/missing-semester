---
layout: lecture-id
title: "Editors"
presenter: Anish
date: 2019-01-22
order: 1
video:
  aspect: 62.5
  id: 1vLcusYSrI4
lang: id
permalink: /id/2019/editors/
---

# Pentingnya Editor

Sebagai programmer, kita menghabiskan sebagian besar waktu kita mengedit berkas teks biasa. Layak
menginvestasikan waktu mempelajari editor yang sesuai kebutuhan Anda.

Bagaimana Anda mempelajari editor baru? Anda memaksa diri Anda menggunakan editor itu untuk
sementara waktu, bahkan jika itu sementara menghambat produktivitas Anda. Itu akan terbayar cukup cepat
(dua pekan cukup untuk mempelajari dasarnya).

Kami akan mengajarkan Vim kepada Anda, tetapi kami mendorong Anda bereksperimen dengan editor
lain. Ini pilihan yang sangat personal, dan orang memiliki [pendapat
kuat](https://en.wikipedia.org/wiki/Editor_war).

Kami tidak dapat mengajarkan cara menggunakan editor yang kuat dalam 50 menit, jadi kami akan
memfokuskan pada mengajarkan dasar-dasarnya, menunjukkan beberapa fungsionalitas
yang lebih canggih, dan memberi Anda sumber daya untuk menguasai tool tersebut. Kami akan mengajarkan
pelajaran dalam konteks Vim, tetapi sebagian besar gagasan akan berlaku untuk editor kuat lain
yang Anda gunakan (dan jika tidak berlaku, maka Anda mungkin tidak sebaiknya menggunakan
editor itu!).

![Kurva belajar editor](/2019/files/editor-learning-curves.jpg)

<!-- source: https://blogs.msdn.microsoft.com/steverowe/2004/11/17/code-editor-learning-curves/ -->

Grafik kurva belajar editor itu mitos. Mempelajari dasar-dasar editor yang kuat
cukup mudah (meskipun mungkin butuh bertahun-tahun untuk menguasainya).

Editor mana yang populer saat ini? Lihat [survei Stack Overflow
ini](https://insights.stackoverflow.com/survey/2018/#development-environments-and-tools)
(mungkin ada bias karena pengguna Stack Overflow mungkin tidak representatif
bagi programmer secara keseluruhan).

## Editor Command-line

Bahkan jika akhirnya Anda memutuskan menggunakan editor GUI, layak mempelajari
editor command-line untuk mengedit berkas dengan mudah di mesin jarak jauh.

# Nano

Nano adalah editor command-line yang sederhana.

- Bergerak dengan tombol panah
- Semua shortcut lain (save, exit) ditampilkan di bagian bawah

# Vim

Vi/Vim adalah text editor yang kuat. Ini adalah program command-line yang biasanya
terpasang di mana-mana, yang membuatnya praktis untuk mengedit berkas di mesin jarak
jauh.

Vim juga memiliki versi grafis, seperti GVim dan
[MacVim](https://macvim-dev.github.io/macvim/). Ini menyediakan fitur tambahan
seperti warna 24-bit, menu, dan popup.

## Filosofi Vim

- Saat memprogram, Anda menghabiskan sebagian besar waktu membaca/mengedit, bukan menulis
    - Vim adalah editor **modal**: mode berbeda untuk menyisipkan teks versus memanipulasi teks
- Vim dapat diprogram (dengan Vimscript dan juga bahasa lain seperti Python)
- Antarmuka Vim itu sendiri seperti bahasa pemrograman
    - Ketukan tombol (dengan nama mnemonik) adalah perintah
    - Perintah dapat dikomposisikan
- Jangan gunakan mouse: terlalu lambat
- Editor harus bekerja secepat Anda berpikir

## Vim pengantar

### Mode

Vim menampilkan mode saat ini di kiri bawah.

- Mode Normal: untuk bergerak di dalam berkas dan membuat edit
    - Habiskan sebagian besar waktu Anda di sini
- Mode Insert: untuk menyisipkan teks
- Mode Visual (visual, line, atau block): untuk memilih blok teks

Anda mengubah mode dengan menekan `<ESC>` untuk beralih dari mode apa pun kembali ke mode
normal. Dari mode normal, masuk ke mode insert dengan `i`, mode visual dengan `v`,
mode visual line dengan `V`, dan mode visual block dengan `<C-v>`.

Anda menggunakan tombol `<ESC>` cukup sering saat menggunakan Vim: pertimbangkan memetakan ulang Caps Lock ke
Escape.

### Dasar-dasar

Perintah ex Vim dikeluarkan melalui `:{command}` pada mode normal.

- `:q` quit (tutup window)
- `:w` save
- `:wq` save dan quit
- `:e {name of file}` buka berkas untuk diedit
- `:ls` tampilkan buffer yang terbuka
- `:help {topic}` buka bantuan
    - `:help :w` membuka bantuan untuk perintah ex `:w`
    - `:help w` membuka bantuan untuk movement `w`

### Berpindah Posisi

Vim adalah soal movement yang efisien. Bernavigasi di berkas pada mode Normal.

- Nonaktifkan tombol panah untuk menghindari kebiasaan buruk
```vim
nnoremap <Left> :echoe "Use h"<CR>
nnoremap <Right> :echoe "Use l"<CR>
nnoremap <Up> :echoe "Use k"<CR>
nnoremap <Down> :echoe "Use j"<CR>
```
- Movement dasar: `hjkl` (kiri, bawah, atas, kanan)
- Kata: `w` (kata berikutnya), `b` (awal kata), `e` (akhir kata)
- Baris: `0` (awal baris), `^` (karakter pertama yang bukan whitespace), `$` (akhir baris)
- Layar: `H` (bagian atas layar), `M` (bagian tengah layar), `L` (bagian bawah layar)
- Berkas: `gg` (awal berkas), `G` (akhir berkas)
- Line numbers: `:{number}<CR>` atau `{number}G` (baris {number})
- Misc: `%` (item yang bersesuaian)
- Find: `f{character}`, `t{character}`, `F{character}`, `T{character}`
    - mencari/menuju {character} ke depan/ke belakang pada baris saat ini
- Mengulang N kali: `{number}{movement}`, misalnya `10j` bergerak turun 10 baris
- Search: `/{regex}`, `n` / `N` untuk bernavigasi antar kecocokan

### Memilih Teks

Mode visual:

- Visual
- Visual Line
- Visual Block

Anda dapat menggunakan tombol movement untuk membuat seleksi.

### Memanipulasi teks

Segala sesuatu yang dulu Anda lakukan dengan mouse, sekarang Anda lakukan dengan keyboard (dan
perintah yang kuat serta dapat dikomposisikan).

- `i` masuk ke mode insert
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
- `s` mengganti karakter (sama dengan `xi`)
- mode visual + manipulasi
    - pilih teks, `d` untuk menghapusnya atau `c` untuk mengubahnya
- `u` untuk undo, `<C-r>` untuk redo
- Masih banyak yang bisa dipelajari: misalnya `~` membalik kapitalisasi sebuah karakter

### Sumber daya

- Program command-line `vimtutor` untuk mengajarkan vim kepada Anda
- Game [Vim Adventures](https://vim-adventures.com/) untuk mempelajari Vim

## Kustomisasi Vim

Vim dikustomisasi melalui berkas konfigurasi teks biasa di `~/.vimrc`
(memuat perintah Vimscript). Mungkin ada banyak pengaturan dasar yang
ingin Anda aktifkan.

Lihat dotfiles orang lain di GitHub untuk inspirasi, tetapi usahakan tidak
menyalin-tempel konfigurasi lengkap orang. Bacalah, pahami, dan ambil
yang Anda butuhkan.

Beberapa kustomisasi yang perlu dipertimbangkan:

- Syntax highlighting: `syntax on`
- Skema warna
- Nomor baris: `set nu` / `set rnu`
- Backspace melewati segalanya: `set backspace=indent,eol,start`

## Vim tingkat lanjut

Berikut beberapa contoh untuk menunjukkan kekuatan editor ini. Kami tidak dapat mengajarkan
semua hal semacam ini, tetapi Anda akan mempelajarinya seiring berjalan. Heuristik
yang baik: setiap kali Anda menggunakan editor dan berpikir "pasti ada
cara yang lebih baik untuk melakukan ini", kemungkinan besar memang ada: carilah daring.

### Mencari dan Mengganti Teks

Perintah `:s` (substitute) ([dokumentasi](https://vim.fandom.com/wiki/Search_and_replace)).

- `%s/foo/bar/g`
    - ganti foo dengan bar secara global di berkas
- `%s/\[.*\](\(.*\))/\1/g`
    - ganti tautan Markdown bernama dengan URL biasa

### Banyak window

- `sp` / `vsp` untuk membagi window
- Dapat memiliki beberapa tampilan dari buffer yang sama.

### Dukungan mouse

- `set mouse+=a`
    - dapat mengklik, menggulir, memilih

### Macros

- `q{character}` untuk mulai merekam macro di register `{character}`
- `q` untuk berhenti merekam
- `@{character}` memutar ulang macro
- Eksekusi macro berhenti saat terjadi error
- `{number}@{character}` mengeksekusi macro {number} kali
- Macro dapat rekursif
    - bersihkan macro terlebih dahulu dengan `q{character}q`
    - rekam macro, dengan `@{character}` untuk memanggil macro secara rekursif
    (akan menjadi no-op sampai perekaman selesai)
- Contoh: konversi xml ke json ([berkas](/2019/files/example-data.xml))
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

## Memperluas Vim

Ada banyak sekali plugin untuk memperluas vim.

Pertama, siapkan diri Anda dengan plugin manager seperti
[vim-plug](https://github.com/junegunn/vim-plug),
[Vundle](https://github.com/VundleVim/Vundle.vim), atau
[pathogen.vim](https://github.com/tpope/vim-pathogen).

Beberapa plugin yang perlu dipertimbangkan:

- [ctrlp.vim](https://github.com/kien/ctrlp.vim): fuzzy file finder
- [vim-fugitive](https://github.com/tpope/vim-fugitive): integrasi git
- [vim-surround](https://github.com/tpope/vim-surround): memanipulasi "surroundings"
- [gundo.vim](https://github.com/sjl/gundo.vim): bernavigasi di undo tree
- [nerdtree](https://github.com/scrooloose/nerdtree): file explorer
- [syntastic](https://github.com/vim-syntastic/syntastic): pemeriksaan sintaks
- [vim-easymotion](https://github.com/easymotion/vim-easymotion): magic motions
- [vim-over](https://github.com/osyo-manga/vim-over): pratinjau substitute

Daftar plugin:

- [Vim Awesome](https://vimawesome.com/)

## Vim-mode di Program Lain

Untuk banyak editor populer (misalnya vim dan emacs), banyak tool lain mendukung emulasi
editor.

- Shell
    - bash: `set -o vi`
    - zsh: `bindkey -v`
    - `export EDITOR=vim` (environment variable yang digunakan program seperti `git`)
- `~/.inputrc`
    - `set editing-mode vi`

Bahkan ada ekstensi keybinding vim untuk web [browser](https://vim.fandom.com/wiki/Vim_key_bindings_for_web_browsers), beberapa yang populer adalah [Vimium](https://chrome.google.com/webstore/detail/vimium/dbepggeogbaibhgnhhndojpepiihcmeb?hl=en) untuk Google Chrome dan [Tridactyl](https://github.com/tridactyl/tridactyl) untuk Firefox.


## Sumber daya

- [Vim Tips Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2018/): berbagai tip Vim
- [Neovim](https://neovim.io/) adalah reimplementasi vim modern dengan pengembangan yang lebih aktif.
- [Vim Golf](https://www.vimgolf.com/): berbagai tantangan Vim

{% comment %}
# Resources

TODO resources for other editors?
{% endcomment %}

# Latihan

1. Bereksperimenlah dengan beberapa editor. Coba setidaknya satu editor command-line (misalnya
   Vim) dan setidaknya satu editor GUI (misalnya Atom). Belajar melalui tutorial seperti
   `vimtutor` (atau padanannya untuk editor lain). Untuk merasakan sungguh-sungguh
   editor baru, berkomitmenlah menggunakannya secara eksklusif selama beberapa hari saat
   mengerjakan pekerjaan Anda.

1. Kustomisasi editor Anda. Telusuri tip dan trik daring, dan telusuri
   konfigurasi orang lain (sering kali terdokumentasi dengan baik).

1. Bereksperimenlah dengan plugin untuk editor Anda.

1. Berkomitmenlah menggunakan editor yang kuat setidaknya selama beberapa pekan: Anda seharusnya
   mulai melihat manfaatnya saat itu. Pada titik tertentu, Anda seharusnya dapat membuat
   editor Anda bekerja secepat Anda berpikir.

1. Pasang linter (misalnya pyflakes untuk python), hubungkan ke editor Anda dan uji bahwa itu berfungsi.
