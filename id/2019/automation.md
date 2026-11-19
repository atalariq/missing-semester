---
layout: lecture-id
title: "Automation"
presenter: Jose
date: 2019-01-24
order: 3
video:
  aspect: 56.25
  id: BaLlAaHz-1k
special: true
lang: id
permalink: /id/2019/automation/
---

Kadang Anda menulis skrip yang melakukan sesuatu tetapi Anda ingin skrip itu berjalan secara berkala, misalnya tugas backup. Anda selalu dapat menulis solusi *ad hoc* yang berjalan di latar belakang dan aktif secara berkala. Namun, sebagian besar sistem UNIX dilengkapi dengan daemon cron yang dapat menjalankan tugas dengan frekuensi hingga satu menit berdasarkan aturan sederhana.

Pada sebagian besar sistem UNIX daemon cron, `crond`, akan berjalan secara default tetapi Anda selalu dapat memeriksanya menggunakan `ps aux | grep crond`.

## Crontab

Berkas konfigurasi untuk cron dapat ditampilkan dengan menjalankan `crontab -l` dan diedit dengan menjalankan `crontab -e` Format waktu yang digunakan cron adalah lima field yang dipisahkan spasi beserta user dan perintah

- **minute** - Menit ke berapa dalam satu jam perintah akan berjalan,
     dan bernilai antara '0' dan '59'
- **hour** -    Ini mengatur pada jam berapa perintah akan berjalan, dan ditentukan dalam
         jam 24 jam, nilainya harus antara 0 dan 23 (0 adalah tengah malam)
- **dom** - Ini adalah Day of Month (hari dalam bulan), saat Anda ingin perintah dijalankan, misalnya untuk
     menjalankan perintah pada tanggal 19 setiap bulan, dom-nya adalah 19.
- **month** -   Ini adalah bulan saat perintah tertentu akan berjalan, dapat ditentukan
     secara numerik (0-12), atau sebagai nama bulan (misalnya May)
- **dow** - Ini adalah Day of Week (hari dalam pekan) saat Anda ingin sebuah perintah dijalankan, dapat
     juga numerik (0-7) atau sebagai nama hari (misalnya sun).
- **user** -    Ini adalah pengguna yang menjalankan perintah.
- **command** - Ini adalah perintah yang ingin Anda jalankan. Field ini dapat memuat
     beberapa kata atau spasi.

Perhatikan bahwa menggunakan asterisk `*` berarti semua dan menggunakan asterisk diikuti slash dan angka berarti setiap nilai ke-n. Jadi `*/5` berarti setiap lima. Beberapa contoh adalah

```shell
*/5   *    *   *   *       # Every five minutes
  0   *    *   *   *       # Every hour at o'clock
  0   9    *   *   *       # Every day at 9:00 am
  0   9-17 *   *   *       # Every hour between 9:00am and 5:00pm
  0   0    *   *   5       # Every Friday at 12:00 am
  0   0    1   */2 *       # Every other month, the first day, 12:00am
```
Anda dapat menemukan lebih banyak contoh jadwal crontab umum di [crontab.guru](https://crontab.guru/examples.html)

## Shell environment dan logging

Jebakan umum saat menggunakan cron adalah cron tidak memuat skrip environment yang sama dengan shell umum seperti `.bashrc`, `.zshrc`, &c dan cron tidak mencatat output di mana pun secara default. Digabungkan dengan frekuensi maksimum satu menit, awalnya bisa cukup menyakitkan untuk men-debug skrip cron.

Untuk menangani environment, pastikan Anda menggunakan path absolut di semua skrip Anda dan memodifikasi environment variable Anda seperti `PATH` sehingga skrip dapat berjalan dengan sukses. Untuk menyederhanakan logging, rekomendasi yang baik adalah menulis crontab Anda dalam format seperti ini


```shell
* * * * *   user  /path/to/cronscripts/every_minute.sh >> /tmp/cron_every_minute.log 2>&1
```

Dan menulis skripnya di berkas terpisah. Ingat bahwa `>>` menambahkan ke berkas dan bahwa `2>&1` me-redirect `stderr` ke `stdout` (meskipun Anda mungkin ingin menyimpannya terpisah).

## Anacron

Satu catatan penting saat menggunakan cron adalah jika komputer dimatikan atau tidur ketika skrip cron seharusnya berjalan maka skrip tersebut tidak dieksekusi. Untuk tugas yang sering ini mungkin tidak masalah, tetapi jika sebuah tugas berjalan lebih jarang, Anda mungkin ingin memastikan tugas itu dieksekusi. [anacron](https://linux.die.net/man/8/anacron) bekerja serupa dengan `cron` kecuali frekuensinya ditentukan dalam hari. Berbeda dengan cron, anacron tidak mengasumsikan mesin berjalan terus-menerus. Karena itu, anacron dapat digunakan pada mesin yang tidak berjalan 24 jam sehari, untuk mengendalikan job reguler seperti job harian, mingguan, dan bulanan.


## Latihan

1. Buat skrip yang setiap menit memeriksa folder downloads Anda untuk berkas apa pun yang berupa gambar (Anda dapat menelaah [MIME type](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types) atau menggunakan regular expression untuk mencocokkan ekstensi umum) dan memindahkannya ke folder Pictures Anda.

1. Tulis skrip cron untuk memeriksa paket yang sudah usang di sistem Anda setiap pekan dan meminta Anda memperbaruinya atau memperbaruinya secara otomatis.



{% comment %}

- [fswatch](https://github.com/emcrisostomo/fswatch)
- GUI automation (pyautogui) [Automating the boring stuff Chapter 18](https://automatetheboringstuff.com/chapter18/)
- Ansible/puppet/chef

- https://xkcd.com/1205/
- https://xkcd.com/1319/

{% endcomment %}
