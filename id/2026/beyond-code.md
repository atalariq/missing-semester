---
layout: lecture-id
title: "Di Luar Kode"
description: >
  Pelajari soft skill penting, termasuk dokumentasi, norma komunitas open-source, dan etika menggunakan AI.
thumbnail: /static/assets/thumbnails/2026/lec8.png
date: 2026-01-22
ready: true
video:
  aspect: 56.25
  id: 2DOEATfXT8k
lang: id
permalink: /id/2026/beyond-code/
---

Menjadi software engineer yang baik bukan hanya soal menulis kode yang
berfungsi. Ini soal menulis kode yang dapat dipahami, dipelihara, dan
dikembangkan lebih lanjut oleh orang lain (termasuk diri Anda di masa depan). Ini soal
berkomunikasi dengan jelas, berkontribusi dengan penuh pertimbangan, dan menjadi warga yang baik dalam
ekosistem yang Anda ikuti—baik open source maupun proprietary.

# Komunikasi satu arah

Sebagian besar software engineering melibatkan penulisan untuk orang yang tidak memiliki
konteks Anda saat ini: rekan tim yang bergabung kemudian, maintainer yang mewarisi
kode Anda, atau diri Anda sendiri enam bulan kemudian ketika Anda telah lupa mengapa Anda
membuat pilihan tertentu. Satu nasihat kunci untuk semua penulisan semacam ini
adalah bahwa tujuan Anda adalah menangkap dan menyampaikan *mengapa*, bukan hanya
*apa*. Yang "apa" cenderung menjelaskan dirinya sendiri, sedangkan *mengapa* adalah
pengetahuan yang diperoleh dengan susah payah yang mudah hilang ditelan waktu.

Mungkin bentuk komunikasi engineer-ke-engineer yang paling umum
(selain kode itu sendiri) adalah komentar kode. Saya pribadi menemukan
bahwa banyak komentar kode tidak berguna. Tetapi komentar tidak harus begitu! Komentar
yang baik menjelaskan hal-hal yang tidak dapat dijelaskan kode itu sendiri: *mengapa* sesuatu
dilakukan dengan cara tertentu, bukan *bagaimana* hal itu bekerja (yang ditunjukkan
kode). Komentar dapat menghemat berjam-jam kebingungan, sedangkan komentar buruk menambah kebisingan
atau, lebih buruk lagi, menyesatkan.

Jenis komentar yang hampir selalu bermanfaat:

- **TODO**: Menandai kode yang belum selesai atau belum rapi, tetapi sisakan cukup
  konteks agar orang lain memahami apa yang belum selesai dan mengapa hal itu
  ditunda. "TODO: optimize" tidak berguna; "TODO: this O(n²) loop is
  fine for `n<100`, but will need indexing if we scale" dapat ditindaklanjuti.
- **Referensi**: Tautkan ke sumber eksternal ketika kode mengimplementasikan
  algoritma dari sebuah paper, mengadaptasi kode dari tempat lain, atau mengodekan
  perilaku yang ditentukan dalam dokumentasi. Gunakan permalink. Catat
  perbedaan apa pun dari referensinya.
- **Argumen kebenaran**: Jelaskan *mengapa* kode non-trivial menghasilkan
  hasil yang benar. Kode menunjukkan langkah-langkahnya; komentar menjelaskan mengapa
  langkah-langkah tersebut bekerja.
- **Pelajaran yang diperoleh dengan susah payah**: Jika Anda menghabiskan 30+ menit men-debug sesuatu
  dan perbaikannya adalah mantra yang tidak jelas, dokumentasikanlah. Diri Anda di masa lalu
  tidak menyadari hal itu diperlukan; pembaca di masa depan juga tidak akan menyadarinya.
- **Alasan untuk konstanta**: Magic number layak mendapat penjelasan. Mengapa
  1492? Mengapa 16 bit? Apakah dipilih secara acak, diturunkan dari pengujian, atau
  diperlukan untuk kebenaran? Bahkan "dipilih secara arbitrer" adalah informasi
  yang berguna.
