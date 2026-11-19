---
layout: lecture-id
title: "Debugging dan Profiling"
description: >
  Pelajari cara men-debug program menggunakan logging dan debugger, serta melakukan profiling kode untuk mengukur performa.
thumbnail: /static/assets/thumbnails/2026/lec4.png
date: 2026-01-15
ready: true
panopto: "https://mit.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=a72c48e3-5eb2-46fa-aa03-b3b700e1ca8d"
video:
  aspect: 56.25
  id: 8VYT9TcUmKs
lang: id
permalink: /id/2026/debugging-profiling/
---

Aturan emas dalam pemrograman adalah kode tidak melakukan apa yang Anda harapkan, tetapi melakukan apa yang Anda perintahkan. Menjembatani kesenjangan itu kadang bisa menjadi pencapaian yang cukup sulit. Pada kuliah ini kita akan membahas teknik berguna untuk menangani kode yang buggy dan boros sumber daya: debugging dan profiling.

# Debugging

## Printf Debugging dan Logging

> "Tool debugging yang paling efektif tetaplah berpikir dengan cermat, disertai print statement yang ditempatkan dengan pertimbangan matang" — Brian Kernighan, _Unix for Beginners_.

Pendekatan pertama untuk men-debug program adalah menambahkan pernyataan print di sekitar tempat Anda mendeteksi masalah, dan terus mengiterasi sampai Anda memperoleh cukup informasi untuk memahami apa yang bertanggung jawab atas masalah tersebut.

Pendekatan kedua adalah menggunakan logging di program Anda, alih-alih pernyataan print ad hoc. Logging pada dasarnya adalah "mencetak dengan lebih cermat", dan biasanya dilakukan melalui framework logging yang menyertakan dukungan bawaan untuk hal-hal seperti:

- kemampuan mengarahkan log (atau sebagian log) ke lokasi output lain;
- menetapkan severity level (seperti INFO, DEBUG, WARN, ERROR, dsb.) dan memungkinkan Anda memfilter output berdasarkan level tersebut; dan
- dukungan structured logging untuk data yang terkait dengan entri log, yang kemudian dapat diekstrak lebih mudah setelah kejadian.

Pernyataan logging juga biasanya Anda sisipkan secara proaktif saat
memprogram agar data yang Anda butuhkan untuk debugging mungkin sudah ada!
Dan memang, setelah Anda menemukan dan memperbaiki masalah menggunakan pernyataan
print, sering kali bermanfaat mengubah print tersebut menjadi pernyataan
log yang layak sebelum menghapusnya. Dengan begitu, jika bug serupa terjadi
di masa depan, Anda sudah memiliki informasi diagnostik yang dibutuhkan
tanpa memodifikasi kode.

> **Log pihak ketiga**: Banyak program mendukung flag `-v` atau `--verbose` untuk mencetak lebih banyak informasi saat berjalan. Ini bisa berguna untuk menemukan mengapa sebuah perintah gagal. Sebagian bahkan mengizinkan pengulangan flag untuk detail lebih banyak. Saat men-debug masalah pada layanan (database, web server, dsb.), periksa log-nya—sering kali di `/var/log/` pada Linux. Gunakan `journalctl -u <service>` untuk melihat log layanan systemd. Untuk library pihak ketiga, periksa apakah library tersebut mendukung debug logging melalui environment variable atau konfigurasi.

## Debuggers

Print debugging berfungsi baik ketika Anda mengetahui apa yang harus dicetak dan dapat dengan mudah memodifikasi serta menjalankan ulang kode Anda. Debugger menjadi berharga ketika Anda tidak yakin informasi apa yang dibutuhkan, ketika bug hanya muncul dalam kondisi yang sulit direproduksi, atau ketika memodifikasi dan me-restart program mahal (waktu startup lama, state kompleks yang harus dibangun ulang, dsb.).

Debugger adalah program yang memungkinkan Anda berinteraksi dengan eksekusi sebuah program saat berlangsung, memungkinkan Anda untuk:

- Menghentikan eksekusi ketika mencapai baris tertentu.
- Melangkah melalui satu instruksi sekaligus.
- Memeriksa nilai variabel setelah crash.
- Menghentikan eksekusi secara kondisional ketika kondisi tertentu terpenuhi.
- Dan banyak fitur lanjutan lainnya.

