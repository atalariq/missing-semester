---
layout: lecture-id
title: "Command-line environment"
presenter: Jose
date: 2019-01-17
order: 1
video:
  aspect: 62.5
  id: i0rf1gpKL1E
lang: id
permalink: /id/2019/command-line/
---

## Alias dan Function

Seperti yang dapat Anda bayangkan, mengetik perintah panjang yang melibatkan banyak flag atau opsi verbose bisa melelahkan. Meskipun demikian, sebagian besar shell mendukung **aliasing**. Misalnya, alias di bash memiliki struktur berikut (perhatikan tidak ada spasi di sekitar tanda `=`):

```bash
alias alias_name="command_to_alias"
```

<!-- We can alias common flags for our commands like `alias ll=ls -ltAh`. Alias can be composed  -->

Alias memiliki banyak fitur praktis

```bash
# Alias can summarize good default flags
alias ll="ls -lh"

# Save a lot of typing for common commands
alias gc="git commit"

# Alias can overwrite existing commands
alias mv="mv -i"
alias mkdir="mkdir -p"

# Alias can be composed
alias la="ls -A"
alias lla="la -l"

# To ignore an alias run it prepended with \
\ls
# Or can be disabled using unalias
unalias la

```
<!--
To get rid of an alias you can run `unalias alias_name` or to ignore alias when running a command you can prepend the command with a backward slash `\alias_name`. This is convenient when an alias is overwriting an existing name. -->


Namun dalam banyak skenario alias bisa membatasi, terutama ketika Anda mencoba menulis perintah berantai yang menerima argumen yang sama. Ada alternatif yang disebut **function** yang merupakan titik tengah antara alias dan skrip shell kustom.

Berikut contoh fungsi yang membuat direktori dan berpindah ke dalamnya.

```bash
mcd () {
    mkdir -p $1
    cd $1
}
```

Alias dan fungsi tidak akan bertahan antar sesi shell secara default. Untuk membuat alias bertahan Anda perlu menyertakannya di salah satu berkas skrip startup shell seperti `.bashrc` atau `.zshrc`. Saran saya adalah menuliskannya terpisah di berkas `.alias` lalu melakukan `source` pada berkas itu dari berbagai berkas konfigurasi shell Anda.

<!-- Lastly, if you decide to alias any of these tools with the "improved" version, e.g. `alias bat=cat` it is useful to know that you can tell bash to ignore aliases by doing `\cat` and ignore both aliases and functions by doing `command cat` -->

## Shell dan Framework

Selama kuliah shell dan scripting kita membahas shell `bash` karena sejauh ini shell yang paling ada di mana-mana dan sebagian besar sistem memilikinya sebagai opsi default. Meskipun demikian, bash bukan satu-satunya opsi.

Misalnya shell `zsh` adalah superset dari `bash` dan menyediakan banyak fitur praktis out of the box seperti:

- Globbing yang lebih cerdas, `**`
- Inline globbing/wildcard expansion
- Koreksi ejaan
- Tab completion/selection yang lebih baik
- Path expansion (`cd /u/lo/b` akan diekspansi sebagai `/usr/local/bin`)

