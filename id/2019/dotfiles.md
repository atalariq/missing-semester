---
layout: lecture-id
title: "Dotfiles"
presenter: Anish
date: 2019-01-24
order: 1
video:
  aspect: 62.5
  id: YSZBWWJw3mI
lang: id
permalink: /id/2019/dotfiles/
---

Banyak program dikonfigurasi menggunakan berkas teks biasa yang dikenal sebagai "dotfiles"
(karena nama berkasnya dimulai dengan `.`, misalnya `~/.gitconfig`, sehingga berkas tersebut
tersembunyi dari pencantuman direktori `ls` secara default).

Banyak tool yang Anda gunakan mungkin memiliki banyak pengaturan yang dapat disetel
dengan cukup teliti. Sering kali, tool dikustomisasi dengan bahasa khusus,
misalnya Vimscript untuk Vim atau bahasa shell itu sendiri untuk sebuah shell.

Menyesuaikan dan mengadaptasi tool Anda ke alur kerja pilihan Anda akan membuat Anda
lebih produktif. Kami menyarankan Anda menginvestasikan waktu untuk menyesuaikan tool Anda sendiri
alih-alih meng-clone dotfiles orang lain dari GitHub.

Anda mungkin sudah memiliki beberapa dotfiles. Beberapa tempat untuk dilihat:

- `~/.bashrc`
- `~/.emacs`
- `~/.vim`
- `~/.gitconfig`

Sebagian program tidak menempatkan berkasnya langsung di bawah folder home Anda dan sebagai gantinya menempatkannya di folder di bawah `~/.config`.

Dotfiles tidak eksklusif untuk aplikasi command line, misalnya pemutar video [MPV](https://mpv.io/) dapat dikonfigurasi dengan mengedit berkas di bawah `~/.config/mpv`

# Belajar menyesuaikan tool

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

# Organisasi

Bagaimana Anda sebaiknya mengorganisasi dotfiles Anda? Dotfiles sebaiknya berada di foldernya sendiri,
di bawah version control, dan **symlink** ke tempatnya menggunakan sebuah skrip. Ini memiliki
manfaat:

- **Pemasangan mudah**: jika Anda login ke mesin baru, menerapkan
kustomisasi Anda hanya akan memakan waktu satu menit
- **Portabilitas**: tool Anda akan bekerja dengan cara yang sama di mana pun
- **Sinkronisasi**: Anda dapat memperbarui dotfiles Anda di mana saja dan menjaga semuanya
tetap sinkron
- **Pelacakan perubahan**: Anda mungkin akan memelihara dotfiles Anda
sepanjang karier pemrograman Anda, dan riwayat versi berguna untuk
proyek yang berumur panjang

```shell
cd ~/src
mkdir dotfiles
cd dotfiles
git init
touch bashrc
# create a bashrc with some settings, e.g.:
#     PS1='\w > '
touch install
chmod +x install
# insert the following into the install script:
#     #!/usr/bin/env bash
#     BASEDIR=$(dirname $0)
#     cd $BASEDIR
#
#     ln -s ${PWD}/bashrc ~/.bashrc
git add bashrc install
git commit -m 'Initial commit'
```

# Topik lanjutan

## Kustomisasi spesifik mesin

Sebagian besar waktu, Anda ingin konfigurasi yang sama di semua mesin, tetapi
kadang, Anda ingin delta kecil pada mesin tertentu. Berikut beberapa cara
Anda dapat menangani situasi ini:

### Branch per mesin

Gunakan version control untuk memelihara branch per mesin. Pendekatan ini
secara logis mudah tetapi bisa cukup berat.

### If statement

Jika berkas konfigurasi mendukungnya, gunakan padanan pernyataan if untuk
menerapkan kustomisasi spesifik mesin. Misalnya, shell Anda dapat memiliki sesuatu
seperti:

```shell
if [[ "$(uname)" == "Linux" ]]; then {do_something else}; fi

# Darwin is the architecture name for macOS systems
if [[ "$(uname)" == "Darwin" ]]; then {do_something}; fi

# You can also make it machine specific
if [[ "$(hostname)" == "myServer" ]]; then {do_something}; fi
```

### Include

Jika berkas konfigurasi mendukungnya, manfaatkan include. Misalnya,
sebuah `~/.gitconfig` dapat memiliki pengaturan:

```
[include]
    path = ~/.gitconfig_local
```

Dan kemudian di setiap mesin, `~/.gitconfig_local` dapat memuat pengaturan
khusus mesin. Anda bahkan dapat melacak ini di repositori terpisah untuk
pengaturan khusus mesin.

Ide ini juga berguna jika Anda ingin program yang berbeda berbagi beberapa konfigurasi. Misalnya jika Anda ingin `bash` dan `zsh` berbagi kumpulan alias yang sama Anda dapat menuliskannya di `.aliases` dan memiliki blok berikut di keduanya.

```bash
# Test if ~/.aliases exists and source it
if [ -f ~/.aliases ]; then
    source ~/.aliases
fi
```

# Sumber daya

- Dotfiles pengajar Anda:
  [Anish](https://github.com/anishathalye/dotfiles),
  [Jon](https://github.com/jonhoo/configs),
  [Jose](https://github.com/jjgo/dotfiles)
- [GitHub does dotfiles](https://dotfiles.github.io/): framework dotfile,
utilitas, contoh, dan tutorial
- [Shell startup
  scripts](https://web.archive.org/web/20260329133158/https://blog.flowblok.id.au/2013-02/shell-startup-scripts.html): penjelasan
  tentang berbagai berkas konfigurasi yang digunakan untuk shell Anda

# Latihan

1. Buat folder untuk dotfiles Anda dan siapkan [version
   control](/2019/version-control/).

1. Tambahkan konfigurasi untuk setidaknya satu program, misalnya shell Anda, dengan sedikit
   kustomisasi (untuk memulai, bisa sesuatu yang sesederhana menyesuaikan
   prompt shell Anda dengan menetapkan `$PS1`).

1. Siapkan metode untuk memasang dotfiles Anda dengan cepat (dan tanpa usaha manual)
   di mesin baru. Ini bisa sesederhana skrip shell yang memanggil `ln -s`
   untuk setiap berkas, atau Anda dapat menggunakan [utilitas
   khusus](https://dotfiles.github.io/utilities/).

1. Uji skrip pemasangan Anda pada virtual machine yang baru.

1. Migrasikan semua konfigurasi tool Anda saat ini ke repositori dotfiles Anda.

1. Publikasikan dotfiles Anda di GitHub.