Sebagian besar bahasa pemrograman mendukung (atau dilengkapi) semacam debugger. Yang paling serbaguna adalah **general-purpose debugger** seperti [`gdb`](https://www.gnu.org/software/gdb/) (GNU Debugger) dan [`lldb`](https://lldb.llvm.org/) (LLVM Debugger), yang dapat men-debug binary native apa pun. Banyak bahasa juga memiliki **debugger khas bahasa** yang terintegrasi lebih erat dengan runtime (seperti pdb pada Python atau jdb pada Java).

`gdb` adalah debugger standar de facto untuk C, C++, Rust, dan bahasa terkompilasi lainnya. Tool ini memungkinkan Anda menyelidiki hampir semua proses dan memperoleh state mesin saat ini: register, stack, program counter, dan banyak lagi.

Beberapa perintah GDB yang berguna:

- `run` - Mulai program
- `b {function}` atau `b {file}:{line}` - Menetapkan breakpoint
- `c` - Melanjutkan eksekusi
- `step` / `next` / `finish` - Step in / step over / step out
- `p {variable}` - Mencetak nilai variabel
- `bt` - Menampilkan backtrace (call stack)
- `watch {expression}` - Berhenti ketika nilai berubah

> Pertimbangkan menggunakan mode TUI GDB (`gdb -tui` atau tekan `Ctrl-x a` di dalam GDB) untuk tampilan layar terbagi yang menampilkan kode sumber di samping prompt perintah.

### Record-Replay Debugging

Sebagian bug yang paling menjengkelkan adalah _Heisenbug_: bug yang tampak hilang atau berubah perilaku ketika Anda mencoba mengamatinya. Race condition, bug yang bergantung pada timing, dan masalah yang hanya muncul di bawah kondisi sistem tertentu termasuk dalam kategori ini. Debugging tradisional sering tidak berguna di sini karena menjalankan program lagi menghasilkan perilaku yang berbeda (misalnya, pernyataan print mungkin memperlambat kode cukup banyak sehingga race tidak lagi terjadi).

**Record-replay debugging** mengatasi ini dengan merekam eksekusi sebuah program dan memungkinkan Anda memutarnya ulang secara deterministik sebanyak yang Anda perlukan. Bahkan lebih baik, Anda dapat _membalik_ eksekusi untuk menemukan tepat di mana masalah terjadi.

[rr](https://rr-project.org/) adalah tool yang kuat untuk Linux yang merekam eksekusi program dan memungkinkan replay deterministik dengan kemampuan debugging penuh. Tool ini bekerja dengan GDB, sehingga Anda sudah mengenal antarmukanya.

Penggunaan dasar:

```bash
# Record a program execution
rr record ./my_program

# Replay the recording (opens GDB)
rr replay
```

Keajaiban terjadi saat replay. Karena eksekusinya deterministik, Anda dapat menggunakan perintah **reverse debugging**:

- `reverse-continue` (`rc`) - Berjalan mundur sampai mengenai breakpoint
- `reverse-step` (`rs`) - Melangkah mundur satu baris
- `reverse-next` (`rn`) - Melangkah mundur, melewati pemanggilan fungsi
- `reverse-finish` - Berjalan mundur sampai masuk ke fungsi saat ini

Ini sangat kuat untuk debugging. Katakanlah Anda memiliki crash—alih-alih menebak di mana bug-nya dan menetapkan breakpoint, Anda dapat:

1. Berjalan sampai crash
2. Memeriksa state yang rusak
3. Menetapkan watchpoint pada variabel yang rusak
4. `reverse-continue` untuk menemukan tepat di mana variabel itu dirusak

**Kapan menggunakan rr:**
- Flaky test yang gagal secara intermiten
- Race condition dan bug threading
- Crash yang sulit direproduksi
- Bug apa pun di mana Anda berharap dapat "kembali ke masa lalu"

> Catatan: rr hanya bekerja di Linux dan memerlukan hardware performance counter. Tool ini tidak bekerja di VM yang tidak mengekspos counter tersebut, seperti pada sebagian besar instans AWS EC2, dan tidak mendukung akses GPU. Untuk macOS, lihat [Warpspeed](https://warpspeed.dev/).

> **rr dan konkurensi**: Karena rr merekam eksekusi secara deterministik, rr menyerialkan penjadwalan thread. Ini berarti sebagian race condition mungkin tidak muncul di bawah rr jika race tersebut bergantung pada timing tertentu. rr tetap berguna untuk men-debug race—setelah Anda menangkap eksekusi yang gagal, Anda dapat memutarnya ulang secara andal—tetapi Anda mungkin memerlukan beberapa percobaan perekaman untuk menangkap bug yang intermiten. Untuk bug yang tidak melibatkan konkurensi, rr paling bersinar: Anda selalu dapat mereproduksi eksekusi yang persis sama dan menggunakan reverse debugging untuk memburu kerusakan.

## System Call Tracing

Kadang Anda perlu memahami bagaimana program Anda berinteraksi dengan sistem operasi. Program melakukan [system call](https://en.wikipedia.org/wiki/System_call) untuk meminta layanan dari kernel—membuka berkas, mengalokasikan memori, membuat proses, dan banyak lagi. Melacak panggilan ini dapat mengungkap mengapa sebuah program menggantung, berkas apa yang coba diaksesnya, atau di mana program menghabiskan waktu menunggu.

### strace (Linux) dan dtruss (macOS)

[`strace`](https://www.man7.org/linux/man-pages/man1/strace.1.html) memungkinkan Anda mengamati setiap system call yang dilakukan sebuah program:

```bash
# Trace all system calls
strace ./my_program

# Trace only file-related calls
strace -e trace=file ./my_program

# Follow child processes (important for programs that start other programs)
strace -f ./my_program

# Trace a running process
strace -p <PID>

# Show timing information
strace -T ./my_program
```

> Di macOS dan BSD, gunakan [`dtruss`](https://www.manpagez.com/man/1/dtruss/) (yang membungkus `dtrace`) untuk fungsionalitas serupa:

> Untuk menyelami `strace` lebih dalam, lihat [strace zine](https://jvns.ca/strace-zine-unfolded.pdf) yang sangat bagus dari Julia Evans.

### bpftrace dan eBPF

[eBPF](https://ebpf.io/) (extended Berkeley Packet Filter) adalah teknologi Linux yang kuat yang memungkinkan menjalankan program tersandbox di dalam kernel. [`bpftrace`](https://github.com/iovisor/bpftrace) menyediakan sintaks tingkat tinggi untuk menulis program eBPF. Ini adalah program arbitrer yang berjalan di dalam kernel, sehingga memiliki kekuatan ekspresif yang besar (meskipun sintaksnya agak canggung seperti awk). Use case paling umum bagi program tersebut adalah menyelidiki system call apa yang dipanggil, termasuk agregasi (seperti hitungan atau statistik latency) atau introspeksi (bahkan filter pada) argumen system call.

```bash
# Trace file opens system-wide (prints immediately)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_openat { printf("%s %s\n", comm, str(args->filename)); }'

# Count system calls by name (prints summary on Ctrl-C)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* { @[probe] = count(); }'
```

Namun, Anda juga dapat menulis program eBPF langsung dalam C menggunakan toolchain seperti [`bcc`](https://github.com/iovisor/bcc), yang juga dilengkapi [banyak tool praktis](https://www.brendangregg.com/blog/2015-09-22/bcc-linux-4.3-tracing.html) seperti `biosnoop` untuk mencetak distribusi latency operasi disk atau `opensnoop` untuk mencetak semua berkas yang terbuka.

Jika `strace` berguna karena mudah "langsung dijalankan", `bpftrace` adalah yang sebaiknya Anda gunakan ketika membutuhkan overhead lebih rendah, ingin melacak melalui fungsi kernel, perlu melakukan semacam agregasi, dsb. Perhatikan bahwa `bpftrace` harus dijalankan sebagai `root`, dan bahwa tool ini umumnya memantau seluruh kernel, bukan hanya proses tertentu. Untuk menargetkan program tertentu, Anda dapat memfilter berdasarkan nama perintah atau PID:

```bash
# Filter by command name (prints summary on Ctrl-C)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* /comm == "bash"/ { @[probe] = count(); }'

# Trace a specific command from startup using -c (cpid = child PID)
sudo bpftrace -e 'tracepoint:syscalls:sys_enter_* /pid == cpid/ { @[probe] = count(); }' -c 'ls -la'
```

Flag `-c` menjalankan perintah yang ditentukan dan menetapkan `cpid` ke PID perintah tersebut, yang berguna untuk melacak program sejak saat dimulai. Ketika perintah yang dilacak keluar, bpftrace mencetak hasil agregasinya.

### Network Debugging

Untuk masalah jaringan, [`tcpdump`](https://www.man7.org/linux/man-pages/man1/tcpdump.1.html) dan [Wireshark](https://www.wireshark.org/) memungkinkan Anda menangkap dan menganalisis paket jaringan:

```bash
# Capture packets on port 80
sudo tcpdump -i any port 80

# Capture and save to file for Wireshark analysis
sudo tcpdump -i any -w capture.pcap
```

Untuk lalu lintas HTTPS, enkripsi membuat tcpdump kurang berguna. Tool seperti [mitmproxy](https://mitmproxy.org/) dapat berperan sebagai intercepting proxy untuk memeriksa lalu lintas terenkripsi. Developer tools di browser (tab Network) sering kali menjadi cara termudah untuk men-debug permintaan HTTPS dari aplikasi web—tool tersebut menampilkan data request/response yang sudah didekripsi, header, dan timing.

## Memory Debugging

Bug memori—buffer overflow, use-after-free, memory leak—termasuk yang paling berbahaya dan paling sulit di-debug. Bug tersebut sering tidak langsung crash tetapi merusak memori dengan cara yang menimbulkan masalah jauh di kemudian hari.

### Sanitizers

Salah satu pendekatan untuk menemukan bug memori adalah menggunakan **sanitizer**, yaitu fitur compiler yang menginstrumentasi kode Anda untuk mendeteksi error saat runtime. Misalnya, **AddressSanitizer (ASan)** yang banyak digunakan mendeteksi:
- Buffer overflow (stack, heap, dan global)
- Use-after-free
- Use-after-return
- Memory leak

```bash
# Compile with AddressSanitizer
gcc -fsanitize=address -g program.c -o program
./program
```

Ada berbagai sanitizer yang berguna:

- **ThreadSanitizer (TSan)**: Mendeteksi data race pada kode multithreaded (`-fsanitize=thread`)
- **MemorySanitizer (MSan)**: Mendeteksi pembacaan memori yang tidak diinisialisasi (`-fsanitize=memory`)
- **UndefinedBehaviorSanitizer (UBSan)**: Mendeteksi undefined behavior seperti integer overflow (`-fsanitize=undefined`)

Sanitizer memerlukan kompilasi ulang tetapi cukup cepat untuk digunakan di pipeline CI dan selama pengembangan rutin.

### Valgrind: Saat Anda Tidak Dapat Melakukan Recompile

[Valgrind](https://valgrind.org/) sebaliknya menjalankan program Anda dalam sesuatu yang mirip dengan virtual machine untuk mendeteksi error memori. Tool ini lebih lambat daripada sanitizer tetapi tidak memerlukan kompilasi ulang:

```bash
valgrind --leak-check=full ./my_program
```

Gunakan Valgrind ketika:
- Anda tidak memiliki kode sumber
- Anda tidak dapat mengompilasi ulang (library pihak ketiga)
- Anda memerlukan tool khusus yang tidak tersedia sebagai sanitizer

Valgrind sebenarnya adalah lingkungan eksekusi terkontrol yang sangat kuat, dan kita akan melihatnya lebih banyak nanti ketika kita membahas profiling!

## AI untuk Debugging

Large language model telah menjadi asisten debugging yang ternyata sangat berguna. LLM unggul dalam tugas debugging tertentu yang melengkapi tool tradisional.

**Di mana LLM bersinar:**

- **Menjelaskan pesan error yang samar**: Error compiler, terutama dari template C++ atau borrow checker Rust, bisa sangat samar. LLM dapat menerjemahkannya ke bahasa yang jelas dan menyarankan perbaikan.

- **Menelusuri batas bahasa dan abstraksi**: Jika Anda men-debug masalah yang melintasi beberapa bahasa (misalnya, bug di library C yang terwujud melalui binding Python), LLM dapat membantu menavigasi lapisan-lapisan yang berbeda. LLM sangat baik dalam memahami batas FFI, masalah build system, dan debugging lintas bahasa (misalnya, program saya error, tetapi saya yakin itu karena bug di salah satu dependensi saya).

- **Mengorelasikan gejala dengan akar masalah**: "Program saya berjalan baik tetapi menggunakan memori 10x lebih banyak dari yang diharapkan" adalah jenis gejala samar yang dapat dibantu LLM untuk diselidiki, dengan menyarankan kemungkinan penyebab dan apa yang harus dicari.

- **Menganalisis crash dump dan stack trace**: Tempelkan stack trace dan tanyakan apa yang mungkin menyebabkannya.

> **Catatan tentang debug symbol**: Untuk stack trace dan debugging yang bermakna, pastikan binary Anda (dan library apa pun yang di-link) dikompilasi dengan debug symbol (flag `-g`). Informasi debug biasanya disimpan dalam format DWARF. Selain itu, mengompilasi dengan frame pointer (`-fno-omit-frame-pointer`) membuat stack trace lebih andal, terutama untuk tool profiling. Tanpa ini, stack trace mungkin hanya menampilkan alamat memori atau tidak lengkap. Ini lebih penting untuk program yang dikompilasi secara native (C++, Rust) daripada Python atau Java.

**Keterbatasan yang perlu diingat:**
- LLM dapat berhalusinasi menghasilkan penjelasan yang terdengar masuk akal tetapi salah
- LLM mungkin menyarankan perbaikan yang menutupi bug alih-alih memperbaikinya
- Selalu verifikasi saran dengan tool debugging yang sebenarnya
- LLM paling berfungsi sebagai pelengkap pemahaman Anda atas kode, bukan penggantinya

> Ini berbeda dengan [kemampuan coding AI secara umum](/2026/development-environment/#ai-powered-development) yang dibahas pada kuliah Development Environment. Di sini kita secara khusus membahas penggunaan LLM sebagai bantuan debugging.

# Profiling

Bahkan jika kode Anda berperilaku secara fungsional seperti yang Anda harapkan, itu mungkin belum cukup baik jika kode tersebut menghabiskan seluruh CPU atau memori Anda dalam prosesnya. Kelas algoritma sering mengajarkan notasi big _O_ tetapi tidak mengajarkan cara menemukan hot spot pada program Anda. Karena [premature optimization is the root of all evil](https://wiki.c2.com/?PrematureOptimization), Anda sebaiknya mempelajari profiler dan tool monitoring. Tool tersebut akan membantu Anda memahami bagian program mana yang menghabiskan sebagian besar waktu dan/atau sumber daya sehingga Anda dapat memfokuskan upaya mengoptimalkan bagian tersebut.

## Pengukuran Waktu

Cara paling sederhana untuk mengukur performa adalah mengukur waktu. Dalam banyak skenario, cukup dengan mencetak waktu yang dibutuhkan kode Anda antara dua titik.

Namun, wall clock time bisa menyesatkan karena komputer Anda mungkin menjalankan proses lain pada waktu yang sama atau menunggu peristiwa terjadi. Perintah `time` membedakan antara waktu _Real_, _User_, dan _Sys_:

- **Real** - Wall clock time dari awal sampai selesai, termasuk waktu yang dihabiskan menunggu
- **User** - Waktu yang dihabiskan di CPU untuk menjalankan kode pengguna
- **Sys** - Waktu yang dihabiskan di CPU untuk menjalankan kode kernel

```bash
$ time curl https://missing.csail.mit.edu &> /dev/null
real	0m0.272s
user	0m0.079s
sys	    0m0.028s
```

Di sini permintaan memakan waktu hampir 300 milidetik (real time) tetapi hanya 107ms waktu CPU (user + sys). Sisanya menunggu jaringan.

## Resource Monitoring

Kadang langkah pertama menuju analisis performa program Anda adalah memahami konsumsi sumber daya aktualnya. Program sering berjalan lambat ketika sumber dayanya terbatas.

- **Monitoring umum**: [`htop`](https://htop.dev/) adalah versi `top` yang ditingkatkan yang menyajikan berbagai statistik untuk proses yang sedang berjalan. Keybinding berguna: `<F6>` untuk mengurutkan proses, `t` untuk menampilkan hierarki tree, `h` untuk menampilkan/menyembunyikan thread. Ada juga [`btop`](https://github.com/aristocratos/btop) yang memantau _jauh_ lebih banyak hal.

- **Operasi I/O**: [`iotop`](https://www.man7.org/linux/man-pages/man8/iotop.8.html) menampilkan informasi penggunaan I/O secara langsung.

- **Penggunaan memori**: [`free`](https://www.man7.org/linux/man-pages/man1/free.1.html) menampilkan total memori bebas dan terpakai.

- **Berkas terbuka**: [`lsof`](https://www.man7.org/linux/man-pages/man8/lsof.8.html) mencantumkan informasi berkas tentang berkas yang dibuka oleh proses. Berguna untuk memeriksa proses mana yang membuka berkas tertentu.

- **Koneksi jaringan**: [`ss`](https://www.man7.org/linux/man-pages/man8/ss.8.html) memungkinkan Anda memantau koneksi jaringan. Use case umum adalah mencari tahu proses apa yang menggunakan port tertentu: `ss -tlnp | grep :8080`.

- **Penggunaan jaringan**: [`nethogs`](https://github.com/raboof/nethogs) dan [`iftop`](https://pdw.ex-parrot.com/iftop/) adalah tool CLI interaktif yang baik untuk memantau penggunaan jaringan per proses.

## Memvisualisasikan Data Performa

Manusia mengenali pola pada grafik jauh lebih cepat daripada pada tabel angka. Saat menganalisis performa, memplot data Anda sering mengungkap tren, lonjakan, dan anomali yang tidak terlihat pada angka mentah.

**Membuat data dapat diplot**: Saat menambahkan pernyataan print atau log untuk debugging, pertimbangkan memformat output agar mudah digrafikkan nanti. Timestamp dan nilai sederhana dalam format CSV (`1705012345,42.5`) jauh lebih mudah diplot daripada kalimat prosa. Log berstruktur JSON juga dapat diurai dan diplot dengan usaha minimal. Dengan kata lain, catat data Anda [dengan cara yang rapi](https://vita.had.co.nz/papers/tidy-data.pdf).

**Plotting cepat dengan gnuplot**: Untuk plotting command-line sederhana, [`gnuplot`](http://www.gnuplot.info/) dapat menghasilkan grafik langsung dari berkas data:

```bash
# Plot a simple CSV with timestamp,value
gnuplot -e "set datafile separator ','; plot 'latency.csv' using 1:2 with lines"
```

**Eksplorasi iteratif dengan matplotlib dan ggplot2**: Untuk analisis lebih mendalam, [`matplotlib`](https://matplotlib.org/) dari Python dan [`ggplot2`](https://ggplot2.tidyverse.org/) dari R memungkinkan eksplorasi iteratif. Berbeda dengan plotting sekali pakai, tool ini memungkinkan Anda dengan cepat memotong dan mentransformasi data untuk menyelidiki hipotesis. Facet plot ggplot2 sangat kuat—Anda dapat memecah satu dataset ke beberapa subplot berdasarkan kategori (misalnya, memfacet latency permintaan berdasarkan endpoint atau waktu dalam sehari) untuk menemukan pola yang jika tidak akan tetap tersembunyi.

**Contoh use case:**
- Memplot latency permintaan dari waktu ke waktu mengungkap perlambatan periodik (garbage collection, cron job, pola lalu lintas) yang tersamarkan oleh persentil mentah
- Memvisualisasikan waktu insert untuk struktur data yang tumbuh dapat mengekspos masalah kompleksitas algoritmik—plot penyisipan vector akan menunjukkan lonjakan khas ketika array di baliknya berlipat ganda ukurannya
- Memfacet metrik berdasarkan dimensi berbeda (jenis permintaan, kohort pengguna, server) sering mengungkap bahwa masalah "seluruh sistem" sebenarnya terisolasi pada satu kategori

## CPU Profilers

Sebagian besar waktu ketika orang menyebut _profiler_ yang mereka maksud adalah _CPU profiler_. Ada dua jenis utama:

- **Tracing profiler** menyimpan catatan setiap pemanggilan fungsi yang dilakukan program Anda
- **Sampling profiler** menyelidiki program Anda secara berkala (umumnya setiap milidetik) dan mencatat stack program

Sampling profiler memiliki overhead lebih rendah dan umumnya lebih disukai untuk penggunaan produksi.

### perf: Sampling Profiler

[`perf`](https://www.man7.org/linux/man-pages/man1/perf.1.html) adalah profiler standar Linux. Tool ini dapat memprofil program apa pun tanpa kompilasi ulang:

`perf stat` memberi Anda gambaran singkat tentang di mana waktu dihabiskan:

```bash
$ perf stat ./slow_program

 Performance counter stats for './slow_program':

         3,210.45 msec task-clock                #    0.998 CPUs utilized
               12      context-switches          #    3.738 /sec
                0      cpu-migrations            #    0.000 /sec
              156      page-faults               #   48.587 /sec
   12,345,678,901      cycles                    #    3.845 GHz
    9,876,543,210      instructions              #    0.80  insn per cycle
    1,234,567,890      branches                  #  384.532 M/sec
       12,345,678      branch-misses             #    1.00% of all branches
```

Output profiler untuk program dunia nyata akan memuat informasi dalam jumlah besar. Manusia adalah makhluk visual dan cukup buruk dalam membaca angka dalam jumlah besar. [Flame graph](https://www.brendangregg.com/flamegraphs.html) adalah visualisasi yang membuat data profiling jauh lebih mudah dipahami.

Flame graph menampilkan hierarki pemanggilan fungsi pada sumbu Y dan waktu yang dihabiskan secara proporsional pada sumbu X. Grafik ini interaktif—Anda dapat mengklik untuk memperbesar bagian tertentu dari program.

[![FlameGraph](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)](https://www.brendangregg.com/FlameGraphs/cpu-bash-flamegraph.svg)

Untuk menghasilkan flame graph dari data `perf`:

```bash
# Record profile
perf record -g ./my_program

# Generate flame graph (requires flamegraph scripts)
perf script | stackcollapse-perf.pl | flamegraph.pl > flamegraph.svg
```

> Pertimbangkan menggunakan [Speedscope](https://www.speedscope.app/) sebagai penampil flame graph interaktif berbasis web, atau [Perfetto](https://perfetto.dev/) untuk analisis tingkat sistem yang komprehensif.

### Callgrind dari Valgrind: Tracing Profiler

[`callgrind`](https://valgrind.org/docs/manual/cl-manual.html) adalah tool profiling yang merekam riwayat pemanggilan dan jumlah instruksi program Anda. Berbeda dengan sampling profiler, tool ini memberikan jumlah pemanggilan yang tepat dan dapat menunjukkan hubungan antara caller dan callee:

```bash
# Run with callgrind
valgrind --tool=callgrind ./my_program

# Analyze with callgrind_annotate (text) or kcachegrind (GUI)
callgrind_annotate callgrind.out.<pid>
kcachegrind callgrind.out.<pid>
```

Callgrind lebih lambat daripada sampling profiler tetapi memberikan jumlah pemanggilan yang tepat dan dapat secara opsional menyimulasikan perilaku cache (dengan `--cache-sim=yes`) jika Anda membutuhkan informasi tersebut.

> Jika Anda menggunakan bahasa tertentu, mungkin ada profiler yang lebih khusus. Misalnya, Python memiliki [`cProfile`](https://docs.python.org/3/library/profile.html) dan [`py-spy`](https://github.com/benfred/py-spy), Go memiliki [`go tool pprof`](https://pkg.go.dev/cmd/pprof), dan Rust memiliki [`cargo-flamegraph`](https://github.com/flamegraph-rs/flamegraph) (yang sebenarnya bekerja untuk program terkompilasi apa pun!).

## Memory Profilers

Memory profiler membantu Anda memahami bagaimana program Anda menggunakan memori seiring waktu dan menemukan memory leak.

### Massif dari Valgrind

[`massif`](https://valgrind.org/docs/manual/ms-manual.html) memprofil penggunaan memori heap:

```bash
valgrind --tool=massif ./my_program
ms_print massif.out.<pid>
```

Ini menunjukkan kepada Anda penggunaan heap seiring waktu, membantu mengidentifikasi memory leak dan alokasi berlebihan.

> Untuk Python, [`memory-profiler`](https://pypi.org/project/memory-profiler/) menyediakan informasi penggunaan memori baris demi baris.

## Benchmarking

Ketika Anda perlu membandingkan performa implementasi atau tool yang berbeda, [`hyperfine`](https://github.com/sharkdp/hyperfine) sangat baik untuk melakukan benchmark program command-line:

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

> Untuk pengembangan web, developer tools di browser menyertakan profiler yang sangat baik. Lihat dokumentasi [Firefox Profiler](https://profiler.firefox.com/docs/) dan [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools/rendering-tools).

# Latihan

## Debugging

1. **Debug algoritma pengurutan**: Pseudocode berikut mengimplementasikan merge sort tetapi memiliki bug. Implementasikan dalam bahasa pilihan Anda, lalu gunakan debugger (gdb, lldb, pdb, atau debugger IDE Anda) untuk menemukan dan memperbaiki bug tersebut.

   ```
   function merge_sort(arr):
       if length(arr) <= 1:
           return arr
       mid = length(arr) / 2
       left = merge_sort(arr[0..mid])
       right = merge_sort(arr[mid..end])
       return merge(left, right)

   function merge(left, right):
       result = []
       i = 0, j = 0
       while i < length(left) AND j < length(right):
           if left[i] <= right[j]:
               append result, left[i]
               i = i + 1
           else:
               append result, right[i]
               j = j + 1
       append remaining elements from left and right
       return result
   ```

   Vektor uji: `merge_sort([3, 1, 4, 1, 5, 9, 2, 6])` seharusnya mengembalikan `[1, 1, 2, 3, 4, 5, 6, 9]`. Gunakan breakpoint dan telusuri fungsi merge langkah demi langkah untuk menemukan di mana elemen yang salah dipilih.

1. Pasang [`rr`](https://rr-project.org/) dan gunakan reverse debugging untuk menemukan bug korupsi. Simpan program ini sebagai `corruption.c`:

   ```c
   #include <stdio.h>

   typedef struct {
       int id;
       int scores[3];
   } Student;

   Student students[2];

   void init() {
       students[0].id = 1001;
       students[0].scores[0] = 85;
       students[0].scores[1] = 92;
       students[0].scores[2] = 78;

       students[1].id = 1002;
       students[1].scores[0] = 90;
       students[1].scores[1] = 88;
       students[1].scores[2] = 95;
   }

   void curve_scores(int student_idx, int curve) {
       for (int i = 0; i < 4; i++) {
           students[student_idx].scores[i] += curve;
       }
   }

   int main() {
       init();
       printf("=== Initial state ===\n");
       printf("Student 0: id=%d\n", students[0].id);
       printf("Student 1: id=%d\n", students[1].id);

       curve_scores(0, 5);

       printf("\n=== After curving ===\n");
       printf("Student 0: id=%d\n", students[0].id);
       printf("Student 1: id=%d\n", students[1].id);

       if (students[1].id != 1002) {
           printf("\nERROR: Student 1's ID was corrupted! Expected 1002, got %d\n",
                  students[1].id);
           return 1;
       }
       return 0;
   }
   ```

   Kompilasi dengan `gcc -g corruption.c -o corruption` dan jalankan. ID Student 1 menjadi rusak, tetapi kerusakan terjadi di fungsi yang hanya menyentuh student 0. Gunakan `rr record ./corruption` dan `rr replay` untuk menemukan penyebabnya. Tetapkan watchpoint pada `students[1].id` dan gunakan `reverse-continue` setelah kerusakan untuk menemukan tepat baris kode mana yang menimpanya.

1. Debug error memori dengan AddressSanitizer. Simpan ini sebagai `uaf.c`:

   ```c
   #include <stdlib.h>
   #include <string.h>
   #include <stdio.h>

   int main() {
       char *greeting = malloc(32);
       strcpy(greeting, "Hello, world!");
       printf("%s\n", greeting);

       free(greeting);

       greeting[0] = 'J';
       printf("%s\n", greeting);

       return 0;
   }
   ```

   Pertama kompilasi dan jalankan tanpa sanitizer: `gcc uaf.c -o uaf && ./uaf`. Program mungkin tampak berfungsi. Sekarang kompilasi dengan AddressSanitizer: `gcc -fsanitize=address -g uaf.c -o uaf && ./uaf`. Baca laporan error-nya. Bug apa yang ditemukan ASan? Perbaiki masalah yang diidentifikasinya.

1. Gunakan `strace` (Linux) atau `dtruss` (macOS) untuk melacak system call yang dilakukan perintah seperti `ls -l`. System call apa yang dilakukan? Coba lacak program yang lebih kompleks dan lihat berkas apa saja yang dibukanya.

1. Gunakan LLM untuk membantu men-debug pesan error yang samar. Coba salin error compiler (terutama dari template C++ atau Rust) dan minta penjelasan serta perbaikannya. Coba masukkan sebagian output dari `strace` atau address sanitizer ke dalamnya.

## Profiling

1. Gunakan `perf stat` untuk memperoleh statistik performa dasar bagi program pilihan Anda. Apa arti berbagai counter tersebut?

1. Lakukan profiling dengan `perf record`. Simpan ini sebagai `slow.c`:

   ```c
   #include <math.h>
   #include <stdio.h>

   double slow_computation(int n) {
       double result = 0;
       for (int i = 0; i < n; i++) {
           for (int j = 0; j < 1000; j++) {
               result += sin(i * j) * cos(i + j);
           }
       }
       return result;
   }

   int main() {
       double r = 0;
       for (int i = 0; i < 100; i++) {
           r += slow_computation(1000);
       }
       printf("Result: %f\n", r);
       return 0;
   }
   ```

   Kompilasi dengan debug symbol: `gcc -g -O2 slow.c -o slow -lm`. Jalankan `perf record -g ./slow`, lalu `perf report` untuk melihat di mana waktu dihabiskan. Coba hasilkan flame graph menggunakan skrip flamegraph.

1. Gunakan `hyperfine` untuk melakukan benchmark dua implementasi berbeda dari tugas yang sama (misalnya, `find` vs `fd`, `grep` vs `ripgrep`, atau dua versi kode Anda sendiri).

1. Gunakan `htop` untuk memantau sistem Anda saat menjalankan program yang intensif sumber daya. Coba gunakan `taskset` untuk membatasi CPU mana yang boleh digunakan sebuah proses: `taskset --cpu-list 0,2 stress -c 3`. Mengapa `stress` tidak menggunakan tiga CPU?

1. Masalah umum adalah port yang ingin Anda dengarkan sudah dipakai proses lain. Pelajari cara menemukan proses tersebut: Pertama jalankan `python -m http.server 4444` untuk memulai web server minimal pada port 4444. Di terminal terpisah jalankan `ss -tlnp | grep 4444` untuk menemukan prosesnya. Hentikan proses tersebut dengan `kill <PID>`.
