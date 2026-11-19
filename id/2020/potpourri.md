---
layout: lecture-id
title: "Potpourri"
description: >
  Pelajari berbagai topik bermanfaat, termasuk keyboard remapping, daemon, backup, API, dan lainnya.
thumbnail: /static/assets/thumbnails/2020/lec10.png
date: 2020-01-29
ready: true
video:
  aspect: 56.25
  id: JZDt-PRq0uo
special: true
lang: id
permalink: /id/2020/potpourri/
---

## Daftar isi

- [Pemetaan ulang keyboard](#keyboard-remapping)
- [Daemon](#daemons)
- [FUSE](#fuse)
- [Backup](#backups)
- [API](#apis)
- [Flag/pola command-line yang umum](#common-command-line-flagspatterns)
- [Window manager](#window-managers)
- [VPN](#vpns)
- [Markdown](#markdown)
- [Hammerspoon (otomasi desktop di macOS)](#hammerspoon-desktop-automation-on-macos)
- [Booting + Live USB](#booting--live-usbs)
- [Docker, Vagrant, VM, Cloud, OpenStack](#docker-vagrant-vms-cloud-openstack)
- [Pemrograman notebook](#notebook-programming)
- [GitHub](#github)

<a id="keyboard-remapping"></a>
## Pemetaan ulang keyboard

Sebagai programmer, keyboard adalah metode input utama Anda. Seperti hampir semua hal di komputer Anda, keyboard dapat dikonfigurasi (dan layak dikonfigurasi).

Perubahan paling dasar adalah memetakan ulang tombol.
Ini biasanya melibatkan beberapa perangkat lunak yang mendengarkan dan, setiap kali tombol tertentu ditekan, mencegat peristiwa tersebut dan menggantinya dengan peristiwa lain yang bersesuaian dengan tombol berbeda. Beberapa contoh:
- Memetakan ulang Caps Lock ke Ctrl atau Escape. Kami (para pengajar) sangat mendorong pengaturan ini karena Caps Lock memiliki posisi yang sangat praktis tetapi jarang digunakan.
- Memetakan ulang PrtSc ke Play/Pause musik. Sebagian besar OS memiliki tombol play/pause.
- Menukar Ctrl dan tombol Meta (Windows atau Command).

Anda juga dapat memetakan tombol ke perintah arbitrer pilihan Anda. Ini berguna untuk tugas umum yang Anda lakukan. Di sini, beberapa perangkat lunak mendengarkan kombinasi tombol tertentu dan mengeksekusi skrip setiap kali peristiwa itu terdeteksi.
- Membuka terminal atau jendela browser baru.
- Menyisipkan teks tertentu, misalnya alamat email panjang Anda atau nomor MIT ID Anda.
- Membuat komputer atau layar tidur.

Bahkan ada modifikasi yang lebih kompleks yang dapat Anda konfigurasi:
- Memetakan ulang rangkaian tombol, misalnya menekan shift lima kali untuk mengaktifkan/mematikan Caps Lock.
- Memetakan ulang saat tap versus saat ditahan, misalnya tombol Caps Lock dipetakan ke Esc jika Anda menekannya sebentar, tetapi dipetakan ke Ctrl jika Anda menahannya dan menggunakannya sebagai modifier.
- Membuat pemetaan ulang spesifik untuk keyboard atau perangkat lunak tertentu.

Beberapa sumber perangkat lunak untuk memulai topik ini:
- macOS - [karabiner-elements](https://karabiner-elements.pqrs.org/), [skhd](https://github.com/koekeishiya/skhd) atau [BetterTouchTool](https://folivora.ai/)
- Linux - [xmodmap](https://wiki.archlinux.org/index.php/Xmodmap) atau [Autokey](https://github.com/autokey/autokey)
- Windows - Bawaan di Control Panel, [AutoHotkey](https://www.autohotkey.com/) atau [SharpKeys](https://www.randyrants.com/category/sharpkeys/)
- QMK - Jika keyboard Anda mendukung firmware kustom Anda dapat menggunakan [QMK](https://docs.qmk.fm/) untuk mengonfigurasi perangkat keras itu sendiri sehingga pemetaan ulang bekerja untuk mesin apa pun yang Anda gunakan bersama keyboard tersebut.

<a id="daemons"></a>
## Daemon

Anda mungkin sudah familiar dengan gagasan daemon, meskipun kata itu terdengar baru.
Sebagian besar komputer memiliki serangkaian proses yang selalu berjalan di latar belakang alih-alih menunggu pengguna meluncurkannya dan berinteraksi dengannya.
Proses ini disebut daemon dan program yang berjalan sebagai daemon sering diakhiri dengan `d` untuk menunjukkannya.
Misalnya `sshd`, daemon SSH, adalah program yang bertanggung jawab mendengarkan permintaan SSH yang masuk dan memeriksa bahwa pengguna jarak jauh memiliki kredensial yang diperlukan untuk login.

Di Linux, `systemd` (system daemon) adalah solusi paling umum untuk menjalankan dan menyiapkan proses daemon.
Anda dapat menjalankan `systemctl status` untuk mencantumkan daemon yang sedang berjalan. Sebagian besar mungkin terdengar asing tetapi bertanggung jawab atas bagian inti sistem seperti mengelola jaringan, menyelesaikan kueri DNS atau menampilkan antarmuka grafis sistem.
Systemd dapat diinteraksikan dengan perintah `systemctl` untuk `enable`, `disable`, `start`, `stop`, `restart` atau memeriksa `status` layanan (itu adalah perintah `systemctl`).

Lebih menarik lagi, `systemd` memiliki antarmuka yang cukup mudah diakses untuk mengonfigurasi dan mengaktifkan daemon (atau layanan) baru.
Berikut contoh daemon untuk menjalankan aplikasi Python sederhana.
Kami tidak akan membahas detailnya tetapi seperti yang Anda lihat sebagian besar field cukup menjelaskan dirinya sendiri.

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Custom App
After=network.target

[Service]
User=foo
Group=foo
WorkingDirectory=/home/foo/projects/mydaemon
ExecStart=/usr/bin/local/python3.7 app.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Juga, jika Anda hanya ingin menjalankan beberapa program dengan frekuensi tertentu tidak perlu membuat daemon khusus, Anda dapat menggunakan [`cron`](https://www.man7.org/linux/man-pages/man8/cron.8.html), daemon yang sudah dijalankan sistem Anda untuk melakukan tugas terjadwal.

<a id="fuse"></a>
## FUSE

Sistem perangkat lunak modern biasanya tersusun dari blok bangunan lebih kecil yang dikomposisikan bersama.
Sistem operasi Anda mendukung penggunaan backend filesystem yang berbeda karena ada bahasa umum tentang operasi apa yang didukung sebuah filesystem.
Misalnya, ketika Anda menjalankan `touch` untuk membuat berkas, `touch` melakukan system call ke kernel untuk membuat berkas dan kernel melakukan pemanggilan filesystem yang sesuai untuk membuat berkas tersebut.
Satu catatan penting adalah filesystem UNIX secara tradisional diimplementasikan sebagai module kernel dan hanya kernel yang diizinkan melakukan pemanggilan filesystem.

[FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace) (Filesystem in User Space) memungkinkan filesystem diimplementasikan oleh program pengguna. FUSE memungkinkan pengguna menjalankan kode user space untuk pemanggilan filesystem lalu menjembatani pemanggilan yang diperlukan ke antarmuka kernel.
Dalam praktiknya, ini berarti pengguna dapat mengimplementasikan fungsionalitas arbitrer untuk pemanggilan filesystem.

Misalnya, FUSE dapat digunakan sehingga setiap kali Anda melakukan operasi di filesystem virtual, operasi tersebut diteruskan melalui SSH ke mesin jarak jauh, dilakukan di sana, dan outputnya dikembalikan kepada Anda.
Dengan cara ini, program lokal dapat melihat berkas tersebut seolah-olah berada di komputer Anda padahal kenyataannya berada di server jarak jauh.
Ini secara efektif adalah apa yang dilakukan `sshfs`.

Beberapa contoh menarik filesystem FUSE adalah:
- [sshfs](https://github.com/libfuse/sshfs) - Membuka berkas/folder remote secara lokal melalui koneksi SSH.
- [rclone](https://rclone.org/commands/rclone_mount/) - Me-mount layanan cloud storage seperti Dropbox, GDrive, Amazon S3 atau Google Cloud Storage dan membuka data secara lokal.
- [gocryptfs](https://nuetzlich.net/gocryptfs/) - Sistem overlay terenkripsi. Berkas disimpan terenkripsi tetapi setelah FS di-mount berkas tampil sebagai plaintext di mountpoint.
- [kbfs](https://keybase.io/docs/kbfs) - Filesystem terdistribusi dengan enkripsi end-to-end. Anda dapat memiliki folder privat, bersama dan publik.
- [borgbackup](https://borgbackup.readthedocs.io/en/stable/usage/mount.html) - Me-mount backup Anda yang telah di-deduplikasi, dikompresi dan dienkripsi agar mudah ditelusuri.

<a id="backups"></a>
## Backup

Data apa pun yang belum Anda backup adalah data yang bisa hilang kapan saja, selamanya.
Menyalin data itu mudah, melakukan backup data secara andal itu sulit.
Berikut beberapa dasar backup yang baik dan jebakan dari beberapa pendekatan.

Pertama, salinan data di disk yang sama bukanlah backup, karena disk adalah single point of failure untuk semua data tersebut. Demikian pula, drive eksternal di rumah Anda juga merupakan solusi backup yang lemah karena bisa hilang dalam kebakaran/perampokan/&c. Sebagai gantinya, memiliki backup off-site adalah praktik yang direkomendasikan.

Solusi sinkronisasi bukanlah backup. Misalnya, Dropbox/GDrive adalah solusi yang praktis, tetapi ketika data dihapus atau rusak, solusi tersebut menyebarkan perubahannya. Karena alasan yang sama, solusi disk mirroring seperti RAID bukanlah backup. Itu tidak membantu jika data terhapus, rusak atau terenkripsi oleh ransomware.

Beberapa fitur inti solusi backup yang baik adalah versioning, deduplication dan security.
Backup dengan versioning memastikan Anda dapat mengakses riwayat perubahan Anda dan memulihkan berkas secara efisien.
Solusi backup yang efisien menggunakan data deduplication untuk hanya menyimpan perubahan inkremental dan mengurangi overhead penyimpanan.
Terkait security, Anda sebaiknya bertanya pada diri sendiri apa yang perlu diketahui/dimiliki seseorang untuk membaca data Anda dan, lebih penting lagi, untuk menghapus semua data Anda dan backup terkait.
Terakhir, memercayai backup secara buta adalah ide buruk dan Anda sebaiknya memverifikasi secara rutin bahwa Anda dapat menggunakannya untuk memulihkan data.

Backup melampaui berkas lokal di komputer Anda.
Mengingat pertumbuhan signifikan aplikasi web, sejumlah besar data Anda hanya tersimpan di cloud.
Misalnya, webmail Anda, foto media sosial, playlist musik di layanan streaming atau dokumen daring akan hilang jika Anda kehilangan akses ke akun yang bersesuaian.
Memiliki salinan offline informasi ini adalah jalan yang tepat, dan Anda dapat menemukan tool daring yang dibuat orang untuk mengambil data dan menyimpannya.

Untuk penjelasan lebih detail, lihat catatan kuliah 2019 tentang [Backups](/2019/backups).


<a id="apis"></a>
## API

Kita telah banyak membahas di kelas ini tentang menggunakan komputer Anda secara lebih
efisien untuk menyelesaikan tugas _lokal_, tetapi Anda akan menemukan bahwa banyak
pelajaran ini juga berlaku untuk internet yang lebih luas. Sebagian besar layanan daring
memiliki "API" yang memungkinkan Anda mengakses datanya secara programatik. Misalnya,
pemerintah AS memiliki API yang memungkinkan Anda memperoleh prakiraan cuaca,
yang dapat Anda gunakan untuk dengan mudah memperoleh prakiraan cuaca di
shell Anda.

Sebagian besar API ini memiliki format serupa. API tersebut berupa URL terstruktur,
sering kali berakar di `api.service.com`, di mana path dan query parameter
menunjukkan data apa yang ingin Anda baca atau tindakan apa yang ingin Anda lakukan.
Untuk data cuaca AS misalnya, untuk memperoleh prakiraan bagi
lokasi tertentu, Anda mengirim permintaan GET (dengan `curl` misalnya) ke
https://api.weather.gov/points/42.3604,-71.094. Responsnya sendiri
memuat banyak URL lain yang memungkinkan Anda memperoleh prakiraan spesifik untuk
wilayah tersebut. Biasanya, responsnya diformat sebagai JSON, yang kemudian dapat Anda
pipe melalui tool seperti [`jq`](https://stedolan.github.io/jq/) untuk
mengolahnya menjadi apa yang Anda pedulikan.

Sebagian API memerlukan autentikasi, dan ini biasanya berbentuk
semacam _token_ rahasia yang perlu Anda sertakan dalam permintaan.
Anda sebaiknya membaca dokumentasi API untuk melihat apa yang digunakan layanan
tertentu yang Anda cari, tetapi "[OAuth](https://www.oauth.com/)"
adalah protokol yang sering Anda lihat digunakan. Pada intinya, OAuth adalah cara
memberi Anda token yang dapat "bertindak sebagai Anda" pada layanan tertentu, dan hanya dapat
digunakan untuk tujuan tertentu. Ingat bahwa token ini
_rahasia_, dan siapa pun yang memperoleh akses ke token Anda dapat melakukan apa pun yang
diizinkan token tersebut atas nama akun _Anda_!

[IFTTT](https://ifttt.com/) adalah situs web dan layanan yang berpusat pada
gagasan API — layanan ini menyediakan integrasi dengan banyak sekali layanan, dan memungkinkan
Anda merangkai peristiwa dari layanan tersebut dengan cara yang hampir arbitrer. Coba lihat!

<a id="common-command-line-flagspatterns"></a>
## Flag/pola command-line yang umum

Tool command-line sangat bervariasi, dan Anda akan sering ingin memeriksa
`man` page-nya sebelum menggunakannya. Namun tool tersebut sering berbagi beberapa
fitur umum yang baik untuk diketahui:

 - Sebagian besar tool mendukung semacam flag `--help` untuk menampilkan instruksi penggunaan
   singkat bagi tool tersebut.
 - Banyak tool yang dapat menyebabkan perubahan tak dapat dipulihkan mendukung gagasan
   "dry run" di mana tool hanya mencetak apa yang _akan dilakukannya_, tetapi
   tidak benar-benar melakukan perubahannya. Demikian pula, tool sering memiliki
   flag "interactive" yang akan meminta konfirmasi Anda untuk setiap aksi destruktif.
 - Anda biasanya dapat menggunakan `--version` atau `-V` agar program mencetak
   versinya sendiri (berguna untuk melaporkan bug!).
 - Hampir semua tool memiliki flag `--verbose` atau `-v` untuk menghasilkan output
   yang lebih verbose. Anda biasanya dapat menyertakan flag tersebut beberapa kali
   (`-vvv`) untuk memperoleh output yang _lebih_ verbose, yang bisa berguna untuk
   debugging. Demikian pula, banyak tool memiliki flag `--quiet` agar
   hanya mencetak sesuatu saat terjadi error.
 - Pada banyak tool, `-` sebagai pengganti nama berkas berarti "standard input" atau
   "standard output", bergantung argumennya.
 - Tool yang berpotensi destruktif umumnya tidak rekursif secara default,
   tetapi mendukung flag "recursive" (sering `-r`) agar melakukan rekursi.
 - Kadang, Anda ingin memberikan sesuatu yang _tampak_ seperti flag sebagai
   argumen normal. Misalnya, bayangkan Anda ingin menghapus berkas
   bernama `-r`. Atau Anda ingin menjalankan satu program "melalui" program lain, seperti
   `ssh machine foo`, dan Anda ingin memberikan flag ke program "dalam"
   (`foo`). Argumen khusus `--` membuat program _berhenti_ memproses
   flag dan opsi (hal yang dimulai dengan `-`) pada apa yang mengikutinya, memungkinkan
   Anda memberikan hal yang tampak seperti flag tanpa diinterpretasikan
   sebagai flag: `rm -- -r` atau `ssh machine --for-ssh -- foo --for-foo`.

<a id="window-managers"></a>
## Window manager

Sebagian besar dari Anda terbiasa menggunakan window manager "drag and drop", seperti
yang disertakan Windows, macOS, dan Ubuntu secara default. Ada window
yang sekadar menggantung di layar, dan Anda dapat menyeretnya, mengubah ukurannya,
dan membuatnya saling tumpang tindih. Tetapi itu hanya satu
_jenis_ window manager, yang sering disebut window manager "floating". Ada banyak
lainnya, terutama di Linux. Alternatif yang sangat umum adalah window manager "tiling".
Pada tiling window manager, window tidak pernah tumpang tindih, dan sebagai gantinya disusun sebagai tile di
layar Anda, mirip pane di tmux. Dengan tiling window manager,
layar selalu diisi oleh window apa pun yang terbuka, disusun
menurut suatu _layout_. Jika Anda hanya memiliki satu window, window itu mengambil
seluruh layar. Jika Anda kemudian membuka window lain, window asli mengecil untuk
memberi ruang (sering kali sesuatu seperti 2/3 dan 1/3). Jika Anda membuka
window ketiga, window lain akan kembali mengecil untuk mengakomodasi window
baru. Sama seperti pane tmux, Anda dapat bernavigasi di antara window bertile ini
dengan keyboard, dan Anda dapat mengubah ukurannya serta memindahkannya,
semuanya tanpa menyentuh mouse. Layak untuk ditelaah!


<a id="vpns"></a>
## VPN

VPN sedang populer saat ini, tetapi tidak jelas apakah itu karena [alasan
yang baik](https://web.archive.org/web/20230710155258/https://gist.github.com/joepie91/5a9909939e6ce7d09e29). Anda
sebaiknya menyadari apa yang diberikan dan tidak diberikan VPN. VPN, dalam
kasus terbaik, _benar-benar_ hanyalah cara bagi Anda untuk mengganti penyedia layanan internet
sejauh yang dilihat internet. Semua lalu lintas Anda
akan tampak berasal dari penyedia VPN alih-alih lokasi "asli" Anda,
dan jaringan yang Anda hubungi hanya akan melihat lalu lintas
terenkripsi.

Meskipun itu mungkin tampak menarik, ingatlah bahwa ketika Anda menggunakan VPN,
yang sebenarnya Anda lakukan hanyalah memindahkan kepercayaan Anda dari ISP Anda saat ini ke
perusahaan hosting VPN. Apa pun yang _bisa_ dilihat ISP Anda, kini dilihat oleh penyedia VPN
_sebagai gantinya_. Jika Anda memercayai mereka _lebih_ daripada ISP Anda, itu
keuntungan, tetapi sebaliknya, tidak jelas bahwa Anda memperoleh banyak. Jika Anda
berada di Wi-Fi publik tidak terenkripsi yang meragukan di bandara, mungkin
Anda tidak terlalu memercayai koneksi tersebut, tetapi di rumah, trade-off-nya
tidak begitu jelas.

Anda juga harus tahu bahwa saat ini, sebagian besar lalu lintas Anda, setidaknya yang
bersifat sensitif, _sudah_ terenkripsi melalui HTTPS atau TLS secara lebih
umum. Dalam kasus itu, biasanya tidak banyak berpengaruh apakah Anda berada di
jaringan "buruk" atau tidak -- operator jaringan hanya akan mengetahui
server mana yang Anda hubungi, tetapi tidak apa pun tentang data yang dipertukarkan.

Perhatikan bahwa saya mengatakan "dalam kasus terbaik" di atas. Bukan hal yang tak terdengar bahwa
penyedia VPN tanpa sengaja salah mengonfigurasi perangkat lunaknya sehingga
enkripsinya lemah atau sepenuhnya dinonaktifkan. Sebagian penyedia VPN
berbahaya (atau setidaknya oportunis), dan akan mencatat semua
lalu lintas Anda, dan mungkin menjual informasi tentangnya kepada pihak ketiga.
Memilih penyedia VPN yang buruk sering kali lebih buruk daripada tidak menggunakannya
sejak awal.

Dalam keadaan darurat, MIT [menjalankan VPN](https://ist.mit.edu/vpn) untuk mahasiswanya,
sehingga itu mungkin layak ditelaah. Juga, jika Anda akan membuat
sendiri, lihat [WireGuard](https://www.wireguard.com/).

<a id="markdown"></a>
## Markdown

Ada kemungkinan besar Anda akan menulis beberapa teks sepanjang
karier Anda. Dan sering kali, Anda ingin menandai teks tersebut dengan cara
sederhana. Anda ingin beberapa teks menjadi tebal atau miring, atau Anda ingin menambahkan
heading, tautan, dan potongan kode. Daripada menggunakan tool berat
seperti Word atau LaTeX, Anda mungkin ingin mempertimbangkan menggunakan bahasa markup
ringan [Markdown](https://commonmark.org/help/).

Anda mungkin sudah melihat Markdown, atau setidaknya salah satu variannya.
Subset-nya digunakan dan didukung hampir di mana-mana, bahkan jika tidak
dengan nama Markdown. Pada intinya, Markdown adalah upaya mengodekan
cara orang sudah sering menandai teks ketika mereka menulis
dokumen teks biasa. Emphasis (*miring*) ditambahkan dengan mengapit
kata dengan `*`. Strong emphasis (**tebal**) ditambahkan menggunakan `**`. Baris
yang dimulai dengan `#` adalah heading (dan jumlah `#` adalah tingkat
subheading). Baris yang dimulai dengan `-` adalah item bullet list, dan baris apa pun
yang dimulai dengan angka + `.` adalah item daftar bernomor. Backtick digunakan
untuk menampilkan kata dalam `code font`, dan code block dapat dimasukkan dengan
mengindentasi baris dengan empat spasi atau mengapitnya dengan
triple-backtick:

    ```
    code goes here
    ```

Untuk menambahkan tautan, letakkan _teks_ untuk tautan dalam kurung siku,
dan URL tepat setelahnya dalam tanda kurung: `[name](url)`.
Markdown mudah dimulai, dan Anda dapat menggunakannya hampir
di mana-mana. Bahkan, catatan kuliah untuk kuliah ini, dan semua
kuliah lainnya, ditulis dalam Markdown, dan Anda dapat melihat Markdown mentahnya
[di sini](https://raw.githubusercontent.com/missing-semester/missing-semester/master/_2020/potpourri.md).



<a id="hammerspoon-desktop-automation-on-macos"></a>
## Hammerspoon (otomasi desktop di macOS)

[Hammerspoon](https://www.hammerspoon.org/) adalah framework otomasi desktop
untuk macOS. Tool ini memungkinkan Anda menulis skrip Lua yang terhubung ke fungsionalitas
sistem operasi, memungkinkan Anda berinteraksi dengan keyboard/mouse, window,
layar, filesystem, dan banyak lagi.

Beberapa contoh hal yang dapat Anda lakukan dengan Hammerspoon:

- Mengikat hotkey untuk memindahkan window ke lokasi tertentu
- Membuat tombol menu bar yang secara otomatis menata window dalam layout tertentu
- Membisukan speaker Anda ketika Anda tiba di lab (dengan mendeteksi jaringan Wi-Fi)
- Menampilkan peringatan jika Anda tanpa sengaja mengambil power supply teman Anda

Pada tingkat tinggi, Hammerspoon memungkinkan Anda menjalankan kode Lua arbitrer, yang diikat ke tombol
menu, penekanan tombol, atau peristiwa, dan Hammerspoon menyediakan library yang luas
untuk berinteraksi dengan sistem, jadi pada dasarnya tidak ada batas apa yang dapat
Anda lakukan dengannya. Banyak orang telah mempublikasikan konfigurasi Hammerspoon mereka, sehingga
Anda umumnya dapat menemukan apa yang Anda butuhkan dengan mencari di internet, tetapi Anda
selalu dapat menulis kode sendiri dari nol.

### Sumber daya

- [Getting Started with Hammerspoon](https://www.hammerspoon.org/go/)
- [Contoh konfigurasi](https://github.com/Hammerspoon/hammerspoon/wiki/Sample-Configurations)
- [Konfigurasi Hammerspoon Anish](https://github.com/anishathalye/dotfiles-local/tree/mac/hammerspoon)

<a id="booting--live-usbs"></a>
## Booting + Live USB

Saat mesin Anda menyala, sebelum sistem operasi dimuat,
[BIOS](https://en.wikipedia.org/wiki/BIOS)/[UEFI](https://en.wikipedia.org/wiki/Unified_Extensible_Firmware_Interface)
menginisialisasi sistem. Selama proses ini, Anda dapat menekan kombinasi
tombol tertentu untuk mengonfigurasi lapisan perangkat lunak ini. Misalnya, komputer Anda mungkin
menampilkan sesuatu seperti "Press F9 to configure BIOS. Press F12 to enter boot menu."
selama proses boot. Anda dapat mengonfigurasi segala macam pengaturan terkait
perangkat keras di menu BIOS. Anda juga dapat memasuki boot menu untuk boot dari
perangkat alternatif alih-alih hard drive Anda.

[Live USB](https://en.wikipedia.org/wiki/Live_USB) adalah USB flash drive
yang memuat sistem operasi. Anda dapat membuatnya dengan mengunduh
sistem operasi (misalnya distribusi Linux) lalu membakarnya ke flash drive.
Proses ini sedikit lebih rumit daripada sekadar menyalin berkas `.iso`
ke disk. Ada tool seperti [UNetbootin](https://unetbootin.github.io/)
untuk membantu Anda membuat live USB.

Live USB berguna untuk berbagai tujuan. Antara lain, jika Anda
merusak instalasi sistem operasi Anda sehingga tidak lagi boot,
Anda dapat menggunakan live USB untuk memulihkan data atau memperbaiki sistem operasi.

<a id="docker-vagrant-vms-cloud-openstack"></a>
## Docker, Vagrant, VM, Cloud, OpenStack

[Virtual machine](https://en.wikipedia.org/wiki/Virtual_machine) dan tool serupa
seperti container memungkinkan Anda mengemulasi seluruh sistem komputer, termasuk
sistem operasinya. Ini dapat berguna untuk membuat lingkungan terisolasi bagi
testing, pengembangan, atau eksplorasi (misalnya menjalankan kode yang berpotensi berbahaya).

[Vagrant](https://www.vagrantup.com/) adalah tool yang memungkinkan Anda mendeskripsikan konfigurasi
mesin (sistem operasi, layanan, paket, dsb.) dalam kode, lalu
menginstansiasi VM dengan `vagrant up` yang sederhana. [Docker](https://www.docker.com/)
secara konseptual serupa tetapi menggunakan container sebagai gantinya.

Anda juga dapat menyewa virtual machine di cloud, dan itu cara yang menyenangkan untuk mendapatkan akses
instan ke:

- Mesin murah yang selalu menyala dan memiliki alamat IP publik, digunakan untuk meng-host layanan
- Mesin dengan CPU, disk, RAM, dan/atau GPU yang banyak
- Jauh lebih banyak mesin daripada yang Anda miliki secara fisik (penagihan sering
per detik, jadi jika Anda menginginkan banyak komputasi untuk waktu singkat,
menyewa 1000 komputer selama beberapa menit itu memungkinkan)

Layanan populer termasuk [Amazon AWS](https://aws.amazon.com/), [Google
Cloud](https://cloud.google.com/),[ Microsoft Azure](https://azure.microsoft.com/),
[DigitalOcean](https://www.digitalocean.com/).

Jika Anda anggota MIT CSAIL, Anda dapat memperoleh VM gratis untuk keperluan penelitian
melalui [instans CSAIL OpenStack](https://tig.csail.mit.edu/shared-computing/open-stack/).

<a id="notebook-programming"></a>
## Pemrograman notebook

[Lingkungan pemrograman
notebook](https://en.wikipedia.org/wiki/Notebook_interface) bisa sangat
berguna untuk melakukan jenis pengembangan interaktif atau eksploratif tertentu.
Mungkin lingkungan pemrograman notebook paling populer saat ini adalah
[Jupyter](https://jupyter.org/), untuk Python (dan beberapa bahasa lain).
[Wolfram Mathematica](https://www.wolfram.com/mathematica/) adalah lingkungan pemrograman
notebook lain yang hebat untuk pemrograman berorientasi matematika.

<a id="github"></a>
## GitHub

[GitHub](https://github.com/) adalah salah satu platform paling populer untuk
pengembangan perangkat lunak open-source. Banyak tool yang telah kita bahas di
kelas ini, dari [vim](https://github.com/vim/vim) hingga
[Hammerspoon](https://github.com/Hammerspoon/hammerspoon), di-host di
GitHub. Mudah untuk mulai berkontribusi ke open-source untuk membantu meningkatkan
tool yang Anda gunakan setiap hari.

Ada dua cara utama orang berkontribusi ke proyek di GitHub:

- Membuat
[issue](https://help.github.com/en/github/managing-your-work-on-github/creating-an-issue).
Ini dapat digunakan untuk melaporkan bug atau meminta fitur baru. Keduanya
tidak melibatkan membaca atau menulis kode, sehingga bisa cukup ringan untuk dilakukan.
Laporan bug berkualitas tinggi bisa sangat berharga bagi pengembang. Berkomentar pada
diskusi yang sudah ada juga bisa membantu.
- Berkontribusi kode melalui [pull
request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).
Ini umumnya lebih rumit daripada membuat issue. Anda dapat
[fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
repositori di GitHub, clone fork Anda, buat branch baru, buat beberapa perubahan
(misalnya memperbaiki bug atau mengimplementasikan fitur), push branch tersebut, lalu [membuat
pull
request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
Setelah itu, biasanya akan ada beberapa bolak-balik dengan maintainer
proyek, yang akan memberi Anda umpan balik atas patch Anda. Akhirnya, jika semuanya
berjalan baik, patch Anda akan di-merge ke repositori upstream. Sering kali,
proyek yang lebih besar memiliki panduan kontribusi, menandai issue yang ramah pemula,
dan sebagian bahkan memiliki program mentorship untuk membantu kontributor pertama kali menjadi
familiar dengan proyek tersebut.
