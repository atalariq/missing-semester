---
layout: lecture-id
title: "Packaging and Shipping Code"
description: >
  Pelajari packaging project, environment, versioning, dan deployment library, aplikasi, serta service.
thumbnail: /static/assets/thumbnails/2026/lec6.png
date: 2026-01-20
ready: true
video:
  aspect: 56.25
  id: KBMiB-8P4Ns
lang: id
permalink: /id/2026/shipping-code/
---

Membuat kode bekerja sesuai harapan itu sulit; membuat kode yang sama berjalan di mesin yang berbeda dari mesin Anda sering kali lebih sulit.

Shipping code berarti mengambil kode yang Anda tulis dan mengubahnya menjadi bentuk yang dapat digunakan sehingga orang lain dapat menjalankannya tanpa pengaturan komputer Anda yang persis sama.
Shipping code mengambil banyak bentuk dan bergantung pada pilihan bahasa pemrograman, system library, dan sistem operasi, di antara banyak faktor lain.
Hal ini juga bergantung pada apa yang Anda bangun: software library, tool command line, dan web service semuanya memiliki kebutuhan dan langkah deployment yang berbeda.
Terlepas dari itu, ada pola umum di antara semua skenario ini: kita perlu mendefinisikan apa hasil akhirnya --- alias _artifact_ --- dan asumsi apa yang dibuatnya tentang environment di sekitarnya.

Pada kuliah ini, kami akan membahas:

