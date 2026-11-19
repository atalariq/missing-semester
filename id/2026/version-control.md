---
layout: lecture-id
title: "Version Control dan Git"
description: >
  Pelajari data model Git dan cara menggunakan Git untuk version control dan kolaborasi.
thumbnail: /static/assets/thumbnails/2026/lec5.png
date: 2026-01-16
ready: true
video:
  aspect: 56.25
  id: 9K8lB61dl3Y
lang: id
permalink: /id/2026/version-control/
---

Version control system (VCS) adalah tool yang digunakan untuk melacak perubahan pada kode sumber
(atau kumpulan berkas dan folder lainnya). Seperti namanya, tool ini
membantu memelihara riwayat perubahan; lebih jauh lagi, tool ini memudahkan kolaborasi.
Secara logis, VCS melacak perubahan pada sebuah folder dan isinya dalam rangkaian
_snapshot_, di mana setiap snapshot merangkum seluruh keadaan berkas/folder
di dalam sebuah direktori tingkat atas. VCS juga memelihara metadata seperti siapa yang membuat setiap
snapshot, pesan yang terkait dengan setiap snapshot, dan seterusnya.

Mengapa version control berguna? Bahkan ketika Anda bekerja sendiri, version control memungkinkan
Anda melihat snapshot lama sebuah proyek, menyimpan catatan mengapa perubahan tertentu
dilakukan, bekerja pada branch pengembangan paralel, dan banyak lagi. Saat bekerja
dengan orang lain, version control adalah tool yang sangat berharga untuk melihat apa yang telah diubah orang lain,
serta menyelesaikan konflik dalam pengembangan bersamaan.

VCS modern juga memungkinkan Anda menjawab pertanyaan berikut dengan mudah (dan sering kali otomatis)
seperti:

- Siapa yang menulis module ini?
- Kapan baris tertentu dari berkas tertentu ini diedit? Oleh siapa? Mengapa
  baris itu diedit?
- Selama 1000 revisi terakhir, kapan/mengapa sebuah unit test tertentu berhenti
  bekerja?

