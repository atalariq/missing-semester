---
layout: lecture-id
title: "Version Control"
presenter: Jon
date: 2019-01-22
order: 2
video:
  aspect: 56.25
  id: 3fig2Vz8QXs
lang: id
permalink: /id/2019/version-control/
---

Setiap kali Anda mengerjakan sesuatu yang berubah seiring waktu, berguna
untuk dapat _melacak_ perubahan tersebut. Ini bisa karena beberapa
alasan: ini memberi Anda catatan tentang apa yang berubah, cara membatalkannya, siapa
yang mengubahnya, dan mungkin bahkan mengapa. Version control system (VCS) memberi
Anda kemampuan itu. VCS memungkinkan Anda _meng-commit_ perubahan pada sekumpulan berkas, beserta
pesan yang menjelaskan perubahan tersebut, serta melihat dan membatalkan
perubahan yang pernah Anda buat.

Sebagian besar VCS mendukung berbagi riwayat commit antar beberapa pengguna. Ini
memungkinkan kolaborasi yang praktis: Anda dapat melihat perubahan yang saya buat,
dan saya dapat melihat perubahan yang Anda buat. Dan karena VCS melacak
_perubahan_, VCS sering (meskipun tidak selalu) dapat mencari tahu cara menggabungkan
perubahan kita selama perubahan tersebut menyentuh hal yang relatif terpisah.