- **Pilihan yang menopang beban**: Jika kebenaran bergantung pada
  detail implementasi yang tampak tidak berbahaya (misalnya, "harus berupa BTreeSet
  karena urutan iterasi penting di bawah ini"), sebutkan secara eksplisit.
- **"Mengapa tidak"**: Ketika Anda sengaja menghindari pendekatan yang jelas,
  jelaskan alasannya. Jika tidak, seseorang akan "memperbaikinya" nanti dan merusak sesuatu.

README (Anda punya satu, kan?) juga merupakan titik sentuh pertama yang umum dengan
pengembang lain. README yang baik langsung menjawab empat pertanyaan: Apa
fungsi proyek ini? Mengapa saya harus peduli? Bagaimana cara menggunakannya? Bagaimana cara memasangnya?
Dalam urutan itu. Susun seperti corong: satu baris ringkas dan mungkin
demo visual di bagian atas agar seseorang dapat memutuskan dalam hitungan detik apakah ini menyelesaikan
masalahnya, lalu tambahkan kedalaman secara bertahap. Tunjukkan penggunaan sebelum
instalasi — orang ingin melihat apa yang akan mereka dapatkan sebelum berkomitmen
pada langkah-langkah setup.

Pesan commit adalah jenis lain dari "menulis untuk orang lain" yang sering
diabaikan. Pesan commit sering ditulis sebagai "fixed blah" atau "added foo", dan
meskipun itu mungkin cukup dalam beberapa kasus, mudah untuk lupa bahwa
pesan tersebut membentuk catatan historis *mengapa* codebase berevolusi seperti
itu. Ketika seseorang (termasuk Anda!) menjalankan `git blame` untuk memahami
perubahan yang membingungkan, pesan commit yang baik seharusnya memberikan jawaban bagi mereka.

Secara umum, isi pesan harus menjawab:
- Masalah apa yang memaksa perubahan ini?
- Alternatif apa yang Anda pertimbangkan?
- Apa trade-off atau implikasinya?
- Apa yang mungkin mengejutkan tentang pendekatan ini?

> Tentu saja Anda harus menyesuaikan tingkat detail dengan kompleksitas. Perbaikan typo
> satu baris hanya memerlukan subjek. Perbaikan race condition halus yang memakan waktu berjam-jam untuk
> di-debug layak mendapat paragraf yang menjelaskan masalah dan solusinya.

Untuk perubahan yang kompleks, mengikuti struktur Masalah → Solusi →
Implikasi bisa berguna: Mulai dari pemicu perubahan atau keterbatasannya,
lalu jelaskan apa yang berubah dan keputusan desain kuncinya, dan kemudian daftarkan
konsekuensi penting (positif dan negatif). Bagian terakhir itu
sangat penting; engineering nyata melibatkan penyeimbangan berbagai pertimbangan,
dan mendokumentasikan bahwa sebuah trade-off memang disengaja mencegah pengembang di masa depan
mengira Anda melewatkan masalahnya.

LLM _dapat_ membantu dalam menulis pesan commit. Namun, jika Anda hanya
mengarahkannya ke perubahan Anda dan memintanya menulis pesan commit untuk
perubahan tersebut, LLM hanya akan memiliki akses ke _apa_, bukan _mengapa_. Dan
pesan commit yang dihasilkan akan sebagian besar bersifat deskriptif (kebalikan
dari yang kita inginkan!). Jika Anda menggunakan LLM untuk membantu Anda membuat
perubahan tersebut sejak awal, meminta LLM menulis pesan commit dalam
sesi yang sama bisa menjadi pilihan yang jauh lebih baik karena percakapan Anda dengan
LLM secara inheren merupakan sumber konteks yang kaya tentang perubahan tersebut!
Jika tidak, atau sebagai tambahan, trik yang berguna adalah secara spesifik memberi tahu
LLM bahwa Anda menginginkan pesan commit yang berfokus pada "mengapa" (dan nuansa lain
dari catatan di atas), lalu _memintanya menanyakan kepada Anda konteks yang hilang_.
Pada dasarnya, Anda berperan seperti "tool" MCP bagi coding
agent yang dapat digunakannya untuk "membaca" konteks.

Seiring perubahan Anda menjadi lebih kompleks, pastikan juga memecah commit secara
logis (`git add -p` adalah teman Anda). Setiap commit harus merepresentasikan
satu perubahan yang koheren yang dapat dipahami dan ditinjau secara independen.
Jangan mencampur refactoring dengan fitur baru atau menggabungkan perbaikan bug yang tidak terkait,
karena ini mengaburkan cerita tentang perubahan mana yang memperbaiki masalah apa, dan hampir
pasti akan memperlambat peninjauan akhir perubahan Anda. Ini juga
memberi Anda kekuatan super melalui `git bisect`, tetapi itu cerita untuk
lain waktu.

> Satu catatan saat Anda mulai lebih tekun dalam technical writing, dan
> menggunakannya secara lebih luas, pastikan Anda menghormati pembaca. Mudah
> untuk akhirnya menjelaskan secara berlebihan setelah Anda mulai, tetapi Anda harus menahan
> dorongan itu agar pembaca tidak sampai mengabaikan _seluruh_ tulisan Anda. Jelaskan
> "mengapa" dan percayakan kepada mereka untuk mencari tahu "bagaimana" untuk situasi mereka.

# Kolaborasi

Sebagai engineer, kita mungkin menghabiskan sebagian besar pekerjaan kita menulis kode di keyboard
kita sendiri, tetapi porsi yang cukup besar dari waktu kita juga terpakai untuk
berkomunikasi dengan orang lain. Waktu itu biasanya terbagi menjadi kolaborasi
dan edukasi, dan manfaat dari berinvestasi untuk menjadi lebih baik dalam keduanya
signifikan.

## Berkontribusi

Baik Anda mengirim laporan bug, berkontribusi perbaikan bug sederhana,
atau mengimplementasikan fitur besar, ada baiknya mengingat bahwa
biasanya jumlah pengguna beberapa orde lebih banyak daripada jumlah kontributor,
dan jumlah kontributor satu orde lebih banyak daripada jumlah maintainer.
Akibatnya, waktu maintainer sangat oversubscribed. Jika Anda ingin
meningkatkan kemungkinan kontribusi Anda menghasilkan sesuatu
produktif, Anda harus memastikan kontribusi Anda membawa rasio signal-to-noise yang tinggi
dan layak untuk waktu maintainer.

Misalnya, laporan bug yang baik menghormati waktu maintainer dengan
menyediakan semua yang diperlukan untuk memahami dan mereproduksi masalah:

- **Environment**: OS, nomor versi, konfigurasi yang relevan
- **Apa yang Anda harapkan** vs **apa yang sebenarnya terjadi**
- **Langkah-langkah untuk mereproduksi**: Spesifiklah. "Klik tombol" kurang berguna
  daripada "Klik tombol Submit di halaman /settings saat login sebagai
  admin."
- **Apa yang sudah Anda coba**: Ini mencegah saran duplikat dan
  menunjukkan Anda telah melakukan investigasi

> Jika Anda menemukan kerentanan keamanan, jangan mempostingnya secara publik. Hubungi
> maintainer secara privat terlebih dahulu dan beri mereka waktu yang wajar untuk memperbaikinya
> sebelum pengungkapan. Banyak proyek memiliki berkas SECURITY.md atau
> serupa untuk tujuan ini.

**Pastikan Anda mencari issue yang sudah ada.** Bug atau permintaan fitur Anda
mungkin sudah dilaporkan, dan jauh lebih baik menambahkan informasi
ke diskusi yang ada daripada membuat duplikat. Belum lagi,
ini mengurangi kebisingan bagi maintainer.

Contoh reproduksi minimal adalah emas, jika Anda dapat membuatnya.
Contoh tersebut menghemat banyak waktu dan usaha maintainer, dan
mereproduksi bug secara andal sering kali menjadi bagian tersulit dalam memperbaikinya. Belum
lagi, usaha yang Anda curahkan untuk mengisolasi masalah sering membantu
Anda memahaminya lebih baik juga, dan kadang mengarahkan Anda menemukan perbaikannya
sendiri.

Jika Anda tidak segera menerima balasan, ingatlah bahwa maintainer sering
merupakan sukarelawan dengan waktu terbatas. Jika Anda menunggu balasan dari
mereka, tindak lanjut sopan setelah beberapa minggu tidak masalah; ping setiap hari
tidak. Demikian pula, komentar "me too", atau laporan bug yang hanya
salin-tempel beberapa output terminal cenderung berdampak negatif dalam hal
mendapatkan respons untuk issue Anda.

Jika Anda ingin berkontribusi kode, Anda juga perlu
membiasakan diri dengan panduan kontribusi. Banyak proyek
memiliki `CONTRIBUTING.md` — ikuti itu. Anda juga biasanya ingin memulai
dari hal kecil; perbaikan typo atau peningkatan dokumentasi adalah kontribusi pertama yang bagus
karena membantu Anda mempelajari proses proyek tanpa juga
harus melalui banyak bolak-balik tentang kontennya.

> Periksa lisensi apa yang digunakan proyek, karena kode apa pun yang Anda kontribusikan akan
> tunduk pada lisensi yang sama. Secara khusus, waspadai lisensi copyleft
> (seperti GPL), yang mewajibkan karya turunan juga open source
> dan mungkin memiliki implikasi bagi perusahaan Anda jika Anda menyentuhnya!
> [choosealicense.com](https://choosealicense.com/) memiliki informasi yang lebih berguna.

Ketika Anda memutuskan untuk membuka pull request ("PR"), pertama pastikan Anda
mengisolasi perubahan yang benar-benar ingin Anda diterima. Jika PR Anda mengubah
banyak hal lain yang tidak terkait pada saat yang sama, kemungkinan besar
reviewer akan mengembalikannya kepada Anda dan meminta Anda merapikannya. Ini
serupa dengan cara Anda sebaiknya memecah commit git Anda menjadi potongan-potongan yang
terkait secara semantik.

Dalam beberapa kasus, jika Anda memiliki banyak perubahan yang tampaknya berbeda tetapi
semuanya diperlukan untuk mengaktifkan satu fitur, mungkin tidak masalah membuka
PR yang lebih besar yang mencakup semua perubahannya. Namun, dalam kasus ini, kebersihan
commit terutama penting agar maintainer memiliki pilihan
untuk meninjau perubahan tersebut "commit per commit".

Selanjutnya, pastikan Anda menjelaskan "mengapa" di balik perubahan itu dengan baik. Jangan hanya
menjelaskan _apa_ yang berubah — jelaskan _mengapa_ perubahan itu diperlukan dan _mengapa_
ini cara yang baik untuk mengatasi masalahnya. Anda juga sebaiknya secara proaktif
menyebutkan bagian perubahan yang memerlukan perhatian khusus dalam
peninjauan, jika ada. Bergantung pada `CONTRIBUTING.md` dan sifat
perubahan Anda, reviewer mungkin juga mengharapkan informasi tambahan seperti
trade-off yang Anda buat atau cara menguji perubahannya.

> Kami menyarankan berkontribusi kembali ke proyek upstream alih-alih
> "fork" proyeknya, setidaknya sebagai pendekatan pertama. Melakukan fork (jika
> lisensi mengizinkan) sebaiknya disimpan untuk kasus ketika kontribusi yang ingin
> Anda buat berada di luar cakupan proyek asli. Jika Anda benar-benar melakukan fork, pastikan
> Anda mengakui proyek aslinya!

AI membuatnya sangat mudah untuk menghasilkan kode dan PR yang tampak masuk akal
dengan cepat, tetapi ini tidak membebaskan Anda dari memahami apa yang Anda
kontribusikan. Mengirim kode hasil AI yang tidak dapat Anda jelaskan membebani
maintainer dengan peninjauan dan berpotensi pemeliharaan kode yang bahkan
penulisnya tidak memahami. Tidak masalah menggunakan AI untuk membantu Anda
mengidentifikasi masalah dan menghasilkan perbaikan/fitur, **asalkan Anda tetap melakukan
uji tuntas** untuk memolesnya menjadi kontribusi yang layak, alih-alih
memindahkan pekerjaan itu kepada maintainer (yang sudah kelebihan beban).

Ingatlah bahwa bagi maintainer, menerima PR berarti menerima tanggung jawab
jangka panjang. Mereka akan memelihara kode ini jauh setelah
kontributor beranjak, sehingga mereka mungkin menolak perubahan yang
berniat baik tetapi tidak sesuai dengan arah proyek, menambah kompleksitas
yang tidak ingin mereka pelihara, atau ketika kebutuhannya tidak cukup
terdokumentasi dengan baik. Ini menjadi tugas _Anda_ sebagai kontributor untuk membangun argumen
mengapa menerima kontribusi tersebut layak atas beban pemeliharaannya.

> Saat menerima umpan balik pada PR, ingatlah bahwa kode Anda bukanlah diri Anda!
> Reviewer berusaha membuat kode menjadi lebih baik, bukan mengkritik Anda
> secara pribadi. Ajukan pertanyaan klarifikasi jika Anda tidak setuju — Anda mungkin belajar
> sesuatu, atau mungkin mereka juga.

## Meninjau

Anda mungkin berpikir code review adalah sesuatu yang dilakukan pengembang senior, tetapi
Anda kemungkinan akan diminta meninjau kode jauh lebih awal dari yang Anda duga, dan
perspektif Anda berharga. Mata yang segar menangkap hal-hal yang terlewat oleh pengembang
berpengalaman, dan pertanyaan dari orang yang kurang akrab dengan
kode sering mengungkap asumsi yang seharusnya didokumentasikan atau disederhanakan.

Review juga salah satu cara tercepat untuk belajar. Anda akan melihat bagaimana orang lain
mendekati masalah, memungut pola dan idiom, dan mengembangkan intuisi
tentang apa yang membuat kode mudah dibaca. Selain pertumbuhan pribadi, review menangkap bug
sebelum mencapai produksi, menyebarkan pengetahuan ke seluruh tim, dan
meningkatkan kualitas kode melalui kolaborasi. Review bukan sekadar
beban birokrasi.

Code review yang baik adalah keterampilan yang perlu Anda asah seiring waktu, tetapi ada
beberapa tip yang dapat membuatnya jauh lebih baik jauh lebih cepat:

- **Tinjau kodenya, bukan orangnya**:
  "Fungsi ini membingungkan" vs "Anda menulis kode yang membingungkan."
- **Utamakan komentar yang dapat ditindaklanjuti**:
  "Bisakah Anda mengganti global ini dengan config dataclass" adalah komentar
  yang lebih mudah ditangani daripada "Jangan gunakan global di sini"
- **Ajukan pertanyaan alih-alih menuntut**:
  "Apa yang terjadi jika X bernilai null di sini?" mengundang diskusi lebih baik daripada
  "Tangani kasus null."
- **Jelaskan "mengapa"**:
  "Pertimbangkan menggunakan konstanta di sini" kurang berguna daripada "Pertimbangkan menggunakan
  konstanta di sini agar kita dapat dengan mudah menyesuaikan timeout berdasarkan
  environment."
- **Bedakan masalah yang memblokir dari saran**:
  Bersikap jelas tentang apa yang harus berubah versus apa yang hanya soal preferensi.
- **Akui apa yang bagus**:
  Menunjukkan solusi cerdas atau implementasi yang bersih itu menyemangati
  dan membantu penulis mengetahui apa yang harus terus dilakukan.
- **Ketahui kapan harus berhenti**:
  Kontributor hanya memiliki waktu dan kesabaran tertentu, dan tidak selalu
  paling baik dihabiskan untuk menangani semua nit. Fokus pada hal-hal besar, dan
  pertimbangkan merapikan nit sendiri setelahnya.

> Tool AI dapat menangkap masalah tertentu, tetapi tool tersebut bukan pengganti
> review manusia. Tool AI melewatkan konteks, tidak memahami kebutuhan
> produk, dan dapat dengan yakin menyarankan hal yang salah. Tool tersebut layak
> digunakan sebagai pemeriksaan pertama, tetapi bukan pengganti review manusia
> yang penuh pertimbangan.

# Pendidikan

Banyak waktu non-coding kita sebagai engineer dihabiskan untuk mengajukan atau
menjawab pertanyaan, mungkin campuran keduanya; selama kolaborasi,
dalam dialog dengan rekan, atau saat mencoba belajar. Mengajukan pertanyaan yang baik
adalah keterampilan yang membuat Anda lebih baik dalam belajar dari siapa pun, bukan hanya dari
penjelas yang sempurna. Julia Evans memiliki beberapa posting blog yang sangat baik tentang "[How
to ask good questions](https://jvns.ca/blog/good-questions/)" dan "[How
to get useful answers to your
questions](https://jvns.ca/blog/2021/10/21/how-to-get-useful-answers-to-your-questions/)"
yang layak dibaca.

Beberapa nasihat yang sangat berharga adalah:

- **Nyatakan pemahaman Anda lebih dulu**: Katakan apa yang menurut Anda Anda ketahui dan
  tanyakan "apakah itu benar?" Ini membantu penjawab mengidentifikasi celah pengetahuan
  Anda yang sebenarnya.
- **Ajukan pertanyaan ya/tidak**: "Apakah X benar?" mencegah penjelasan
  yang melenceng dan biasanya tetap memicu penjelasan tambahan yang berguna.
- **Spesifiklah**: "Bagaimana cara kerja SQL join?" terlalu kabur. "Apakah LEFT
  JOIN menyertakan baris ketika tabel kanan tidak memiliki kecocokan?" dapat dijawab.
- **Akui ketika Anda tidak memahami**: Interupsi untuk bertanya tentang istilah
  yang tidak familiar. Ini mencerminkan kepercayaan diri, bukan kelemahan. Demikian pula, jika mereka mengajukan
  pertanyaan kepada Anda yang tidak Anda ketahui jawabannya, sebaiknya katakan
  "Saya tidak tahu", dan mungkin lanjutkan dengan "tetapi saya rasa ..." atau bahkan
  "tetapi saya dapat mencarinya".
- **Jangan menerima jawaban yang tidak lengkap**: Terus ajukan tindak lanjut sampai Anda
  benar-benar memahami.
- **Lakukan riset terlebih dahulu**: Investigasi dasar membantu Anda mengajukan
  pertanyaan yang lebih terarah (meskipun pertanyaan santai di antara kolega
  tidak masalah).

Ingat: pertanyaan yang dirumuskan dengan baik bermanfaat bagi seluruh komunitas. Pertanyaan itu
mengungkap asumsi tersembunyi yang juga perlu dipahami orang lain.

> Perhatikan bahwa nasihat ini berlaku sama besarnya saat berkomunikasi dengan
> LLM!

# Etika Menggunakan AI

Dengan meningkatnya penggunaan LLM dan AI di seluruh software engineering, norma
sosial dan profesional di sekitarnya masih berubah. Kita telah
membahas banyak pertimbangan taktis pada [kuliah agentic
coding](/2026/agentic-coding/), tetapi ada juga bagian yang lebih "lunak" dari
penggunaannya yang layak didiskusikan.

Yang pertama adalah ketika AI berkontribusi secara berarti pada pekerjaan Anda,
**ungkapkanlah**. Ini bukan soal rasa malu — ini soal kejujuran,
menetapkan ekspektasi yang sesuai, dan memastikan pekerjaan yang dihasilkan mendapat
tingkat peninjauan yang sesuai. Ada baiknya juga mengungkapkan _bagian_ mana
yang Anda gunakan AI di dalamnya — ada perbedaan yang berarti antara "seluruh
hal ini di-vibecode" dan "saya menulis tool backup ini dan menggunakan LLM
untuk menata gaya frontend web-nya". Misalnya, kami telah menggunakan LLM untuk membantu menulis
sebagian catatan kuliah ini, termasuk proofreading, brainstorming, dan
menghasilkan draf pertama potongan kode dan latihan.

Anda juga perlu mengikuti norma tim dan proyek yang Anda
kontribusikan di sini. Sebagian tim memiliki kebijakan yang lebih ketat terkait penggunaan
AI daripada yang lain (misalnya, untuk alasan kepatuhan atau data residency), dan
Anda tidak ingin tanpa sengaja melanggarnya. Bersikap terbuka tentang
penggunaan Anda membantu mencegah kesalahan yang berpotensi mahal.

> Jika Anda bertujuan belajar sebagai bagian dari pekerjaan yang Anda lakukan, ingatlah
> bahwa jika Anda membiarkan AI melakukan semua atau sebagian besar pekerjaan untuk Anda, itu bisa
> merugikan diri sendiri; Anda kemungkinan akan lebih banyak belajar tentang prompting (dan mungkin
> meninjau output AI) daripada tentang tugas itu sendiri. Terutama ketika Anda
> belajar, intinya mungkin adalah perjalanan, bukan tujuannya, sehingga menggunakan
> AI untuk "mendapatkan solusi dengan cepat" adalah anti-tujuan.

Kekhawatiran terkait muncul dalam wawancara dan situasi penilaian lainnya. Situasi tersebut
sering dimaksudkan untuk secara khusus mengevaluasi keterampilan dan kemampuan _Anda_,
bukan kemampuan LLM. Lebih banyak perusahaan sekarang mengizinkan
Anda menggunakan LLM dan tooling berbantuan AI lain dalam wawancara asalkan Anda
membiarkan mereka mengamati interaksi tersebut sebagai bagian dari wawancara (yakni, mereka
juga mengevaluasi keterampilan Anda dalam memanfaatkan tool tersebut!), tetapi itu
masih minoritas. Jika Anda tidak yakin apakah bantuan AI
termasuk dalam cakupan tugas tertentu, tanyakan!

> Tidak perlu dikatakan bahwa jika situasi penilaian secara eksplisit
> mengharuskan tidak ada tool eksternal, tidak ada LLM, dan sebagainya, Anda tidak boleh menggunakannya.
> Mencoba melakukannya secara diam-diam tanpa ketahuan **akan** kembali
> merugikan Anda.

# Latihan

1. Telusuri kode sumber proyek terkenal (misalnya,
   [Redis](https://github.com/redis/redis) atau
   [curl](https://github.com/curl/curl)). Temukan contoh beberapa jenis
   komentar yang disebutkan dalam kuliah: TODO yang berguna, referensi ke
   dokumentasi eksternal, komentar "mengapa tidak" yang menjelaskan pendekatan yang dihindari,
   atau pelajaran yang diperoleh dengan susah payah. Apa yang akan hilang jika komentar
   itu tidak ada?

1. Pilih proyek open-source yang Anda minati dan lihat riwayat commit
   terbarunya (`git log`). Temukan satu commit dengan pesan yang baik
   yang menjelaskan *mengapa* perubahan itu dibuat, dan satu dengan pesan yang lemah
   yang hanya menjelaskan *apa* yang berubah. Untuk yang lemah, lihat
   diff-nya (`git show <hash>`) dan coba tulis pesan commit yang lebih baik
   mengikuti struktur Masalah → Solusi → Implikasi. Perhatikan betapa
   banyak usaha yang diperlukan untuk menyusun ulang konteks yang diperlukan setelah
   kejadian!

1. Bandingkan README tiga proyek GitHub dengan 1000+ bintang. Apakah
   semuanya sama-sama berguna? Carilah hal-hal yang menurut Anda sebagian besar
   hanya menjadi kebisingan, sebagai pelajaran untuk README yang akan Anda tulis sendiri.

1. Temukan issue terbuka pada proyek yang Anda gunakan (periksa label "good first issue"
   atau "help wanted" jika tersedia). Evaluasi issue tersebut terhadap
   kriteria dari kuliah: apakah issue itu tampak menghargai waktu
   maintainer dan memuat semua informasi yang diperlukan untuk men-debug-nya, atau apakah Anda menduga
   maintainer mungkin perlu melalui beberapa putaran pertanyaan dengan pengirim
   untuk sampai ke akar masalahnya?

1. Pikirkan bug yang pernah Anda temui dalam perangkat lunak yang Anda gunakan (atau temukan satu di
   issue tracker). Berlatihlah membuat contoh reproduksi minimal:
   singkirkan semua yang tidak terkait dengan bug sampai Anda memiliki
   kasus terkecil yang masih menunjukkan masalahnya. Tuliskan apa yang Anda
   hapus dan alasannya.

1. Temukan pull request yang sudah di-merge pada proyek yang Anda kenal yang memiliki
   komentar review substantif (bukan hanya "LGTM"). Bacalah
   review-nya. Apakah semua komentar sama produktifnya? Jika Anda adalah penulis PR,
   bagaimana pengalaman Anda menerima semua komentar tersebut?

1. Kunjungi Stack Overflow dan temukan pertanyaan dalam teknologi yang Anda ketahui
   yang memiliki jawaban dengan banyak upvote. Lalu temukan satu yang ditutup atau
   banyak di-downvote. Bandingkan keduanya dengan nasihat dari kuliah;
   apakah dapat diprediksi pertanyaan mana yang akan mendapat jawaban lebih baik?