- [Dependencies & Environments](#dependencies--environments)
- [Artifacts & Packaging](#artifacts--packaging)
- [Releases & Versioning](#releases--versioning)
- [Reproducibility](#reproducibility)
- [VMs & Containers](#vms--containers)
- [Configuration](#configuration)
- [Services & Orchestration](#services--orchestration)
- [Publishing](#publishing)

Kami akan menjelaskan konsep-konsep ini melalui contoh dari ekosistem Python, karena contoh konkret membantu pemahaman. Meskipun tool-nya berbeda untuk ekosistem bahasa pemrograman lain, konsepnya sebagian besar akan sama.

<a id="dependencies--environments"></a>
# Dependency dan Environment

Dalam pengembangan perangkat lunak modern, lapisan abstraksi ada di mana-mana.
Program secara alami menyerahkan logika ke library atau layanan lain.
Namun, ini memperkenalkan hubungan _dependency_ antara program Anda dan library yang dibutuhkannya untuk berfungsi.
Misalnya, di Python, untuk mengambil isi sebuah situs web kita sering melakukan:

```python
import requests

response = requests.get("https://missing.csail.mit.edu")
```

Namun library `requests` tidak disertakan bersama runtime Python, jadi jika kita mencoba menjalankan kode ini tanpa `requests` terpasang, Python akan memunculkan error:

```console
$ python fetch.py
Traceback (most recent call last):
  File "fetch.py", line 1, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
```

Untuk membuat library ini tersedia kita perlu menjalankan `pip install requests` terlebih dahulu untuk memasangnya.
`pip` adalah tool command line yang disediakan bahasa pemrograman Python untuk memasang paket.
Mengeksekusi `pip install requests` menghasilkan rangkaian tindakan berikut:

1. Mencari requests di Python Package Index ([PyPI](https://pypi.org/))
1. Mencari artifact yang sesuai untuk platform tempat kita berjalan
1. Menyelesaikan dependency --- library `requests` itu sendiri bergantung pada paket lain, sehingga installer harus menemukan versi yang kompatibel dari semua dependency transitif dan memasangnya terlebih dahulu
1. Mengunduh artifact, lalu membongkar dan menyalin berkas ke tempat yang tepat di file system kita

```console
$ pip install requests
Collecting requests
  Downloading requests-2.32.3-py3-none-any.whl (64 kB)
Collecting charset-normalizer<4,>=2
  Downloading charset_normalizer-3.4.0-cp311-cp311-manylinux_x86_64.whl (142 kB)
Collecting idna<4,>=2.5
  Downloading idna-3.10-py3-none-any.whl (70 kB)
Collecting urllib3<3,>=1.21.1
  Downloading urllib3-2.2.3-py3-none-any.whl (126 kB)
Collecting certifi>=2017.4.17
  Downloading certifi-2024.8.30-py3-none-any.whl (167 kB)
Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests
Successfully installed certifi-2024.8.30 charset-normalizer-3.4.0 idna-3.10 requests-2.32.3 urllib3-2.2.3
```

Di sini kita dapat melihat bahwa `requests` memiliki dependency sendiri seperti `certifi` atau `charset-normalizer` dan bahwa dependency tersebut harus dipasang sebelum `requests` dapat dipasang.
Setelah terpasang, runtime Python dapat menemukan library ini saat mengimpornya.

```console
$ python -c 'import requests; print(requests.__path__)'
['/usr/local/lib/python3.11/dist-packages/requests']

$ pip list | grep requests
requests        2.32.3
```

Bahasa pemrograman memiliki tool, konvensi, dan praktik berbeda untuk memasang dan mempublikasikan library.
Pada sebagian bahasa seperti Rust, toolchain-nya terpadu --- `cargo` menangani building, testing, dependency management, dan publishing.
Pada bahasa lain seperti Python, penyatuannya terjadi di tingkat spesifikasi --- alih-alih satu tool, ada spesifikasi terstandar yang mendefinisikan cara packaging bekerja, memungkinkan beberapa tool yang bersaing untuk setiap tugas (`pip` vs [`uv`](https://docs.astral.sh/uv/), `setuptools` vs [`hatch`](https://hatch.pypa.io/) vs [`poetry`](https://python-poetry.org/)).
Dan pada sebagian ekosistem seperti LaTeX, distribusi seperti TeX Live atau MacTeX hadir dengan ribuan paket yang sudah terpasang.

Memperkenalkan dependency juga memperkenalkan konflik dependency.
Konflik terjadi ketika program membutuhkan versi yang tidak kompatibel dari dependency yang sama.
Misalnya, jika `tensorflow==2.3.0` membutuhkan `numpy>=1.16.0,<1.19.0` dan `pandas==1.2.0`  membutuhkan `numpy>=1.16.5`, maka versi apa pun yang memenuhi `numpy>=1.16.5,<1.19.0` akan valid.
Tetapi jika paket lain di proyek Anda membutuhkan `numpy>=1.19`, Anda memiliki konflik tanpa versi valid yang memenuhi semua constraint.

Situasi ini --- di mana beberapa paket membutuhkan versi yang saling tidak kompatibel dari dependency bersama --- umumnya disebut _dependency hell_.
Salah satu cara menangani konflik adalah mengisolasi dependency setiap program ke dalam _environment_-nya sendiri.
Di Python kita membuat virtual environment dengan menjalankan:

```console
$ which python
/usr/bin/python
$ pwd
/home/missingsemester
$ python -m venv venv
$ source venv/bin/activate
$ which python
/home/missingsemester/venv/bin/python
$ which pip
/home/missingsemester/venv/bin/pip
$ python -c 'import requests; print(requests.__path__)'
['/home/missingsemester/venv/lib/python3.11/site-packages/requests']

$ pip list
Package Version
------- -------
pip     24.0
```

Anda dapat memandang environment sebagai versi standalone utuh dari runtime bahasa dengan rangkaian paket terpasangnya sendiri.
Virtual environment atau venv ini mengisolasi dependency yang terpasang dari instalasi Python global.
Praktik yang baik adalah memiliki virtual environment untuk setiap proyek, yang memuat dependency yang dibutuhkannya.

> Meskipun banyak sistem operasi modern hadir dengan instalasi runtime bahasa pemrograman seperti Python, tidak bijaksana memodifikasi instalasi tersebut karena OS mungkin bergantung padanya untuk fungsionalitasnya sendiri. Lebih baik gunakan environment terpisah.

Pada sebagian bahasa, protokol instalasi tidak didefinisikan oleh sebuah tool tetapi sebagai spesifikasi.
Di Python [PEP 517](https://peps.python.org/pep-0517/) mendefinisikan antarmuka build system dan [PEP 621](https://peps.python.org/pep-0621/) menentukan bagaimana metadata proyek disimpan di `pyproject.toml`.
Ini memungkinkan pengembang memperbaiki `pip` dan menghasilkan tool yang lebih teroptimasi seperti `uv`. Untuk memasang `uv` cukup lakukan `pip install uv`.

Menggunakan `uv` alih-alih `pip` mengikuti antarmuka yang sama tetapi jauh lebih cepat:

```console
$ uv pip install requests
Resolved 5 packages in 12ms
Prepared 5 packages in 0.45ms
Installed 5 packages in 8ms
 + certifi==2024.8.30
 + charset-normalizer==3.4.0
 + idna==3.10
 + requests==2.32.3
 + urllib3==2.2.3
```

> Kami sangat menyarankan menggunakan `uv pip` alih-alih `pip` bila memungkinkan karena tool ini secara drastis mengurangi waktu pemasangan.

Selain isolasi dependency, environment juga memungkinkan Anda memiliki versi runtime bahasa pemrograman yang berbeda.

```console
$ uv venv --python 3.12 venv312
Using CPython 3.12.7
Creating virtual environment at: venv312

$ source venv312/bin/activate && python --version
Python 3.12.7

$ uv venv --python 3.11 venv311
Using CPython 3.11.10
Creating virtual environment at: venv311

$ source venv311/bin/activate && python --version
Python 3.11.10
```

Ini membantu ketika Anda perlu menguji kode Anda di beberapa versi Python atau ketika sebuah proyek membutuhkan versi tertentu.

> Pada sebagian bahasa pemrograman, setiap proyek otomatis mendapatkan environment sendiri untuk dependency-nya alih-alih Anda membuatnya secara manual, tetapi prinsipnya sama. Sebagian besar bahasa saat ini juga memiliki mekanisme untuk mengelola beberapa versi bahasa pada satu sistem, lalu menentukan versi mana yang digunakan untuk masing-masing proyek.

<a id="artifacts--packaging"></a>
# Artifact dan Packaging

Dalam pengembangan perangkat lunak kita membedakan antara kode sumber dan artifact. Pengembang menulis dan membaca kode sumber, sedangkan artifact adalah output terpaket dan dapat didistribusikan yang dihasilkan dari kode sumber tersebut --- siap dipasang atau di-deploy.
Sebuah artifact bisa sesederhana berkas kode yang kita jalankan, dan sekompleks seluruh Virtual Machine yang memuat semua bagian yang diperlukan sebuah aplikasi.
Perhatikan contoh ini di mana kita memiliki berkas Python `greet.py` di direktori saat ini:

```console
$ cat greet.py
def greet(name):
    print(f"Hello, {name}!")

$ python -c "from greet import greet; greet('World')"
Hello, World!

$ cd /tmp
$ python -c "from greet import greet; greet('World')"
ModuleNotFoundError: No module named 'greet'
```

Import gagal setelah kita pindah ke direktori lain karena Python hanya mencari module di lokasi tertentu (direktori saat ini, paket yang terpasang, dan path di `PYTHONPATH`). Packaging menyelesaikan ini dengan memasang kode ke lokasi yang diketahui.

Di Python, packaging sebuah library melibatkan pembuatan artifact yang dapat digunakan installer paket seperti `pip` atau `uv` untuk memasang berkas yang relevan.
Artifact Python disebut _wheel_ dan memuat semua informasi yang diperlukan untuk memasang sebuah paket: berkas kode, metadata tentang paket (nama, versi, dependency), dan instruksi tentang di mana menempatkan berkas di environment.
Membangun artifact mengharuskan kita menulis berkas proyek (juga sering dikenal sebagai manifest) yang merinci spesifikasi proyek, dependency yang diperlukan, versi paket, dan informasi lain. Di Python, kita menggunakan `pyproject.toml` untuk tujuan ini.

> `pyproject.toml` adalah cara modern dan direkomendasikan. Meskipun metode packaging sebelumnya seperti `requirements.txt` atau `setup.py` masih didukung, Anda sebaiknya mengutamakan `pyproject.toml` bila memungkinkan.

Berikut `pyproject.toml` minimal untuk library yang juga menyediakan tool command-line:

```toml
[project]
name = "greeting"
version = "0.1.0"
description = "A simple greeting library"
dependencies = ["typer>=0.9"]

[project.scripts]
greet = "greeting:cli"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

Library `typer` adalah paket Python populer untuk membuat command-line interface dengan boilerplate minimal.

Dan `greeting.py` yang bersesuaian:

```python
import typer


def greet(name: str) -> None:
    print(f"Hello, {name}!")


def cli() -> None:
    typer.run(greet)


if __name__ == "__main__":
    cli()
```

Dengan berkas ini, sekarang kita dapat membangun wheel:

```console
$ uv build
Building source distribution...
Building wheel from source distribution...
Successfully built dist/greeting-0.1.0.tar.gz
Successfully built dist/greeting-0.1.0-py3-none-any.whl

$ ls dist/
greeting-0.1.0-py3-none-any.whl
greeting-0.1.0.tar.gz
```

Berkas `.whl` adalah wheel (arsip zip dengan struktur tertentu), dan `.tar.gz` adalah source distribution untuk sistem yang perlu membangun dari source.

Anda dapat memeriksa isi wheel untuk melihat apa yang dipaketkan:

```console
$ unzip -l dist/greeting-0.1.0-py3-none-any.whl
Archive:  dist/greeting-0.1.0-py3-none-any.whl
  Length      Date    Time    Name
---------  ---------- -----   ----
      150  2024-01-15 10:30   greeting.py
      312  2024-01-15 10:30   greeting-0.1.0.dist-info/METADATA
       92  2024-01-15 10:30   greeting-0.1.0.dist-info/WHEEL
        9  2024-01-15 10:30   greeting-0.1.0.dist-info/top_level.txt
      435  2024-01-15 10:30   greeting-0.1.0.dist-info/RECORD
---------                     -------
      998                     5 files
```

Sekarang jika kita memberikan wheel ini kepada orang lain, mereka dapat memasangnya dengan menjalankan:

```console
$ uv pip install ./greeting-0.1.0-py3-none-any.whl
$ greet Alice
Hello, Alice!
```

Ini akan memasang library yang kita bangun tadi ke environment mereka, termasuk tool cli `greet`.

Ada keterbatasan pada pendekatan ini. Secara khusus jika library kita bergantung pada library khas platform, misalnya CUDA untuk akselerasi GPU, maka artifact kita hanya bekerja pada sistem dengan library khusus tersebut terpasang, dan kita mungkin perlu membangun wheel terpisah untuk platform berbeda (Linux, macOS, Windows) dan arsitektur berbeda (x86, ARM).


Saat memasang perangkat lunak, ada perbedaan penting antara memasang dari source dan memasang binary yang sudah dibangun. Memasang dari source berarti mengunduh kode asli dan mengompilasinya di mesin Anda --- ini memerlukan compiler dan build tool terpasang, dan bisa memakan waktu signifikan untuk proyek besar.

Memasang binary yang sudah dibangun berarti mengunduh artifact yang sudah dikompilasi oleh orang lain --- lebih cepat dan sederhana, tetapi binary harus sesuai dengan platform dan arsitektur Anda.
Misalnya, [halaman rilis ripgrep](https://github.com/BurntSushi/ripgrep/releases) menampilkan binary yang sudah dibangun untuk Linux (x86_64, ARM), macOS (Intel, Apple Silicon), dan Windows.


<a id="releases--versioning"></a>
# Release dan Versioning

Kode dibangun dalam proses yang berkelanjutan tetapi dirilis secara diskret.
Dalam pengembangan perangkat lunak ada perbedaan jelas antara environment pengembangan dan produksi.
Kode perlu dibuktikan berfungsi di environment dev sebelum di-_ship_ ke prod.
Proses rilis melibatkan banyak langkah, termasuk testing, dependency management, versioning, konfigurasi, deployment dan publishing.


Software library tidak statis dan berevolusi seiring waktu dengan perbaikan dan fitur baru.
Kita melacak evolusi ini melalui identifier versi diskret yang bersesuaian dengan keadaan library pada titik waktu tertentu.
Perubahan perilaku sebuah library dapat berkisar dari patch yang memperbaiki fungsionalitas non-kritis, fitur baru yang memperluas fungsionalitasnya, hingga perubahan yang merusak kompatibilitas ke belakang.
Changelog mendokumentasikan perubahan apa yang diperkenalkan sebuah versi --- ini adalah dokumen yang digunakan pengembang perangkat lunak untuk mengomunikasikan perubahan yang terkait dengan sebuah rilis baru.

Namun, melacak perubahan yang berlangsung pada setiap dependency sangat tidak praktis, terlebih lagi ketika kita mempertimbangkan dependency transitif --- yaitu dependency dari dependency kita.

> Anda dapat memvisualisasikan seluruh pohon dependency proyek Anda dengan `uv tree`, yang menampilkan semua paket dan dependency transitifnya dalam format tree.

Untuk menyederhanakan masalah ini ada konvensi tentang cara memberi versi perangkat lunak, dan salah satu yang paling lazim adalah [Semantic Versioning](https://semver.org/) atau SemVer.
Di bawah Semantic Versioning sebuah versi memiliki identifier berbentuk MAJOR.MINOR.PATCH di mana masing-masing nilai berupa bilangan bulat. Versi singkatnya adalah bahwa melakukan upgrade:

- PATCH (misalnya, 1.2.3 → 1.2.4) seharusnya hanya berisi perbaikan bug dan sepenuhnya kompatibel ke belakang
- MINOR (misalnya, 1.2.3 → 1.3.0) menambahkan fungsionalitas baru dengan cara yang kompatibel ke belakang
- MAJOR (misalnya, 1.2.3 → 2.0.0) menunjukkan perubahan yang merusak yang mungkin memerlukan modifikasi kode

> Ini adalah penyederhanaan dan kami mendorong membaca spesifikasi SemVer lengkap untuk memahami misalnya mengapa beralih dari 0.1.3 ke 0.2.0 mungkin menyebabkan perubahan yang merusak atau apa arti 1.0.0-rc.1.
Packaging Python mendukung version specifier terstandar yang didefinisikan oleh [PEP 440](https://peps.python.org/pep-0440/), sehingga ketika kita menentukan versi dependency kita dapat menggunakan berbagai constraint:

Di `pyproject.toml` kita memiliki cara berbeda untuk membatasi rentang versi kompatibel dari dependency kita:

```toml
[project]
dependencies = [
    "requests==2.32.3",  # Exact version - only this specific version
    "click>=8.0",        # Minimum version - 8.0 or newer
    "numpy>=1.24,<2.0",  # Range - at least 1.24 but less than 2.0
    "pandas~=2.1.0",     # Compatible release - >=2.1.0 and <2.2.0
]
```

Version specifier ada di banyak package manager (npm, cargo, dsb.) dengan semantik yang sedikit berbeda-beda. Operator `~=` adalah operator "compatible release" Python --- `~=2.1.0` berarti "versi apa pun yang kompatibel dengan 2.1.0", yang berarti `>=2.1.0` dan `<2.2.0`. Ini kurang lebih setara dengan operator caret (`^`) di npm dan cargo, yang mengikuti gagasan kompatibilitas SemVer.

Tidak semua perangkat lunak menggunakan semantic versioning. Alternatif yang umum adalah Calendar Versioning (CalVer), di mana versi didasarkan pada tanggal rilis alih-alih makna semantik. Misalnya, Ubuntu menggunakan versi seperti `24.04` (April 2024) dan `24.10` (Oktober 2024). CalVer memudahkan melihat berapa umur sebuah rilis, meskipun tidak mengomunikasikan apa pun tentang kompatibilitas. Terakhir, semantic versioning tidak luput dari kesalahan, dan kadang maintainer tanpa sengaja memperkenalkan perubahan yang merusak pada rilis minor atau patch.


<a id="reproducibility"></a>
# Reproducibility

Dalam pengembangan perangkat lunak modern kode yang Anda tulis berada di atas lapisan abstraksi yang signifikan jumlahnya.
Ini mencakup hal-hal seperti runtime bahasa pemrograman Anda, library pihak ketiga, sistem operasi, atau bahkan perangkat keras itu sendiri.
Perbedaan apa pun pada salah satu lapisan ini mungkin mengubah perilaku kode Anda atau bahkan mencegahnya bekerja sesuai harapan.
Lebih jauh lagi, bahkan perbedaan pada perangkat keras yang mendasarinya memengaruhi kemampuan Anda mengirim perangkat lunak.

Pinning sebuah library berarti menentukan versi yang persis, bukan rentang, misalnya `requests==2.32.3` alih-alih `requests>=2.0`.

Sebagian tugas package manager adalah mempertimbangkan semua constraint yang diberikan oleh dependency --- dan dependency transitif --- lalu menghasilkan daftar versi valid yang memenuhi semua constraint.
Daftar versi spesifik tersebut kemudian dapat disimpan ke berkas untuk keperluan reproducibility; berkas ini disebut _lock file_.

```console
$ uv lock
Resolved 12 packages in 45ms

$ cat uv.lock | head -20
version = 1
requires-python = ">=3.11"

[[package]]
name = "certifi"
version = "2024.8.30"
source = { registry = "https://pypi.org/simple" }
sdist = { url = "https://files.pythonhosted.org/...", hash = "sha256:..." }
wheels = [
    { url = "https://files.pythonhosted.org/...", hash = "sha256:..." },
]
...
```

Satu perbedaan kritis saat menangani dependency versioning dan reproducibility adalah perbedaan antara library dan aplikasi/layanan.
Sebuah library dimaksudkan untuk diimpor dan digunakan kode lain yang mungkin memiliki dependency sendiri, sehingga menentukan constraint versi yang terlalu ketat dapat menyebabkan konflik dengan dependency lain pengguna.
Sebaliknya, aplikasi atau layanan adalah konsumen akhir perangkat lunak dan biasanya mengekspos fungsionalitasnya melalui antarmuka pengguna atau API, bukan melalui programming interface.
Untuk library, praktik yang baik adalah menentukan rentang versi untuk memaksimalkan kompatibilitas dengan ekosistem paket yang lebih luas. Untuk aplikasi, pinning versi persis memastikan reproducibility --- semua orang yang menjalankan aplikasi menggunakan dependency yang persis sama.


Untuk proyek yang menuntut reproducibility maksimal, tool seperti [Nix](https://nixos.org/) dan [Bazel](https://bazel.build/) menyediakan build yang _hermetic_ --- di mana setiap input termasuk compiler, system library, dan bahkan build environment itu sendiri di-pin dan dialamatkan berdasarkan konten. Ini menjamin output identik bit-per-bit terlepas dari kapan atau di mana build berjalan.

> Anda bahkan dapat menggunakan NixOS untuk mengelola seluruh instalasi komputer Anda sehingga Anda dapat dengan mudah membuat salinan baru pengaturan komputer Anda dan mengelola konfigurasi lengkapnya melalui berkas konfigurasi di bawah version control.

Ketegangan tanpa akhir dalam pengembangan perangkat lunak adalah versi perangkat lunak baru memperkenalkan kerusakan entah secara sengaja atau tidak, sementara di sisi lain, versi perangkat lunak lama menjadi terkompromi dengan kerentanan keamanan seiring waktu.
Kita dapat mengatasi ini dengan menggunakan pipeline continuous integration (kita akan melihat lebih banyak pada kuliah [Code Quality and CI](/2026/code-quality/)) yang menguji aplikasi kita terhadap versi perangkat lunak baru dan memiliki otomatisasi untuk mendeteksi kapan versi baru dependency kita dirilis, seperti [Dependabot](https://github.com/dependabot).

Bahkan dengan CI testing, masalah tetap terjadi saat melakukan upgrade versi perangkat lunak, sering karena ketidaksesuaian yang tak terhindarkan antara environment dev dan prod.
Dalam keadaan seperti itu tindakan terbaik adalah memiliki rencana _rollback_, di mana upgrade versi dibatalkan dan versi yang diketahui baik di-deploy ulang.

<a id="vms--containers"></a>
# VM dan Container

Saat Anda mulai bergantung pada dependency yang lebih kompleks, kemungkinan besar dependency kode Anda akan melampaui batas yang dapat ditangani package manager.
Salah satu alasan umum adalah keharusan berinteraksi dengan system library atau driver perangkat keras tertentu.
Misalnya, dalam scientific computing dan AI, program sering membutuhkan library dan driver khusus untuk memanfaatkan perangkat keras GPU.
Banyak dependency tingkat sistem (driver GPU, versi compiler tertentu, shared library seperti OpenSSL) masih memerlukan pemasangan system-wide.

Secara tradisional masalah dependency yang lebih luas ini diselesaikan dengan Virtual Machine (VM).
VM mengabstraksi seluruh komputer dan menyediakan environment yang sepenuhnya terisolasi dengan sistem operasi khusus miliknya.
Pendekatan yang lebih modern adalah container, yang memaketkan aplikasi beserta dependency, library, dan file system-nya, tetapi berbagi kernel sistem operasi host alih-alih memvirtualkan seluruh komputer.
Container lebih ringan daripada VM karena berbagi kernel, sehingga lebih cepat dimulai dan lebih efisien dijalankan.

Platform container paling populer adalah [Docker](https://www.docker.com/). Docker memperkenalkan cara terstandar untuk membangun, mendistribusikan, dan menjalankan container. Di balik layar, Docker menggunakan containerd sebagai container runtime-nya --- standar industri yang juga digunakan tool lain seperti Kubernetes.

Menjalankan container sangatlah mudah. Misalnya, untuk menjalankan interpreter Python di dalam container kita menggunakan `docker run` (flag `-it` membuat container interaktif dengan terminal. Ketika Anda keluar, container berhenti.).

```console
$ docker run -it python:3.12 python
Python 3.12.7 (main, Nov  5 2024, 02:53:25) [GCC 12.2.0] on linux
>>> print("Hello from inside a container!")
Hello from inside a container!
```

Dalam praktiknya program Anda mungkin bergantung pada seluruh file system.
Untuk mengatasi ini, kita dapat menggunakan container image yang mengirimkan seluruh file system aplikasi sebagai artifact.
Container image dibuat secara programatik. Dengan docker kita menentukan persis dependency, system library, dan konfigurasi image menggunakan sintaks Dockerfile:

```dockerfile
FROM python:3.12
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libpq-dev
RUN pip install numpy
RUN pip install pandas
COPY . /app
WORKDIR /app
RUN pip install .
```

Perbedaan penting: Docker **image** adalah artifact terpaket (seperti template), sedangkan **container** adalah instans yang berjalan dari image tersebut. Anda dapat menjalankan beberapa container dari image yang sama. Image dibangun dalam layer, di mana setiap instruksi (`FROM`, `RUN`, `COPY`, dsb.) dalam Dockerfile membuat layer baru. Docker menyimpan layer ini di cache, sehingga jika Anda mengubah satu baris di Dockerfile, hanya layer itu dan layer berikutnya yang perlu dibangun ulang.

Dockerfile sebelumnya memiliki beberapa masalah: ia menggunakan image Python penuh alih-alih varian slim, menjalankan perintah `RUN` terpisah yang membuat layer tidak perlu, versi tidak di-pin, dan tidak membersihkan cache package manager, sehingga mengirim berkas yang tidak perlu. Kesalahan lain yang sering terjadi termasuk menjalankan container sebagai root secara tidak aman dan tanpa sengaja menyematkan secret di layer.

Berikut versi yang diperbaiki

```dockerfile
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project
COPY . .
RUN uv sync --locked --no-dev
```

Pada contoh sebelumnya kita melihat bahwa alih-alih memasang `uv` dari source, kita menyalin binary yang sudah dibangun dari image `ghcr.io/astral-sh/uv:latest`. Ini dikenal sebagai pola _builder_. Dengan pola ini kita tidak perlu mengirim semua tool yang dibutuhkan untuk mengompilasi kode kita, hanya binary akhir yang diperlukan untuk menjalankan aplikasi (`uv` dalam kasus ini).

Docker memiliki keterbatasan penting yang perlu diketahui. Pertama, container image sering khas platform --- image yang dibangun untuk `linux/amd64` tidak akan berjalan secara native di `linux/arm64` (Mac Apple Silicon) tanpa emulasi, yang lambat. Kedua, container Docker memerlukan kernel Linux, sehingga di macOS dan Windows, Docker sebenarnya menjalankan Linux VM ringan di balik layar, menambah overhead. Ketiga, isolasi Docker lebih lemah daripada VM --- container berbagi kernel host, yang menjadi kekhawatiran keamanan di lingkungan multi-tenant.

> Saat ini, lebih banyak proyek juga memanfaatkan nix untuk mengelola bahkan library dan aplikasi "system-wide" per proyek melalui [nix flake](https://serokell.io/blog/practical-nix-flakes).

<a id="configuration"></a>
# Configuration

Perangkat lunak secara inheren dapat dikonfigurasi. Pada kuliah [command line environment](/2026/command-line-environment/) kita melihat program menerima opsi melalui flag, environment variable atau bahkan berkas konfigurasi alias dotfiles. Ini berlaku bahkan untuk aplikasi yang lebih kompleks, dan ada pola mapan untuk mengelola konfigurasi dalam skala besar.
Konfigurasi perangkat lunak sebaiknya tidak disematkan dalam kode tetapi disediakan saat runtime.
Beberapa yang umum adalah environment variable dan berkas config.

Berikut contoh aplikasi yang dikonfigurasi melalui environment variable:

```python
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///local.db")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
API_KEY = os.environ["API_KEY"]  # Required - will raise if not set
```

Aplikasi juga dapat dikonfigurasi melalui berkas konfigurasi (misalnya, program Python yang memuat config melalui `yaml.load`), `config.yaml`:

```yaml
database:
  url: "postgresql://localhost/myapp"
  pool_size: 5
server:
  host: "0.0.0.0"
  port: 8080
  debug: false
```

Aturan praktis yang baik untuk memikirkan konfigurasi adalah bahwa codebase yang sama harus dapat di-deploy ke environment berbeda (development, staging, production) hanya dengan perubahan konfigurasi, bukan pernah dengan perubahan kode.

Di antara banyak opsi konfigurasi sering terdapat data sensitif seperti API key.
Secret perlu ditangani dengan hati-hati agar tidak terekspos secara tidak sengaja, dan tidak boleh disertakan dalam version control.


<a id="services--orchestration"></a>
# Service dan Orchestration

Aplikasi modern jarang berdiri sendiri. Aplikasi web tipikal mungkin membutuhkan database untuk penyimpanan persisten, cache untuk performa, message queue untuk tugas background, dan berbagai layanan pendukung lainnya. Alih-alih membundel semuanya menjadi satu aplikasi monolitik, arsitektur modern sering mendekomposisi fungsionalitas menjadi layanan terpisah yang dapat dikembangkan, di-deploy, dan diskalakan secara independen.

Sebagai contoh, jika kita menentukan bahwa aplikasi kita mungkin mendapat manfaat dari menggunakan cache, alih-alih membuat sendiri kita dapat memanfaatkan solusi yang sudah terbukti seperti [Redis](https://redis.io/) atau [Memcached](https://memcached.org/).
Kita dapat menyematkan Redis dalam dependency aplikasi kita dengan membangunnya sebagai bagian dari container, tetapi itu berarti menyelaraskan semua dependency antara Redis dan aplikasi kita yang bisa jadi menantang atau bahkan tidak mungkin.
Sebagai gantinya yang dapat kita lakukan adalah men-deploy setiap aplikasi secara terpisah dalam container-nya sendiri.
Ini umumnya disebut arsitektur microservice di mana setiap komponen berjalan sebagai layanan independen yang berkomunikasi melalui jaringan, biasanya melalui HTTP API.

[Docker Compose](https://docs.docker.com/compose/) adalah tool untuk mendefinisikan dan menjalankan aplikasi multi-container. Alih-alih mengelola container satu per satu, Anda mendeklarasikan semua layanan dalam satu berkas YAML dan mengorkestrasinya bersama. Sekarang aplikasi lengkap kita mencakup lebih dari satu container:

```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      - REDIS_URL=redis://cache:6379
    depends_on:
      - cache

  cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

Dengan `docker compose up`, kedua layanan mulai bersama, dan aplikasi web dapat terhubung ke Redis menggunakan hostname `cache` (DNS internal Docker menyelesaikan nama layanan secara otomatis).
Docker Compose memungkinkan kita mendeklarasikan bagaimana kita ingin men-deploy satu atau lebih layanan, dan menangani orkestrasi memulainya bersama, menyiapkan jaringan di antaranya, dan mengelola volume bersama untuk persistensi data.

Untuk deployment produksi, Anda sering ingin layanan docker compose Anda mulai otomatis saat boot dan restart ketika gagal. Pendekatan umum adalah menggunakan systemd untuk mengelola deployment docker compose:

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/myapp
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down

[Install]
WantedBy=multi-user.target
```

Berkas unit systemd ini memastikan aplikasi Anda mulai ketika sistem boot (setelah Docker siap), dan menyediakan kontrol standar seperti `systemctl start myapp`, `systemctl stop myapp`, dan `systemctl status myapp`.

Seiring kebutuhan deployment tumbuh lebih kompleks --- membutuhkan scalability di banyak mesin, fault tolerance ketika layanan crash, dan jaminan high availability --- organisasi beralih ke platform orkestrasi container canggih seperti Kubernetes (k8s), yang dapat mengelola ribuan container di kluster mesin. Meskipun demikian, Kubernetes memiliki kurva belajar yang curam dan overhead operasional yang signifikan, sehingga sering berlebihan untuk proyek yang lebih kecil.

Pengaturan multi-container ini sebagian dapat diwujudkan karena layanan modern berkomunikasi satu sama lain melalui API terstandar, dengan HTTP REST API. Misalnya, setiap kali sebuah program berinteraksi dengan penyedia LLM seperti OpenAI atau Anthropic, di balik layar program tersebut mengirim permintaan HTTP ke server mereka dan mengurai responsnya:

```console
$ curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 256,
         "messages": [{"role": "user", "content": "Explain containers vs VMs in one sentence."}]}'
```

<a id="publishing"></a>
# Publikasi

Setelah Anda menunjukkan kode Anda berfungsi, Anda mungkin tertarik mendistribusikannya agar orang lain dapat mengunduh dan memasangnya.
Distribusi mengambil banyak bentuk dan secara intrinsik terkait dengan bahasa pemrograman dan environment tempat Anda beroperasi.

Bentuk distribusi paling sederhana adalah mengunggah artifact agar orang dapat mengunduh dan memasangnya secara lokal.
Ini masih umum dan Anda dapat menemukannya di tempat seperti [arsip paket Ubuntu](http://archive.ubuntu.com/ubuntu/pool/main/), yang pada dasarnya adalah daftar direktori HTTP berisi berkas `.deb`.

Saat ini, GitHub telah menjadi platform de facto untuk mempublikasikan kode sumber dan artifact.
Meskipun kode sumber sering tersedia publik, GitHub Releases memungkinkan maintainer melampirkan binary yang sudah dibangun dan artifact lain ke versi yang diberi tag.


Package manager kadang mendukung pemasangan langsung dari GitHub, baik dari source maupun dari wheel yang sudah dibangun:

```console
# Install from source (will clone and build)
$ pip install git+https://github.com/psf/requests.git

# Install from a specific tag/branch
$ pip install git+https://github.com/psf/requests.git@v2.32.3

# Install a wheel directly from a GitHub release
$ pip install https://github.com/user/repo/releases/download/v1.0/package-1.0-py3-none-any.whl
```

Bahkan, sebagian bahasa seperti Go menggunakan model distribusi terdesentralisasi --- alih-alih repositori paket terpusat, modul Go didistribusikan langsung dari repositori kode sumbernya.
Path module seperti `github.com/gorilla/mux` menunjukkan di mana kode berada, dan `go get` mengambil langsung dari sana. Namun, sebagian besar package manager seperti `pip`, `cargo`, atau `brew` memiliki indeks terpusat proyek yang sudah dipaketkan untuk memudahkan distribusi dan pemasangan. Jika kita menjalankan

```console
$ uv pip install requests --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: requests==2.32.5 [compatible] (requests-2.32.5-py3-none-any.whl)
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl.metadata
DEBUG No cache entry for: https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl
```

kita melihat dari mana kita mengambil wheel `requests`. Perhatikan `py3-none-any` pada nama berkasnya --- ini berarti wheel tersebut bekerja dengan versi Python 3 mana pun, pada OS mana pun, pada arsitektur mana pun. Untuk paket dengan kode terkompilasi, wheel bersifat khas platform:

```console
$ uv pip install numpy --verbose --no-cache 2>&1 | grep -F '.whl'
DEBUG Selecting: numpy==2.2.1 [compatible] (numpy-2.2.1-cp312-cp312-macosx_14_0_arm64.whl)
```

Di sini `cp312-cp312-macosx_14_0_arm64` menunjukkan wheel ini khusus untuk CPython 3.12 di macOS 14+ untuk ARM64 (Apple Silicon). Jika Anda berada di platform berbeda, `pip` akan mengunduh wheel berbeda atau membangun dari source.

Sebaliknya, agar orang dapat menemukan paket yang kita buat, kita perlu mempublikasikannya ke salah satu registry tersebut.
Di Python, registry utamanya adalah [Python Package Index (PyPI)](https://pypi.org).
Seperti halnya pemasangan, ada beberapa cara mempublikasikan paket. Perintah `uv publish` menyediakan antarmuka modern untuk mengunggah paket ke PyPI:

```console
$ uv publish --publish-url https://test.pypi.org/legacy/
Publishing greeting-0.1.0.tar.gz
Publishing greeting-0.1.0-py3-none-any.whl
```

Di sini kita menggunakan [TestPyPI](https://test.pypi.org) --- registry paket terpisah yang dimaksudkan untuk menguji alur publishing Anda tanpa mengotori PyPI yang sebenarnya. Setelah diunggah, Anda dapat memasang dari TestPyPI:

```console
$ uv pip install --index-url https://test.pypi.org/simple/ greeting
```

Pertimbangan kunci saat mempublikasikan perangkat lunak adalah trust. Bagaimana pengguna memverifikasi bahwa paket yang mereka unduh benar-benar berasal dari Anda dan belum dimanipulasi? Registry paket menggunakan checksum untuk memverifikasi integritas, dan sebagian ekosistem mendukung penandatanganan paket untuk memberikan bukti kriptografis atas kepengarangan.

Bahasa yang berbeda memiliki registry paketnya sendiri: [crates.io](https://crates.io) untuk Rust, [npm](https://www.npmjs.com) untuk JavaScript, [RubyGems](https://rubygems.org) untuk Ruby, dan [Docker Hub](https://hub.docker.com) untuk container image. Sementara itu, untuk paket privat atau internal, organisasi sering men-deploy repositori paket mereka sendiri (seperti server PyPI privat atau registry Docker privat) atau menggunakan solusi terkelola dari penyedia cloud.

Men-deploy web service ke internet melibatkan infrastruktur tambahan: pendaftaran nama domain, konfigurasi DNS untuk mengarahkan domain Anda ke server Anda, dan sering kali reverse proxy seperti nginx untuk menangani HTTPS dan merutekan lalu lintas. Untuk use case yang lebih sederhana seperti dokumentasi atau situs statis, [GitHub Pages](https://pages.github.com/) menyediakan hosting gratis langsung dari sebuah repository.

<!--
## Documentation

So far we have emphasized the deliverable _artifact_ as the main output of packaging and shipping code.
In addition to the artifact, we need to document for users the code's functionality, installation instructions, and usage examples.

Tools like [Sphinx](https://www.sphinx-doc.org/) (Python) and [MkDocs](https://www.mkdocs.org/) can automatically generate browsable documentation from docstrings and markdown files, often hosted on services like [Read the Docs](https://readthedocs.org/).
For HTTP-based APIs, the [OpenAPI specification](https://www.openapis.org/) (formerly Swagger) provides a standard format for describing API endpoints, which tools can use to generate interactive documentation and client libraries automatically. -->


# Latihan

1. Simpan environment Anda dengan `printenv` ke sebuah berkas, buat venv, aktifkan, `printenv` ke berkas lain dan `diff before.txt after.txt`. Apa yang berubah di environment? Mengapa shell lebih memilih venv? (Petunjuk: lihat `$PATH` sebelum dan sesudah aktivasi.) Jalankan `which deactivate` dan nalar tentang apa yang dilakukan fungsi bash deactivate.
1. Buat paket Python dengan `pyproject.toml` dan pasang di virtual environment. Buat lockfile dan periksa isinya.
1. Pasang Docker dan gunakan untuk membangun situs kelas Missing Semester secara lokal menggunakan docker compose.
1. Tulis Dockerfile untuk aplikasi Python sederhana. Lalu tulis `docker-compose.yml` yang menjalankan aplikasi Anda bersama cache Redis.
1. Publikasikan paket Python ke TestPyPI (jangan publikasikan ke PyPI asli kecuali memang layak dibagikan!). Lalu bangun Docker image dengan paket tersebut dan push ke `ghcr.io`.
1. Buat situs web menggunakan [GitHub Pages](https://docs.github.com/en/pages/quickstart). Kredit (non-)tambahan: konfigurasikan dengan domain kustom.
