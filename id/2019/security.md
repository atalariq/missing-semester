---
layout: lecture-id
title: "Security dan Privacy"
presenter: Jon
date: 2019-01-31
order: 2
video:
  aspect: 56.25
  id: OBx_c-i-M8s
special: true
lang: id
permalink: /id/2019/security/
---

Dunia ini tempat yang menakutkan, dan semua orang berusaha mencelakai Anda.

Oke, mungkin tidak, tetapi itu tidak berarti Anda ingin memamerkan semua
rahasia Anda. Security (dan privacy) umumnya soal menaikkan standar
bagi penyerang. Cari tahu apa threat model Anda, lalu rancang mekanisme
security Anda berdasarkan itu! Jika threat model-nya adalah NSA atau
Mossad, Anda _mungkin_ akan mengalami masa sulit.

Ada _banyak_ cara membuat persona teknis Anda lebih aman. Kami akan
menyinggung banyak hal tingkat tinggi di sini, tetapi ini adalah proses, dan
mendidik diri Anda adalah salah satu hal terbaik yang dapat Anda lakukan. Jadi:

## Ikuti Orang yang Tepat

Salah satu cara terbaik untuk meningkatkan pengetahuan security Anda adalah mengikuti
orang lain yang vokal tentang security. Beberapa saran:

 - [@TroyHunt](https://twitter.com/TroyHunt)
 - [@SwiftOnSecurity](https://twitter.com/SwiftOnSecurity)
 - [@taviso](https://twitter.com/taviso)
 - [@thegrugq](https://twitter.com/thegrugq)
 - [@tqbf](https://twitter.com/tqbf)
 - [@mattblaze](https://twitter.com/mattblaze)
 - [@moxie](https://twitter.com/moxie)

Lihat juga [daftar
ini](https://heimdalsecurity.com/blog/best-twitter-cybersec-accounts/)
untuk saran lebih banyak.

## Nasihat Security Umum

Tech Solidarity memiliki daftar [do dan don't untuk
jurnalis](https://web.archive.org/web/20221123204419/https://techsolidarity.org/resources/basic_security.htm)
yang cukup hebat dan memuat banyak nasihat masuk akal, serta cukup mutakhir. [@thegrugq](https://medium.com/@thegrugq)
juga memiliki posting blog yang baik tentang [nasihat keamanan
perjalanan](https://medium.com/@thegrugq/stop-fabricating-travel-security-advice-35259bf0e869)
yang layak dibaca. Kami akan mengulang banyak nasihat dari sumber tersebut
di sini, ditambah beberapa lagi. Juga, dapatkan [USB data
blocker](https://www.amazon.com/dp/B00QRRZ2QM/), karena [USB itu
menakutkan](https://www.bleepingcomputer.com/news/security/heres-a-list-of-29-different-types-of-usb-attacks/).

## Autentikasi

Hal pertama yang sebaiknya Anda lakukan, jika belum, adalah mengunduh
password manager. Beberapa yang baik adalah:

 - [1password](https://1password.com/)
 - [KeePass](https://keepass.info/)
 - [BitWarden](https://bitwarden.com/)
 - [`pass`](https://git.zx2c4.com/password-store/about/)

Jika Anda sangat paranoid, gunakan yang mengenkripsi password
secara lokal di komputer Anda, bukan menyimpannya dalam plain-text di
server. Gunakan itu untuk menghasilkan password
untuk semua situs web yang Anda pedulikan saat ini. Lalu, aktifkan
autentikasi dua faktor, idealnya dengan dongle
[FIDO/U2F](https://fidoalliance.org/) (misalnya
[YubiKey](https://www.yubico.com/quiz/), yang memiliki [diskon 20%
untuk pelajar](https://www.yubico.com/why-yubico/for-education/)). TOTP
(seperti Google Authenticator atau Duo) juga akan berfungsi dalam keadaan darurat, tetapi
[tidak melindungi dari
phishing](https://twitter.com/taviso/status/1082015009348104192). SMS
hampir tidak berguna kecuali threat model Anda hanya mencakup orang asing acak
yang mengambil password Anda saat transit.

Juga, catatan tentang paper key. Sering kali, layanan akan memberi Anda "backup
key" yang dapat Anda gunakan sebagai faktor kedua jika Anda kehilangan faktor kedua
yang asli (btw, selalu simpan dongle cadangan di tempat aman!). Meskipun Anda
_dapat_ menempelkannya di password manager Anda, itu berarti jika
seseorang memperoleh akses ke password manager Anda, Anda benar-benar celaka (tetapi
mungkin Anda tidak masalah dengan threat model itu). Jika Anda benar-benar paranoid,
cetak paper key ini, jangan pernah menyimpannya secara digital, dan letakkan
di brankas di dunia nyata.

## Komunikasi Privat

Gunakan [Signal](https://www.signal.org/) ([instruksi
setup](https://medium.com/@mshelton/signal-for-beginners-c6b44f76a1f0).
[Wire](https://wire.com/en/) juga
[baik](https://www.securemessagingapps.com/); WhatsApp tidak masalah; [jangan gunakan
Telegram](https://twitter.com/bascule/status/897187286554628096)).
Messenger desktop cukup rusak (sebagian karena biasanya bergantung
pada Electron, yang merupakan trust stack besar).

E-mail sangat bermasalah, bahkan jika ditandatangani PGP. E-mail umumnya
tidak forward-secure, dan masalah distribusi key cukup
parah. [keybase.io](https://keybase.io/) membantu, dan berguna untuk
sejumlah alasan lain. Juga, PGP key umumnya ditangani di komputer
desktop, yang merupakan salah satu lingkungan komputasi paling tidak aman.
Terkait itu, pertimbangkan membeli Chromebook, atau cukup bekerja di tablet dengan
keyboard.

## Keamanan Berkas

Keamanan berkas itu sulit, dan beroperasi pada banyak level. Apa yang sedang Anda
coba amankan?

[![$5 wrench](https://imgs.xkcd.com/comics/security.png)](https://xkcd.com/538/)

 - Serangan offline (seseorang mencuri laptop Anda saat mati): aktifkan
   full disk encryption. ([cryptsetup +
   LUKS](https://wiki.archlinux.org/index.php/Dm-crypt/Encrypting_a_non-root_file_system)
   di Linux,
   [BitLocker](https://fossbytes.com/enable-full-disk-encryption-windows-10/)
   di Windows, [FileVault](https://support.apple.com/en-us/HT204837) di
   macOS. Perhatikan bahwa ini tidak akan membantu jika penyerang _juga_ menahan Anda dan
   benar-benar menginginkan rahasia Anda.
 - Serangan online (seseorang memiliki laptop Anda dan laptop itu menyala): gunakan file
   encryption. Ada dua mekanisme utama untuk melakukannya
    - Filesystem terenkripsi: perangkat lunak stacked filesystem encryption mengenkripsi berkas satu per satu alih-alih memiliki block device terenkripsi. Anda dapat "me-mount" filesystem ini dengan memberikan decryption key, lalu menjelajahi berkas di dalamnya dengan bebas. Ketika Anda meng-unmount-nya, berkas tersebut semuanya tidak tersedia. Solusi modern termasuk [gocryptfs](https://github.com/rfjakob/gocryptfs) dan [eCryptFS](https://www.ecryptfs.org/). Perbandingan lebih detail dapat ditemukan [di sini](https://nuetzlich.net/gocryptfs/comparison/) dan [di sini](https://wiki.archlinux.org/index.php/disk_encryption#Comparison_table)
    - Berkas terenkripsi: enkripsi berkas individual dengan symmetric
      encryption (lihat `gpg -c`) dan secret key. Atau, seperti `pass`, juga
      enkripsi key tersebut dengan public key Anda sehingga hanya Anda yang dapat membacanya kembali
      nanti dengan private key Anda. Pengaturan enkripsi yang tepat sangat
      penting!
 - [Plausible
   deniability](https://en.wikipedia.org/wiki/Plausible_deniability)
   (sepertinya apa masalahnya, Pak Petugas?): biasanya performa lebih rendah,
   dan lebih mudah kehilangan data. Sulit membuktikan bahwa ini benar-benar memberikan
   [deniable
   encryption](https://en.wikipedia.org/wiki/Deniable_encryption)! Lihat
   [diskusi
   di sini](https://security.stackexchange.com/questions/135846/is-plausible-deniability-actually-feasible-for-encrypted-volumes-disks),
   lalu pertimbangkan apakah Anda mungkin ingin mencoba
   [VeraCrypt](https://www.veracrypt.fr/en/Home.html) (fork yang masih dipelihara
   dari TrueCrypt yang legendaris).
 - Backup terenkripsi: gunakan [Tarsnap](https://www.tarsnap.com/) atau [Borgbase](https://www.borgbase.com/)
    - Pikirkan apakah penyerang dapat menghapus backup Anda jika mereka
      memperoleh laptop Anda!

## Keamanan & Privasi Internet

Internet adalah tempat yang _sangat_ menakutkan. Jaringan WiFi terbuka
[menakutkan](https://www.troyhunt.com/the-beginners-guide-to-breaking-website/)
[sekali](https://www.troyhunt.com/talking-with-scott-hanselman-on/). Pastikan
Anda menghapusnya setelahnya, jika tidak ponsel Anda akan dengan senang hati
mengumumkan dan terhubung kembali ke sesuatu dengan nama yang sama nanti!

Jika Anda berada di jaringan yang tidak Anda percayai, VPN _mungkin_ layak,
tetapi ingat bahwa Anda mempercayai penyedia VPN _sangat besar_. Apakah Anda
benar-benar memercayai mereka lebih daripada ISP Anda? Jika Anda benar-benar menginginkan VPN, gunakan
penyedia yang Anda yakin tepercaya, dan sebaiknya Anda membayarnya. Atau
siapkan [WireGuard](https://www.wireguard.com/) sendiri -- itu
[luar biasa](https://web.archive.org/web/20210526211307/https://latacora.micro.blog/there-will-be/)!

Ada juga pengaturan konfigurasi aman untuk banyak aplikasi
yang mendukung internet di [cipherlist.eu](https://cipherlist.eu/). Jika Anda sangat
berorientasi privacy, [privacytools.io](https://privacytools.io) juga sumber yang
baik.

Sebagian dari Anda mungkin bertanya-tanya tentang [Tor](https://www.torproject.org/). Ingat
bahwa Tor _tidak_ terlalu tahan terhadap penyerang global yang kuat,
dan lemah terhadap serangan traffic analysis. Tor mungkin
berguna untuk menyembunyikan lalu lintas dalam skala kecil, tetapi tidak benar-benar memberi Anda
banyak dalam hal privacy. Anda lebih baik menggunakan layanan yang lebih aman
sejak awal (Signal, TLS + certificate pinning, dsb.).

## Keamanan Web

Jadi, Anda ingin menjelajahi Web juga?
Ya ampun, Anda benar-benar mendorong keberuntungan di sini.

Pasang [HTTPS Everywhere](https://www.eff.org/https-everywhere).
SSL/TLS itu
[kritis](https://www.troyhunt.com/ssl-is-not-about-encryption/), dan
ini _bukan_ hanya soal enkripsi, tetapi juga soal kemampuan memverifikasi
bahwa Anda berbicara dengan layanan yang tepat sejak awal! Jika Anda menjalankan
web server sendiri, [ujilah](https://www.ssllabs.com/ssltest/index.html). Konfigurasi TLS
[bisa menjadi rumit](https://wiki.mozilla.org/Security/Server_Side_TLS).
HTTPS Everywhere akan berusaha sebaik mungkin untuk tidak pernah membawa Anda ke situs
HTTP ketika ada alternatif. Itu tidak menyelamatkan Anda, tetapi membantu.
Jika Anda benar-benar paranoid, blacklist CA SSL/TLS mana pun yang tidak
benar-benar Anda butuhkan.

Pasang [uBlock Origin](https://github.com/gorhill/uBlock). Ini adalah
[wide-spectrum
blocker](https://github.com/gorhill/uBlock/wiki/Blocking-mode) yang
tidak hanya menghentikan iklan, tetapi segala macam komunikasi pihak ketiga yang mungkin
dicoba sebuah halaman. Dan inline script dan sejenisnya. Jika Anda bersedia meluangkan
waktu untuk konfigurasi agar semuanya berfungsi, masuk ke [medium
mode](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-medium-mode)
atau bahkan [hard
mode](https://github.com/gorhill/uBlock/wiki/Blocking-mode:-hard-mode).
Mode tersebut _akan_ membuat sebagian situs tidak berfungsi sampai Anda cukup mengutak-atik
pengaturannya, tetapi juga akan secara signifikan meningkatkan keamanan daring
Anda.

Jika Anda menggunakan Firefox, aktifkan [Multi-Account
Containers](https://support.mozilla.org/en-US/kb/containers). Buat
container terpisah untuk media sosial, perbankan, belanja, dsb. Firefox
akan menjaga cookie dan state lain untuk setiap container sepenuhnya
terpisah, sehingga situs yang Anda kunjungi di satu container tidak dapat mengintip
data sensitif dari yang lain. Di Google Chrome, Anda dapat menggunakan [Chrome
Profile](https://support.google.com/chrome/answer/2364824) untuk mencapai
hasil serupa.

## Latihan

1. Enkripsi sebuah berkas menggunakan PGP
1. Gunakan veracrypt untuk membuat volume terenkripsi sederhana
1. Aktifkan 2FA untuk akun paling sensitif terhadap data Anda yaitu GMail, Dropbox, Github, &c
