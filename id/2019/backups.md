---
layout: lecture-id
title: "Backups"
presenter: Jose
date: 2019-01-24
order: 2
video:
  aspect: 56.25
  id: lrpqYF8tcYQ
special: true
lang: id
permalink: /id/2019/backups/
---

Ada dua jenis orang:

- Mereka yang melakukan backup
- Mereka yang akan melakukan backup

Data apa pun yang Anda miliki dan belum Anda backup adalah data yang bisa hilang kapan saja, selamanya. Di sini kita akan membahas beberapa dasar backup yang baik dan jebakan dari beberapa pendekatan.

## Aturan 3-2-1

[Aturan 3-2-1](https://www.us-cert.gov/sites/default/files/publications/data_backup_options.pdf) adalah strategi umum yang direkomendasikan untuk membackup data Anda. Aturan ini menyatakan bahwa Anda sebaiknya memiliki:

- setidaknya **3 salinan** data Anda
- **2** salinan pada **medium berbeda**
- **1** dari salinan tersebut berada **offsite**

Ide utama di balik rekomendasi ini adalah jangan menaruh semua telur dalam satu keranjang. Memiliki 2 perangkat/disk berbeda memastikan satu kegagalan perangkat keras tidak menghilangkan semua data Anda. Demikian pula, jika Anda menyimpan satu-satunya backup di rumah dan rumah terbakar atau dirampok, Anda akan kehilangan semuanya! Itulah fungsi salinan offsite. Backup onsite memberi Anda ketersediaan dan kecepatan, backup offsite memberi Anda ketahanan jika terjadi bencana.

## Menguji backup Anda

Jebakan umum saat melakukan backup adalah memercayai secara buta apa pun yang dikatakan sistem dan tidak memverifikasi bahwa data dapat dipulihkan dengan benar. Toy Story 2 hampir hilang dan backup mereka tidak berfungsi, [keberuntungan](https://www.youtube.com/watch?v=8dhp_20j0Ys) yang akhirnya menyelamatkan mereka.

## Versioning

Anda sebaiknya memahami bahwa [RAID](https://en.wikipedia.org/wiki/RAID) bukanlah backup, dan secara umum **mirroring bukanlah solusi backup**. Sekadar menyinkronkan berkas Anda ke suatu tempat tidak akan membantu dalam beberapa skenario, seperti:

- Korupsi data
- Perangkat lunak berbahaya
- Menghapus berkas karena kesalahan

Jika perubahan pada data Anda menyebar ke backup maka Anda tidak akan dapat memulihkan dalam skenario tersebut. Perhatikan bahwa ini terjadi pada banyak solusi cloud storage seperti Dropbox, Google Drive, One Drive, &c. Sebagian dari solusi itu menyimpan data yang dihapus untuk waktu singkat tetapi biasanya antarmuka untuk memulihkannya bukan sesuatu yang ingin Anda gunakan untuk memulihkan berkas dalam jumlah besar.

Sistem backup yang tepat sebaiknya memiliki versioning untuk mencegah mode kegagalan ini. Dengan menyediakan berbagai snapshot dalam waktu, seseorang dapat dengan mudah menelusurinya untuk memulihkan apa pun yang hilang. Perangkat lunak paling dikenal semacam ini adalah macOS Time Machine.

## Deduplication

Namun, membuat beberapa salinan data Anda bisa sangat mahal dalam hal ruang disk. Meskipun demikian, dari satu versi ke versi berikutnya, sebagian besar data akan identik dan tidak perlu ditransfer lagi. Di sinilah [data deduplication](https://en.wikipedia.org/wiki/Data_deduplication) berperan, dengan melacak apa yang sudah disimpan seseorang dapat melakukan **incremental backup** di mana hanya perubahan dari satu versi ke versi berikutnya yang perlu disimpan. Ini secara signifikan mengurangi jumlah ruang yang dibutuhkan untuk backup di luar salinan pertama.

## Enkripsi

Karena kita mungkin membackup ke pihak ketiga yang tidak tepercaya seperti penyedia cloud, ada baiknya mempertimbangkan bahwa jika Anda membackup, data Anda disalin *apa adanya* sehingga berpotensi dilihat oleh agen yang tidak diinginkan. Dokumen seperti pajak Anda adalah informasi sensitif yang sebaiknya tidak dibackup dalam format plain. Untuk mencegah ini, banyak solusi backup menawarkan **client side encryption** di mana data dienkripsi sebelum dikirim ke server. Dengan begitu server tidak dapat membaca data yang disimpannya tetapi Anda dapat mendekripsinya dengan secret key Anda.

Sebagai catatan tambahan, jika disk Anda (atau partisi home) tidak terenkripsi, maka siapa pun yang memperoleh komputer Anda dapat mengakali kontrol akses pengguna dan membaca data Anda. Perangkat keras modern mendukung baca dan tulis data terenkripsi yang cepat dan efisien sehingga Anda mungkin ingin mempertimbangkan mengaktifkan **full disk encryption**.


## Append only

Properti yang dibahas sejauh ini berfokus pada kegagalan perangkat keras atau kesalahan pengguna tetapi gagal menjawab apa yang terjadi jika agen berbahaya ingin menghapus data Anda. Yaitu, misalkan seseorang meretas sistem Anda, apakah mereka mampu menghapus semua salinan data yang Anda pedulikan? Jika Anda mengkhawatirkan skenario itu maka Anda memerlukan semacam solusi backup append only. Secara umum, ini berarti memiliki server yang memungkinkan Anda mengirim data baru tetapi menolak menghapus data yang ada. Biasanya pengguna memiliki dua key, key append only yang mendukung pembuatan backup baru dan key akses penuh yang juga memungkinkan penghapusan backup lama yang tidak lagi dibutuhkan. Yang terakhir disimpan offline.

Perhatikan bahwa ini adalah skenario yang cukup menantang karena Anda membutuhkan kemampuan membuat perubahan sekaligus mencegah pengguna berbahaya menghapus data Anda. Solusi komersial yang ada termasuk [Tarsnap](https://www.tarsnap.com/) dan [Borgbase](https://www.borgbase.com/).


## Pertimbangan tambahan

Beberapa hal lain yang mungkin ingin Anda telaah adalah:

- **Backup berkala**: backup yang sudah usang bisa menjadi tidak berguna. Melakukan backup secara rutin sebaiknya menjadi pertimbangan bagi sistem Anda
- **Bootable backup**: sebagian program memungkinkan Anda meng-clone seluruh disk. Dengan begitu Anda memiliki image yang memuat salinan lengkap sistem Anda dan dapat Anda boot langsung.
- **Strategi differential backup**, Anda belum tentu peduli sama besar pada semua data Anda. Anda dapat mendefinisikan kebijakan backup berbeda untuk jenis data berbeda.
- **Append only backup** pertimbangan tambahan adalah menegakkan operasi append only pada repositori backup Anda untuk mencegah agen berbahaya menghapusnya jika mereka memperoleh mesin Anda.


## Layanan web

Tidak semua data yang Anda gunakan berada di hard disk Anda. Jika Anda menggunakan **layanan web**, maka bisa jadi sebagian data yang Anda pedulikan, seperti presentasi Google Docs atau playlist Spotify, tersimpan daring. Contoh mudah lain yang mudah dilupakan adalah akun email dengan akses web, seperti Gmail. Mencari solusi backup dalam kasus ini agak lebih rumit. Namun, ada banyak layanan yang memungkinkan Anda mengunduh data Anda, baik secara langsung maupun melalui API. Tool seperti [gmvault](https://github.com/gaubert/gmvault) untuk Gmail tersedia untuk mengunduh berkas email ke komputer Anda.


## Halaman web

Demikian pula, sebagian konten berkualitas tinggi dapat ditemukan daring dalam bentuk halaman web. Jika konten tersebut statis, seseorang dapat dengan mudah membackupnya dengan sekadar menyimpan situs web dan semua lampirannya. Alternatif lain adalah [Wayback Machine](https://archive.org/web/), arsip digital besar World Wide Web yang dikelola [Internet Archive](https://archive.org/), organisasi nirlaba yang berfokus pada pelestarian segala macam media. Wayback Machine memungkinkan Anda menangkap dan mengarsipkan halaman web serta kemudian mengambil semua snapshot yang telah diarsipkan untuk situs web tersebut. Jika Anda merasa ini berguna, pertimbangkan [berdonasi](https://archive.org/donate/) ke proyek tersebut.


## Sumber daya

Beberapa program dan layanan backup yang baik yang pernah kami gunakan dan dapat kami rekomendasikan dengan jujur:

- [Tarsnap](https://www.tarsnap.com/) - layanan backup daring yang terdeduplikasi dan terenkripsi untuk yang benar-benar paranoid.
- [Borg Backup](https://borgbackup.readthedocs.io) - program backup terdeduplikasi yang mendukung kompresi dan authenticated encryption. Jika Anda membutuhkan penyedia cloud [BorgBase](https://www.borgbase.com/) adalah salah satu opsi populer.
- [rsync](https://rsync.samba.org/) adalah utilitas yang menyediakan transfer berkas inkremental yang cepat. Ini bukan solusi backup lengkap.
- [rclone](https://rclone.org/) seperti rsync tetapi untuk penyedia cloud storage seperti Amazon S3, Dropbox, Google Drive, rsync.net, &c. Mendukung client side encryption untuk folder remote.

## Latihan

1. Pertimbangkan bagaimana Anda (tidak) membackup data Anda dan telaah perbaikan/peningkatannya.

1. Cari tahu cara membackup akun email Anda

1. Pilih layanan web yang sering Anda gunakan (Spotify, Google Music, dsb.) dan cari tahu opsi apa yang tersedia untuk membackup data Anda. Sering kali orang sudah membuat tool (seperti [youtube-dl](https://ytdl-org.github.io/youtube-dl/)) solusi berdasarkan API yang tersedia.

1. Pikirkan situs web yang berulang kali Anda kunjungi selama bertahun-tahun dan cari di [archive.org](https://archive.org/web/), berapa versi yang dimilikinya?

1. Salah satu cara efisien mengimplementasikan deduplication adalah menggunakan hardlink. Symbolic link (juga disebut soft link atau symlink) adalah berkas yang menunjuk ke berkas atau folder lain, sedangkan hardlink adalah salinan persis dari pointer tersebut (menggunakan inode yang sama dan menunjuk ke tempat yang sama di disk). Dengan demikian jika berkas asli dihapus symlink berhenti berfungsi sedangkan hardlink tidak. Namun, hardlink hanya berfungsi untuk berkas. Coba gunakan perintah `ln` untuk membuat hardlink dan bandingkan dengan symlink yang dibuat dengan `ln -s`. (Di macOS Anda perlu memasang gnu coreutils atau paket hln).
