---
layout: lecture-id
title: "Code Quality"
description: >
  Pelajari formatting, linting, testing, continuous integration, dan lainnya.
thumbnail: /static/assets/thumbnails/2026/lec9.png
date: 2026-01-23
ready: true
video:
  aspect: 56.25
  id: XBiLUNx84CQ
lang: id
permalink: /id/2026/code-quality/
---

Ada berbagai tool dan teknik yang mendukung pengembang dalam menulis kode berkualitas tinggi. Pada kuliah ini, kami akan membahas:

- [Formatting](#formatting)
- [Linting](#linting)
- [Testing](#testing)
- [Pre-commit hooks](#pre-commit-hooks)
- [Continuous integration](#continuous-integration)
- [Command runners](#command-runners)

Sebagai topik bonus, kami juga akan membahas [regular expression](#regular-expressions), topik lintas bidang yang memiliki aplikasi dalam kualitas kode (misalnya, untuk menjalankan sebagian test yang cocok dengan suatu pola) serta domain lain seperti IDE (misalnya, untuk search and replace).

Banyak dari tool ini akan khas bahasa tertentu (misalnya, linter/formatter [Ruff](https://docs.astral.sh/ruff/) untuk Python). Dalam beberapa kasus, tool akan mendukung beberapa bahasa (misalnya, code formatter [Prettier](https://prettier.io/)). Namun konsepnya hampir universal --- Anda dapat menemukan code formatter, linter, library testing, dan sebagainya untuk bahasa pemrograman apa pun.

<a id="formatting"></a>
# Formatting

Code auto-formatter secara otomatis merapikan surface syntax. Dengan begitu, Anda dapat fokus pada masalah yang lebih dalam dan menantang, sementara tool auto-formatting menangani detail membosankan seperti konsistensi sintaks `'` versus `"` untuk string, adanya spasi di sekitar operator biner (`x + y` alih-alih `x+y`), pernyataan `import` dalam urutan terurut, dan menghindari baris yang terlalu panjang. Salah satu manfaat utama code formatter adalah formatter menstandarkan gaya kode di antara semua pengembang yang bekerja pada sebuah codebase.

Sebagian tool seperti Prettier [sangat dapat dikonfigurasi](https://prettier.io/docs/configuration); Anda sebaiknya memasukkan berkas konfigurasinya ke [version control](/2026/version-control/) untuk proyek Anda. Tool lain, seperti [Black](https://github.com/psf/black) dan [gofmt](https://pkg.go.dev/cmd/gofmt) memiliki kemampuan konfigurasi terbatas atau tidak sama sekali, untuk mengurangi [bikeshedding](https://en.wikipedia.org/wiki/Law_of_triviality).

Anda dapat menyiapkan [integrasi IDE](/2026/development-environment/#code-intelligence-and-language-servers) dengan code formatter Anda, sehingga kode Anda akan otomatis diformat saat Anda mengetik atau saat Anda menyimpan berkas. Anda juga dapat menambahkan berkas [EditorConfig](https://editorconfig.org/) ke proyek Anda, yang mengomunikasikan ke IDE Anda pengaturan tingkat proyek tertentu seperti ukuran indentasi untuk setiap jenis berkas.

<a id="linting"></a>
# Linting

Linter menjalankan static analysis (menganalisis kode Anda tanpa menjalankannya) untuk menemukan antipattern dan masalah potensial dalam kode Anda. Tool ini berjalan lebih dalam daripada autoformatter, melihat melampaui surface syntax. Kedalaman analisisnya berbeda-beda per tool.

Linter dilengkapi dengan daftar _rule_, dengan preset yang dapat dikonfigurasi pada tingkat proyek. Sebagian rule linter menghasilkan false positive, sehingga Anda dapat menonaktifkannya pada tingkat per-berkas atau per-baris.

Linter yang baik memiliki bantuan atau dokumentasi bawaan yang menjelaskan setiap rule linter --- apa yang dicari rule tersebut, mengapa hal itu buruk, dan apa alternatif yang lebih baik untuk pola kode tersebut. Misalnya, lihat dokumentasi untuk rule [SIM102](https://docs.astral.sh/ruff/rules/collapsible-if/) di [Ruff](https://docs.astral.sh/ruff/) yang menangkap pernyataan `if` bersarang yang tidak perlu dalam kode Python.

Sebagian linter tidak hanya dapat menandai masalah tetapi juga secara otomatis memperbaiki masalah tertentu untuk Anda.

Selain linter khas bahasa, tool lain yang mungkin berguna adalah [semgrep](https://github.com/semgrep/semgrep), sebuah tool "semantic grep" yang bekerja pada tingkat AST (bukan tingkat karakter, seperti grep) dan mendukung banyak bahasa. Anda dapat menggunakan semgrep untuk menulis rule linter kustom dengan mudah bagi proyek Anda. Misalnya, jika Anda ingin mencegah `subprocess.Popen(..., shell=True)` yang berbahaya di Python, Anda dapat menemukan pola kode tersebut dengan:

```bash
semgrep -l python -e "subprocess.Popen(..., shell=True, ...)"
```

<a id="testing"></a>
# Testing

Software testing adalah teknik standar untuk meningkatkan keyakinan Anda pada kebenaran kode. Anda menulis kode, lalu Anda menulis kode yang menjalankan kode yang Anda tulis dan memunculkan error jika kode tersebut tidak bekerja seperti yang diharapkan.

Anda dapat menulis test untuk potongan kode pada tingkat granularitas berbeda: _unit test_ untuk fungsi individual, _integration test_ untuk interaksi antara module atau layanan, dan _functional test_ untuk skenario end-to-end. Anda dapat melakukan _test-driven development_, di mana Anda menulis test sebelum menulis kode implementasi apa pun. Ketika Anda menemukan bug dalam kode Anda, Anda dapat menulis _regression test_, sehingga Anda akan menangkapnya jika fungsionalitas itu pernah rusak di masa depan. Anda dapat menulis _property-based test_, yang dipelopori di [QuickCheck](https://hackage.haskell.org/package/QuickCheck) pada Haskell, dan diimplementasikan di banyak library, seperti [Hypothesis](https://hypothesis.readthedocs.io/) untuk Python. Pendekatan testing mana yang tepat bergantung pada proyek Anda; kemungkinan besar Anda akan mengadopsi kombinasi dari beberapa pendekatan.

Jika program Anda memiliki dependency eksternal seperti database atau web API, mungkin berguna untuk melakukan _mock_ pada dependency tersebut dalam test Anda, alih-alih membiarkan kode Anda berinteraksi dengan dependency pihak ketiga pada saat test.

## Code coverage

Code coverage adalah metrik yang dapat Anda gunakan untuk mengukur seberapa baik test Anda. Code coverage melihat baris kode mana yang dieksekusi ketika test Anda dijalankan, sehingga Anda dapat memastikan Anda mencakup semua jalur kode. Tool code coverage dapat menunjukkan coverage baris demi baris untuk memandu Anda menulis test. Layanan seperti [Codecov](https://app.codecov.io) menyediakan antarmuka web untuk melacak dan melihat code coverage sepanjang riwayat sebuah proyek.

Seperti metrik apa pun, code coverage tidak sempurna; jangan terlalu berpatokan pada coverage, fokuslah menulis test berkualitas tinggi.

<a id="pre-commit-hooks"></a>
# Pre-commit hooks

[hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks) pre-commit Git, yang dipermudah oleh framework [pre-commit](https://pre-commit.com/), secara otomatis menjalankan kode yang ditentukan pengguna sebelum setiap commit Git. Proyek umumnya menggunakan pre-commit hook untuk menjalankan formatter dan linter, dan kadang test, secara otomatis sebelum setiap commit, untuk memastikan kode yang di-commit sesuai dengan gaya kode proyek dan bebas dari masalah tertentu.

<a id="continuous-integration"></a>
# Continuous integration

Layanan continuous integration (CI) seperti [GitHub Actions](https://github.com/features/actions) dapat menjalankan skrip untuk Anda setiap kali Anda push kode (atau pada setiap pull request, atau sesuai jadwal). Pengembang umumnya menggunakan layanan CI untuk menjalankan tool kualitas kode termasuk formatter, linter, dan test. Untuk bahasa terkompilasi, Anda dapat memastikan kode dapat dikompilasi; untuk bahasa bertipe statis, Anda dapat memastikan kode lolos type check. Menjalankan CI setiap push commit baru dapat menangkap error yang masuk ke versi utama kode; menjalankan pada pull request dapat menangkap masalah pada kiriman kontributor; menjalankan sesuai jadwal dapat menangkap masalah dengan dependency eksternal (misalnya, seorang pengembang tanpa sengaja merilis perubahan yang merusak sebagai [kompatibel semver](/2026/shipping-code/#releases--versioning)).

Karena skrip CI berjalan terpisah dari mesin pengembang, Anda dapat dengan mudah menjalankan job berjalan lama di sana. Ini dapat dimanfaatkan, misalnya, untuk menjalankan _matrix_ test di berbagai sistem operasi dan versi bahasa pemrograman untuk memastikan perangkat lunak bekerja dengan baik di semuanya.

Umumnya, skrip yang berjalan di CI tidak akan langsung membuat perubahan pada kode Anda: skrip akan menjalankan tool dalam mode "check-only" alih-alih mode "fix", sehingga misalnya, auto-formatter akan memunculkan error ketika kode tidak sesuai format.

Repository sering menyertakan [status badge](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge) di README mereka, yang menampilkan status CI dan informasi lain seperti code coverage. Misalnya, berikut adalah status build Missing Semester saat ini.

[![Build Status](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/build.yml) [![Links Status](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml/badge.svg)](https://github.com/missing-semester/missing-semester/actions/workflows/links.yml)

> [Pemeriksa tautan](https://github.com/missing-semester/missing-semester/blob/master/.github/workflows/links.yml) kami, yang menggunakan GitHub Action [proof-html](https://github.com/anishathalye/proof-html) sering gagal, biasanya karena masalah dengan situs web pihak ketiga. Meskipun demikian, tool ini telah membantu kami menangkap dan memperbaiki banyak tautan rusak (kadang karena typo, sebagian besar karena situs web memindahkan konten tanpa menambahkan redirect atau situs web yang menghilang).

Cara yang baik untuk mempelajari seluk-beluk layanan CI, formatter, linter, dan library testing adalah dengan contoh. Temukan proyek open-source berkualitas tinggi di GitHub---semakin mirip dengan proyek Anda dalam hal bahasa pemrograman, domain, ukuran dan cakupan, dan sebagainya, semakin baik---dan pelajari `pyproject.toml`, `.github/workflows/`, `DEVELOPMENT.md`, dan berkas relevan lainnya.

## Continuous deployment

Continuous deployment memanfaatkan infrastruktur CI untuk benar-benar _men-deploy_ perubahan. Misalnya, repository Missing Semester menggunakan continuous deployment ke GitHub pages sehingga setiap kali kami `git push` catatan kuliah yang diperbarui, situs dibangun dan di-deploy secara otomatis. Anda dapat membangun jenis [artifact](/2026/shipping-code/) lain di CI, seperti binary untuk aplikasi atau Docker image untuk layanan.

<a id="command-runners"></a>
# Command runners

Command runner seperti [just](https://github.com/casey/just) menyederhanakan tugas menjalankan perintah dalam konteks sebuah proyek. Saat Anda membangun infrastruktur kualitas kode untuk proyek Anda, Anda tidak ingin membuat pengembang Anda menghafal perintah seperti `uv run ruff check --fix`. Dengan command runner, itu bisa berubah menjadi `just lint`, dan Anda dapat memiliki pemanggilan serupa seperti `just format`, `just typecheck`, dsb., untuk semua tool berbeda yang mungkin ingin dijalankan pengembang untuk proyek Anda.

Sebagian project atau package manager khas bahasa memiliki dukungan bawaan untuk fungsionalitas semacam itu, yang berarti Anda tidak perlu menggunakan tool yang language-agnostic seperti `just`. Misalnya, bagian `scripts` pada `package.json` untuk [npm](https://nodejs.org/en/learn/getting-started/an-introduction-to-the-npm-package-manager) (Node.js) dan bagian `tool.hatch.envs.*.scripts` pada `pyproject.toml` untuk [Hatch](https://hatch.pypa.io/) (Python) mendukung fungsionalitas ini.

<a id="regular-expressions"></a>
# Regular expressions

_Regular expression_, yang umumnya disingkat "regex", adalah bahasa yang digunakan untuk merepresentasikan kumpulan string. Pola regex umumnya digunakan untuk pattern matching dalam berbagai konteks seperti tool command-line dan IDE. Misalnya, [ag](https://github.com/ggreer/the_silver_searcher) mendukung pola regex untuk pencarian di seluruh codebase (misalnya, `ag "import .* as .*"` akan menemukan semua import yang diganti namanya di Python), dan [go test](https://pkg.go.dev/cmd/go#hdr-Test_packages) mendukung opsi `-run [regexp]` untuk memilih sebagian test. Lebih jauh lagi, bahasa pemrograman memiliki dukungan bawaan atau library pihak ketiga untuk regex matching, sehingga Anda dapat menggunakan regex untuk fungsionalitas seperti pattern matching, validasi, dan parsing.

Untuk membantu membangun intuisi, berikut beberapa contoh pola regex. Pada kuliah ini, kami menggunakan [sintaks regex Python](https://docs.python.org/3/library/re.html). Ada banyak ragam regex, dengan variasi kecil di antaranya, terutama pada fungsionalitas yang lebih canggih. Anda dapat menggunakan penguji regex daring seperti [regex101](https://regex101.com/) untuk mengembangkan dan men-debug regular expression.

- `abc` --- cocok dengan literal "abc".
- `missing|semester` --- cocok dengan string "missing" atau string "semester".
- `\d{4}-\d{2}-\d{2}` --- cocok dengan tanggal dalam format YYYY-MM-DD, seperti "2026-01-14". Selain memastikan bahwa string terdiri dari empat digit, tanda dash, dua digit, tanda dash, dan dua digit, pola ini tidak memvalidasi tanggal, sehingga "2026-01-99" juga cocok dengan pola regex ini.
- `.+@.+` --- cocok dengan alamat email, string yang memuat beberapa teks, lalu "@", lalu beberapa teks lagi. Ini hanya melakukan validasi paling dasar dan cocok dengan string seperti "nonsense@@@email". Regex yang cocok dengan alamat email tanpa false positive atau false negative [ada](https://pdw.ex-parrot.com/Mail-RFC822-Address.html) tetapi tidak praktis.

## Sintaks regex

Anda dapat menemukan panduan komprehensif tentang sintaks regex di [dokumentasi ini](https://docs.python.org/3/library/re.html#regular-expression-syntax) (atau salah satu dari banyak sumber lain yang tersedia daring). Berikut beberapa blok penyusun dasar:

- `abc` cocok dengan string literal, ketika karakternya tidak memiliki makna khusus (dalam contoh ini, "abc")
- `.` cocok dengan satu karakter apa pun
- `[abc]` cocok dengan satu karakter yang termuat dalam kurung siku (dalam contoh ini, "a", "b", atau "c")
- `[^abc]` cocok dengan satu karakter kecuali yang termuat dalam kurung siku (misalnya, "d")
- `[a-f]` cocok dengan satu karakter yang termuat dalam rentang yang ditunjukkan dalam kurung siku (misalnya, "c", tetapi bukan "q")
- `a|b` cocok dengan salah satu pola (misalnya, "a" atau "b")
- `\d` cocok dengan karakter digit apa pun (misalnya, "3")
- `\w` cocok dengan karakter word apa pun (misalnya, "x")
- `\b` cocok dengan _boundary_ word apa pun (misalnya, pada string "missing semester", cocok tepat sebelum "m", tepat setelah "g", tepat sebelum "s", dan tepat setelah "r")
- `(...)` cocok dengan grup sebuah pola
- `...?` cocok dengan nol atau satu dari sebuah pola, seperti `words?` untuk mencocokkan "word" atau "words"
- `...*` cocok dengan berapa pun jumlah dari sebuah pola, seperti `.*` untuk mencocokkan berapa pun jumlah karakter apa pun
- `...+` cocok dengan satu atau lebih dari sebuah pola, seperti `\d+` untuk mencocokkan jumlah digit bukan nol
- `...{N}` cocok dengan tepat N dari sebuah pola, seperti `\d{4}` untuk 4 digit
- `\.` cocok dengan literal "."
- `\\` cocok dengan literal "\\"
- `^` cocok dengan awal baris
- `$` cocok dengan akhir baris

## Capture group dan reference

Jika Anda menggunakan grup regex `(...)`, Anda dapat merujuk sub-bagian dari kecocokan untuk keperluan ekstraksi atau search-and-replace. Misalnya, untuk mengekstrak hanya bulan dari tanggal bergaya YYYY-MM-DD, Anda dapat menggunakan kode Python berikut:

```python
>>> import re
>>> re.match(r"\d{4}-(\d{2})-\d{2}", "2026-01-14").group(1)
'01'
```

Di text editor Anda, Anda dapat menggunakan reference capture group dalam pola penggantian. Sintaksnya mungkin berbeda antar IDE. Misalnya, di VS Code, Anda dapat menggunakan variabel seperti `$1`, `$2`, dsb., dan di Vim, Anda dapat menggunakan `\1`, `\2`, dsb., untuk merujuk grup.

## Keterbatasan

[Regular language](https://en.wikipedia.org/wiki/Regular_language) itu kuat tetapi terbatas; ada kelas string yang tidak dapat dinyatakan sebagai regex standar (misalnya, [tidak mungkin](https://en.wikipedia.org/wiki/Pumping_lemma_for_regular_languages) menulis regular expression yang cocok dengan himpunan string {a^n b^n \| n &ge; 0}, yaitu himpunan string sejumlah "a" diikuti dengan jumlah "b" yang sama; lebih praktisnya, bahasa seperti HTML bukanlah regular language). Dalam praktiknya, mesin regex modern mendukung fitur seperti lookahead dan backreference yang memperluas dukungan melampaui regular language, dan fitur tersebut praktis sangat berguna, tetapi penting untuk mengetahui bahwa kemampuan ekspresifnya tetap terbatas. Untuk bahasa yang lebih canggih, Anda mungkin perlu menggunakan jenis parser yang lebih mumpuni (untuk satu contoh, lihat [pyparsing](https://github.com/pyparsing/pyparsing), sebuah parser [PEG](https://en.wikipedia.org/wiki/Parsing_expression_grammar)).

## Mempelajari regex

Kami menyarankan mempelajari dasar-dasarnya (apa yang telah kami bahas pada kuliah ini), lalu melihat referensi regex saat Anda membutuhkannya, alih-alih menghafal seluruh bahasanya.

Tool AI percakapan dapat efektif membantu Anda menghasilkan pola regex. Misalnya, coba beri prompt ke LLM favorit Anda dengan kueri berikut:

```
Write a Python-style regex pattern that matches the requested path from log lines from Nginx. Here is an example log line:

169.254.1.1 - - [09/Jan/2026:21:28:51 +0000] "GET /feed.xml HTTP/2.0" 200 2995 "-" "python-requests/2.32.3"
```

# Latihan

1. Konfigurasikan formatter, linter, dan pre-commit hook untuk proyek yang sedang Anda kerjakan. Jika Anda memiliki banyak error: autoformatting seharusnya menangani error format. Untuk error linter, coba gunakan [AI agent](/2026/agentic-coding/) untuk memperbaiki semua error linter tersebut. Pastikan AI agent dapat menjalankan linter dan mengamati hasilnya, sehingga agent dapat berjalan dalam loop iteratif untuk memperbaiki semua masalah. Periksa hasilnya dengan cermat untuk memastikan AI tidak merusak kode Anda!
1. Pelajari library testing untuk bahasa yang Anda kuasai dan tulis unit test untuk proyek yang sedang Anda kerjakan. Jalankan tool code coverage, hasilkan laporan coverage berformat HTML, dan amati hasilnya. Dapatkah Anda menemukan baris-baris yang tercakup? Code coverage Anda kemungkinan akan sangat rendah. Coba tulis beberapa test secara manual untuk meningkatkannya. Coba gunakan [AI agent](/2026/agentic-coding/) untuk meningkatkan coverage; pastikan coding agent dapat menjalankan test dengan coverage dan menghasilkan laporan coverage baris demi baris, sehingga agent mengetahui di mana harus fokus. Apakah test yang dihasilkan AI benar-benar bagus?
1. Siapkan continuous integration untuk berjalan pada setiap push bagi proyek yang sedang Anda kerjakan. Buat CI menjalankan formatting, linting, dan test. Rusak kode Anda dengan sengaja (misalnya, masukkan pelanggaran linter), dan pastikan CI menangkapnya.
1. Coba tulis [pola regex](#regular-expressions) dan gunakan [tool command-line](/2026/course-shell/) `grep` untuk menemukan kemunculan `subprocess.Popen(..., shell=True)` di kode Anda. Sekarang, coba "rusak" pola regex tersebut. Apakah [semgrep](#linting) tetap berhasil mencocokkan kode berbahaya yang membuat pemanggilan grep Anda gagal?
1. Berlatihlah regex search-and-replace di IDE atau text editor Anda dengan mengganti [penanda bullet Markdown](https://spec.commonmark.org/0.31.2/#bullet-list-marker) `-` dengan penanda bullet `*` pada [catatan kuliah ini](https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/code-quality.md). Perhatikan bahwa hanya mengganti semua karakter "-" di berkas itu akan salah, karena ada banyak penggunaan karakter tersebut yang bukan penanda bullet.
1. Tulis regex untuk menangkap nama dari struktur JSON berbentuk `{"name": "Alyssa P. Hacker", "college": "MIT"}` (misalnya, `Alyssa P. Hacker`, dalam contoh ini). Petunjuk: pada percobaan pertama Anda, Anda mungkin akhirnya menulis regex yang mengekstrak `Alyssa P. Hacker", "college": "MIT`; baca tentang greedy quantifier di [dokumentasi regex Python](https://docs.python.org/3/library/re.html) untuk mencari tahu cara memperbaikinya.
    1. Buat pola regex tetap bekerja bahkan dalam situasi di mana nama memuat karakter `"` (tanda kutip ganda dapat di-escape dalam JSON dengan `\"`).
    1. Kami **tidak** menyarankan menggunakan regular expression untuk masalah parsing yang canggih dalam praktik. Cari tahu cara menggunakan parser JSON bahasa pemrograman Anda untuk tugas ini. Tulis program command-line yang menerima sebagai input, pada stdin, struktur JSON berbentuk seperti dijelaskan di atas, dan mengeluarkan, pada stdout, nama tersebut. Anda seharusnya hanya membutuhkan beberapa baris kode untuk melakukan ini. Di Python, Anda dapat melakukannya dengan mudah dalam satu baris kode selain `import json`.
