---
layout: lecture-id
title: "Web dan Browser"
presenter: Jose
date: 2019-01-31
order: 1
video:
  aspect: 62.5
  id: XpZO3S8odec
special: true
lang: id
permalink: /id/2019/web/
---

Selain terminal, web browser adalah tool yang akan membuat Anda menghabiskan banyak waktu. Karena itu layak mempelajari cara menggunakannya secara efisien dan produktif.

## Shortcut

Mengklik sana-sini di browser Anda sering bukan opsi tercepat, membiasakan diri dengan shortcut umum benar-benar dapat membuahkan hasil dalam jangka panjang.

- `Middle Button Click` pada sebuah tautan membukanya di tab baru
- `Ctrl+T` Membuka tab baru
- `Ctrl+Shift+T` Membuka kembali tab yang baru saja ditutup
- `Ctrl+L` memilih isi search bar
- `Ctrl+F` untuk mencari di dalam halaman web. Jika Anda sering melakukan ini, Anda mungkin mendapat manfaat dari ekstensi yang mendukung regular expression dalam pencarian.


## Operator pencarian

Mesin pencari web seperti Google atau DuckDuckGo menyediakan operator pencarian untuk memungkinkan pencarian web yang lebih rumit:

- `"bar foo"` menegakkan kecocokan persis bar foo
- `foo site:bar.com` mencari foo di dalam bar.com
- `foo -bar ` mengecualikan istilah yang memuat bar dari pencarian
- `foobar filetype:pdf` Mencari berkas dengan ekstensi tersebut
- `(foo|bar)` mencari kecocokan yang memiliki foo ATAU bar

