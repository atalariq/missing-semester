---
layout: lecture-id
title: "Package Management dan Dependency Management"
presenter: Anish
date: 2019-01-29
order: 2
video:
  aspect: 56.25
  id: tgvt473T8xA
lang: id
permalink: /id/2019/package-management/
---

Perangkat lunak biasanya dibangun di atas (kumpulan) perangkat lunak lain, yang menuntut
dependency management.

Program package/dependency management bersifat khas bahasa, tetapi banyak yang berbagi
gagasan umum.

# Repositori paket

Paket di-host di _repositori paket_. Ada repositori berbeda
untuk bahasa berbeda (dan kadang beberapa untuk bahasa tertentu),
seperti [PyPI](https://pypi.org/) untuk Python, [RubyGems](https://rubygems.org/)
untuk Ruby, dan [crates.io](https://crates.io/) untuk Rust. Repositori tersebut umumnya menyimpan
perangkat lunak (kode sumber dan kadang binary yang sudah dikompilasi untuk platform
tertentu) untuk semua versi sebuah paket.

# Semantic versioning

Perangkat lunak berevolusi seiring waktu, dan kita memerlukan cara untuk merujuk versi perangkat lunak.
Beberapa cara sederhana bisa berupa merujuk perangkat lunak dengan nomor urut atau
hash commit, tetapi kita dapat berbuat lebih baik dalam mengomunikasikan lebih banyak informasi: menggunakan
nomor versi.

Ada banyak pendekatan; salah satu yang populer adalah [Semantic
Versioning](https://semver.org/):

```
x.y.z
^ ^ ^
| | +- patch
| +--- minor
+----- major
```

Naikkan versi **major** ketika Anda membuat perubahan API yang tidak kompatibel.

Naikkan versi **minor** ketika Anda menambahkan fungsionalitas dengan cara yang kompatibel ke belakang.

Naikkan **patch** ketika Anda membuat perbaikan bug yang kompatibel ke belakang.

Misalnya, jika Anda bergantung pada fitur yang diperkenalkan di `v1.2.0` suatu
perangkat lunak, maka Anda dapat memasang `v1.x.y` untuk versi minor `x >= 2` berapa pun dan
versi patch `y` berapa pun. Anda perlu memasang versi major `1` (karena `2` dapat
memperkenalkan perubahan yang tidak kompatibel ke belakang), dan Anda perlu memasang versi minor
`>= 2` (karena Anda bergantung pada fitur yang diperkenalkan di versi minor
tersebut). Anda dapat menggunakan versi minor atau versi patch yang lebih baru karena
versi tersebut seharusnya tidak memperkenalkan perubahan yang tidak kompatibel ke belakang.

# Lock file

Selain menentukan versi, alangkah baiknya menegakkan bahwa
_isi_ dependency tidak berubah untuk mencegah manipulasi. Sebagian tool
menggunakan _lock file_ untuk menentukan hash kriptografis dependency (beserta
versinya) yang diperiksa saat pemasangan paket.

# Menentukan versi

Tool sering memungkinkan Anda menentukan versi dengan berbagai cara, seperti:

- versi persis, misalnya `2.3.12`
- versi major minimum, misalnya `>= 2`
- versi major tertentu dan versi patch minimum, misalnya `>= 2.3, <3.0`

Menentukan versi persis bisa menguntungkan untuk menghindari perilaku berbeda
berdasarkan dependency yang terpasang (ini seharusnya tidak terjadi jika semua dependency
mengikuti semver dengan setia, tetapi kadang orang membuat kesalahan). Menentukan
persyaratan minimum memiliki keuntungan memungkinkan perbaikan bug dipasang
(misalnya upgrade patch).

# Dependency resolution

Package manager menggunakan berbagai algoritma dependency resolution untuk memenuhi
persyaratan dependency. Ini sering menjadi menantang dengan dependency yang kompleks
(misalnya sebuah paket dapat secara tidak langsung menjadi dependency dari beberapa dependency
tingkat atas, dan versi berbeda mungkin dibutuhkan). Package manager berbeda
memiliki tingkat kecanggihan berbeda dalam dependency
resolution-nya, tetapi ini sesuatu yang perlu diketahui: Anda mungkin perlu memahaminya
jika Anda men-debug dependency.

# Virtual environment

Jika Anda mengembangkan beberapa proyek perangkat lunak, proyek tersebut mungkin bergantung pada versi
berbeda dari suatu perangkat lunak tertentu. Kadang, build tool Anda akan
menangani ini secara alami (misalnya dengan membangun binary statis).

Untuk build tool dan bahasa pemrograman lain, salah satu pendekatan adalah menanganinya
dengan virtual environment (misalnya dengan tool
[virtualenv](https://docs.python-guide.org/dev/virtualenvs/) untuk Python).
Alih-alih memasang dependency secara system-wide, Anda dapat memasang dependency
per-proyek di virtual environment, dan _mengaktifkan_ virtual environment
yang ingin Anda gunakan ketika Anda bekerja pada proyek tertentu.

# Vendoring

Pendekatan lain yang sangat berbeda untuk dependency management adalah _vendoring_.
Alih-alih menggunakan dependency manager atau build tool untuk mengambil perangkat lunak, Anda menyalin
seluruh kode sumber sebuah dependency ke repositori perangkat lunak Anda. Ini
memiliki keuntungan bahwa Anda selalu membangun terhadap versi dependency yang sama
dan Anda tidak perlu bergantung pada repositori paket, tetapi lebih banyak
usaha untuk melakukan upgrade dependency.
