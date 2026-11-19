---
layout: lecture-id
title: "Command-line Environment"
description: >
  Pelajari job control, terminal multiplexer, dotfiles, dan mesin jarak jauh dengan SSH.
thumbnail: /static/assets/thumbnails/2020/lec5.png
date: 2020-01-21
ready: true
video:
  aspect: 56.25
  id: e8BO_dYxk5c
lang: id
permalink: /id/2020/command-line/
---

Pada kuliah ini kita akan membahas beberapa cara untuk meningkatkan alur kerja Anda saat menggunakan shell. Kita sudah bekerja dengan shell cukup lama, tetapi kita terutama berfokus pada mengeksekusi berbagai perintah. Sekarang kita akan melihat cara menjalankan beberapa proses sekaligus sambil melacaknya, cara menghentikan atau menjeda proses tertentu dan cara membuat proses berjalan di latar belakang.

Kita juga akan mempelajari berbagai cara meningkatkan shell dan tool Anda, dengan mendefinisikan alias dan mengonfigurasinya menggunakan dotfiles. Keduanya dapat membantu Anda menghemat waktu, misalnya dengan menggunakan konfigurasi yang sama di semua mesin Anda tanpa harus mengetik perintah panjang. Kita akan melihat cara bekerja dengan mesin jarak jauh menggunakan SSH.


# Job Control

Dalam beberapa kasus Anda perlu menginterupsi sebuah job saat sedang dieksekusi, misalnya jika sebuah perintah terlalu lama selesai (seperti `find` dengan struktur direktori yang sangat besar untuk ditelusuri).
Sebagian besar waktu, Anda dapat menekan `Ctrl-C` dan perintah tersebut akan berhenti.
Tetapi bagaimana ini sebenarnya bekerja dan mengapa kadang gagal menghentikan prosesnya?

## Menghentikan proses

Shell Anda menggunakan mekanisme komunikasi UNIX yang disebut _signal_ untuk mengomunikasikan informasi ke proses. Ketika sebuah proses menerima sinyal, proses menghentikan eksekusinya, menangani sinyal tersebut dan berpotensi mengubah alur eksekusi berdasarkan informasi yang dibawa sinyal. Karena alasan ini, sinyal adalah _software interrupt_.

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

```
$ python sigint.py
24^C
I got a SIGINT, but I am not stopping
26^C
I got a SIGINT, but I am not stopping
30^\[1]    39913 quit       python sigint.py
```

