---
layout: lecture-id
title: "Agentic Coding"
description: >
  Pelajari cara menggunakan AI coding agent secara efektif untuk tugas software development.
thumbnail: /static/assets/thumbnails/2026/lec7.png
date: 2026-01-21
ready: true
video:
  aspect: 56.25
  id: sTdz6PZoAnw
lang: id
permalink: /id/2026/agentic-coding/
---

Coding agent adalah model AI percakapan yang memiliki akses ke tool seperti membaca/menulis berkas, web search, dan memanggil perintah shell. Agent tersebut berada di dalam IDE atau di tool command-line maupun GUI yang berdiri sendiri. Coding agent merupakan tool yang sangat otonom dan kuat, sehingga memungkinkan beragam use case.

Kuliah ini melanjutkan materi AI-powered development dari kuliah [Development Environment and Tools](/2026/development-environment/). Sebagai demo singkat, mari lanjutkan contoh dari bagian [AI-powered development](/2026/development-environment/#ai-powered-development):

```python
from urllib.request import urlopen

def download_contents(url: str) -> str:
    with urlopen(url) as response:
        return response.read().decode('utf-8')

def extract(content: str) -> list[str]:
    import re
    pattern = r'\[.*?\]\((.*?)\)'
    return re.findall(pattern, content)

print(extract(download_contents("https://raw.githubusercontent.com/missing-semester/missing-semester/refs/heads/master/_2026/development-environment.md")))
```

Kita dapat mencoba memberi coding agent tugas berikut:

```
Turn this into a proper command-line program, with argparse for argument parsing. Add type annotations, and make sure the program passes type checking.
```

Agent akan membaca berkas untuk memahaminya, lalu melakukan beberapa perubahan, dan akhirnya memanggil type checker untuk memastikan type annotation-nya benar. Jika agent membuat kesalahan sehingga type checking gagal, biasanya agent akan mengulanginya, meskipun tugas ini cukup sederhana sehingga hal itu kecil kemungkinannya terjadi. Karena coding agent memiliki akses ke tool yang berpotensi berbahaya, secara default agent harness meminta pengguna mengonfirmasi pemanggilan tool.

> Jika coding agent membuat kesalahan — misalnya, Anda memiliki binary `mypy` yang tersedia langsung di `$PATH` tetapi agent mencoba memanggil `python -m mypy` — Anda dapat memberi umpan balik teks untuk membantunya memperbaiki arah.

Coding agent mendukung interaksi multi-turn, sehingga Anda dapat mengiterasi pekerjaan melalui percakapan bolak-balik dengan agent. Anda bahkan dapat menginterupsi agent jika ia sedang menempuh jalur yang salah. Salah satu mental model yang membantu adalah membayangkan diri Anda sebagai manajer bagi seorang intern: intern akan mengerjakan hal-hal teknis yang rinci, tetapi memerlukan arahan, dan sesekali melakukan hal yang salah sehingga perlu dikoreksi.

> Untuk demo yang lebih ilustratif, coba minta agent sebagai tindak lanjut untuk menjalankan skrip yang dihasilkan. Amati outputnya, lalu coba minta agent membuat perubahan (misalnya, minta agent hanya menyertakan URL absolut).

<a id="how-ai-models-and-agents-work"></a>
# Cara kerja model AI dan agent

Menjelaskan secara lengkap cara kerja internal [large language model (LLM)](https://en.wikipedia.org/wiki/Large_language_model) modern serta infrastruktur seperti agent harness berada di luar cakupan kursus ini. Namun, pemahaman tingkat tinggi tentang beberapa ide kunci akan membantu Anda _menggunakan_ teknologi yang masih berkembang pesat ini secara efektif dan memahami keterbatasannya.

LLM dapat dipandang sebagai model distribusi probabilitas string penyelesaian (output) dengan syarat string prompt (input). LLM inference (yang terjadi ketika Anda, misalnya, mengirim kueri ke aplikasi chat percakapan) melakukan _sampling_ dari distribusi probabilitas ini. LLM memiliki _context window_ tetap, yaitu panjang maksimum string input dan output.

{% comment %}
> In mathematical notation, the LLM models the probability distribution $\pi_\theta$ of completions $y$ conditioned on prompts $x$, and we sample from this distribution: $\hat{y} \sim \pi_\theta(\cdot \mid x)$.
{% endcomment %}

Tool AI seperti chat percakapan dan coding agent dibangun di atas primitif ini. Untuk interaksi multi-turn, aplikasi chat dan agent menggunakan penanda turn serta menyuplai seluruh riwayat percakapan sebagai string prompt setiap kali ada prompt pengguna baru, sehingga LLM inference dipanggil sekali per prompt pengguna. Untuk agent yang memanggil tool, harness menafsirkan output LLM tertentu sebagai permintaan untuk memanggil sebuah tool, dan harness menyuplai hasil pemanggilan tool tersebut kembali ke model sebagai bagian dari string prompt (jadi LLM inference berjalan lagi setiap kali ada pemanggilan/respons tool). Konsep inti pada agent yang memanggil tool dapat [diimplementasikan dalam 200 baris kode](https://www.mihaileric.com/The-Emperor-Has-No-Clothes/).

## Privasi

Sebagian besar tool AI coding dalam konfigurasi standarnya mengirim banyak data Anda ke cloud. Kadang harness berjalan secara lokal sementara LLM inference berjalan di cloud, pada kesempatan lain bahkan lebih banyak bagian perangkat lunak yang berjalan di cloud (dan, misalnya, penyedia layanan bisa jadi secara efektif memperoleh salinan seluruh repositori Anda serta semua interaksi Anda dengan tool AI tersebut).

Ada tool AI coding open-source dan LLM open-source yang cukup bagus (meskipun belum sebaik model proprietary), tetapi saat ini, bagi sebagian besar pengguna, menjalankan LLM open yang terdepan secara lokal tidak akan praktis karena keterbatasan perangkat keras.

# Use case

Coding agent dapat membantu untuk berbagai macam tugas. Beberapa contoh:

- **Mengimplementasikan fitur baru.** Seperti contoh di atas, Anda dapat meminta coding agent mengimplementasikan sebuah fitur. Memberikan spesifikasi yang baik masih lebih merupakan seni daripada ilmu pada tahap ini; Anda ingin input ke agent cukup deskriptif sehingga agent melakukan apa yang Anda inginkan (setidaknya bergerak ke arah yang benar agar Anda dapat mengiterasi), tetapi tidak terlalu deskriptif sampai Anda sendiri mengerjakan terlalu banyak. Test-driven development bisa sangat efektif: tulis test (atau gunakan coding agent untuk membantu Anda menulis test), audit test tersebut untuk memastikan test menangkap apa yang Anda inginkan, lalu minta coding agent mengimplementasikan fiturnya. Model terus berkembang, jadi Anda harus terus memperbarui intuisi Anda tentang apa yang mampu dilakukan model.
    > Kami menggunakan Claude Code untuk [mengimplementasikan](https://github.com/missing-semester/missing-semester/pull/345) sidenote bergaya Tufte ini.
{%- comment %}
No need to demo this, since the intro of a lecture was a small demo of adding a new feature.
{% endcomment %}
- **Memperbaiki error.** Jika Anda memiliki error dari compiler, linter, type checker, atau test, Anda dapat meminta agent Anda memperbaikinya, misalnya dengan prompt seperti "fix the issues with mypy". Coding model sangat efektif apabila Anda dapat memasukkannya ke dalam feedback loop, jadi cobalah mengatur segalanya agar model dapat menjalankan pemeriksaan yang gagal secara langsung, sehingga model dapat beriterasi secara otonom. Jika hal itu tidak praktis, Anda dapat memberi umpan balik ke model secara manual.
    > Pada commit [f552b55](https://github.com/missing-semester/missing-semester/commit/f552b5523462b22b8893a8404d2110c4e59613dd) repo missing-semester, kami memberi prompt ke Claude Code "Review the agentic coding lecture for typos and grammatical issues" dan kemudian memintanya memperbaiki masalah yang ditemukan, yang di-commit dalam [f1e1c41](https://github.com/missing-semester/missing-semester/commit/f1e1c417adba6b4149f7eef91ff5624de40dc637).
{%- comment %}
Demo a coding agent fixing the bug in https://github.com/anishathalye/dotbot/commit/cef40c902ef0f52f484153413142b5154bbc5e99.

Write the failing tests to demo the bug, and then ask the agent to fix. Prepped in branch demo-bugfix.

Can run the failing test with:

    hatch test tests/test_cli.py::test_issue_357

Can prompt coding agent with:

    There is a bug I wrote a failing test for, you can repro it with `hatch test tests/test_cli.py::test_issue_357`. Fix the bug.

Get it to commit the changes.
{% endcomment %}
- **Refactoring.** Anda dapat menggunakan coding agent untuk melakukan refactoring kode dengan berbagai cara, dari tugas sederhana seperti mengganti nama method (refactoring jenis ini juga didukung oleh [code intelligence](/2026/development-environment/#code-intelligence-and-language-servers)) hingga tugas yang lebih kompleks seperti memisahkan fungsionalitas ke modul tersendiri.
    > Kami menggunakan Claude Code untuk [memisahkan](https://github.com/missing-semester/missing-semester/pull/344) agentic coding menjadi kuliah tersendiri.
{%- comment %}
Show usage in Missing Semester, point out that the agent did make some mistakes.
{% endcomment %}
- **Code review.** Anda dapat meminta coding agent meninjau kode. Anda dapat memberi panduan dasar, seperti "review my latest changes that are not yet committed". Jika Anda ingin meninjau sebuah pull request dan coding agent Anda mendukung web fetch, atau Anda memiliki tool command-line seperti [GitHub CLI](https://cli.github.com/) terpasang, Anda bahkan mungkin dapat meminta coding agent "Review the pull request {link}" dan agent akan menanganinya dari sana.
{%- comment %}
In Porcupine repo, prompt agent with:

    Review this PR: https://github.com/anishathalye/porcupine/pull/39
{% endcomment %}
- **Memahami kode.** Anda dapat mengajukan pertanyaan tentang codebase kepada coding agent, yang bisa sangat membantu saat onboarding.
{%- comment %}
Some prompts to try in the missing-semester repo:

    How do I run this site locally?

    How are the social preview cards implemented?
{% endcomment %}
- **Sebagai shell.** Anda dapat meminta coding agent menggunakan tool tertentu untuk menyelesaikan tugas, sehingga Anda dapat memanggil perintah shell menggunakan bahasa alami, seperti "use the find command to find all files older than 30 days" atau "use mogrify to resize all the jpgs to 50% of their original size".
{%- comment %}
In Dotbot repo, prompt agent with:

    Use the ag command to find all Python renaming imports
{% endcomment %}
- **Vibe coding.** Agent cukup kuat sehingga Anda dapat mengimplementasikan sebagian aplikasi tanpa menulis satu baris kode pun sendiri.
    > [Ini sebuah contoh](https://github.com/cleanlab/office-presence-dashboard) proyek dunia nyata yang di-vibe-code oleh salah satu pengajar.
{%- comment %}
In missing-semester repo, prompt agent with:

    Make this site look retro.
{% endcomment %}

# Agent tingkat lanjut

Di sini kami memberikan ringkasan singkat tentang beberapa pola penggunaan dan kemampuan coding agent yang lebih lanjut.

- **Prompt yang dapat digunakan ulang.** Buat prompt atau template yang dapat digunakan ulang. Misalnya, Anda dapat menulis prompt terperinci untuk melakukan code review dengan cara tertentu, lalu menyimpannya sebagai prompt yang dapat digunakan ulang.
    > Tooling agent berkembang cepat. Pada sebagian tool, prompt yang dapat digunakan ulang sebagai fitur mandiri sudah deprecated. Misalnya, di Codex dan Claude Code, fitur tersebut [diserap](https://developers.openai.com/codex/custom-prompts) oleh [skill](https://code.claude.com/docs/en/skills).
- **Agent paralel.** Coding agent bisa lambat: Anda dapat memberi prompt ke agent, dan agent dapat mengerjakan suatu masalah selama puluhan menit. Anda dapat menjalankan beberapa salinan agent secara bersamaan, baik yang mengerjakan tugas yang sama (LLM bersifat stokastik, sehingga menjalankan hal yang sama beberapa kali lalu mengambil solusi terbaik bisa membantu) maupun tugas yang berbeda (misalnya, mengimplementasikan dua fitur yang tidak saling tumpang tindih secara bersamaan). Agar perubahan dari agent yang berbeda tidak saling mengganggu, Anda dapat menggunakan [git worktree](https://git-scm.com/docs/git-worktree), yang kami bahas pada kuliah [version control](/2026/version-control/).
- **MCP.** MCP, singkatan dari _Model Context Protocol_, adalah protokol terbuka yang dapat Anda gunakan untuk menghubungkan coding agent Anda dengan tool. Misalnya, [Notion MCP server](https://github.com/makenotion/notion-mcp-server) ini memungkinkan agent Anda membaca/menulis dokumen Notion, sehingga memungkinkan use case seperti "read the spec linked in {Notion doc}, draft an implementation plan as a new page in Notion, and then implement a prototype". Untuk menemukan MCP, Anda dapat menggunakan direktori seperti [Pulse](https://www.pulsemcp.com/servers) dan [Glama](https://glama.ai/mcp/servers).
- **Manajemen context.** Seperti kami sebutkan [di atas](#how-ai-models-and-agents-work), LLM yang mendasari coding agent memiliki _context window_ yang terbatas. Penggunaan coding agent yang efektif menuntut pemanfaatan context secara baik. Anda ingin memastikan agent memiliki akses ke informasi yang dibutuhkannya, tetapi menghindari context yang tidak perlu agar tidak meluap dari context window atau menurunkan performa model (yang cenderung terjadi seiring bertambahnya ukuran context, meskipun tidak meluap dari context window). Agent harness secara otomatis menyuplai, dan sampai batas tertentu mengelola, context, tetapi banyak kendali tetap berada di tangan pengguna.
    - **Membersihkan context window.** Kendali paling dasar, coding agent mendukung pembersihan context window (memulai percakapan baru), yang sebaiknya Anda lakukan untuk kueri yang tidak berkaitan.
    - **Mundur dalam percakapan.** Sebagian coding agent mendukung pembatalan langkah dalam riwayat percakapan. Daripada memberikan pesan lanjutan yang mengarahkan agent ke arah berbeda, dalam situasi ketika "undo" lebih masuk akal, cara ini mengelola context secara lebih efektif.
{%- comment %}
Make up a quick demo.
{% endcomment %}
    - **Compaction.** Untuk memungkinkan percakapan dengan panjang tak terbatas, coding agent mendukung _compaction_ context: jika riwayat percakapan tumbuh terlalu panjang, agent akan otomatis memanggil LLM untuk merangkum awalan percakapan, lalu mengganti riwayat percakapan dengan ringkasan tersebut. Sebagian agent memberi kendali kepada pengguna untuk memicu compaction saat diinginkan.
{%- comment %}
Show `/compact` in Claude Code, show full summary.
{% endcomment %}
    - **llms.txt.** Berkas `/llms.txt` adalah lokasi [standar](https://llmstxt.org/) yang diusulkan untuk dokumen yang dimaksudkan agar digunakan LLM saat inference. Produk (misalnya, [cursor.com/llms.txt](https://cursor.com/llms.txt)), library perangkat lunak (misalnya, [ai.pydantic.dev/llms.txt](https://ai.pydantic.dev/llms.txt)), dan API (misalnya, [apify.com/llms.txt](https://apify.com/llms.txt)) mungkin memiliki berkas `llms.txt` yang berguna untuk pengembangan. Dokumen semacam itu lebih padat informasi per token, sehingga lebih hemat context daripada meminta coding agent Anda mengambil dan membaca halaman HTML. Dokumentasi eksternal berguna ketika coding agent tidak memiliki pengetahuan bawaan tentang dependensi yang ingin Anda gunakan (misalnya, karena dependensi itu diterbitkan setelah knowledge cutoff LLM tersebut).
{%- comment %}
Side-by-side comparison in an empty repo (on Desktop or some other self-contained place, with `git init` run in it):

    Write a single-file Python program example in demo.py using semlib to sort "Ilya Sutskever", "Soumith Chintala", and "Donald Knuth" in terms of their fame as AI researchers.

    Write a single-file Python program example in demo.py using semlib to sort "Ilya Sutskever", "Soumith Chintala", and "Donald Knuth" in terms of their fame as AI researchers. See https://semlib.anish.io/llms.txt. Follow links to Markdown versions of any pages linked in llms.txt files.

Not sure why the agent doesn't do this by default. You'd probably put that last sentence in a CLAUDE.md file.
{% endcomment %}
    - **AGENTS.md.** Sebagian besar coding agent mendukung [AGENTS.md](https://agents.md/) atau yang serupa (misalnya, Claude Code mencari `CLAUDE.md`) sebagai README untuk coding agent. Saat agent dimulai, agent mengisi context terlebih dahulu dengan seluruh isi `AGENTS.md`. Anda dapat memanfaatkan ini untuk memberi agent saran yang berlaku umum lintas sesi (misalnya, menginstruksikannya untuk selalu menjalankan type checker setelah mengubah kode, menjelaskan cara menjalankan unit test, atau memberikan tautan ke dokumentasi pihak ketiga yang dapat dijelajahi agent). Sebagian coding agent dapat membuat berkas ini secara otomatis (misalnya, perintah `/init` di Claude Code). Lihat [di sini](https://github.com/pydantic/pydantic-ai/blob/main/CLAUDE.md) untuk contoh nyata sebuah `AGENTS.md`.
{%- comment %}
Dotbot example, CLAUDE.md that includes @DEVELOPMENT.md and says to always run the type checker and code formatter after making any changes to Python code.

Example prompt, off of master:

    Remove the "--version" command-line flag.

This is something that'll be fast, for demonstration purposes.
{% endcomment %}
    - **Skill.** Konten dalam `AGENTS.md` selalu dimuat, secara keseluruhan, ke dalam context window agent. _Skill_ menambahkan satu lapis indirection untuk menghindari pembengkakan context: Anda dapat menyediakan daftar skill beserta deskripsinya kepada agent, dan agent dapat "membuka" skill tersebut (memuatnya ke context window-nya) sesuai kebutuhan.
    - **Subagent.** Sebagian coding agent memungkinkan Anda mendefinisikan subagent, yaitu agent untuk alur kerja yang spesifik terhadap tugas. Coding agent tingkat atas dapat memanggil subagent untuk menyelesaikan tugas tertentu, sehingga baik agent tingkat atas maupun subagent dapat mengelola context secara lebih efektif. Context agent tingkat atas tidak dipenuhi dengan semua yang dilihat subagent, dan subagent dapat memperoleh hanya context yang dibutuhkannya untuk tugasnya. Sebagai salah satu contoh, sebagian coding agent mengimplementasikan web research sebagai subagent: agent tingkat atas akan mengajukan kueri kepada subagent, yang akan menjalankan web search, mengambil halaman web satu per satu, menganalisisnya, dan memberikan jawaban atas kueri tersebut kepada agent tingkat atas. Dengan cara ini, context agent tingkat atas tidak dipenuhi oleh seluruh konten semua halaman web yang diambil, dan subagent tidak memiliki sisa riwayat percakapan agent tingkat atas di dalam context-nya.

Untuk banyak fitur lanjutan yang memerlukan penulisan prompt (misalnya, skill atau subagent), Anda dapat menggunakan LLM untuk membantu Anda memulai. Sebagian coding agent bahkan memiliki dukungan bawaan untuk melakukan hal ini. Misalnya, Claude Code dapat menghasilkan subagent dari prompt singkat (panggil `/agents` dan buat agent baru). Coba buat subagent dengan prompt ini:

```
A Python code checking agent that uses `mypy` and `ruff` to type-check, lint, and format *check* any files that have been modified from the last git commit.
```

Kemudian, Anda dapat menggunakan agent tingkat atas untuk memanggil subagent tersebut secara eksplisit dengan pesan seperti "use the code checker subagent". Anda mungkin juga dapat membuat agent tingkat atas memanggil subagent tersebut secara otomatis bila sesuai, misalnya, setelah mengubah berkas Python apa pun.

# Hal yang perlu diwaspadai

Tool AI dapat membuat kesalahan. Tool tersebut dibangun di atas LLM, yang hanyalah model prediksi token berikutnya yang bersifat probabilistik. LLM tidak "cerdas" dengan cara yang sama seperti manusia. Tinjau output AI untuk bug kebenaran dan keamanan. Terkadang memverifikasi kode bisa lebih sulit daripada menulis kodenya sendiri; untuk kode yang kritis, pertimbangkan menulisnya secara manual. AI dapat masuk ke lubang kelinci dan mencoba menggiring Anda pada kesimpulan yang keliru; waspadai spiral debugging. Jangan menggunakan AI sebagai tongkat penopang, dan waspadai ketergantungan berlebih atau pemahaman yang dangkal. Masih ada kelas besar tugas pemrograman yang belum mampu dilakukan AI. Computational thinking tetap bernilai.

# Perangkat lunak yang direkomendasikan

Banyak IDE / ekstensi AI coding menyertakan coding agent (lihat rekomendasi dari [kuliah development environment](/2026/development-environment/)). Coding agent populer lainnya termasuk [Claude Code](https://www.claude.com/product/claude-code) dari Anthropic, [Codex](https://openai.com/codex/) dari OpenAI, dan agent open-source seperti [opencode](https://github.com/anomalyco/opencode).

# Latihan

1. Bandingkan pengalaman menulis kode secara manual, menggunakan autocomplete AI, inline chat, dan agent dengan mengerjakan tugas pemrograman yang sama empat kali. Kandidat terbaik adalah fitur berukuran kecil dari proyek yang sudah Anda kerjakan. Jika Anda mencari ide lain, Anda dapat mempertimbangkan menyelesaikan tugas bergaya "good first issue" pada proyek open-source di GitHub, atau soal [Advent of Code](https://adventofcode.com/) atau [LeetCode](https://leetcode.com/).
1. Gunakan AI coding agent untuk menelusuri codebase yang belum Anda kenal. Ini paling baik dilakukan dalam konteks keinginan untuk men-debug atau menambahkan fitur baru pada proyek yang benar-benar Anda pedulikan. Jika tidak ada yang terlintas, coba gunakan AI agent untuk memahami cara kerja fitur terkait keamanan pada agent [opencode](https://github.com/anomalyco/opencode).
1. Vibe code aplikasi kecil dari nol. Jangan menulis satu baris kode pun secara manual.
1. Untuk coding agent pilihan Anda, buat dan uji sebuah `AGENTS.md` (atau yang serupa untuk agent pilihan Anda, seperti `CLAUDE.md`), sebuah skill (misalnya, [skill di Claude Code](https://code.claude.com/docs/en/skills) atau [skill di Codex](https://developers.openai.com/codex/skills/)), dan sebuah subagent (misalnya, [subagent di Claude Code](https://code.claude.com/docs/en/sub-agents)). Pikirkan kapan Anda ingin menggunakan salah satunya dibandingkan yang lain. Perhatikan bahwa coding agent pilihan Anda mungkin tidak mendukung sebagian fungsi ini; Anda dapat melewatinya, atau mencoba coding agent lain yang mendukungnya.
1. Gunakan coding agent untuk mencapai tujuan yang sama seperti pada latihan regex bullet point Markdown dari [kuliah Code Quality](/2026/code-quality/). Apakah agent menyelesaikan tugas tersebut melalui pengeditan berkas secara langsung? Apa kekurangan dan keterbatasan agent yang mengedit berkas secara langsung untuk menyelesaikan tugas semacam itu? Cari tahu cara memberi prompt kepada agent agar tidak menyelesaikan tugas melalui pengeditan berkas secara langsung. Petunjuk: minta agent menggunakan salah satu tool command-line yang disebutkan pada [kuliah pertama](/2026/course-shell/).
1. Sebagian besar coding agent mendukung semacam "yolo mode" (misalnya, di Claude Code, `--dangerously-skip-permissions`). Tidak aman menggunakan mode ini secara langsung, tetapi mungkin dapat diterima menjalankan coding agent di lingkungan terisolasi seperti virtual machine atau container lalu mengaktifkan operasi otonom. Jalankan pengaturan ini di mesin Anda. Dokumentasi seperti [Claude Code devcontainer](https://code.claude.com/docs/en/devcontainer) atau [Docker Sandboxes / Claude Code](https://docs.docker.com/ai/sandboxes/agents/claude-code/) mungkin berguna. Ada lebih dari satu cara untuk menyiapkan ini.