Daftar yang lebih lengkap tersedia untuk mesin populer seperti [Google](https://ahrefs.com/blog/google-advanced-search-operators/) dan [DuckDuckGo](https://duck.co/help/results/syntax)


## Searchbar

Searchbar juga merupakan tool yang kuat. Sebagian besar browser dapat menyimpulkan search engine dari situs web dan menyimpannya. Dengan mengedit argumen keyword

- Di Google Chrome mereka ada di [chrome://settings/searchEngines](chrome://settings/searchEngines)
- Di Firefox mereka ada di [about:preferences#search](about:preferences#search)

Misalnya Anda dapat membuat agar `y SOME SEARCH TERMS` langsung mencari di youtube.

Lebih jauh lagi, jika Anda memiliki sebuah domain Anda dapat menyiapkan forward subdomain menggunakan registrar Anda. Misalnya saya telah memetakan `https://ht.josejg.com` ke situs web kursus ini. Dengan begitu saya cukup mengetik `ht.` dan searchbar akan melengkapi otomatis. Fitur lain yang baik dari pengaturan ini adalah berbeda dengan bookmark, ini akan berfungsi di setiap browser.

## Ekstensi privacy

Saat ini menjelajahi web bisa cukup mengganggu karena iklan dan cukup invasif karena tracker. Lebih jauh lagi adblocker yang baik tidak hanya memblokir sebagian besar konten iklan tetapi juga akan memblokir situs web yang meragukan dan berbahaya karena situs tersebut akan disertakan dalam blacklist umum. Ekstensi tersebut juga akan mengurangi waktu muat halaman kadang dengan mengurangi jumlah permintaan yang dilakukan. Beberapa rekomendasi adalah:

- **uBlock origin** ([Chrome](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm), [Firefox](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)): memblokir iklan dan tracker berdasarkan aturan yang telah ditentukan. Anda juga sebaiknya mempertimbangkan melihat blacklist yang diaktifkan di pengaturan karena Anda dapat mengaktifkan lebih banyak berdasarkan wilayah atau kebiasaan browsing Anda. Anda bahkan dapat memasang filter dari [seluruh web](https://github.com/gorhill/uBlock/wiki/Filter-lists-from-around-the-web)

- **[Privacy Badger](https://privacybadger.org/)**: mendeteksi dan memblokir tracker secara otomatis. Misalnya ketika Anda berpindah dari situs web ke situs web perusahaan iklan melacak situs mana yang Anda kunjungi dan menyusun profil Anda

- **[HTTPS everywhere](https://www.eff.org/https-everywhere)** adalah ekstensi luar biasa yang otomatis mengalihkan ke versi HTTPS sebuah situs web, jika tersedia.

Anda dapat menemukan lebih banyak addon semacam ini [di sini](https://www.privacytools.io/privacy-browser-addons/)

## Kustomisasi gaya

Web browser hanyalah perangkat lunak lain yang berjalan di _mesin Anda_ sehingga Anda biasanya memiliki keputusan terakhir tentang apa yang harus ditampilkannya atau bagaimana ia harus berperilaku. Contohnya adalah custom style. Browser menentukan cara merender gaya sebuah halaman web menggunakan Cascading Style Sheets yang sering disingkat CSS.

Anda dapat mengakses kode sumber sebuah situs web dengan memeriksanya dan mengubah isi serta gayanya untuk sementara (ini juga alasan mengapa Anda tidak boleh memercayai tangkapan layar halaman web).

Jika Anda ingin secara permanen memberi tahu browser Anda untuk menimpa pengaturan gaya sebuah halaman web Anda perlu menggunakan ekstensi. Rekomendasi kami adalah **[Stylus](https://github.com/openstyles/stylus)** ([Firefox](https://addons.mozilla.org/en-US/firefox/addon/styl-us/), [Chrome](https://chrome.google.com/webstore/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne?hl=en)).


Misalnya, kita dapat menulis gaya berikut untuk situs web kelas


```css

body {
    background-color: #2d2d2d;
    color: #eee;
    font-family: Fira Code;
    font-size: 16pt;
}

a:link {
    text-decoration: none;
    color: #0a0;
}
```

Lebih jauh lagi, Stylus dapat menemukan gaya yang ditulis pengguna lain dan dipublikasikan di [userstyles.org](https://userstyles.org/). Sebagian besar situs web umum memiliki satu atau beberapa stylesheet dark theme misalnya. FYI, Anda sebaiknya tidak menggunakan Stylish karena tool itu terbukti membocorkan data pengguna, selengkapnya [di sini](https://arstechnica.com/information-technology/2018/07/stylish-extension-with-2m-downloads-banished-for-tracking-every-site-visit/)


## Kustomisasi fungsionalitas

Dengan cara yang sama Anda dapat memodifikasi gaya, Anda juga dapat memodifikasi perilaku sebuah situs web dengan menulis javascript kustom lalu memuatnya menggunakan ekstensi web browser seperti [Tampermonkey](https://tampermonkey.net/)

Misalnya skrip berikut mengaktifkan navigasi mirip vim menggunakan tombol J dan K.

```js
// ==UserScript==
// @name         VIM HT
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Vim JK for our website
// @author       You
// @match        https://hacker-tools.github.io/*
// @grant        none
// ==/UserScript==


(function() {
    'use strict';

    window.onkeyup = function(e) {
        var key = e.keyCode ? e.keyCode : e.which;

        if (key == 74) { // J is key 74
            window.scrollBy(0,500);;
        }else if (key == 75) { // K is key 75
            window.scrollBy(0,-500);;
        }
    }
})();
```

Ada juga repositori skrip seperti [OpenUserJS](https://openuserjs.org/) dan [Greasy Fork](https://greasyfork.org/en). Namun, perlu diwaspadai, memasang user script dari orang lain bisa sangat berbahaya karena skrip tersebut hampir dapat melakukan apa pun seperti mencuri nomor kartu kredit Anda. Jangan pernah memasang skrip kecuali Anda membaca seluruhnya sendiri, memahami apa yang dilakukannya, dan benar-benar yakin bahwa skrip itu tidak melakukan sesuatu yang mencurigakan. Jangan pernah memasang skrip yang memuat kode ter-minify atau ter-obfuscate yang tidak dapat Anda baca!

## Web API

Semakin umum bagi layanan web menawarkan antarmuka aplikasi alias web API sehingga Anda dapat berinteraksi dengan layanan tersebut dengan membuat permintaan web.
Pengantar yang lebih mendalam tentang topik ini dapat ditemukan [di sini](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction). Ada [banyak API publik](https://github.com/toddmotto/public-apis). Web API dapat berguna karena sangat banyak alasan:

- **Pengambilan data**. Web API dapat dengan mudah memberikan Anda informasi seperti peta, cuaca atau apa alamat ip publik Anda. Misalnya `curl ipinfo.io` akan mengembalikan objek JSON dengan beberapa detail tentang ip publik, wilayah, lokasi, &c. Dengan parsing yang tepat tool ini bahkan dapat diintegrasikan dengan tool command line. Fungsi bash berikut berbicara dengan API autocompletion Google dan mengembalikan sepuluh kecocokan pertama.

```bash
function c() {
    url='https://www.google.com/complete/search?client=hp&hl=en&xhr=t'
    # NB: user-agent must be specified to get back UTF-8 data!
    curl -H 'user-agent: Mozilla/5.0' -sSG --data-urlencode "q=$*" "$url" |
        jq -r ".[1][][0]" |
        sed 's,</\?b>,,g'
}
```

- **Interaksi**. Endpoint web API juga dapat digunakan untuk memicu tindakan. Ini biasanya memerlukan semacam authentication token yang dapat Anda peroleh melalui layanan tersebut. Misalnya melakukan berikut
`curl -X POST -H 'Content-type: application/json' --data '{"text":"Hello, World!"}' "https://hooks.slack.com/services/$SLACK_TOKEN"` akan mengirim pesan `Hello, World!` di sebuah channel.

- **Piping**. Karena sebagian layanan dengan web API cukup populer, "pengeleman" web API umum sudah diimplementasikan dan disediakan lengkap dengan servernya. Ini terjadi pada layanan seperti [If This Then That](https://ifttt.com/) dan [Zapier](https://zapier.com/)


## Otomasi Web

Kadang web API tidak cukup. Jika hanya perlu membaca Anda dapat menggunakan parser html seperti `pup` atau menggunakan library, misalnya python memiliki BeautifulSoup. Namun jika diperlukan interaktivitas atau eksekusi javascript, solusi tersebut tidak memadai.

- **WebDriver**. Misalnya, skrip berikut akan menyimpan url yang ditentukan menggunakan wayback machine dengan menyimulasikan interaksi mengetik situs web.

```python
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys


def snapshot_wayback(driver, url):

    driver.get("https://web.archive.org/")
    elem = driver.find_element_by_class_name('web-save-url-input')
    elem.clear()
    elem.send_keys(url)
    elem.send_keys(Keys.RETURN)
    driver.close()


driver = Firefox()
url = 'https://hacker-tools.github.io'
snapshot_wayback(driver, url)
```


## Latihan

1. Edit keyword search engine yang sering Anda gunakan di web browser Anda
1. Pasang ekstensi yang disebutkan. Telaah bagaimana uBlock Origin/Privacy Badger dapat dinonaktifkan untuk sebuah situs web. Perbedaan apa yang Anda lihat? Coba lakukan pada situs web dengan banyak iklan seperti YouTube.
1. Pasang Stylus dan tulis custom style untuk situs web kelas menggunakan CSS yang disediakan. Berikut beberapa karakter pemrograman umum `=   ==   ===   >=   =>   ++   /=   ~=`. Apa yang terjadi padanya ketika mengubah font ke Fira Code? Jika Anda ingin tahu lebih banyak cari tentang programming font ligature.
1. Temukan web api untuk mendapatkan cuaca di kota/wilayah Anda.
1. Gunakan perangkat lunak WebDriver seperti [Selenium](https://www.selenium.dev/documentation/) untuk mengotomatiskan tugas manual berulang yang sering Anda lakukan dengan browser Anda.