Meskipun `SIGINT` dan `SIGQUIT` keduanya biasanya terkait dengan permintaan yang berhubungan dengan terminal, sinyal yang lebih generik untuk meminta proses keluar secara graceful adalah sinyal `SIGTERM`.
Untuk mengirim sinyal ini kita dapat menggunakan perintah [`kill`](https://www.man7.org/linux/man-pages/man1/kill.1.html), dengan sintaks `kill -TERM <PID>`.

## Menjeda dan mem-background proses

Sinyal dapat melakukan hal lain selain mematikan proses. Misalnya, `SIGSTOP` menjeda sebuah proses. Di terminal, mengetik `Ctrl-Z` akan memicu shell mengirim sinyal `SIGTSTP`, singkatan dari Terminal Stop (yakni versi terminal dari `SIGSTOP`).

Kita kemudian dapat melanjutkan job yang dijeda tersebut di foreground atau di background menggunakan [`fg`](https://www.man7.org/linux/man-pages/man1/fg.1p.html) atau [`bg`](https://man7.org/linux/man-pages/man1/bg.1p.html), masing-masing.

Perintah [`jobs`](https://www.man7.org/linux/man-pages/man1/jobs.1p.html) mencantumkan job yang belum selesai yang terkait dengan sesi terminal saat ini.
Anda dapat merujuk job tersebut menggunakan pid-nya (Anda dapat menggunakan [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) untuk mengetahuinya).
Lebih intuitif, Anda juga dapat merujuk sebuah proses menggunakan simbol persen diikuti nomor job-nya (ditampilkan oleh `jobs`). Untuk merujuk job terakhir yang di-background Anda dapat menggunakan parameter khusus `$!`.

Satu hal lagi yang perlu diketahui adalah sufiks `&` pada sebuah perintah akan menjalankan perintah tersebut di background, mengembalikan prompt kepada Anda, meskipun perintah itu tetap menggunakan STDOUT shell yang bisa mengganggu (gunakan shell redirection dalam kasus itu).

Untuk mem-background program yang sudah berjalan Anda dapat melakukan `Ctrl-Z` diikuti `bg`.
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

$ bg %1
[1]  - 18653 continued  sleep 1000

$ jobs
[1]  - running    sleep 1000
[2]  + running    nohup sleep 2000

$ kill -STOP %1
[1]  + 18653 suspended (signal)  sleep 1000

$ jobs
[1]  + suspended (signal)  sleep 1000
[2]  - running    nohup sleep 2000

$ kill -SIGHUP %1
[1]  + 18653 hangup     sleep 1000

$ jobs
[2]  + running    nohup sleep 2000

$ kill -SIGHUP %2

$ jobs
[2]  + running    nohup sleep 2000

$ kill %2
[2]  + 18745 terminated  nohup sleep 2000

$ jobs

```

Sinyal khusus adalah `SIGKILL` karena sinyal ini tidak dapat ditangkap oleh proses dan akan selalu menghentikannya segera. Namun, sinyal ini dapat menimbulkan efek samping buruk seperti meninggalkan child process yang yatim.

Anda dapat mempelajari lebih lanjut tentang sinyal-sinyal ini dan sinyal lainnya [di sini](https://en.wikipedia.org/wiki/Signal_(IPC)) atau dengan mengetik [`man signal`](https://www.man7.org/linux/man-pages/man7/signal.7.html) atau `kill -l`.


# Terminal Multiplexers

Saat menggunakan command line interface Anda akan sering ingin menjalankan lebih dari satu hal sekaligus.
Misalnya, Anda mungkin ingin menjalankan editor dan program Anda secara berdampingan.
Meskipun hal ini dapat dicapai dengan membuka jendela terminal baru, menggunakan terminal multiplexer adalah solusi yang lebih serbaguna.

Terminal multiplexer seperti [`tmux`](https://www.man7.org/linux/man-pages/man1/tmux.1.html) memungkinkan Anda memultipleks jendela terminal menggunakan pane dan tab sehingga Anda dapat berinteraksi dengan beberapa sesi shell.
Selain itu, terminal multiplexer memungkinkan Anda melepas sesi terminal saat ini dan menghubungkannya kembali di waktu lain.
Ini dapat membuat alur kerja Anda jauh lebih baik saat bekerja dengan mesin jarak jauh karena menghindari kebutuhan menggunakan `nohup` dan trik serupa.

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

Untuk bacaan lebih lanjut,
[di sini](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) ada tutorial singkat tentang `tmux` dan [ini](https://linuxcommand.org/lc3_adv_termmux.php) memiliki penjelasan yang lebih terperinci yang juga membahas perintah `screen` yang asli. Anda mungkin juga ingin membiasakan diri dengan [`screen`](https://www.man7.org/linux/man-pages/man1/screen.1.html), karena tool ini terpasang di sebagian besar sistem UNIX.

# Aliases

Mengetik perintah panjang yang melibatkan banyak flag atau opsi verbose bisa melelahkan.
Karena alasan ini, sebagian besar shell mendukung _aliasing_.
Shell alias adalah bentuk singkat untuk perintah lain yang akan diganti otomatis oleh shell Anda.
Misalnya, alias di bash memiliki struktur berikut:

```bash
alias alias_name="command_to_alias arg1 arg2"
```

Perhatikan bahwa tidak ada spasi di sekitar tanda sama dengan `=`, karena [`alias`](https://www.man7.org/linux/man-pages/man1/alias.1p.html) adalah perintah shell yang menerima satu argumen.

Alias memiliki banyak fitur praktis:

```bash
# Make shorthands for common flags
alias ll="ls -lh"

# Save a lot of typing for common commands
alias gs="git status"
alias gc="git commit"
alias v="vim"

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

Perhatikan bahwa alias tidak bertahan antar sesi shell secara default.
Untuk membuat alias bertahan Anda perlu menyertakannya dalam berkas startup shell, seperti `.bashrc` atau `.zshrc`, yang akan kami perkenalkan pada bagian berikutnya.


# Dotfiles

Banyak program dikonfigurasi menggunakan berkas teks biasa yang dikenal sebagai _dotfiles_
(karena nama berkasnya dimulai dengan `.`, misalnya `~/.vimrc`, sehingga berkas tersebut
tersembunyi dari pencantuman direktori `ls` secara default).

Shell adalah salah satu contoh program yang dikonfigurasi dengan berkas semacam itu. Saat startup, shell Anda akan membaca banyak berkas untuk memuat konfigurasinya.
Bergantung pada shell-nya, apakah Anda memulai sesi login dan/atau interaktif, keseluruhan proses bisa cukup kompleks.
[Di sini](https://web.archive.org/web/20260329133158/https://blog.flowblok.id.au/2013-02/shell-startup-scripts.html) ada sumber yang sangat baik tentang topik ini.

Untuk `bash`, mengedit `.bashrc` atau `.bash_profile` Anda akan berfungsi di sebagian besar sistem.
Di sini Anda dapat menyertakan perintah yang ingin Anda jalankan saat startup, seperti alias yang baru kami jelaskan atau modifikasi pada environment variable `PATH` Anda.
Bahkan, banyak program akan meminta Anda menyertakan baris seperti `export PATH="$PATH:/path/to/program/bin"` di berkas konfigurasi shell Anda agar binary-nya dapat ditemukan.

Beberapa contoh lain tool yang dapat dikonfigurasi melalui dotfiles adalah:

- `bash` - `~/.bashrc`, `~/.bash_profile`
- `git` - `~/.gitconfig`
- `vim` - `~/.vimrc` dan folder `~/.vim`
- `ssh` - `~/.ssh/config`
- `tmux` - `~/.tmux.conf`

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


## Portabilitas

Masalah umum dengan dotfiles adalah konfigurasinya mungkin tidak berfungsi saat bekerja dengan beberapa mesin, misalnya jika mesin tersebut memiliki sistem operasi atau shell yang berbeda. Kadang Anda juga ingin beberapa konfigurasi hanya diterapkan pada mesin tertentu.

Ada beberapa trik untuk mempermudahnya.
Jika berkas konfigurasi mendukungnya, gunakan padanan pernyataan if untuk
menerapkan kustomisasi spesifik mesin. Misalnya, shell Anda dapat memiliki sesuatu
seperti:

```bash
if [[ "$(uname)" == "Linux" ]]; then {do_something}; fi

# Check before using shell-specific features
if [[ "$SHELL" == "zsh" ]]; then {do_something}; fi

# You can also make it machine-specific
if [[ "$(hostname)" == "myServer" ]]; then {do_something}; fi
```

Jika berkas konfigurasi mendukungnya, manfaatkan include. Misalnya,
sebuah `~/.gitconfig` dapat memiliki pengaturan:

```
[include]
    path = ~/.gitconfig_local
```

Dan kemudian di setiap mesin, `~/.gitconfig_local` dapat memuat pengaturan
khusus mesin. Anda bahkan dapat melacak ini di repositori terpisah untuk
pengaturan khusus mesin.

Ide ini juga berguna jika Anda ingin program yang berbeda berbagi beberapa konfigurasi. Misalnya, jika Anda ingin `bash` dan `zsh` berbagi kumpulan alias yang sama Anda dapat menuliskannya di `.aliases` dan memiliki blok berikut di keduanya:

```bash
# Test if ~/.aliases exists and source it
if [ -f ~/.aliases ]; then
    source ~/.aliases
fi
```

# Mesin Jarak Jauh

Semakin umum bagi programmer untuk menggunakan server jarak jauh dalam pekerjaan sehari-hari mereka. Jika Anda perlu menggunakan server jarak jauh untuk men-deploy perangkat lunak backend atau Anda membutuhkan server dengan kemampuan komputasi lebih tinggi, pada akhirnya Anda akan menggunakan Secure Shell (SSH). Seperti pada sebagian besar tool yang dibahas, SSH sangat dapat dikonfigurasi sehingga layak untuk dipelajari.

Untuk `ssh` ke sebuah server Anda mengeksekusi perintah sebagai berikut

```bash
ssh foo@bar.mit.edu
```

Di sini kita mencoba ssh sebagai pengguna `foo` di server `bar.mit.edu`.
Server dapat ditentukan dengan URL (seperti `bar.mit.edu`) atau IP (sesuatu seperti `foobar@192.168.1.42`). Nanti kita akan melihat bahwa jika Anda memodifikasi berkas config ssh Anda dapat mengakses hanya dengan sesuatu seperti `ssh bar`.

## Mengeksekusi perintah

Fitur `ssh` yang sering terlewat adalah kemampuan menjalankan perintah secara langsung.
`ssh foobar@server ls` akan mengeksekusi `ls` di folder home foobar.
Ini bekerja dengan pipe, sehingga `ssh foobar@server ls | grep PATTERN` akan melakukan grep secara lokal pada output remote `ls` dan `ls | ssh foobar@server grep PATTERN` akan melakukan grep secara remote pada output lokal `ls`.


## SSH Keys

Autentikasi berbasis key memanfaatkan public-key cryptography untuk membuktikan kepada server bahwa klien memiliki private key rahasia tanpa mengungkapkan key tersebut. Dengan cara ini Anda tidak perlu memasukkan ulang password setiap kali. Meskipun demikian, private key (sering `~/.ssh/id_rsa` dan lebih baru `~/.ssh/id_ed25519`) secara efektif adalah password Anda, jadi perlakukan seperti itu.

### Pembuatan key

Untuk menghasilkan pasangan key Anda dapat menjalankan [`ssh-keygen`](https://www.man7.org/linux/man-pages/man1/ssh-keygen.1.html).
```bash
ssh-keygen -a 100 -t ed25519 -f ~/.ssh/id_ed25519
```
Anda sebaiknya memilih passphrase, untuk menghindari seseorang yang memperoleh private key Anda mengakses server yang berwenang. Gunakan [`ssh-agent`](https://www.man7.org/linux/man-pages/man1/ssh-agent.1.html) atau [`gpg-agent`](https://linux.die.net/man/1/gpg-agent) agar Anda tidak perlu mengetik passphrase setiap kali.

Jika Anda pernah mengonfigurasi push ke GitHub menggunakan SSH key, maka Anda mungkin pernah melakukan langkah-langkah yang diuraikan [di sini](https://help.github.com/articles/connecting-to-github-with-ssh/) dan sudah memiliki pasangan key yang valid. Untuk memeriksa apakah Anda memiliki passphrase dan memvalidasinya Anda dapat menjalankan `ssh-keygen -y -f /path/to/key`.

### Autentikasi berbasis key

`ssh` akan memeriksa `.ssh/authorized_keys` untuk menentukan klien mana yang boleh masuk. Untuk menyalin public key Anda dapat menggunakan:

```bash
cat .ssh/id_ed25519.pub | ssh foobar@remote 'cat >> ~/.ssh/authorized_keys'
```

Solusi yang lebih sederhana dapat dicapai dengan `ssh-copy-id` bila tersedia:

```bash
ssh-copy-id -i .ssh/id_ed25519 foobar@remote
```

## Menyalin berkas melalui SSH

Ada banyak cara menyalin berkas melalui ssh:

- `ssh+tee`, yang paling sederhana adalah menggunakan eksekusi perintah `ssh` dan input STDIN dengan melakukan `cat localfile | ssh remote_server tee serverfile`. Ingat bahwa [`tee`](https://www.man7.org/linux/man-pages/man1/tee.1.html) menulis output dari STDIN ke sebuah berkas.
- [`scp`](https://www.man7.org/linux/man-pages/man1/scp.1.html) saat menyalin berkas/direktori dalam jumlah besar, perintah secure copy `scp` lebih praktis karena dapat dengan mudah melakukan rekursi pada path. Sintaksnya adalah `scp path/to/local_file remote_host:path/to/remote_file`
- [`rsync`](https://www.man7.org/linux/man-pages/man1/rsync.1.html) meningkatkan `scp` dengan mendeteksi berkas identik di lokal dan remote, serta mencegah penyalinan ulang berkas tersebut. Tool ini juga memberikan kendali lebih terperinci atas symlink, permission dan memiliki fitur tambahan seperti flag `--partial` yang dapat melanjutkan dari penyalinan yang sebelumnya terinterupsi. `rsync` memiliki sintaks yang mirip dengan `scp`.

## Port Forwarding

Dalam banyak skenario Anda akan menemukan perangkat lunak yang mendengarkan port tertentu di mesin. Ketika ini terjadi di mesin lokal Anda dapat mengetik `localhost:PORT` atau `127.0.0.1:PORT`, tetapi apa yang Anda lakukan dengan server jarak jauh yang port-nya tidak tersedia langsung melalui jaringan/internet?.

Ini disebut _port forwarding_ dan hadir
dalam dua bentuk: Local Port Forwarding dan Remote Port Forwarding (lihat gambar untuk detail lebih lanjut, kredit gambar dari [posting StackOverflow ini](https://unix.stackexchange.com/questions/115897/whats-ssh-port-forwarding-and-whats-the-difference-between-ssh-local-and-remot)).

**Local Port Forwarding**
![Local Port Forwarding](/static/media/images/local-port-forwarding.png)

**Remote Port Forwarding**
![Remote Port Forwarding](/static/media/images/remote-port-forwarding.png)

Skenario paling umum adalah local port forwarding, di mana sebuah layanan di mesin remote mendengarkan di sebuah port dan Anda ingin menautkan port di mesin lokal Anda untuk meneruskan ke port remote tersebut. Misalnya, jika kita mengeksekusi `jupyter notebook` di server jarak jauh yang mendengarkan port `8888`. Jadi, untuk meneruskannya ke port lokal `9999`, kita akan melakukan `ssh -L 9999:localhost:8888 foobar@remote_server` lalu bernavigasi ke `localhost:9999` di mesin lokal kita.


## Konfigurasi SSH

Kita telah membahas banyak argumen yang dapat kita berikan. Alternatif yang menggoda adalah membuat alias shell seperti
```bash
alias my_server="ssh -i ~/.ssh/id_ed25519 --port 2222 -L 9999:localhost:8888 foobar@remote_server"
```

Namun, ada alternatif yang lebih baik menggunakan `~/.ssh/config`.

```bash
Host vm
    User foobar
    HostName 172.16.174.141
    Port 2222
    IdentityFile ~/.ssh/id_ed25519
    LocalForward 9999 localhost:8888

# Configs can also take wildcards
Host *.mit.edu
    User foobaz
```

Keuntungan tambahan menggunakan berkas `~/.ssh/config` dibandingkan alias adalah bahwa program lain seperti `scp`, `rsync`, `mosh`, &c juga dapat membacanya dan mengonversi pengaturannya menjadi flag yang sesuai.


Perhatikan bahwa berkas `~/.ssh/config` dapat dianggap sebagai dotfile, dan secara umum tidak masalah menyertakannya bersama dotfiles Anda lainnya. Namun, jika Anda mempublikasikannya, pikirkan informasi yang berpotensi Anda berikan kepada orang asing di internet: alamat server Anda, pengguna, port terbuka, &c. Ini dapat memudahkan beberapa jenis serangan sehingga pertimbangkan dengan matang sebelum membagikan konfigurasi SSH Anda.

Konfigurasi sisi server biasanya ditentukan di `/etc/ssh/sshd_config`. Di sini Anda dapat membuat perubahan seperti menonaktifkan autentikasi password, mengubah port ssh, mengaktifkan X11 forwarding, &c. Anda dapat menentukan pengaturan config per pengguna.

## Lain-lain

Masalah umum saat terhubung ke server jarak jauh adalah pemutusan koneksi karena komputer Anda mati, masuk mode sleep, atau berganti jaringan. Lebih jauh lagi jika seseorang memiliki koneksi dengan lag signifikan, menggunakan ssh bisa menjadi sangat menjengkelkan. [Mosh](https://mosh.org/), mobile shell, meningkatkan ssh, memungkinkan koneksi roaming, konektivitas intermiten dan menyediakan intelligent local echo.

Kadang praktis untuk me-mount folder remote. [sshfs](https://github.com/libfuse/sshfs) dapat me-mount folder di server jarak jauh
secara lokal, lalu Anda dapat menggunakan editor lokal.


# Shell dan Framework

Selama kuliah shell tool dan scripting kita membahas shell `bash` karena sejauh ini shell yang paling ada di mana-mana dan sebagian besar sistem memilikinya sebagai opsi default. Meskipun demikian, bash bukan satu-satunya opsi.

Misalnya, shell `zsh` adalah superset dari `bash` dan menyediakan banyak fitur praktis out of the box seperti:

- Globbing yang lebih cerdas, `**`
- Inline globbing/wildcard expansion
- Koreksi ejaan
- Tab completion/selection yang lebih baik
- Path expansion (`cd /u/lo/b` akan diekspansi sebagai `/usr/local/bin`)

**Framework** juga dapat meningkatkan shell Anda. Beberapa framework umum yang populer adalah [prezto](https://github.com/sorin-ionescu/prezto) atau [oh-my-zsh](https://ohmyz.sh/), dan yang lebih kecil yang berfokus pada fitur tertentu seperti [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) atau [zsh-history-substring-search](https://github.com/zsh-users/zsh-history-substring-search). Shell seperti [fish](https://fishshell.com/) menyertakan banyak fitur ramah pengguna ini secara default. Beberapa fitur tersebut meliputi:

- Right prompt
- Command syntax highlighting
- History substring search
- manpage based flag completions
- Autocompletion yang lebih cerdas
- Tema prompt

Satu hal yang perlu diperhatikan saat menggunakan framework ini adalah bahwa framework dapat memperlambat shell Anda, terutama jika kode yang dijalankannya tidak dioptimalkan dengan baik atau terlalu banyak kode. Anda selalu dapat memprofilnya dan menonaktifkan fitur yang tidak sering Anda gunakan atau yang kurang Anda hargai dibandingkan kecepatan.

# Terminal Emulators

Selain menyesuaikan shell Anda, ada baiknya meluangkan waktu untuk memikirkan pilihan **terminal emulator** dan pengaturannya. Ada banyak terminal emulator di luar sana (berikut [perbandingannya](https://anarc.at/blog/2018-04-12-terminal-emulators-1/)).

Karena Anda mungkin menghabiskan ratusan hingga ribuan jam di terminal Anda, menelaah pengaturannya akan terbayar. Beberapa aspek yang mungkin ingin Anda ubah pada terminal Anda meliputi:

- Pilihan font
- Skema warna
- Pintasan keyboard
- Dukungan Tab/Pane
- Konfigurasi scrollback
- Performa (sebagian terminal yang lebih baru seperti [Alacritty](https://github.com/jwilm/alacritty) atau [kitty](https://sw.kovidgoyal.net/kitty/) menawarkan akselerasi GPU).

# Latihan

## Kontrol job

1. Dari apa yang telah kita lihat, kita dapat menggunakan beberapa perintah `ps aux | grep` untuk memperoleh pid job kita lalu mematikannya, tetapi ada cara yang lebih baik untuk melakukannya. Mulai job `sleep 10000` di terminal, background-kan dengan `Ctrl-Z` dan lanjutkan eksekusinya dengan `bg`. Sekarang gunakan [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) untuk menemukan pid-nya dan [`pkill`](https://man7.org/linux/man-pages/man1/pgrep.1.html) untuk mematikannya tanpa pernah mengetik pid itu sendiri. (Petunjuk: gunakan flag `-af`).

1. Misalkan Anda tidak ingin memulai sebuah proses sampai proses lain selesai. Bagaimana Anda melakukannya? Pada latihan ini, proses pembatas kita akan selalu `sleep 60 &`.
Salah satu cara untuk mencapainya adalah menggunakan perintah [`wait`](https://www.man7.org/linux/man-pages/man1/wait.1p.html). Coba jalankan perintah sleep dan buat `ls` menunggu sampai proses background selesai.

    Namun, strategi ini akan gagal jika kita memulai di sesi bash yang berbeda, karena `wait` hanya berfungsi untuk child process. Satu fitur yang tidak kita bahas di catatan adalah bahwa exit status perintah `kill` akan bernilai nol jika berhasil dan bukan nol jika sebaliknya. `kill -0` tidak mengirim sinyal tetapi akan memberikan exit status bukan nol jika proses tidak ada.
    Tulis fungsi bash bernama `pidwait` yang menerima sebuah pid dan menunggu sampai proses yang diberikan selesai. Anda sebaiknya menggunakan `sleep` agar tidak membuang CPU secara tidak perlu.

## Terminal multiplexer

1. Ikuti [tutorial](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/) `tmux` ini lalu pelajari cara melakukan beberapa kustomisasi dasar mengikuti [langkah-langkah ini](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/).

## Aliases

1. Buat alias `dc` yang bermuara ke `cd` untuk saat Anda salah mengetiknya.

1.  Jalankan `history | awk '{$1="";print substr($0,2)}' | sort | uniq -c | sort -n | tail -n 10`  untuk mendapatkan 10 perintah paling sering Anda gunakan dan pertimbangkan menulis alias yang lebih pendek untuk perintah tersebut. Catatan: ini berfungsi untuk Bash; jika Anda menggunakan ZSH, gunakan `history 1` alih-alih hanya `history`.


## Dotfiles

Mari kita perkenalkan Anda dengan dotfiles.
1. Buat folder untuk dotfiles Anda dan siapkan version
   control.
1. Tambahkan konfigurasi untuk setidaknya satu program, misalnya shell Anda, dengan sedikit
   kustomisasi (untuk memulai, bisa sesuatu yang sesederhana menyesuaikan prompt shell Anda dengan menetapkan `$PS1`).
1. Siapkan metode untuk memasang dotfiles Anda dengan cepat (dan tanpa usaha manual) di mesin baru. Ini bisa sesederhana skrip shell yang memanggil `ln -s` untuk setiap berkas, atau Anda dapat menggunakan [utility
   khusus](https://dotfiles.github.io/utilities/).
1. Uji skrip pemasangan Anda pada virtual machine yang baru.
1. Migrasikan semua konfigurasi tool Anda saat ini ke repositori dotfiles Anda.
1. Publikasikan dotfiles Anda di GitHub.

## Mesin Jarak Jauh

Pasang Linux virtual machine (atau gunakan yang sudah ada) untuk latihan ini. Jika Anda belum familiar dengan virtual machine, lihat [ini](https://hibbard.eu/install-ubuntu-virtual-box/) tutorial untuk memasangnya.

1. Buka `~/.ssh/` dan periksa apakah Anda memiliki pasangan SSH key di sana. Jika tidak, hasilkan dengan `ssh-keygen -a 100 -t ed25519`. Disarankan Anda menggunakan password dan menggunakan `ssh-agent` , info lebih lanjut [di sini](https://www.ssh.com/ssh/agent).
1. Edit `.ssh/config` agar memiliki entri sebagai berikut

    ```bash
    Host vm
        User username_goes_here
        HostName ip_goes_here
        IdentityFile ~/.ssh/id_ed25519
        LocalForward 9999 localhost:8888
    ```
1. Gunakan `ssh-copy-id vm` untuk menyalin ssh key Anda ke server.
1. Mulai webserver di VM Anda dengan mengeksekusi `python -m http.server 8888`. Akses webserver VM dengan bernavigasi ke `http://localhost:9999` di mesin Anda.
1. Edit konfigurasi server SSH Anda dengan melakukan  `sudo vim /etc/ssh/sshd_config` dan nonaktifkan autentikasi password dengan mengedit nilai `PasswordAuthentication`. Nonaktifkan login root dengan mengedit nilai `PermitRootLogin`. Restart layanan `ssh` dengan `sudo service sshd restart`. Coba ssh masuk lagi.
1. (Challenge) Pasang [`mosh`](https://mosh.org/) di VM dan bangun koneksi. Lalu putuskan network adapter server/VM tersebut. Dapatkah mosh pulih dengan benar?
1. (Challenge) Telaah apa fungsi flag `-N` dan `-f` pada `ssh` dan cari tahu perintah untuk mencapai background port forwarding.
