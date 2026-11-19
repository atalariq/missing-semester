---
layout: lecture-id
title: "Q&A"
description: >
  Jawaban atas pertanyaan peserta tentang topik seperti operating system, shell scripting, rekomendasi tool, dan lainnya.
thumbnail: /static/assets/thumbnails/2020/lec11.png
date: 2020-01-30
ready: true
video:
  aspect: 56.25
  id: Wz50FvGG6xU
special: true
lang: id
permalink: /id/2020/qa/
---

Untuk kuliah terakhir, kami menjawab pertanyaan yang diajukan mahasiswa:

- [Ada rekomendasi untuk mempelajari topik terkait Operating System seperti processes, virtual memory, interrupts, memory management, dsb.](#any-recommendations-on-learning-operating-systems-related-topics-like-processes-virtual-memory-interrupts-memory-management-etc)
- [Apa saja tool yang akan Anda prioritaskan untuk dipelajari lebih dulu?](#what-are-some-of-the-tools-youd-prioritize-learning-first)
- [Kapan saya menggunakan Python versus skrip Bash versus bahasa lain?](#when-do-i-use-python-versus-a-bash-scripts-versus-some-other-language)
- [Apa perbedaan antara `source script.sh` dan `./script.sh`](#what-is-the-difference-between-source-scriptsh-and-scriptsh)
- [Di mana berbagai paket dan tool disimpan dan bagaimana referensinya bekerja? Apa itu `/bin` atau `/lib`?](#what-are-the-places-where-various-packages-and-tools-are-stored-and-how-does-referencing-them-work-what-even-is-bin-or-lib)
- [Apakah saya sebaiknya `apt-get install` python-whatever, atau `pip install` paket whatever?](#should-i-apt-get-install-a-python-whatever-or-pip-install-whatever-package)
- [Apa tool profiling termudah dan terbaik untuk meningkatkan performa kode saya?](#whats-the-easiest-and-best-profiling-tools-to-use-to-improve-performance-of-my-code)
- [Plugin browser apa yang Anda gunakan?](#what-browser-plugins-do-you-use)
- [Apa tool data wrangling lain yang berguna?](#what-are-other-useful-data-wrangling-tools)
- [Apa perbedaan antara Docker dan Virtual Machine?](#what-is-the-difference-between-docker-and-a-virtual-machine)
- [Apa kelebihan dan kekurangan masing-masing OS dan bagaimana kita memilih di antaranya (misalnya memilih distribusi Linux terbaik untuk keperluan kita)?](#what-are-the-advantages-and-disadvantages-of-each-os-and-how-can-we-choose-between-them-eg-choosing-the-best-linux-distribution-for-our-purposes)
- [Vim vs Emacs?](#vim-vs-emacs)
- [Ada tip atau trik untuk aplikasi Machine Learning?](#any-tips-or-tricks-for-machine-learning-applications)
- [Ada tip Vim lagi?](#any-more-vim-tips)
- [Apa itu 2FA dan mengapa saya harus menggunakannya?](#what-is-2fa-and-why-should-i-use-it)
- [Ada komentar tentang perbedaan antar web browser?](#any-comments-on-differences-between-web-browsers)

<a id="any-recommendations-on-learning-operating-systems-related-topics-like-processes-virtual-memory-interrupts-memory-management-etc"></a>
## Ada rekomendasi untuk mempelajari topik terkait Operating System seperti processes, virtual memory, interrupts, memory management, dsb

Pertama, tidak jelas apakah Anda benar-benar perlu sangat familiar dengan semua topik ini karena ini topik yang sangat low level.
Topik tersebut akan penting ketika Anda mulai menulis kode yang lebih low level seperti mengimplementasikan atau memodifikasi kernel. Selain itu, sebagian besar topik tidak akan relevan, kecuali processes dan signals yang sempat dibahas pada kuliah lain.

Beberapa sumber yang baik untuk mempelajari topik ini:

- [Kelas 6.828 MIT](https://pdos.csail.mit.edu/6.828/) - Kelas tingkat pascasarjana tentang Operating System Engineering. Materi kelas tersedia publik.
- Modern Operating Systems (edisi ke-4) - oleh Andrew S. Tanenbaum memberikan gambaran umum yang baik tentang banyak konsep yang disebutkan.
- The Design and Implementation of the FreeBSD Operating System - Sumber yang baik tentang OS FreeBSD (perhatikan bahwa ini bukan Linux).
- Panduan lain seperti [Writing an OS in Rust](https://os.phil-opp.com/) di mana orang mengimplementasikan kernel langkah demi langkah dalam berbagai bahasa, sebagian besar untuk keperluan pengajaran.


<a id="what-are-some-of-the-tools-youd-prioritize-learning-first"></a>
## Apa saja tool yang akan Anda prioritaskan untuk dipelajari lebih dulu?

Beberapa topik yang layak diprioritaskan:

- Mempelajari cara lebih banyak menggunakan keyboard dan lebih sedikit menggunakan mouse. Ini dapat melalui keyboard shortcut, mengubah antarmuka, &c.
- Mempelajari editor Anda dengan baik. Sebagai programmer sebagian besar waktu Anda dihabiskan mengedit berkas sehingga sangat bermanfaat mempelajari keterampilan ini dengan baik.
- Mempelajari cara mengotomatiskan dan/atau menyederhanakan tugas berulang dalam alur kerja Anda karena penghematan waktunya akan sangat besar...
- Mempelajari tool version control seperti Git dan cara menggunakannya bersama GitHub untuk berkolaborasi dalam proyek perangkat lunak modern.

<a id="when-do-i-use-python-versus-a-bash-scripts-versus-some-other-language"></a>
## Kapan saya menggunakan Python versus skrip Bash versus bahasa lain?

Secara umum, skrip bash berguna untuk skrip sekali pakai yang singkat dan sederhana ketika Anda hanya ingin menjalankan rangkaian perintah tertentu. bash memiliki sekumpulan keanehan yang membuatnya sulit digunakan untuk program atau skrip yang lebih besar:

- bash mudah dibuat benar untuk use case sederhana tetapi bisa sangat sulit dibuat benar untuk semua input yang mungkin. Misalnya, spasi dalam argumen skrip telah menyebabkan banyak sekali bug pada skrip bash.
- bash tidak ramah terhadap code reuse sehingga bisa sulit menggunakan kembali komponen dari program yang pernah Anda tulis. Lebih umum, tidak ada konsep software library di bash.
- bash bergantung pada banyak string ajaib seperti `$?` atau `$@` untuk merujuk nilai tertentu, sedangkan bahasa lain merujuknya secara eksplisit, seperti `exitCode` atau `sys.args` masing-masing.

Oleh karena itu, untuk skrip yang lebih besar dan/atau lebih kompleks kami menyarankan menggunakan bahasa scripting yang lebih matang seperti Python atau Ruby.
Anda dapat menemukan banyak sekali library daring yang sudah ditulis orang untuk menyelesaikan masalah umum dalam bahasa tersebut.
Jika Anda menemukan library yang mengimplementasikan fungsionalitas spesifik yang Anda pedulikan dalam suatu bahasa, biasanya hal terbaik adalah cukup menggunakan bahasa tersebut.

<a id="what-is-the-difference-between-source-scriptsh-and-scriptsh"></a>
## Apa perbedaan antara `source script.sh` dan `./script.sh`

Dalam kedua kasus `script.sh` akan dibaca dan dieksekusi dalam sesi bash, perbedaannya terletak pada sesi mana yang menjalankan perintahnya.
Untuk `source` perintahnya dieksekusi di sesi bash Anda saat ini sehingga setiap perubahan yang dibuat pada environment saat ini, seperti mengubah direktori atau mendefinisikan fungsi akan bertahan di sesi saat ini setelah perintah `source` selesai dieksekusi.
Saat menjalankan skrip secara mandiri seperti `./script.sh`, sesi bash Anda saat ini memulai instans bash baru yang akan menjalankan perintah di `script.sh`.
Dengan demikian, jika `script.sh` mengubah direktori, instans bash baru akan mengubah direktori tetapi setelah keluar dan mengembalikan kendali ke sesi bash induk, sesi induk akan tetap di tempat yang sama.
Demikian pula, jika `script.sh` mendefinisikan fungsi yang ingin Anda akses di terminal Anda, Anda perlu melakukan `source` agar fungsi itu terdefinisi di sesi bash Anda saat ini. Jika tidak, saat Anda menjalankannya, proses bash baru yang akan memproses definisi fungsi tersebut alih-alih shell Anda saat ini.

<a id="what-are-the-places-where-various-packages-and-tools-are-stored-and-how-does-referencing-them-work-what-even-is-bin-or-lib"></a>
## Di mana berbagai paket dan tool disimpan dan bagaimana referensinya bekerja? Apa itu `/bin` atau `/lib`?

Terkait program yang Anda eksekusi di terminal Anda, semuanya ditemukan di direktori yang tercantum pada environment variable `PATH` Anda dan Anda dapat menggunakan perintah `which` (atau perintah `type`) untuk memeriksa di mana shell Anda menemukan program tertentu.
Secara umum, ada beberapa konvensi tentang di mana jenis berkas tertentu berada. Berikut beberapa yang kami bahas, lihat [Filesystem, Hierarchy Standard](https://en.wikipedia.org/wiki/Filesystem_Hierarchy_Standard) untuk daftar yang lebih komprehensif.

- `/bin` - Binary perintah esensial
- `/sbin` - Binary sistem esensial, biasanya dijalankan oleh root
- `/dev` - Berkas device, berkas khusus yang sering menjadi antarmuka ke perangkat keras
- `/etc` - Berkas konfigurasi sistem-wide yang spesifik host
- `/home` - Direktori home untuk pengguna di sistem
- `/lib` - Library umum untuk program sistem
- `/opt` - Perangkat lunak aplikasi opsional
- `/sys` - Memuat informasi dan konfigurasi untuk sistem (dibahas pada [kuliah pertama](/2020/course-shell/))
- `/tmp` - Berkas sementara (juga `/var/tmp`). Biasanya dihapus antar reboot.
- `/usr/` - Data pengguna yang hanya-baca
  + `/usr/bin` - Binary perintah non-esensial
  + `/usr/sbin` - Binary sistem non-esensial, biasanya dijalankan oleh root
  + `/usr/local/bin` - Binary untuk program yang dikompilasi pengguna
- `/var` - Berkas variabel seperti log atau cache

<a id="should-i-apt-get-install-a-python-whatever-or-pip-install-whatever-package"></a>
## Apakah saya sebaiknya `apt-get install` python-whatever, atau `pip install` paket whatever?

Tidak ada jawaban universal untuk pertanyaan ini. Ini terkait dengan pertanyaan yang lebih umum apakah Anda sebaiknya menggunakan package manager sistem Anda atau package manager khas bahasa untuk memasang perangkat lunak. Beberapa hal yang perlu dipertimbangkan:

- Paket umum akan tersedia melalui keduanya, tetapi paket yang kurang populer atau lebih baru mungkin tidak tersedia di package manager sistem Anda. Dalam kasus ini, menggunakan tool khas bahasa adalah pilihan yang lebih baik.
- Demikian pula, package manager khas bahasa biasanya memiliki versi paket yang lebih mutakhir daripada package manager sistem.
- Saat menggunakan package manager sistem, library akan dipasang secara system-wide. Ini berarti jika Anda membutuhkan versi library yang berbeda untuk keperluan pengembangan, package manager sistem mungkin tidak memadai. Untuk skenario ini, sebagian besar bahasa pemrograman menyediakan semacam environment terisolasi atau virtual sehingga Anda dapat memasang versi library yang berbeda tanpa menemui konflik. Untuk Python, ada virtualenv, dan untuk Ruby, ada RVM.
- Bergantung pada sistem operasi dan arsitektur perangkat keras, sebagian paket ini mungkin disertai binary atau mungkin perlu dikompilasi. Misalnya, pada komputer ARM seperti Raspberry Pi, menggunakan package manager sistem bisa lebih baik daripada yang khas bahasa jika yang pertama tersedia dalam bentuk binary dan yang kedua perlu dikompilasi. Ini sangat bergantung pada pengaturan spesifik Anda.

Anda sebaiknya mencoba menggunakan salah satu solusi dan bukan keduanya karena itu dapat menyebabkan konflik yang sulit di-debug. Rekomendasi kami adalah menggunakan package manager khas bahasa bila memungkinkan, dan menggunakan environment terisolasi (seperti virtualenv Python) untuk menghindari pencemaran environment global.

<a id="whats-the-easiest-and-best-profiling-tools-to-use-to-improve-performance-of-my-code"></a>
## Apa tool profiling termudah dan terbaik untuk meningkatkan performa kode saya?

Tool termudah yang cukup berguna untuk keperluan profiling adalah [print timing](/2020/debugging-profiling/#timing).
Anda cukup menghitung secara manual waktu yang diambil di antara berbagai bagian kode Anda. Dengan melakukannya berulang kali, Anda secara efektif dapat melakukan binary search pada kode Anda dan menemukan segmen kode yang memakan waktu paling lama.

Untuk tool yang lebih canggih, [Callgrind](https://valgrind.org/docs/manual/cl-manual.html) dari Valgrind memungkinkan Anda menjalankan program dan mengukur berapa lama setiap hal dijalankan beserta semua call stack-nya, yaitu fungsi mana memanggil fungsi mana. Tool ini lalu menghasilkan versi beranotasi dari kode sumber program Anda dengan waktu yang diambil per baris. Namun, tool ini memperlambat program Anda satu orde besaran dan tidak mendukung thread. Untuk kasus lain, tool [`perf`](https://www.brendangregg.com/perf.html) dan sampling profiler khas bahasa lain dapat mengeluarkan data berguna dengan cukup cepat. [Flamegraph](https://www.brendangregg.com/flamegraphs.html) adalah tool visualisasi yang baik untuk output sampling profiler tersebut. Anda juga sebaiknya mencoba menggunakan tool spesifik untuk bahasa pemrograman atau tugas yang Anda kerjakan. Misalnya, untuk pengembangan web, dev tool yang tertanam di Chrome dan Firefox memiliki profiler yang fantastis.

Kadang bagian lambat dari kode Anda disebabkan sistem menunggu peristiwa seperti pembacaan disk atau paket jaringan. Dalam kasus itu, ada baiknya memeriksa bahwa perhitungan kasar (back-of-the-envelope) tentang kecepatan teoretis dari kemampuan perangkat keras tidak menyimpang dari pembacaan aktual. Ada juga tool khusus untuk menganalisis waktu tunggu pada system call. Ini termasuk tool seperti [eBPF](https://www.brendangregg.com/blog/2019-01-01/learn-ebpf-tracing.html) yang melakukan kernel tracing pada program pengguna. Secara khusus [`bpftrace`](https://github.com/iovisor/bpftrace) layak ditelaah jika Anda perlu melakukan profiling low level semacam ini.


<a id="what-browser-plugins-do-you-use"></a>
## Plugin browser apa yang Anda gunakan?

Beberapa favorit kami, sebagian besar terkait security dan usability:

- [uBlock Origin](https://github.com/gorhill/uBlock) - Ini adalah blocker [wide-spectrum](https://github.com/gorhill/uBlock/wiki/Blocking-mode) yang tidak hanya menghentikan iklan, tetapi segala macam komunikasi pihak ketiga yang mungkin dicoba sebuah halaman. Ini juga mencakup inline script dan jenis pemuatan resource lain. Jika Anda bersedia meluangkan waktu untuk konfigurasi agar semuanya berfungsi, masuk ke [medium mode](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-medium-mode) atau bahkan [hard mode](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-hard-mode). Mode tersebut akan membuat sebagian situs tidak berfungsi sampai Anda cukup mengutak-atik pengaturannya, tetapi juga akan secara signifikan meningkatkan keamanan daring Anda. Jika tidak, [easy mode](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-easy-mode) sudah menjadi default yang baik yang memblokir sebagian besar iklan dan tracking. Anda juga dapat mendefinisikan aturan sendiri tentang objek situs web mana yang diblokir.
- [Stylus](https://github.com/openstyles/stylus/) - fork dari Stylish (jangan gunakan Stylish, tool itu terbukti [mencuri riwayat browsing pengguna](https://www.theregister.co.uk/2018/07/05/browsers_pull_stylish_but_invasive_browser_extension/)), memungkinkan Anda memuat custom CSS stylesheet ke situs web. Dengan Stylus Anda dapat dengan mudah menyesuaikan dan memodifikasi tampilan situs web. Ini bisa berupa menghapus sidebar, mengubah warna latar atau bahkan ukuran teks atau pilihan font. Ini fantastis untuk membuat situs web yang sering Anda kunjungi lebih mudah dibaca. Lebih jauh lagi, Stylus dapat menemukan style yang ditulis pengguna lain dan dipublikasikan di [userstyles.org](https://userstyles.org/). Sebagian besar situs web umum memiliki satu atau beberapa stylesheet dark theme misalnya.
- Full Page Screen Capture - [Tertanam di Firefox](https://screenshots.firefox.com/) dan [ekstensi Chrome](https://chrome.google.com/webstore/detail/full-page-screen-capture/fdpohaocaechififmbbbbbknoalclacl?hl=en). Memungkinkan Anda mengambil tangkapan layar seluruh situs web, sering kali jauh lebih baik daripada mencetak untuk keperluan referensi.
- [Multi Account Containers](https://addons.mozilla.org/en-US/firefox/addon/multi-account-containers/) - memungkinkan Anda memisahkan cookie ke dalam "container", sehingga Anda dapat menjelajahi web dengan identitas berbeda dan/atau memastikan situs web tidak dapat berbagi informasi di antaranya.
- Integrasi Password Manager - Sebagian besar password manager memiliki ekstensi browser yang membuat pemasukan kredensial Anda ke situs web tidak hanya lebih praktis tetapi juga lebih aman. Dibandingkan sekadar menyalin-tempel user dan password Anda, tool ini akan terlebih dahulu memeriksa bahwa domain situs web cocok dengan yang tercantum untuk entri tersebut, sehingga mencegah serangan phishing yang menyamar sebagai situs web populer untuk mencuri kredensial.
- [Vimium](https://github.com/philc/vimium) - Ekstensi browser yang menyediakan navigasi dan kendali web berbasis keyboard dalam semangat editor Vim.

<a id="what-are-other-useful-data-wrangling-tools"></a>
## Apa tool data wrangling lain yang berguna?

Beberapa tool data wrangling yang tidak sempat kami bahas selama kuliah data wrangling termasuk `jq` atau `pup` yang masing-masing merupakan parser khusus untuk data JSON dan HTML. Bahasa pemrograman Perl adalah tool lain yang baik untuk pipeline data wrangling yang lebih canggih. Trik lain adalah perintah `column -t` yang dapat digunakan untuk mengonversi teks berwhitespace (tidak harus rata) menjadi teks yang rata kolomnya dengan benar.

Lebih umum, beberapa tool data wrangling yang lebih tidak konvensional adalah vim dan Python. Untuk sebagian transformasi kompleks dan multi-baris, macro vim bisa menjadi tool yang sangat berharga. Anda cukup merekam rangkaian aksi dan mengulanginya sebanyak yang Anda mau, misalnya pada [catatan kuliah](/2020/editors/#macros) editors (dan [video](/2019/editors/) tahun lalu) ada contoh mengonversi berkas berformat XML menjadi JSON hanya menggunakan macro vim.

Untuk data tabular, yang sering disajikan dalam CSV, library Python [pandas](https://pandas.pydata.org/) adalah tool yang hebat. Tidak hanya karena membuat operasi kompleks seperti group by, join atau filter menjadi cukup mudah; tetapi juga memudahkan plotting berbagai properti data Anda. Library ini juga mendukung ekspor ke banyak format tabel termasuk XLS, HTML atau LaTeX. Alternatifnya bahasa pemrograman R (bahasa pemrograman yang bisa dibilang [buruk](https://arrgh.tim-smith.us/)) memiliki banyak fungsionalitas untuk menghitung statistik atas data dan bisa sangat berguna sebagai langkah terakhir pipeline Anda. [ggplot2](https://ggplot2.tidyverse.org/) adalah library plotting yang hebat di R.

<a id="what-is-the-difference-between-docker-and-a-virtual-machine"></a>
## Apa perbedaan antara Docker dan Virtual Machine?

Docker didasarkan pada konsep yang lebih umum yang disebut container. Perbedaan utama antara container dan virtual machine adalah virtual machine akan menjalankan seluruh stack OS, termasuk kernel, bahkan jika kernel-nya sama dengan mesin host. Berbeda dengan VM, container menghindari menjalankan instans kernel lain dan sebagai gantinya berbagi kernel dengan host. Di Linux, ini dicapai melalui mekanisme yang disebut LXC, dan memanfaatkan serangkaian mekanisme isolasi untuk menjalankan program yang mengira berjalan di perangkat kerasnya sendiri tetapi sebenarnya berbagi perangkat keras dan kernel dengan host. Dengan demikian, container memiliki overhead lebih rendah daripada VM penuh.
Sebaliknya, container memiliki isolasi yang lebih lemah dan hanya berfungsi jika host menjalankan kernel yang sama. Misalnya jika Anda menjalankan Docker di macOS, Docker perlu menjalankan Linux virtual machine untuk memperoleh kernel Linux awal sehingga overhead-nya masih signifikan. Terakhir, Docker adalah implementasi spesifik dari container dan dirancang untuk deployment perangkat lunak. Karena itu, ada beberapa keanehannya: misalnya, container Docker tidak akan mempertahankan bentuk penyimpanan apa pun antar reboot secara default.

<a id="what-are-the-advantages-and-disadvantages-of-each-os-and-how-can-we-choose-between-them-eg-choosing-the-best-linux-distribution-for-our-purposes"></a>
## Apa kelebihan dan kekurangan masing-masing OS dan bagaimana kita memilih di antaranya (misalnya memilih distribusi Linux terbaik untuk keperluan kita)?

Terkait distro Linux, meskipun ada banyak sekali distro, sebagian besar akan berperilaku cukup identik untuk sebagian besar use case.
Sebagian besar fitur dan cara kerja internal Linux dan UNIX dapat dipelajari di distro mana pun.
Perbedaan mendasar antar distro adalah cara mereka menangani pembaruan paket.
Sebagian distro, seperti Arch Linux, menggunakan kebijakan rolling update di mana segala sesuatunya bleeding-edge tetapi kadang bisa rusak. Di sisi lain, sebagian distro seperti rilis Debian, CentOS atau Ubuntu LTS jauh lebih konservatif dalam merilis pembaruan di repositorinya sehingga biasanya lebih stabil dengan mengorbankan fitur yang lebih baru.
Rekomendasi kami untuk pengalaman yang mudah dan stabil dengan desktop maupun server adalah menggunakan Debian atau Ubuntu.

Mac OS adalah titik tengah yang baik antara Windows dan Linux yang memiliki antarmuka yang dipoles dengan baik. Namun, Mac OS didasarkan pada BSD alih-alih Linux, sehingga sebagian bagian sistem dan perintahnya berbeda.
Alternatif yang layak ditelaah adalah FreeBSD. Meskipun sebagian program tidak akan berjalan di FreeBSD, ekosistem BSD jauh lebih tidak terfragmentasi dan lebih terdokumentasi daripada Linux.
Kami tidak menyarankan Windows kecuali untuk mengembangkan aplikasi Windows atau jika ada fitur deal breaker yang Anda butuhkan, seperti dukungan driver yang baik untuk gaming.

Untuk sistem dual boot, kami pikir implementasi yang paling berfungsi adalah bootcamp macOS dan kombinasi lainnya bisa bermasalah dalam jangka panjang, terutama jika Anda menggabungkannya dengan fitur lain seperti enkripsi disk.

<a id="vim-vs-emacs"></a>
## Vim atau Emacs?

Kami bertiga menggunakan vim sebagai editor utama kami tetapi Emacs juga alternatif yang baik dan layak dicoba keduanya untuk melihat mana yang lebih cocok bagi Anda. Emacs tidak mengikuti modal editing vim, tetapi ini dapat diaktifkan melalui plugin Emacs seperti [Evil](https://github.com/emacs-evil/evil) atau [Doom Emacs](https://github.com/hlissner/doom-emacs).
Keuntungan menggunakan Emacs adalah ekstensi dapat diimplementasikan dalam Lisp, bahasa scripting yang lebih baik daripada vimscript, bahasa scripting default Vim.

<a id="any-tips-or-tricks-for-machine-learning-applications"></a>
## Ada tip atau trik untuk aplikasi Machine Learning?

Sebagian pelajaran dan intisari dari kelas ini dapat langsung diterapkan pada aplikasi ML.
Seperti pada banyak disiplin ilmu, dalam ML Anda sering melakukan serangkaian eksperimen dan ingin memeriksa apa yang berhasil dan apa yang tidak.
Anda dapat menggunakan shell tool untuk mencari dengan mudah dan cepat melalui eksperimen tersebut dan mengagregasi hasilnya dengan cara yang masuk akal. Ini bisa berarti memilih sebagian eksperimen dalam rentang waktu tertentu atau yang menggunakan dataset tertentu. Dengan menggunakan berkas JSON sederhana untuk mencatat semua parameter relevan dari eksperimen, ini bisa sangat sederhana dengan tool yang kami bahas di kelas ini.
Terakhir, jika Anda tidak bekerja dengan semacam cluster tempat Anda mengirim job GPU, Anda sebaiknya menelaah cara mengotomatiskan proses ini karena bisa menjadi tugas yang cukup memakan waktu dan juga menguras energi mental Anda.

<a id="any-more-vim-tips"></a>
## Ada tip Vim lagi?

Beberapa tip lagi:

- Plugin - Luangkan waktu Anda dan jelajahi lanskap plugin. Ada banyak plugin hebat yang mengatasi sebagian kekurangan vim atau menambahkan fungsionalitas baru yang terkomposisi baik dengan alur kerja vim yang ada. Untuk ini, sumber yang baik adalah [VimAwesome](https://vimawesome.com/) dan dotfiles programmer lain.
- Marks - Di vim, Anda dapat menetapkan mark dengan `m<X>` untuk suatu huruf `X`. Anda kemudian dapat kembali ke mark tersebut dengan `'<X>`. Ini memungkinkan Anda bernavigasi cepat ke lokasi tertentu di dalam berkas atau bahkan lintas berkas.
- Navigasi - `Ctrl+O` dan `Ctrl+I` memindahkan Anda mundur dan maju masing-masing melalui lokasi yang baru saja Anda kunjungi.
- Undo Tree - Vim memiliki mekanisme yang cukup canggih untuk melacak perubahan. Berbeda dengan editor lain, vim menyimpan pohon perubahan sehingga bahkan jika Anda melakukan undo lalu membuat perubahan berbeda Anda tetap dapat kembali ke keadaan asli dengan bernavigasi di pohon undo. Sebagian plugin seperti [gundo.vim](https://github.com/sjl/gundo.vim) dan [undotree](https://github.com/mbbill/undotree) mengekspos pohon ini secara grafis.
- Undo dengan waktu - Perintah `:earlier` dan `:later` memungkinkan Anda bernavigasi di berkas menggunakan referensi waktu alih-alih satu perubahan setiap kali.
- [Persistent undo](https://vim.fandom.com/wiki/Using_undo_branches#Persistent_undo) adalah fitur bawaan vim yang luar biasa yang dinonaktifkan secara default. Fitur ini mempertahankan riwayat undo antar pemanggilan vim. Dengan menetapkan `undofile` dan `undodir` di `.vimrc` Anda, vim akan menyimpan riwayat perubahan per berkas.
- Leader Key - Leader key adalah tombol khusus yang sering diserahkan kepada pengguna untuk dikonfigurasi bagi perintah kustom. Polanya biasanya menekan dan melepaskan tombol ini (sering kali tombol spasi) lalu tombol lain untuk mengeksekusi perintah tertentu. Sering kali, plugin akan menggunakan tombol ini untuk menambahkan fungsionalitas mereka sendiri, misalnya plugin UndoTree menggunakan `<Leader> U` untuk membuka undo tree.
- Advanced Text Objects - Text object seperti pencarian juga dapat dikomposisikan dengan perintah vim. Misalnya `d/<pattern>` akan menghapus sampai kecocokan berikutnya dari pola tersebut atau `cgn` akan mengubah kemunculan berikutnya dari string yang terakhir dicari.

<a id="what-is-2fa-and-why-should-i-use-it"></a>
## Apa itu 2FA dan mengapa saya harus menggunakannya?

Two Factor Authentication (2FA) menambahkan lapisan perlindungan ekstra untuk akun Anda di atas password. Untuk login, Anda tidak hanya harus mengetahui suatu password, tetapi Anda juga harus "membuktikan" dengan cara tertentu bahwa Anda memiliki akses ke suatu perangkat keras. Pada kasus paling sederhana, ini dapat dicapai dengan menerima SMS di ponsel Anda, meskipun ada [masalah yang diketahui](https://www.kaspersky.com/blog/2fa-practical-guide/24219/) dengan SMS 2FA. Alternatif yang lebih baik yang kami dukung adalah menggunakan solusi [U2F](https://en.wikipedia.org/wiki/Universal_2nd_Factor) seperti [YubiKey](https://www.yubico.com/).

<a id="any-comments-on-differences-between-web-browsers"></a>
## Ada komentar tentang perbedaan antar web browser?

Lanskap browser saat ini per 2020 adalah sebagian besar di antaranya seperti Chrome karena menggunakan engine yang sama (Blink). Ini berarti Microsoft Edge yang juga berbasis Blink, dan Safari, yang berbasis WebKit, engine yang mirip Blink, hanyalah versi yang lebih buruk dari Chrome. Chrome adalah browser yang cukup baik dari segi performa maupun usability. Jika Anda menginginkan alternatif, Firefox adalah rekomendasi kami. Browser ini sebanding dengan Chrome dalam hampir semua hal dan unggul karena alasan privacy.
Browser lain bernama [Flow](https://www.ekioh.com/flow-browser/) belum siap pengguna, tetapi sedang mengimplementasikan rendering engine baru yang menjanjikan lebih cepat daripada yang ada saat ini.