Lebih jauh lagi banyak shell dapat ditingkatkan dengan **framework**, beberapa framework umum yang populer seperti [prezto](https://github.com/sorin-ionescu/prezto) atau [oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh), dan yang lebih kecil yang berfokus pada fitur tertentu seperti misalnya [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) atau [zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search). Shell lain seperti [fish](https://fishshell.com/) menyertakan banyak fitur ramah pengguna ini secara default. Beberapa fitur tersebut meliputi:

- Right prompt
- Command syntax highlighting
- History substring search
- manpage based flag completions
- Autocompletion yang lebih cerdas
- Tema prompt

Satu hal yang perlu diperhatikan saat menggunakan framework ini adalah jika kode yang dijalankannya tidak dioptimalkan dengan baik atau terlalu banyak kode, shell Anda bisa mulai melambat. Anda selalu dapat memprofilnya dan menonaktifkan fitur yang tidak sering Anda gunakan atau yang kurang Anda hargai dibandingkan kecepatan.

## Terminal Emulator dan Multiplexer

Selain menyesuaikan shell Anda, ada baiknya meluangkan waktu untuk memikirkan pilihan **terminal emulator** dan pengaturannya. Ada banyak terminal emulator di luar sana (berikut [perbandingannya](https://anarc.at/blog/2018-04-12-terminal-emulators-1/)).

Karena Anda mungkin menghabiskan ratusan hingga ribuan jam di terminal Anda, menelaah pengaturannya akan terbayar. Beberapa aspek yang mungkin ingin Anda ubah pada terminal Anda meliputi:

- Pilihan font
- Skema warna
- Pintasan keyboard
- Dukungan Tab/Pane
- Konfigurasi scrollback
- Performa (sebagian terminal yang lebih baru seperti [Alacritty](https://github.com/jwilm/alacritty) menawarkan akselerasi GPU)

Ada baiknya juga menyebutkan **terminal multiplexer** seperti [tmux](https://github.com/tmux/tmux). `tmux` memungkinkan Anda membuat pane dan tab untuk beberapa sesi shell. Tool ini juga mendukung attach dan detach yang merupakan use case sangat umum ketika Anda bekerja di server jarak jauh dan ingin menjaga shell Anda tetap berjalan tanpa harus khawatir melakukan disown pada proses Anda saat ini (secara default ketika Anda logout proses Anda dihentikan). Dengan cara ini, dengan `tmux` Anda dapat masuk dan keluar dari tata letak terminal yang kompleks. Serupa dengan terminal emulator, `tmux` mendukung kustomisasi berat dengan mengedit berkas `~/.tmux.conf`.


## Utilitas command-line

Utilitas command-line yang dimiliki sebagian besar sistem operasi berbasis UNIX secara default lebih dari cukup untuk melakukan 99% hal yang biasanya perlu Anda lakukan.


Pada beberapa subbagian berikutnya saya akan membahas tool alternatif untuk operasi shell yang sangat umum yang lebih praktis digunakan. Sebagian tool ini menambahkan fungsionalitas baru yang lebih baik pada perintah sedangkan yang lain hanya berfokus memberikan antarmuka yang lebih sederhana dan intuitif dengan default yang lebih baik.

### `fasd` vs `cd`

Bahkan dengan path expansion dan tab autocomplete yang lebih baik, berpindah direktori bisa menjadi cukup berulang. [Fasd](https://github.com/clvv/fasd) (atau [autojump](https://github.com/wting/autojump)) menyelesaikan masalah ini dengan melacak folder yang baru dan sering Anda kunjungi serta melakukan fuzzy matching.

Jadi jika saya pernah mengunjungi path `/home/user/awesome_project/code` menjalankan `z code` akan melakukan `cd` ke sana. Jika saya memiliki beberapa folder bernama code saya dapat memperjelasnya dengan menjalankan `z awe code` yang akan lebih mendekati. Berbeda dengan autojump, fasd juga menyediakan perintah yang alih-alih melakukan `cd` hanya mengekspansi berkas, folder, atau keduanya yang sering dan/atau baru.


### `bat` vs `cat`

Meskipun `cat` melakukan tugasnya dengan sempurna, [bat](https://github.com/sharkdp/bat) meningkatkannya dengan menyediakan syntax highlighting, paging, nomor baris dan integrasi git.


### `exa`/`ranger` vs `ls`

`ls` adalah perintah yang hebat tetapi sebagian defaultnya bisa mengganggu seperti menampilkan ukuran dalam byte mentah. [exa](https://github.com/ogham/exa) menyediakan default yang lebih baik

Jika Anda perlu bernavigasi di banyak folder dan/atau mempratinjau banyak berkas, [ranger](https://github.com/ranger/ranger) bisa jauh lebih efisien daripada `cd` dan `cat` karena antarmukanya yang luar biasa. Tool ini cukup dapat disesuaikan dan dengan pengaturan yang benar Anda bahkan dapat [mempratinjau gambar](https://github.com/ranger/ranger/wiki/Image-Previews) di terminal Anda

### `fd` vs `find`

[fd](https://github.com/sharkdp/fd) adalah alternatif `find` yang sederhana, cepat dan ramah pengguna. Default `find` seperti harus menggunakan flag `--name` (yang 99% waktu adalah yang ingin Anda lakukan) membuatnya lebih mudah digunakan sehari-hari. Tool ini juga sadar `git` dan akan melewati berkas di `.gitignore` dan folder `.git` Anda secara default. Tool ini juga memiliki color coding yang bagus secara default.

### `rg/fzf` vs `grep`

`grep` adalah tool yang hebat tetapi jika Anda ingin melakukan grep melalui banyak berkas sekaligus, ada tool yang lebih baik untuk tujuan itu. [ack](https://github.com/beyondgrep/ack3), [ag](https://github.com/ggreer/the_silver_searcher) & [rg](https://github.com/BurntSushi/ripgrep) mencari pola regex di direktori saat ini secara rekursif sambil mematuhi aturan gitignore Anda. Semuanya bekerja cukup mirip tetapi saya lebih memilih `rg` karena kecepatannya mencari seluruh direktori home saya.

Demikian pula, mudah untuk mendapati diri Anda melakukan `CMD | grep PATTERN` berulang kali. [fzf](https://github.com/junegunn/fzf) adalah fuzzy finder command line yang memungkinkan Anda memfilter output hampir semua perintah secara interaktif.

### `rsync` vs `cp/scp`

Meskipun `mv` dan `scp` sangat sempurna untuk sebagian besar skenario, saat menyalin/memindahkan berkas dalam jumlah besar, berkas besar, atau ketika sebagian data sudah ada di tujuan `rsync` adalah peningkatan besar. `rsync` akan melewati berkas yang sudah ditransfer dan dengan flag `--partial` tool ini dapat melanjutkan dari penyalinan yang sebelumnya terinterupsi.

### `trash` vs `rm`

`rm` adalah perintah berbahaya dalam arti setelah Anda menghapus berkas tidak ada jalan kembali. Namun, OS modern tidak berperilaku seperti itu ketika Anda menghapus sesuatu di file explorer, OS hanya memindahkannya ke folder Trash yang dikosongkan secara berkala.

Karena cara trash dikelola berbeda antar OS tidak ada satu utilitas CLI tunggal. Di macOS ada [trash](https://hasseg.org/trash/) dan di linux ada [trash-cli](https://github.com/andreafrancia/trash-cli/) antara lain.

### `mosh` vs `ssh`

`ssh ` adalah tool yang sangat praktis tetapi jika Anda memiliki koneksi lambat, lag-nya bisa mengganggu dan jika koneksi terputus Anda harus terhubung kembali. [mosh](https://mosh.org/) adalah tool praktis yang memungkinkan roaming, mendukung konektivitas intermiten, dan menyediakan intelligent local echo.

### `tldr` vs `man`

Anda dapat mencari tahu apa yang dilakukan sebuah perintah dan opsi apa yang dimilikinya menggunakan `man` dan flag `-h`/'--help' sebagian besar waktu. Namun, dalam beberapa kasus bisa sedikit menakutkan menelusurinya jika sangat detail

Perintah [tldr](https://github.com/tldr-pages/tldr) adalah sistem dokumentasi yang digerakkan komunitas yang tersedia dari command line dan memberikan beberapa contoh ilustratif sederhana tentang apa yang dilakukan perintah serta opsi argumen yang paling umum.


### `aunpack` vs `tar/unzip/unrar`

Seperti yang dirujuk [xkcd ini](https://xkcd.com/1168/), cukup rumit untuk mengingat opsi `tar` dan kadang Anda membutuhkan tool yang sama sekali berbeda seperti `unrar` untuk berkas .rar.
Paket [atool](https://www.nongnu.org/atool/) menyediakan perintah `aunpack` yang akan mencari tahu opsi yang benar dan selalu menempatkan arsip yang diekstrak ke folder baru.


## Latihan

1. Jalankan `cat .bash_history | sort | uniq -c | sort -rn | head -n 10` (atau `cat .zhistory | sort | uniq -c | sort -rn | head -n 10` untuk zsh)  untuk mendapatkan 10 perintah paling sering digunakan dan pertimbangkan menulis alias yang lebih pendek untuk perintah tersebut
1. Pilih sebuah terminal emulator dan cari tahu cara mengubah properti berikut:
    - Pilihan font
    - Skema warna. Berapa banyak warna yang dimiliki skema standar? mengapa?
    - Ukuran riwayat scrollback

1. Pasang `fasd` atau perangkat lunak serupa dan tulis fungsi bash/zsh bernama `v` yang melakukan fuzzy matching pada argumen yang diberikan dan membuka hasil teratas di editor pilihan Anda. Lalu, modifikasi agar jika ada beberapa kecocokan Anda dapat memilihnya dengan `fzf`.
1. Karena `fzf` cukup praktis untuk melakukan pencarian fuzzy dan riwayat shell cukup rentan terhadap pencarian semacam itu, selidiki cara mengikat `fzf` ke `^R`. Anda dapat menemukan beberapa info [di sini](https://github.com/junegunn/fzf/wiki/Configuring-shell-key-bindings)
1. Apa fungsi opsi `--bar` di `ack`?