Ada [_banyak
sekali_](https://en.wikipedia.org/wiki/Comparison_of_version-control_software)
VCS di luar sana yang sangat berbeda dalam apa yang didukung, cara
berfungsinya, dan cara Anda berinteraksi dengannya. Di sini, kita akan memfokuskan pada
[git](https://git-scm.com/), salah satu yang lebih umum digunakan, tetapi saya
menyarankan Anda juga menelaah
[Mercurial](https://www.mercurial-scm.org/).

Dengan semua itu dikatakan -- mari ke ringkasannya!

## Apakah git itu sihir hitam?

tidak juga.. Anda perlu memahami data model-nya.
kita akan melewati beberapa detailnya, tetapi secara kasar,
"hal" _inti_ di git adalah commit.

 - setiap commit memiliki nama unik, "revision hash"
   hash panjang seperti `998622294a6c520db718867354bf98348ae3c7e2`
   sering dipendekkan menjadi prefiks pendek (cukup unik): `9986222`
 - commit memiliki author + pesan commit
 - juga memiliki hash dari _ancestor commit_ mana pun
   biasanya hanya hash dari commit sebelumnya
 - commit juga merepresentasikan sebuah _diff_, representasi bagaimana Anda beranjak dari
   ancestor commit ke commit itu (misalnya, hapus baris ini di
   berkas ini, tambahkan baris ini ke berkas ini, ganti nama berkas itu, dsb.)
   - pada kenyataannya, git menyimpan keadaan lengkap sebelum dan sesudah
   - mungkin Anda tidak ingin menyimpan berkas besar yang berubah!

awalnya, _repository_ (secara kasar: folder yang dikelola git) tidak
memiliki konten, dan tidak memiliki commit. mari siapkan itu:

```console
$ git init hackers
$ cd hackers
$ git status
```

output di sini sebenarnya memberi kita titik awal yang baik. mari selami
dan pastikan kita memahaminya semua.

pertama, "On branch master".

 - tidak ingin menggunakan hash sepanjang waktu.
 - branch adalah nama yang menunjuk ke hash.
 - master secara tradisional adalah nama untuk commit "terbaru".
   setiap kali commit baru dibuat, nama master akan dibuat
   menunjuk ke hash commit baru tersebut.
 - nama khusus `HEAD` merujuk nama "saat ini"
 - Anda juga dapat membuat nama sendiri dengan `git branch` (atau `git tag`)
   kita akan kembali ke itu

mari lewati "No commits yet" karena hanya itu isinya.

lalu, "nothing to commit".

 - setiap commit memuat diff dengan semua perubahan yang Anda buat.
   tetapi bagaimana diff itu dibangun pada awalnya?
 - _bisa_ selalu meng-commit _semua_ perubahan yang Anda buat sejak commit
   terakhir
   - kadang Anda ingin hanya meng-commit sebagiannya (misalnya, bukan `TODO`)
   - kadang Anda ingin memecah sebuah perubahan menjadi beberapa commit untuk
     memberikan pesan commit terpisah untuk masing-masing
 - git memungkinkan Anda _stage_ perubahan untuk membangun sebuah commit
   - tambahkan perubahan pada sebuah berkas atau beberapa berkas ke perubahan yang di-stage dengan `git add`
     - tambahkan hanya sebagian perubahan dalam sebuah berkas dengan `git add -p`
     - tanpa argumen `git add` beroperasi pada "semua berkas yang diketahui"
   - hapus sebuah berkas dan stage penghapusannya dengan `git rm`
   - kosongkan kumpulan perubahan yang di-stage `git reset`
     - perhatikan bahwa ini *tidak* mengubah berkas Anda!
       ini *hanya* berarti tidak ada perubahan yang akan disertakan dalam sebuah commit
     - untuk menghapus hanya sebagian perubahan yang di-stage:
       `git reset FILE` atau `git reset -p`
   - periksa perubahan yang di-stage dengan `git diff --staged`
   - lihat sisa perubahan dengan `git diff`
   - ketika Anda puas dengan stage-nya, buat commit dengan `git commit`
     - jika Anda hanya ingin meng-commit *semua* perubahan: `git commit -a`
     - `git help add` memiliki banyak info berguna lainnya

saat Anda bermain dengan di atas, coba jalankan `git status` untuk melihat apa yang menurut
git sedang Anda lakukan -- itu ternyata sangat membantu!

## Sebuah commit, katamu...

oke, kita punya commit, lalu bagaimana?

 - kita dapat melihat perubahan terkini: `git log` (atau `git log --oneline`)
 - kita dapat melihat perubahan lengkap: `git log -p`
 - kita dapat menampilkan commit tertentu: `git show master`
   - atau dengan `-p` untuk diff/patch lengkap
 - kita dapat kembali ke keadaan pada sebuah commit menggunakan `git checkout NAME`
   - jika `NAME` adalah hash commit, git mengatakan kita "detached". ini hanya
     berarti tidak ada `NAME` yang merujuk commit ini, jadi jika kita membuat
     commit, tidak ada yang akan mengetahuinya.
 - kita dapat membatalkan sebuah perubahan dengan `git revert NAME`
   - menerapkan diff pada commit di `NAME` secara terbalik.
 - kita dapat membandingkan versi lama dengan versi ini menggunakan `git diff NAME..`
   - `a..b` adalah _range_ commit. jika salah satu dihilangkan, itu berarti `HEAD`.
 - kita dapat menampilkan semua commit di antaranya menggunakan `git log NAME..`
   - `-p` juga berfungsi di sini
 - kita dapat mengubah `master` agar menunjuk ke commit tertentu (secara efektif
   membatalkan semua sejak itu) dengan `git reset NAME`:
   - hmm, mengapa? bukankah `reset` untuk mengubah perubahan yang di-stage?
     reset memiliki bentuk "kedua" (lihat `git help reset`) yang menetapkan `HEAD`
     ke commit yang ditunjuk nama yang diberikan.
   - perhatikan bahwa ini tidak mengubah berkas apa pun -- `git diff` sekarang
     secara efektif menampilkan `git diff NAME..`.

## Apa arti sebuah nama?

jelas, nama itu penting di git. dan nama adalah kunci untuk
memahami *banyak* dari apa yang terjadi di git. sejauh ini, kita telah membahas
hash commit, master, dan `HEAD`. tetapi ada lagi!

 - Anda dapat membuat branch sendiri (seperti master) dengan `git branch b`
   - membuat nama baru, `b`, yang menunjuk ke commit di `HEAD`
   - Anda masih "on" master, jadi jika Anda membuat commit baru,
     master akan menunjuk ke commit baru itu, `b` tidak.
   - beralih ke sebuah branch dengan `git checkout b`
     - commit apa pun yang Anda buat sekarang akan memperbarui nama `b`
     - beralih kembali ke master dengan `git checkout master`
       - semua perubahan Anda di `b` disembunyikan
     - cara yang sangat praktis untuk dapat dengan mudah menguji perubahan
 - tag adalah nama lain yang tidak pernah berubah, dan yang memiliki pesan
   sendiri. sering digunakan untuk menandai rilis + changelog.
 - `NAME^` berarti "commit sebelum `NAME`
   - dapat diterapkan secara rekursif: `NAME^^^`
   - Anda _kemungkinan besar_ bermaksud `~` ketika Anda menggunakan `~`
     - `~` bersifat "temporal", sedangkan `^` berjalan berdasarkan ancestor
     - `~~` sama dengan `^^`
     - dengan `~` Anda juga dapat menulis `X~3` untuk "3 commit lebih lama dari `X`
     - Anda tidak ingin `^3`
   - `git diff HEAD^`
 - `-` berarti "nama sebelumnya"
 - sebagian besar perintah beroperasi pada `HEAD` kecuali Anda memberikan argumen lain

## Rapikan kekacauan Anda

riwayat commit Anda _sangat_ sering akan berakhir sebagai:

 - `add feature x` -- bahkan mungkin dengan pesan commit tentang `x`!
 - `forgot to add file`
 - `fix bug`
 - `typo`
 - `typo2`
 - `actually fix`
 - `actually actually fix`
 - `tests pass`
 - `fix example code`
 - `typo`
 - `x`
 - `x`
 - `x`
 - `x`

itu _tidak masalah_ sejauh git peduli, tetapi tidak terlalu membantu bagi
diri Anda di masa depan, atau bagi orang lain yang penasaran tentang apa yang telah
berubah. git memungkinkan Anda merapikan hal-hal ini:

 - `git commit --amend`: melipat perubahan yang di-stage ke commit sebelumnya
   - perhatikan bahwa ini _mengubah_ commit sebelumnya, memberinya hash baru!
 - `git rebase -i HEAD~13` itu _ajaib_.
   untuk setiap commit dari 13 terakhir, pilih apa yang harus dilakukan:
   - defaultnya adalah `pick`; lakukan apa-apa
   - `r`: ubah pesan commit
   - `e`: ubah commit (tambah atau hapus berkas)
   - `s`: gabungkan commit dengan sebelumnya dan edit pesan commit
   - `f`: "fixup" -- gabungkan commit dengan sebelumnya; buang pesan commit
   - di akhir, `HEAD` dibuat menunjuk ke apa yang kini menjadi commit terakhir
   - sering disebut _squashing_ commit
   - apa yang sebenarnya dilakukan: memundurkan `HEAD` ke titik awal rebase, lalu
     menerapkan ulang commit sesuai urutan seperti yang diarahkan.
 - `git reset --hard NAME`: reset keadaan semua berkas ke keadaan
   `NAME` (atau `HEAD` jika tidak ada nama yang diberikan). berguna untuk membatalkan perubahan.

## Bermain dengan orang lain

use case umum untuk version control adalah memungkinkan beberapa orang
membuat perubahan pada sekumpulan berkas tanpa menginjak kaki satu sama lain.
atau lebih tepatnya, untuk memastikan bahwa _jika_ mereka menginjak kaki satu sama lain, mereka
tidak akan diam-diam menimpa perubahan satu sama lain.

git adalah VCS _terdistribusi_: setiap orang memiliki salinan lokal dari seluruh
repository (ya, dari semua yang telah dipilih orang lain untuk dipublikasikan). sebagian
VCS bersifat _terpusat_ (misalnya, subversion): server memiliki semua
commit, klien hanya memiliki berkas yang telah mereka "check out". pada dasarnya,
klien hanya memiliki berkas _saat ini_, dan perlu bertanya ke server jika mereka
menginginkan hal lain.

setiap salinan repository git dapat dicantumkan sebagai "remote". Anda dapat menyalin
repository git yang ada menggunakan `git clone ADDRESS` (alih-alih `git
init`). ini membuat remote bernama _origin_ yang menunjuk ke `ADDRESS`.
Anda dapat mengambil nama dan commit yang mereka tuju dari remote dengan
`git fetch REMOTE`. semua nama di remote tersedia bagi Anda sebagai
`REMOTE/NAME`, dan Anda dapat menggunakannya seperti nama lokal.

jika Anda memiliki akses tulis ke sebuah remote, Anda dapat mengubah nama di remote
agar menunjuk ke commit yang Anda buat menggunakan `git push`. misalnya, mari
buat nama master (branch) di remote `origin` menunjuk ke commit
yang saat ini ditunjuk branch master kita:

   - `git push origin master:master`
   - untuk kemudahan, Anda dapat menetapkan `origin/master` sebagai target default
     ketika Anda `git push` dari branch saat ini dengan `-u`
   - pertimbangkan: apa yang dilakukan ini? `git push origin master:HEAD^`

sering kali Anda akan menggunakan GitHub, GitLab, BitBucket, atau lainnya sebagai
remote Anda. tidak ada yang "istimewa" tentang itu sejauh git peduli.
semuanya hanya nama dan commit. jika seseorang membuat perubahan pada master dan
memperbarui `github/master` agar menunjuk ke commit mereka (kita akan kembali ke
itu sebentar lagi), maka ketika Anda `git fetch github`, Anda akan dapat
melihat perubahan mereka dengan `git log github/master`.

## Bekerja dengan orang lain

sejauh ini, branch tampak cukup tidak berguna: Anda dapat membuatnya, mengerjakan
padanya, tetapi lalu apa? pada akhirnya, Anda akan membuat master menunjuk ke sana
juga, kan?

 - bagaimana jika Anda harus memperbaiki sesuatu sambil mengerjakan fitur besar?
 - bagaimana jika orang lain membuat perubahan pada master sementara itu?

tak terhindarkan, Anda harus _merge_ perubahan di satu branch dengan perubahan
di branch lain, entah perubahan itu dibuat oleh Anda atau orang lain. git
memungkinkan Anda melakukan ini dengan, tidak mengherankan, `git merge NAME`. `merge` akan:

 - mencari titik terakhir di mana `HEAD` dan `NAME` berbagi sebuah commit
   ancestor (yaitu, di mana keduanya bercabang)
 - (mencoba) menerapkan semua perubahan tersebut ke `HEAD` saat ini
 - menghasilkan commit yang memuat semua perubahan tersebut, dan mencantumkan kedua
   `HEAD` dan `NAME` sebagai ancestor-nya
 - menetapkan `HEAD` ke hash commit tersebut

setelah fitur besar Anda selesai, Anda dapat merge branch-nya ke
master, dan git akan memastikan Anda tidak kehilangan perubahan apa pun dari kedua
branch!

jika Anda pernah menggunakan git sebelumnya, Anda mungkin mengenali `merge` dengan nama
berbeda: `pull`. ketika Anda melakukan `git pull REMOTE BRANCH`, itu sama dengan:

 - `git fetch REMOTE`
 - `git merge REMOTE/BRANCH`
 - di mana, seperti `push`, `REMOTE` dan `BRANCH` sering dihilangkan dan menggunakan
   remote branch "tracking" (ingat `-u`?)

ini biasanya bekerja _hebat_. selama perubahan pada branch yang di-merge
tidak tumpang tindih. jika tumpang tindih, Anda mendapatkan _merge conflict_. terdengar
menakutkan...

 - merge conflict hanyalah git memberi tahu Anda bahwa ia tidak tahu bagaimana
   diff akhirnya seharusnya
 - git berhenti dan meminta Anda menyelesaikan staging "merge commit"
 - buka berkas yang berkonflik di editor Anda dan cari banyak tanda kurung
   sudut (`<<<<<<<`). hal di atas `=======` adalah perubahan yang dibuat di
   `HEAD` sejak commit ancestor bersama. hal di bawahnya adalah
   perubahan yang dibuat di `NAME` sejak commit bersama tersebut.
 - `git mergetool` cukup praktis -- membuka diff editor
 - setelah Anda _menyelesaikan_ konflik dengan mencari tahu bagaimana berkas
   seharusnya terlihat sekarang, stage perubahan tersebut dengan `git add`.
 - ketika semua konflik terselesaikan, selesaikan dengan `git commit`
   - Anda dapat menyerah dengan `git merge --abort`

Anda baru saja menyelesaikan merge conflict git pertama Anda! \o/
sekarang Anda dapat mempublikasikan perubahan Anda yang sudah selesai dengan `git push`

## Ketika dunia bertabrakan

ketika Anda `push`, git memeriksa bahwa pekerjaan orang lain tidak hilang jika Anda
memperbarui nama remote yang Anda push. git melakukan ini dengan memeriksa
bahwa commit saat ini dari nama remote adalah ancestor dari commit
yang Anda push. jika ya, git dapat dengan aman hanya memperbarui nama; ini disebut
_fast-forwarding_. jika tidak, git akan menolak memperbarui
nama remote, dan memberi tahu Anda bahwa telah ada perubahan.

jika push Anda ditolak, apa yang Anda lakukan?

 - merge perubahan remote dengan `git pull` (yaitu `fetch` + `merge`)
 - paksa push dengan `--force`: ini akan menghilangkan perubahan orang lain!
   - ada juga `--force-with-lease`, yang hanya akan memaksa perubahan
     jika nama remote belum berubah sejak terakhir kali Anda fetch
     dari remote tersebut. jauh lebih aman!
   - jika Anda telah melakukan rebase pada commit lokal yang sebelumnya Anda push
     ("history rewriting"; mungkin jangan lakukan ini), Anda harus force
     push. pikirkan alasannya!
 - coba terapkan ulang perubahan Anda "di atas" perubahan yang dibuat di remote
   - ini adalah `rebase`!
     - mundurkan semua commit lokal sejak ancestor bersama
     - fast-forward `HEAD` ke commit di nama remote
     - terapkan commit lokal sesuai urutan
       - mungkin ada konflik yang harus Anda selesaikan secara manual
       - `git rebase --continue` atau `--abort`
     - lebih banyak [di sini](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
   - `git pull --rebase` akan memulai proses ini untuk Anda
   - apakah Anda sebaiknya merge atau rebase adalah topik hangat! beberapa bacaan bagus:
     - [ini](https://www.atlassian.com/git/tutorials/merging-vs-rebasing)
     - [ini](https://web.archive.org/web/20210106220723/https://derekgourlay.com/blog/git-when-to-merge-vs-when-to-rebase/)
     - [ini](https://stackoverflow.com/questions/804115/when-do-you-use-git-rebase-instead-of-git-merge)

# Bacaan lanjutan

[![XKCD tentang git](https://imgs.xkcd.com/comics/git.png)](https://xkcd.com/1597/)

 - [Learn git branching](https://learngitbranching.js.org/)
 - [How to explain git in simple words](https://smusamashah.github.io/blog/2017/10/14/explain-git-in-simple-words)
 - [Git from the bottom up](https://jwiegley.github.io/git-from-the-bottom-up/)
 - [Git for computer scientists](https://eagain.net/articles/git-for-computer-scientists/)
 - [Oh shit, git!](https://ohshitgit.com/)
 - [Buku Pro Git](https://git-scm.com/book/en/v2)

# Latihan

1. Pada sebuah repo coba modifikasi berkas yang sudah ada. Apa yang terjadi ketika Anda melakukan `git stash`? Apa yang Anda lihat saat menjalankan `git log --all --oneline`? Jalankan `git stash pop` untuk membatalkan apa yang Anda lakukan dengan `git stash`. Dalam skenario apa ini mungkin berguna?

1. Kesalahan umum saat mempelajari git adalah meng-commit berkas besar yang seharusnya tidak dikelola git atau menambahkan informasi sensitif. Coba tambahkan sebuah berkas ke repository, buat beberapa commit lalu hapus berkas tersebut dari riwayat (Anda mungkin ingin melihat [ini](https://help.github.com/articles/removing-sensitive-data-from-a-repository/)). Juga jika Anda memang ingin git mengelola berkas besar untuk Anda, telaah [Git-LFS](https://git-lfs.github.com/)

1. Git sangat praktis untuk membatalkan perubahan tetapi seseorang harus familiar bahkan dengan perubahan yang paling tidak mungkin
   1. Jika sebuah berkas keliru dimodifikasi di suatu commit, berkas itu dapat dikembalikan dengan `git revert`. Namun jika sebuah commit melibatkan beberapa perubahan `revert` mungkin bukan opsi terbaik. Bagaimana kita dapat menggunakan `git checkout` untuk memulihkan versi berkas dari commit tertentu?
   1. Buat sebuah branch, buat commit di branch tersebut lalu hapus branch itu. Dapatkah Anda masih memulihkan commit tersebut? Coba telaah `git reflog`. (Catatan: Pulihkan hal-hal dangling dengan cepat, git akan secara berkala otomatis membersihkan commit yang tidak ditunjuk apa pun.)
   1. Jika seseorang terlalu cepat menggunakan `git reset --hard` alih-alih `git reset`, perubahan dapat mudah hilang. Namun karena perubahannya telah di-stage, kita dapat memulihkannya. (telaah `git fsck --lost-found` dan `.git/lost-found`)

1. Di repo git mana pun lihat di bawah folder `.git/hooks` Anda akan menemukan sekumpulan skrip yang diakhiri `.sample`. Jika Anda mengganti namanya tanpa `.sample`, skrip akan berjalan berdasarkan namanya. Misalnya `pre-commit` akan dieksekusi sebelum melakukan commit. Bereksperimenlah dengannya

1. Seperti banyak tool command line, `git` menyediakan berkas konfigurasi (atau dotfile) bernama `~/.gitconfig` . Buat alias menggunakan `~/.gitconfig` sehingga ketika Anda menjalankan `git graph` Anda mendapatkan output `git log --oneline --decorate --all --graph` (ini perintah yang baik untuk dengan cepat memvisualisasikan commit graph)

1. Git juga memungkinkan Anda mendefinisikan pola ignore global di `~/.gitignore_global`, ini berguna untuk mencegah kesalahan umum seperti menambahkan RSA key. Buat berkas `~/.gitignore_global` dan tambahkan pola `*rsa`, lalu uji bahwa itu berfungsi di sebuah repo.

1. Setelah Anda mulai lebih familiar dengan `git`, Anda akan mendapati diri Anda menemui tugas umum, seperti mengedit `.gitignore` Anda. [git extras](https://github.com/tj/git-extras/blob/master/Commands.md) menyediakan banyak utilitas kecil yang terintegrasi dengan `git`. Misalnya `git ignore PATTERN` akan menambahkan pola yang ditentukan ke berkas `.gitignore` di repo Anda dan `git ignore-io LANGUAGE` akan mengambil pola ignore umum untuk bahasa tersebut dari [gitignore.io](https://www.gitignore.io). Pasang `git extras` dan coba gunakan beberapa tool seperti `git alias` atau `git ignore`.

1. Program GUI Git bisa menjadi sumber daya yang hebat kadang. Coba jalankan [gitk](https://git-scm.com/docs/gitk) di sebuah repo git dan jelajahi berbagai bagian antarmukanya. Lalu jalankan `gitk --all` apa perbedaannya?

1. Setelah terbiasa dengan aplikasi command line, tool GUI bisa terasa berat/membengkak. Kompromi yang baik antara keduanya adalah tool berbasis ncurses yang dapat dinavigasi dari command line dan tetap menyediakan antarmuka interaktif. Git memiliki [tig](https://github.com/jonas/tig), coba pasang dan jalankan di sebuah repo. Anda dapat menemukan beberapa contoh penggunaan [di sini](https://www.atlassian.com/blog/git/git-tig).


{% comment %}

 - forced push + `--force-with-lease`
 - git merge/rebase --abort
 - git blame
 - exercise about why rebasing public commits is bad

{% endcomment %}
