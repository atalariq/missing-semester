---
layout: lecture-id
title: "Development Environment dan Tool"
description: >
  Pelajari IDE, Vim, language server, dan tool development dengan bantuan AI.
thumbnail: /static/assets/thumbnails/2026/lec3.png
date: 2026-01-14
ready: true
video:
  aspect: 56.25
  id: QnM1nVzrkx8
lang: id
permalink: /id/2026/development-environment/
---

Sebuah _development environment_ adalah sekumpulan tool untuk mengembangkan perangkat lunak. Di jantung development environment terdapat fungsionalitas text editing, beserta fitur pendamping seperti syntax highlighting, type checking, code formatting, dan autocomplete. _Integrated development environment_ (IDE) seperti [VS Code][vs-code] menyatukan seluruh fungsionalitas ini ke dalam satu aplikasi. Workflow pengembangan berbasis terminal menggabungkan tool seperti [tmux](https://github.com/tmux/tmux) (terminal multiplexer), [Vim](https://www.vim.org/) (text editor), [Zsh](https://www.zsh.org/) (shell), dan tool command-line khas bahasa tertentu, seperti [Ruff](https://docs.astral.sh/ruff/) (linter dan code formatter Python) dan [Mypy](https://mypy-lang.org/) (type checker Python).

IDE dan workflow berbasis terminal masing-masing memiliki kekuatan dan kelemahannya. Misalnya, IDE grafis bisa lebih mudah dipelajari, dan IDE saat ini umumnya memiliki integrasi AI out-of-the-box yang lebih baik seperti autocomplete AI; di sisi lain, workflow berbasis terminal bersifat ringan, dan bisa menjadi satu-satunya pilihan Anda di lingkungan di mana Anda tidak memiliki GUI atau tidak dapat memasang perangkat lunak. Kami menyarankan Anda membangun keakraban dasar dengan keduanya dan menguasai setidaknya satu. Jika Anda belum memiliki IDE favorit, kami menyarankan memulai dengan [VS Code][vs-code].

Pada kuliah ini, kami akan membahas:

- [Text editing and Vim](#text-editing-and-vim)
- [Code intelligence and language servers](#code-intelligence-and-language-servers)
- [AI-powered development](#ai-powered-development)
- [Extensions and other IDE functionality](#extensions-and-other-ide-functionality)

[vs-code]: https://code.visualstudio.com/

<a id="text-editing-and-vim"></a>
# Penyuntingan Teks dan Vim

Saat memprogram, Anda menghabiskan sebagian besar waktu Anda bernavigasi melalui kode, membaca potongan kode, dan membuat edit pada kode, bukan menulis aliran panjang atau membaca berkas dari atas ke bawah. [Vim] adalah text editor yang dioptimalkan untuk distribusi tugas seperti ini.

**Filosofi Vim.** Vim memiliki gagasan indah sebagai fondasinya: antarmukanya sendiri adalah sebuah bahasa pemrograman, yang dirancang untuk bernavigasi dan mengedit teks. Ketukan tombol (dengan nama mnemonik) adalah perintah, dan perintah-perintah ini dapat dikomposisikan. Vim menghindari penggunaan mouse, karena terlalu lambat; Vim bahkan menghindari penggunaan tombol panah karena memerlukan terlalu banyak gerakan. Hasilnya: sebuah editor yang terasa seperti brain-computer interface dan sesuai dengan kecepatan berpikir Anda.

**Dukungan Vim di perangkat lunak lain.** Anda tidak harus menggunakan [Vim] itu sendiri untuk memanfaatkan gagasan di intinya. Banyak program yang melibatkan segala bentuk text editing mendukung "Vim mode", baik sebagai fungsionalitas bawaan maupun sebagai plugin. Misalnya, VS Code memiliki plugin [VSCodeVim](https://marketplace.visualstudio.com/items?itemName=vscodevim.vim), Zsh memiliki [dukungan bawaan](https://zsh.sourceforge.io/Guide/zshguide04.html) untuk emulasi Vim, dan bahkan Claude Code memiliki [dukungan bawaan](https://code.claude.com/docs/en/interactive-mode#vim-editor-mode) untuk mode editor Vim. Kemungkinan besar tool apa pun yang Anda gunakan yang melibatkan text editing mendukung Vim mode dengan satu cara atau lainnya.

## Modal editing

Vim adalah _modal editor_: Vim memiliki mode operasi berbeda untuk kelas tugas yang berbeda.

- **Normal**: untuk bergerak di dalam berkas dan membuat edit
- **Insert**: untuk menyisipkan teks
- **Replace**: untuk mengganti teks
- **Visual** (biasa, baris, atau blok): untuk memilih blok teks
- **Command-line**: untuk menjalankan sebuah perintah

Ketukan tombol memiliki arti berbeda pada mode operasi berbeda. Misalnya, huruf `x` pada mode Insert hanya akan menyisipkan karakter literal "x", tetapi pada mode Normal, huruf itu akan menghapus karakter di bawah kursor, dan pada mode Visual, huruf itu akan menghapus seleksi.

Dalam konfigurasi defaultnya, Vim menampilkan mode saat ini di kiri bawah. Mode awal/default adalah mode Normal. Anda umumnya akan menghabiskan sebagian besar waktu Anda antara mode Normal dan mode Insert.

Anda mengubah mode dengan menekan `<ESC>` (tombol escape) untuk beralih dari mode apa pun kembali ke mode Normal. Dari mode Normal, masuk ke mode Insert dengan `i`, mode Replace dengan `R`, mode Visual dengan `v`, mode Visual Line dengan `V`, mode Visual Block dengan `<C-v>` (Ctrl-V, kadang juga ditulis `^V`), dan mode Command-line dengan `:`.

Anda menggunakan tombol `<ESC>` cukup sering saat menggunakan Vim: pertimbangkan memetakan ulang Caps Lock ke Escape ([instruksi macOS](https://vim.fandom.com/wiki/Map_caps_lock_to_escape_in_macOS)) atau membuat [pemetaan alternatif](https://vim.fandom.com/wiki/Avoid_the_escape_key#Mappings) untuk `<ESC>` dengan rangkaian tombol yang sederhana.

## Dasar-dasar: menyisipkan teks

Dari mode Normal, tekan `i` untuk masuk ke mode Insert. Sekarang, Vim berperilaku seperti text editor lain, sampai Anda menekan `<ESC>` untuk kembali ke mode Normal. Ini, beserta dasar-dasar yang dijelaskan di atas, adalah semua yang Anda butuhkan untuk mulai mengedit berkas menggunakan Vim (meskipun tidak terlalu efisien, jika Anda menghabiskan seluruh waktu Anda mengedit dari mode Insert).

## Antarmuka Vim adalah sebuah bahasa pemrograman

Antarmuka Vim adalah sebuah bahasa pemrograman. Ketukan tombol (dengan nama mnemonik) adalah perintah, dan perintah-perintah ini _dapat dikomposisikan_. Ini memungkinkan pergerakan dan edit yang efisien, terutama setelah perintah-perintah tersebut menjadi muscle memory, sama seperti mengetik menjadi sangat efisien setelah Anda menguasai tata letak keyboard Anda.

### Berpindah Posisi

Anda sebaiknya menghabiskan sebagian besar waktu Anda di mode Normal, menggunakan perintah movement untuk bernavigasi di berkas. Movement di Vim juga disebut "noun", karena merujuk pada potongan-potongan teks.

- Movement dasar: `hjkl` (kiri, bawah, atas, kanan)
- Kata: `w` (kata berikutnya), `b` (awal kata), `e` (akhir kata)
- Baris: `0` (awal baris), `^` (karakter pertama yang bukan whitespace), `$` (akhir baris)
- Layar: `H` (bagian atas layar), `M` (bagian tengah layar), `L` (bagian bawah layar)
- Scroll: `Ctrl-u` (ke atas), `Ctrl-d` (ke bawah)
- Berkas: `gg` (awal berkas), `G` (akhir berkas)
- Line numbers: `:{number}<CR>` atau `{number}G` (baris {number})
    - `<CR>` merujuk pada tombol carriage return / enter
- Misc: `%` (item pasangannya, seperti tanda kurung atau kurawal)
- Find: `f{character}`, `t{character}`, `F{character}`, `T{character}`
    - mencari/menuju {character} ke depan/ke belakang pada baris saat ini
    - `,` / `;` untuk bernavigasi antar kecocokan
- Search: `/{regex}`, `n` / `N` untuk bernavigasi antar kecocokan

### Memilih Teks

Mode visual:

- Visual: `v`
- Visual Line: `V`
- Visual Block: `Ctrl-v`

Anda dapat menggunakan tombol movement untuk membuat seleksi.

### Penyuntingan

Segala sesuatu yang dulu Anda lakukan dengan mouse, sekarang Anda lakukan dengan keyboard menggunakan perintah editing yang dapat dikomposisikan dengan perintah movement. Di sinilah antarmuka Vim mulai terlihat seperti bahasa pemrograman. Perintah editing Vim juga disebut "verb", karena verb bekerja pada noun.

- `i` masuk ke mode Insert
    - tetapi untuk memanipulasi/menghapus teks, Anda ingin menggunakan sesuatu yang lebih dari backspace
- `o` / `O` menyisipkan baris di bawah / di atas
- `d{motion}` menghapus {motion}
    - misalnya `dw` adalah menghapus kata, `d$` adalah menghapus hingga akhir baris, `d0` adalah menghapus hingga awal baris
- `c{motion}` mengubah {motion}
    - misalnya `cw` adalah mengubah kata
    - seperti `d{motion}` diikuti `i`
- `x` menghapus karakter (setara dengan `dl`)
- `s` mengganti karakter (setara dengan `cl`)
- Mode Visual + manipulasi
    - pilih teks, `d` untuk menghapusnya atau `c` untuk mengubahnya
- `u` untuk undo, `<C-r>` untuk redo
- `y` untuk menyalin / "yank" (beberapa perintah lain seperti `d` juga menyalin)
- `p` untuk paste
- Masih banyak yang bisa dipelajari: misalnya, `~` membalik kapitalisasi sebuah karakter, dan `J` menyatukan baris-baris

### Count dan Jumlah Pengulangan

Anda dapat menggabungkan noun dan verb dengan sebuah count, yang akan melakukan aksi tertentu sejumlah kali.

- `3w` bergerak maju 3 kata
- `5j` bergerak turun 5 baris
- `7dw` menghapus 7 kata

### Modifiers

Anda dapat menggunakan modifier untuk mengubah makna sebuah noun. Beberapa modifier adalah `i`, yang berarti "inner" atau "inside", dan `a`, yang berarti "around".

- `ci(` ubah isi di dalam pasangan tanda kurung saat ini
- `ci[` ubah isi di dalam pasangan tanda kurung siku saat ini
- `da'` hapus string berkutip tunggal, termasuk tanda kutip tunggal di sekelilingnya

## Menggabungkan semuanya

Berikut implementasi [fizz buzz](https://en.wikipedia.org/wiki/Fizz_buzz) yang rusak:

```python
def fizz_buzz(limit):
    for i in range(limit):
        if i % 3 == 0:
            print("fizz", end="")
        if i % 5 == 0:
            print("fizz", end="")
        if i % 3 and i % 5:
            print(i, end="")
        print()

def main():
    fizz_buzz(20)
```

Kami menggunakan rangkaian perintah berikut untuk memperbaiki masalahnya, dimulai dari mode Normal:

- Main tidak pernah dipanggil
    - `G` untuk melompat ke akhir berkas
    - `o` untuk **o**pen a new line below (membuka baris baru di bawah)
    - Ketik `if __name__ == "__main__": main()`
        - Jika editor Anda memiliki dukungan bahasa Python, editor mungkin melakukan auto-indentation untuk Anda di mode Insert
    - `<ESC>` untuk kembali ke mode Normal
- Dimulai dari 0 alih-alih 1
    - `/` diikuti `range` dan `<CR>` untuk mencari "range"
    - `ww` untuk maju dua **w**ord (Anda juga dapat menggunakan `2w`, tetapi dalam praktiknya, untuk count kecil biasanya mengulang tombolnya alih-alih menggunakan fungsionalitas count)
    - `i` untuk beralih ke mode **i**nsert, lalu tambahkan `1,`
    - `<ESC>` untuk kembali ke mode Normal
    - `e` untuk melompat ke **e**nd of the next word (akhir kata berikutnya)
    - `a` untuk mulai **a**ppending text, lalu tambahkan `+ 1`
    - `<ESC>` untuk kembali ke mode Normal
- Mencetak "fizz" untuk kelipatan 5
    - `:6<CR>` untuk menuju baris 6
    - `ci"` untuk **c**hange **i**nside the '**"**', ubah menjadi `"buzz"`
    - `<ESC>` untuk kembali ke mode Normal

## Mempelajari Vim

Cara terbaik mempelajari Vim adalah mempelajari dasar-dasarnya (yang telah kita bahas sejauh ini) lalu cukup mengaktifkan Vim mode di semua perangkat lunak Anda dan mulai menggunakannya dalam praktik. Hindari godaan untuk menggunakan mouse atau tombol panah; pada sebagian editor, Anda dapat melepas keybinding tombol panah untuk memaksa diri Anda membangun kebiasaan yang baik.

### Sumber daya tambahan

- [Kuliah Vim](/2020/editors/) dari iterasi kelas sebelumnya --- kami membahas Vim lebih mendalam di sana
- `vimtutor` adalah tutorial yang terpasang bersama Vim --- jika Vim terpasang, Anda seharusnya dapat menjalankan `vimtutor` dari shell Anda
- [Vim Adventures](https://vim-adventures.com/) adalah game untuk mempelajari Vim
- [Vim Tips Wiki](https://vim.fandom.com/wiki/Vim_Tips_Wiki)
- [Vim Advent Calendar](https://vimways.org/2019/) memiliki berbagai tip Vim
- [VimGolf](https://www.vimgolf.com/) adalah [code golf](https://en.wikipedia.org/wiki/Code_golf), tetapi bahasa pemrogramannya adalah UI Vim
- [Vi/Vim Stack Exchange](https://vi.stackexchange.com/)
- [Vim Screencasts](http://vimcasts.org/)
- [Practical Vim](https://pragprog.com/titles/dnvim2/) (buku)

[Vim]: https://www.vim.org/

<a id="code-intelligence-and-language-servers"></a>
# Code Intelligence dan Language Server

IDE umumnya menawarkan dukungan khas bahasa tertentu yang memerlukan pemahaman semantik atas kode melalui ekstensi IDE yang terhubung ke _language server_ yang mengimplementasikan [Language Server Protocol](https://microsoft.github.io/language-server-protocol/). Misalnya, [ekstensi Python untuk VS Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python) bergantung pada [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance), dan [ekstensi Go untuk VS Code](https://marketplace.visualstudio.com/items?itemName=golang.go) bergantung pada [gopls](https://go.dev/gopls/) pihak pertama. Dengan memasang ekstensi dan language server untuk bahasa yang Anda gunakan, Anda dapat mengaktifkan banyak fitur khas bahasa di IDE Anda, seperti:

- **Code completion.** Autocomplete dan autosuggest yang lebih baik, seperti kemampuan melihat field dan method sebuah objek setelah mengetik `object.`.
- **Inline documentation.** Melihat dokumentasi saat hover dan saat autosuggest.
- **Jump-to-definition.** Melompat dari tempat penggunaan ke definisinya, seperti kemampuan berpindah dari referensi field `object.field` ke definisi field tersebut.
- **Find references.** Kebalikan dari yang di atas, menemukan semua tempat di mana item tertentu seperti field atau tipe dirujuk.
- **Bantuan import.** Menata import, menghapus import yang tidak terpakai, menandai import yang hilang.
- **Kualitas kode.** Tool ini dapat digunakan secara mandiri, tetapi fungsionalitas ini sering juga disediakan oleh language server. Code formatting melakukan auto-indent dan auto-format pada kode, serta type checker dan linter menemukan error pada kode Anda, saat Anda mengetik. Kami akan membahas kelas fungsionalitas ini lebih mendalam pada [kuliah tentang code quality](/2026/code-quality/).

## Mengonfigurasi language server

Untuk sebagian bahasa, yang perlu Anda lakukan hanyalah memasang ekstensi dan language server, dan semuanya sudah siap. Untuk bahasa lain, agar memperoleh manfaat maksimal dari language server, Anda perlu memberi tahu IDE tentang environment Anda. Misalnya, mengarahkan VS Code ke [environment Python](https://code.visualstudio.com/docs/python/environments) Anda akan memungkinkan language server melihat paket yang terpasang. Environment dibahas lebih mendalam pada [kuliah tentang packaging dan shipping code](/2026/shipping-code/).

Bergantung pada bahasanya, mungkin ada beberapa pengaturan yang dapat Anda konfigurasi untuk language server Anda. Misalnya, dengan dukungan Python di VS Code, Anda dapat menonaktifkan static type checking untuk proyek yang tidak memanfaatkan type annotation opsional Python.

<a id="ai-powered-development"></a>
# Development dengan Bantuan AI

Sejak diperkenalkannya [GitHub Copilot][github-copilot] yang menggunakan [model Codex](https://openai.com/index/openai-codex/) dari OpenAI pada pertengahan 2021, [LLM](https://en.wikipedia.org/wiki/Large_language_model) telah diadopsi secara luas dalam software engineering. Ada tiga bentuk utama yang digunakan saat ini: autocomplete, inline chat, dan coding agent.

[github-copilot]: https://github.com/features/copilot/ai-code-editor

## Autocomplete

Autocomplete bertenaga AI memiliki bentuk yang sama dengan autocomplete tradisional di IDE Anda, menyarankan completion pada posisi kursor Anda saat Anda mengetik. Kadang fitur ini digunakan sebagai fitur pasif yang "just works". Selain itu, autocomplete AI umumnya di-[prompt](https://en.wikipedia.org/wiki/Prompt_engineering) menggunakan komentar kode.

Misalnya, mari tulis skrip untuk mengunduh isi catatan kuliah ini dan mengekstrak semua tautannya. Kita dapat memulai dengan:

```python
import requests

def download_contents(url: str) -> str:
```

Model akan melengkapi isi fungsi tersebut secara otomatis:

```python
    response = requests.get(url)
    return response.text
```

Kita dapat lebih lanjut memandu completion menggunakan komentar. Misalnya, jika kita mulai menulis fungsi untuk mengekstrak semua tautan Markdown, tetapi namanya tidak terlalu deskriptif:

```python
def extract(contents: str) -> list[str]:
```

Model akan melengkapi sesuatu seperti ini:

```python
    lines = contents.splitlines()
    return [line for line in lines if line.strip()]
```

Kita dapat memandu completion melalui komentar kode:

```python
def extract(content: str) -> list[str]:
    # extract all Markdown links from the content
```

Kali ini, model memberikan completion yang lebih baik:

```python
    import re
    pattern = r'\[.*?\]\((.*?)\)'
    return re.findall(pattern, content)
```

Di sini, kita melihat satu kelemahan tool coding AI ini: tool hanya dapat memberikan completion pada posisi kursor. Dalam kasus ini, praktik yang lebih baik adalah meletakkan `import re` di tingkat module, bukan di dalam fungsi.

Contoh di atas menggunakan fungsi dengan nama yang kurang baik untuk mendemonstrasikan bagaimana code completion dapat diarahkan menggunakan komentar; dalam praktiknya, Anda ingin menulis kode dengan fungsi yang namanya lebih deskriptif, seperti `extract_links`, dan Anda ingin menulis docstring (dan berdasarkan itu, model seharusnya menghasilkan completion yang serupa dengan yang di atas).

Untuk keperluan demonstrasi, kita dapat melengkapi skripnya:

```python
print(extract(download_contents("https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/development-environment.md")))
```

## Inline chat

Inline chat memungkinkan Anda memilih sebuah baris atau blok lalu langsung memberi prompt kepada model AI untuk mengusulkan edit. Pada mode interaksi ini, model dapat membuat perubahan pada kode yang sudah ada (yang berbeda dengan autocomplete, yang hanya melengkapi kode setelah kursor).

Melanjutkan contoh di atas, misalkan kita memutuskan untuk tidak menggunakan library pihak ketiga `requests`. Kita dapat memilih tiga baris kode yang relevan, memanggil inline chat, dan mengatakan sesuatu seperti:

```
use built-in libraries instead
```

Model mengusulkan:

```python
from urllib.request import urlopen

def download_contents(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode('utf-8')
```

## Coding agents

Coding agent dibahas secara mendalam pada kuliah [Agentic Coding](/2026/agentic-coding/).

## Perangkat lunak yang direkomendasikan

Beberapa AI IDE populer adalah [VS Code][vs-code] dengan ekstensi [GitHub Copilot][github-copilot] dan [Cursor](https://cursor.com/). GitHub Copilot saat ini tersedia [gratis untuk pelajar](https://github.com/education/students), pengajar, dan maintainer proyek open source populer. Ini adalah bidang yang berkembang pesat. Banyak produk terkemuka memiliki fungsionalitas yang kurang lebih setara.

<a id="extensions-and-other-ide-functionality"></a>
# Extension dan Fungsi IDE Lainnya

IDE adalah tool yang kuat, yang menjadi bahkan lebih kuat berkat _extension_. Kami tidak dapat membahas semua fitur ini dalam satu kuliah, tetapi di sini kami memberikan beberapa petunjuk ke beberapa ekstensi populer. Kami mendorong Anda untuk menjelajahi bidang ini sendiri; ada banyak daftar ekstensi IDE populer yang tersedia daring, seperti [Vim Awesome](https://vimawesome.com/) untuk plugin Vim dan [ekstensi VS Code yang diurutkan berdasarkan popularitas](https://marketplace.visualstudio.com/search?target=VSCode&category=All%20categories&sortBy=Installs).

- [Development container](https://containers.dev/): didukung oleh IDE populer (misalnya, [didukung VS Code](https://code.visualstudio.com/docs/devcontainers/containers)), dev container memungkinkan Anda menggunakan container untuk menjalankan tool pengembangan. Ini dapat membantu untuk portabilitas atau isolasi. [Kuliah tentang packaging dan shipping code](/2026/shipping-code/) membahas container lebih mendalam.
- Remote development: melakukan pengembangan di mesin jarak jauh menggunakan SSH (misalnya, dengan [plugin Remote SSH untuk VS Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh)). Ini bisa berguna, misalnya, jika Anda ingin mengembangkan dan menjalankan kode di mesin GPU yang kuat di cloud.
- Collaborative editing: mengedit berkas yang sama, ala Google Docs (misalnya, dengan [plugin Live Share untuk VS Code](https://marketplace.visualstudio.com/items?itemName=MS-vsliveshare.vsliveshare)).

# Latihan

1. Aktifkan Vim mode di semua perangkat lunak yang Anda gunakan yang mendukungnya, seperti editor dan shell Anda, dan gunakan Vim mode untuk semua text editing Anda selama bulan berikutnya. Setiap kali sesuatu terasa tidak efisien, atau ketika Anda berpikir "pasti ada cara yang lebih baik", coba cari di Google, kemungkinan besar memang ada cara yang lebih baik.
1. Selesaikan sebuah tantangan dari [VimGolf](https://www.vimgolf.com/).
1. Konfigurasikan ekstensi IDE dan language server untuk proyek yang sedang Anda kerjakan. Pastikan semua fungsionalitas yang diharapkan, seperti jump-to-definition untuk dependensi library, bekerja sesuai harapan. Jika Anda tidak memiliki kode yang dapat digunakan untuk latihan ini, Anda dapat menggunakan beberapa proyek open-source dari GitHub (seperti [yang ini](https://github.com/spf13/cobra)).
1. Telusuri daftar ekstensi IDE dan pasang satu yang menurut Anda berguna.