Meskipun VCS lain ada, **Git** adalah standar de facto untuk version control.
[Komik XKCD ini](https://xkcd.com/1597/) menangkap reputasi Git:

![xkcd 1597](https://imgs.xkcd.com/comics/git.png)

Karena antarmuka Git adalah abstraksi yang bocor, mempelajari Git secara top-down (dimulai
dari antarmuka / command-line interface-nya) dapat menimbulkan banyak kebingungan.
Ada kemungkinan untuk menghafal beberapa perintah dan menganggapnya sebagai mantra
ajaib, lalu mengikuti pendekatan pada komik di atas setiap kali ada yang
salah.

Meskipun diakui antarmuka Git jelek, desain dan gagasan di baliknya
indah. Antarmuka yang jelek harus _dihafal_, sedangkan desain yang indah
dapat _dipahami_. Karena alasan ini, kami memberikan penjelasan Git secara bottom-up,
dimulai dari data model-nya dan kemudian membahas command-line interface-nya.
Setelah data model dipahami, perintah-perintahnya dapat lebih dipahami dalam
kaitannya dengan cara perintah tersebut memanipulasi data model di baliknya.

# Data Model Git

Kecerdikan Git terletak pada data model-nya yang dirancang dengan baik yang memungkinkan semua
fitur version control yang bagus, seperti memelihara riwayat, mendukung branch, dan
memungkinkan kolaborasi.

## Snapshots

Git memodelkan riwayat sekumpulan berkas dan folder di dalam sebuah
direktori tingkat atas sebagai rangkaian snapshot. Dalam terminologi Git, sebuah berkas
disebut "blob", dan blob hanyalah sekumpulan byte. Sebuah direktori disebut
"tree", dan tree memetakan nama ke blob atau tree (sehingga direktori dapat berisi
direktori lain). Sebuah snapshot adalah tree tingkat atas yang dilacak. Misalnya,
kita mungkin memiliki tree sebagai berikut:

```
<root> (tree)
|
+- foo (tree)
|  |
|  + bar.txt (blob, contents = "hello world")
|
+- baz.txt (blob, contents = "git is wonderful")
```

Tree tingkat atas berisi dua elemen, sebuah tree "foo" (yang sendiri berisi
satu elemen, sebuah blob "bar.txt"), dan sebuah blob "baz.txt".

## Memodelkan Riwayat: Menghubungkan Snapshot

Bagaimana seharusnya sebuah version control system menghubungkan snapshot? Salah satu model sederhana adalah
memiliki riwayat linear. Sebuah riwayat akan menjadi daftar snapshot dalam urutan waktu.
Karena banyak alasan, Git tidak menggunakan model sesederhana itu.

Di Git, sebuah riwayat adalah directed acyclic graph (DAG) dari snapshot. Itu mungkin
terdengar seperti istilah matematika yang keren, tetapi jangan merasa terintimidasi. Semua ini berarti bahwa
setiap snapshot di Git merujuk pada sekumpulan "parent", yaitu snapshot yang mendahuluinya.
Ini adalah sekumpulan parent, bukan satu parent tunggal (seperti yang akan terjadi pada
riwayat linear) karena sebuah snapshot mungkin berasal dari beberapa parent, misalnya
karena menggabungkan (merge) dua branch pengembangan paralel.

Git menyebut snapshot ini "commit". Memvisualisasikan riwayat commit mungkin terlihat
seperti ini:

```
o <-- o <-- o <-- o
            ^
             \
              --- o <-- o
```

Pada ASCII art di atas, setiap `o` bersesuaian dengan commit individual (snapshot).
Panah menunjuk ke parent setiap commit (ini adalah relasi "comes before",
bukan "comes after"). Setelah commit ketiga, riwayat bercabang menjadi dua
branch terpisah. Ini mungkin bersesuaian dengan, misalnya, dua fitur terpisah
yang dikembangkan secara paralel, independen satu sama lain. Di masa depan,
branch ini mungkin di-merge untuk membuat snapshot baru yang memadukan kedua
fitur tersebut, menghasilkan riwayat baru yang terlihat seperti ini, dengan
merge commit yang baru dibuat ditampilkan dalam huruf tebal:

<pre class="highlight">
<code>
o <-- o <-- o <-- o <---- <strong>o</strong>
            ^            /
             \          v
              --- o <-- o
</code>
</pre>

Commit di Git bersifat immutable. Ini tidak berarti kesalahan tidak dapat
diperbaiki; hanya saja "edit" pada riwayat commit sebenarnya
membuat commit yang sepenuhnya baru, dan reference (lihat di bawah) diperbarui agar menunjuk
ke commit yang baru tersebut.

## Data model, sebagai pseudocode

Mungkin bermanfaat untuk melihat data model Git dituliskan dalam pseudocode:

```
// a file is a bunch of bytes
type blob = array<byte>

// a directory contains named files and directories
type tree = map<string, tree | blob>

// a commit has parents, metadata, and the top-level tree
type commit = struct {
    parents: array<commit>
    author: string
    message: string
    snapshot: tree
}
```

Itu adalah model riwayat yang bersih dan sederhana.

## Object dan Content-addressing

Sebuah "object" adalah blob, tree, atau commit:

```
type object = blob | tree | commit
```

Dalam data store Git, semua object dialamatkan berdasarkan kontennya melalui [hash
SHA-1](https://en.wikipedia.org/wiki/SHA-1).

```
objects = map<string, object>

def store(object):
    id = sha1(object)
    objects[id] = object

def load(id):
    return objects[id]
```

Blob, tree, dan commit disatukan dengan cara ini: semuanya adalah object. Ketika
satu object merujuk object lain, object tersebut tidak benar-benar _memuat_ object lain itu dalam
representasi on-disk-nya, tetapi memiliki referensi ke object tersebut melalui hash-nya.

Misalnya, tree untuk struktur direktori contoh [di atas](#snapshots)
(ditampilkan menggunakan `git cat-file -p 698281bc680d1995c5f4caaf3359721a5a58d48d`),
terlihat seperti ini:

```
100644 blob 4448adbf7ecd394f42ae135bbeed9676e894af85    baz.txt
040000 tree c68d233a33c5c06e0340e4c224f0afca87c8ce87    foo
```

Tree itu sendiri berisi pointer ke isinya, `baz.txt` (sebuah blob) dan `foo`
(sebuah tree). Jika kita melihat isi yang dialamatkan oleh hash yang bersesuaian dengan
baz.txt dengan `git cat-file -p 4448adbf7ecd394f42ae135bbeed9676e894af85`, kita mendapatkan
yang berikut:

```
git is wonderful
```

## Rujukan

Sekarang, semua snapshot dapat diidentifikasi melalui hash SHA-1-nya. Itu tidak praktis,
karena manusia tidak pandai mengingat rangkaian 40 karakter heksadesimal.

Solusi Git untuk masalah ini adalah nama yang dapat dibaca manusia untuk hash SHA-1, yang disebut
"reference". Reference adalah pointer ke commit. Berbeda dengan object, yang bersifat
immutable, reference bersifat mutable (dapat diperbarui agar menunjuk ke commit baru).
Misalnya, reference `master` biasanya menunjuk ke commit terbaru pada
branch utama pengembangan.

```
references = map<string, string>

def update_reference(name, id):
    references[name] = id

def read_reference(name):
    return references[name]

def load_reference(name_or_id):
    if name_or_id in references:
        return load(references[name_or_id])
    else:
        return load(name_or_id)
```

Dengan ini, Git dapat menggunakan nama yang dapat dibaca manusia seperti "master" untuk merujuk
snapshot tertentu dalam riwayat, alih-alih string heksadesimal yang panjang.

Satu detail adalah bahwa kita sering menginginkan gagasan "di mana kita saat ini" dalam
riwayat, sehingga ketika kita mengambil snapshot baru, kita mengetahui relatif terhadap apa (bagaimana
kita menetapkan field `parents` pada commit). Di Git, "di mana kita saat ini" itu adalah
reference khusus yang disebut "HEAD".

## Repositories

Terakhir, kita dapat mendefinisikan apa (secara kasar) sebuah _repository_ Git: repository adalah data
`objects` dan `references`.

Di disk, semua penyimpanan Git adalah object dan reference: hanya itu saja isi data model
Git. Semua perintah `git` berkaitan dengan semacam manipulasi commit DAG dengan
menambahkan object dan menambahkan/memperbarui reference.

Setiap kali Anda mengetik perintah apa pun, pikirkan manipulasi apa yang
dilakukan perintah tersebut pada struktur data graph di baliknya. Sebaliknya, jika Anda
ingin membuat jenis perubahan tertentu pada commit DAG, misalnya "buang
perubahan yang belum di-commit dan buat ref 'master' menunjuk ke commit `5d83f9e`", kemungkinan
ada perintah untuk melakukannya (misalnya dalam kasus ini, `git checkout master; git reset
--hard 5d83f9e`).

# Staging area

Ini adalah konsep lain yang ortogonal terhadap data model, tetapi merupakan bagian dari
antarmuka untuk membuat commit.

Salah satu cara Anda mungkin membayangkan implementasi snapshot seperti dijelaskan di atas adalah memiliki
perintah "create snapshot" yang membuat snapshot baru berdasarkan _keadaan saat ini_
dari working directory. Sebagian tool version control bekerja seperti ini, tetapi
tidak dengan Git. Kita menginginkan snapshot yang bersih, dan membuat
snapshot dari keadaan saat ini tidak selalu ideal. Misalnya, bayangkan skenario di mana Anda telah
mengimplementasikan dua fitur terpisah, dan Anda ingin membuat dua commit terpisah,
di mana commit pertama memperkenalkan fitur pertama, dan commit berikutnya memperkenalkan
fitur kedua. Atau bayangkan skenario di mana Anda memiliki pernyataan print debugging
yang ditambahkan di seluruh kode Anda, bersama dengan sebuah perbaikan bug; Anda ingin meng-commit perbaikan bug
sambil membuang semua pernyataan print tersebut.

Git mengakomodasi skenario seperti itu dengan memungkinkan Anda menentukan modifikasi mana
yang harus disertakan dalam snapshot berikutnya melalui mekanisme yang disebut "staging
area".

# Command-line Interface Git

Untuk menghindari duplikasi informasi, kami tidak akan menjelaskan perintah di bawah ini
secara terperinci dalam catatan kuliah ini. Lihat [Pro
Git](https://git-scm.com/book/en/v2) yang sangat kami rekomendasikan untuk informasi lebih lanjut, atau tonton video
kuliahnya.

## Dasar-dasar

- `git help <command>`: dapatkan bantuan untuk perintah git
- `git init`: membuat repo git baru, dengan data tersimpan di direktori `.git`
- `git status`: memberi tahu Anda apa yang sedang terjadi
- `git add <filename>`: menambahkan berkas ke staging area
- `git commit`: membuat commit baru
    - Tulis [pesan commit yang baik](https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html)!
    - Alasan lebih banyak lagi untuk menulis [pesan commit yang baik](https://chris.beams.io/posts/git-commit/)!
- `git log`: menampilkan log riwayat yang diratakan
- `git log --all --graph --decorate`: memvisualisasikan riwayat sebagai DAG
- `git diff <filename>`: menampilkan perubahan yang Anda buat relatif terhadap staging area
- `git diff <revision> <filename>`: menampilkan perbedaan sebuah berkas antarsnapshot
- `git checkout <revision>`: memperbarui HEAD (dan branch saat ini jika melakukan checkout branch)

## Branching dan Merging

- `git branch`: menampilkan branch
- `git branch <name>`: membuat branch
- `git switch <name>`: beralih ke branch
- `git checkout -b <name>`: membuat branch dan beralih ke branch tersebut
    - sama dengan `git branch <name>; git switch <name>`
- `git merge <revision>`: melakukan merge ke branch saat ini
- `git mergetool`: gunakan tool canggih untuk membantu menyelesaikan konflik merge
- `git rebase`: melakukan rebase kumpulan patch ke base baru

## Remotes

- `git remote`: mencantumkan remote
- `git remote add <name> <url>`: menambahkan remote
- `git push <remote> <local branch>:<remote branch>`: mengirim object ke remote, dan memperbarui reference remote
- `git branch --set-upstream-to=<remote>/<remote branch>`: menyiapkan korespondensi antara branch lokal dan remote
- `git fetch`: mengambil object/reference dari remote
- `git pull`: sama dengan `git fetch; git merge`
- `git clone`: mengunduh repository dari remote

## Membatalkan Perubahan

- `git commit --amend`: mengedit isi/pesan sebuah commit
- `git reset <file>`: meng-unstage sebuah berkas
- `git restore`: membuang perubahan

# Git Tingkat Lanjut

- `git config`: Git sangat [dapat dikonfigurasi](https://git-scm.com/docs/git-config)
- `git clone --depth=1`: shallow clone, tanpa seluruh riwayat versi
- `git add -p`: staging interaktif
- `git rebase -i`: rebase interaktif
- `git blame`: menunjukkan siapa yang terakhir mengedit baris mana
- `git stash`: menghapus sementara modifikasi pada working directory
- `git bisect`: binary search pada riwayat (misalnya untuk regresi)
- `git revert`: membuat commit baru yang membalik efek commit sebelumnya
- `git worktree`: melakukan checkout beberapa branch sekaligus
- `.gitignore`: [menentukan](https://git-scm.com/docs/gitignore) berkas yang sengaja tidak dilacak untuk diabaikan

# Lain-lain

- **GUI**: ada banyak [klien GUI](https://git-scm.com/downloads/guis)
di luar sana untuk Git. Kami pribadi tidak menggunakannya dan menggunakan command-line
interface sebagai gantinya.
- **Integrasi shell**: sangat praktis memiliki status Git sebagai bagian dari
prompt shell Anda ([zsh](https://github.com/olivierverdier/zsh-git-prompt),
[bash](https://github.com/magicmonty/bash-git-prompt)). Sering disertakan dalam
framework seperti [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh).
- **Integrasi editor**: serupa dengan di atas, integrasi praktis dengan banyak
fitur. [fugitive.vim](https://github.com/tpope/vim-fugitive) adalah yang standar
untuk Vim.
- **Workflow**: kami mengajarkan data model kepada Anda, plus beberapa perintah dasar; kami
tidak memberi tahu Anda praktik apa yang harus diikuti saat bekerja pada proyek besar (dan
ada [banyak](https://nvie.com/posts/a-successful-git-branching-model/)
[pendekatan](https://www.endoflineblog.com/gitflow-considered-harmful)
[berbeda](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow)).
- **GitHub**: Git bukanlah GitHub. GitHub memiliki cara khusus untuk berkontribusi kode
ke proyek lain, yang disebut [pull
request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).
- **Penyedia Git lain**: GitHub tidak istimewa: ada banyak host repository
Git, seperti [GitLab](https://about.gitlab.com/) dan
[BitBucket](https://bitbucket.org/).

# Sumber Belajar

- [Pro Git](https://git-scm.com/book/en/v2) adalah **bacaan yang sangat direkomendasikan**.
Membaca Bab 1--5 seharusnya mengajarkan kepada Anda sebagian besar yang Anda butuhkan untuk menggunakan Git
secara mahir, sekarang setelah Anda memahami data model-nya. Bab-bab berikutnya memiliki
beberapa materi lanjutan yang menarik.
- [Oh Shit, Git!?!](https://ohshitgit.com/) adalah panduan singkat tentang cara pulih
dari beberapa kesalahan Git yang umum.
- [Git for Computer
Scientists](https://eagain.net/articles/git-for-computer-scientists/) adalah
penjelasan singkat tentang data model Git, dengan lebih sedikit pseudocode dan lebih banyak diagram
menarik daripada catatan kuliah ini.
- [Git from the Bottom Up](https://jwiegley.github.io/git-from-the-bottom-up/)
adalah penjelasan terperinci tentang detail implementasi Git di luar sekadar data
model, untuk yang penasaran.
- [How to explain git in simple
words](https://smusamashah.github.io/blog/2017/10/14/explain-git-in-simple-words)
- [Learn Git Branching](https://learngitbranching.js.org/) adalah game berbasis browser
yang mengajarkan Git kepada Anda.

# Latihan

1. Jika Anda tidak memiliki pengalaman masa lalu dengan Git, coba baca beberapa
   bab pertama [Pro Git](https://git-scm.com/book/en/v2) atau ikuti
   tutorial seperti [Learn Git Branching](https://learngitbranching.js.org/). Saat
   Anda mengerjakannya, kaitkan perintah Git dengan data model.
1. Clone [repository untuk
situs kelas](https://github.com/missing-semester/missing-semester).
    1. Jelajahi riwayat versinya dengan memvisualisasikannya sebagai graph.
    1. Siapa orang terakhir yang memodifikasi `README.md`? (Petunjuk: gunakan `git log` dengan
       sebuah argumen).
    1. Apa pesan commit yang terkait dengan modifikasi terakhir pada
       baris `collections:` di `_config.yml`? (Petunjuk: gunakan `git blame` dan `git
       show`).
1. Kesalahan umum saat mempelajari Git adalah meng-commit berkas besar yang seharusnya
   tidak dikelola Git atau menambahkan informasi sensitif. Coba tambahkan sebuah berkas ke
   sebuah repository, buat beberapa commit lalu hapus berkas tersebut dari _riwayat_
   (bukan hanya dari commit terbaru). Anda mungkin ingin melihat
   [ini](https://help.github.com/articles/removing-sensitive-data-from-a-repository/).
1. Clone beberapa repository dari GitHub, dan modifikasi salah satu berkas yang sudah ada.
   Apa yang terjadi ketika Anda melakukan `git stash`? Apa yang Anda lihat saat menjalankan `git log
   --all --oneline`? Jalankan `git stash pop` untuk membatalkan apa yang Anda lakukan dengan `git stash`.
   Dalam skenario apa ini mungkin berguna?
1. Seperti banyak tool command line, Git menyediakan berkas konfigurasi (atau dotfile)
   bernama `~/.gitconfig`. Buat alias di `~/.gitconfig` sehingga ketika Anda
   menjalankan `git graph`, Anda mendapatkan output `git log --all --graph --decorate
   --oneline`. Anda dapat melakukannya dengan langsung
   [mengedit](https://git-scm.com/docs/git-config#Documentation/git-config.txt-alias)
   berkas `~/.gitconfig`, atau Anda dapat menggunakan perintah `git config` untuk menambahkan
   alias. Informasi tentang alias git dapat ditemukan
   [di sini](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases).
1. Anda dapat mendefinisikan pola ignore global di `~/.gitignore_global` setelah menjalankan
   `git config --global core.excludesfile ~/.gitignore_global`. Ini menetapkan
   lokasi berkas ignore global yang akan digunakan Git, tetapi Anda masih perlu
   membuat berkas tersebut secara manual di path itu. Siapkan berkas gitignore global Anda untuk
   mengabaikan berkas sementara khas OS atau khas editor, seperti `.DS_Store`.
1. Fork [repository untuk situs
   kelas](https://github.com/missing-semester/missing-semester), temukan typo
   atau perbaikan lain yang dapat Anda lakukan, dan ajukan pull request di GitHub
   (Anda mungkin ingin melihat [ini](https://github.com/firstcontributions/first-contributions)).
   Mohon hanya ajukan PR yang berguna (jangan spam kami, ya!). Jika Anda
   tidak dapat menemukan perbaikan yang bisa dilakukan, Anda dapat melewati latihan ini.
1. Berlatih menyelesaikan konflik merge dengan menyimulasikan skenario kolaboratif:
    1. Buat repository baru dengan `git init` dan buat berkas bernama
       `recipe.txt` dengan beberapa baris (misalnya, resep sederhana).
    1. Commit berkas tersebut, lalu buat dua branch: `git branch salty` dan `git branch
       sweet`.
    1. Pada branch `salty`, modifikasi sebuah baris (misalnya, ubah "1 cup sugar" menjadi "1
       cup salt") dan commit.
    1. Pada branch `sweet`, modifikasi baris yang sama dengan cara berbeda (misalnya, ubah "1
       cup sugar" menjadi "2 cups sugar") dan commit.
    1. Sekarang beralih ke `master` dan coba `git merge salty`, lalu `git merge
       sweet`. Apa yang terjadi? Lihat isi `recipe.txt` - apa arti penanda
       `<<<<<<<`, `=======`, dan `>>>>>>>`?
    1. Selesaikan konflik dengan mengedit berkas agar mempertahankan konten yang Anda inginkan,
       menghapus penanda konflik, dan menyelesaikan merge dengan `git add`
       dan `git commit` (atau `git merge --continue`). Alternatifnya, coba gunakan
       `git mergetool` untuk menyelesaikan konflik dengan tool merge grafis atau
       berbasis terminal.
    1. Gunakan `git log --graph --oneline` untuk memvisualisasikan riwayat merge yang baru saja
       Anda buat.
