---
layout: lecture-id
title: "OS Customization"
presenter: Anish
date: 2019-01-29
order: 3
video:
  aspect: 62.5
  id: epSRVqQzeDo
special: true
lang: id
permalink: /id/2019/os-customization/
---

Ada banyak yang dapat Anda lakukan untuk menyesuaikan sistem operasi Anda di luar apa yang
tersedia di menu pengaturan.

# Pemetaan ulang keyboard

Keyboard Anda mungkin memiliki tombol yang tidak banyak Anda gunakan. Daripada
memiliki tombol yang tidak berguna, Anda dapat memetakannya ulang untuk melakukan hal yang berguna.

## Memetakan ulang ke tombol lain

Hal paling sederhana adalah memetakan tombol ke tombol lain. Misalnya, jika Anda tidak
banyak menggunakan tombol caps lock, maka Anda dapat memetakannya ke sesuatu yang lebih
berguna. Jika Anda pengguna Vim, misalnya, Anda mungkin ingin memetakan caps lock
ke escape.

Di macOS, Anda dapat melakukan beberapa pemetaan ulang melalui pengaturan Keyboard di System
Preferences; untuk pemetaan yang lebih rumit, Anda memerlukan perangkat lunak khusus.

## Memetakan ulang ke perintah arbitrer

Anda tidak hanya harus memetakan tombol ke tombol lain: ada tool yang memungkinkan
Anda memetakan tombol (atau kombinasi tombol) ke perintah arbitrer. Misalnya,
Anda dapat membuat command-shift-t membuka jendela terminal baru.

# Menyesuaikan pengaturan OS tersembunyi

## macOS

macOS mengekspos banyak pengaturan berguna melalui perintah `defaults`. Misalnya,
Anda dapat membuat ikon Dock aplikasi tersembunyi menjadi transparan:

```shell
defaults write com.apple.dock showhidden -bool true
```

Tidak ada satu daftar tunggal semua pengaturan yang mungkin, tetapi Anda dapat menemukan daftar
kustomisasi spesifik secara daring, seperti
[.macos](https://github.com/mathiasbynens/dotfiles/blob/master/.macos) milik Mathias Bynens.

# Manajemen window

## Tiling window management

[Tiling window management](https://en.wikipedia.org/wiki/Tiling_window_manager)
adalah salah satu pendekatan manajemen window, di mana Anda menata window ke dalam
frame yang tidak tumpang tindih. Jika Anda menggunakan sistem operasi berbasis Linux, Anda dapat
memasang tiling window manager; jika Anda menggunakan sesuatu seperti Windows atau
macOS, Anda dapat memasang aplikasi yang memungkinkan Anda mendekati perilaku ini.

## Manajemen layar

Anda dapat menyiapkan keyboard shortcut untuk membantu Anda memanipulasi window di berbagai
layar.

## Layout

Jika ada cara spesifik Anda menata window di layar, alih-alih
"mengeksekusi" layout itu secara manual, Anda dapat menuliskannya sebagai skrip, sehingga membuat instansiasi
layout menjadi mudah.

# Sumber daya

- [Hammerspoon](https://www.hammerspoon.org/) - otomasi desktop macOS
- [Rectangle](https://rectangleapp.com/) - window manager macOS
- [Karabiner](https://karabiner-elements.pqrs.org/) - pemetaan ulang keyboard macOS yang canggih
- [r/unixporn](https://www.reddit.com/r/unixporn/) - tangkapan layar dan
dokumentasi konfigurasi mewah orang lain

# Latihan

1. Cari tahu cara memetakan ulang tombol Caps Lock Anda ke sesuatu yang lebih sering Anda gunakan
   (seperti Escape atau Ctrl atau Backspace).

1. Buat keyboard shortcut global kustom untuk membuka jendela terminal baru atau
   jendela browser baru.

{% comment %}

TODO

- Bitbar / Polybar
- Clipboard Manager (stack/searchable history)

{% endcomment %}
