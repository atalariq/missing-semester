---
layout: lecture-id
title: "Security dan Cryptography"
description: >
  Pelajari cryptographic primitive seperti hash dan key derivation function, serta pahami cara tool seperti Git dan SSH menggunakannya.
thumbnail: /static/assets/thumbnails/2020/lec9.png
date: 2020-01-28
ready: true
video:
  aspect: 56.25
  id: tjwobAmnKTo
special: true
lang: id
permalink: /id/2020/security/
---

[Kuliah security dan privacy tahun lalu](/2019/security/) berfokus pada bagaimana Anda
dapat lebih aman sebagai _pengguna_ komputer. Tahun ini, kami akan memfokuskan pada konsep
security dan cryptography yang relevan untuk memahami tool yang dibahas
sebelumnya di kelas ini, seperti penggunaan hash function di Git atau key
derivation function dan cryptosystem simetris/asimetris di SSH.

Kuliah ini bukan pengganti kursus yang lebih ketat dan lengkap tentang
keamanan sistem komputer ([6.858](https://css.csail.mit.edu/6.858/)) atau
cryptography ([6.857](https://courses.csail.mit.edu/6.857/) dan 6.875). Jangan
melakukan pekerjaan security tanpa pelatihan formal di bidang security. Kecuali Anda seorang ahli,
jangan [membuat sendiri
crypto](https://www.schneier.com/blog/archives/2015/05/amateurs_produc.html).
Prinsip yang sama berlaku untuk keamanan sistem.

Kuliah ini memiliki perlakuan yang sangat informal (tetapi kami anggap praktis) atas konsep
cryptography dasar. Kuliah ini tidak akan cukup untuk mengajarkan cara
_merancang_ sistem aman atau protokol kriptografis, tetapi kami berharap ini cukup
untuk memberi Anda pemahaman umum tentang program dan protokol yang
sudah Anda gunakan.

# Entropy

[Entropy](https://en.wikipedia.org/wiki/Entropy_(information_theory)) adalah
ukuran keacakan. Ini berguna, misalnya, saat menentukan
kekuatan sebuah password.

![XKCD 936: Password Strength](https://imgs.xkcd.com/comics/password_strength.png)

Seperti yang diilustrasikan [komik XKCD](https://xkcd.com/936/) di atas, password seperti
"correcthorsebatterystaple" lebih aman daripada "Tr0ub4dor&3". Tetapi bagaimana
Anda mengukur hal semacam itu?

Entropy diukur dalam _bit_, dan ketika memilih secara acak seragam dari
sekumpulan hasil yang mungkin, entropy sama dengan `log_2(# of possibilities)`.
Lemparan koin adil memberikan 1 bit entropy. Lemparan dadu (dadu 6 sisi) memiliki
\~2,58 bit entropy.

Anda sebaiknya menganggap bahwa penyerang mengetahui _model_ password tersebut, tetapi
bukan keacakan (misalnya dari [lemparan
dadu](https://en.wikipedia.org/wiki/Diceware)) yang digunakan untuk memilih password
tertentu.

Berapa bit entropy yang cukup? Itu bergantung pada threat model Anda. Untuk tebakan
daring, seperti yang ditunjukkan komik XKCD, \~40 bit entropy sudah cukup baik. Untuk
tahan terhadap tebakan offline, password yang lebih kuat akan diperlukan (misalnya
80 bit, atau lebih).

# Hash functions

Sebuah [cryptographic hash
function](https://en.wikipedia.org/wiki/Cryptographic_hash_function) memetakan data
berukuran arbitrer ke ukuran tetap, dan memiliki beberapa sifat khusus. Spesifikasi
kasar sebuah hash function adalah sebagai berikut:

```
hash(value: array<byte>) -> vector<byte, N>  (for some fixed N)
```

Contoh hash function adalah [SHA1](https://en.wikipedia.org/wiki/SHA-1),
yang digunakan di Git. Fungsi ini memetakan input berukuran arbitrer ke output 160-bit (yang
dapat direpresentasikan sebagai 40 karakter heksadesimal). Kita dapat mencoba hash SHA1
pada sebuah input menggunakan perintah `sha1sum`:

```console
$ printf 'hello' | sha1sum
aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
$ printf 'hello' | sha1sum
aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d
$ printf 'Hello' | sha1sum
f7ff9e8b7bb2e09b70935a5d785e0cc5d9d0abf0
```

Pada tingkat tinggi, hash function dapat dianggap sebagai fungsi (deterministik) yang
tampak acak dan sulit dibalik (dan ini adalah [model ideal dari
hash function](https://en.wikipedia.org/wiki/Random_oracle)). Sebuah hash function
memiliki sifat berikut:

- Deterministik: input yang sama selalu menghasilkan output yang sama.
- Non-invertible: sulit menemukan input `m` sehingga `hash(m) = h` untuk
suatu output `h` yang diinginkan.
- Tahan collision target: diberikan input `m_1`, sulit menemukan
input berbeda `m_2` sehingga `hash(m_1) = hash(m_2)`.
- Tahan collision: sulit menemukan dua input `m_1` dan `m_2` sehingga
`hash(m_1) = hash(m_2)` (perhatikan bahwa ini adalah sifat yang secara ketat lebih kuat daripada
ketahanan collision target).

Catatan: meskipun mungkin berfungsi untuk tujuan tertentu, SHA-1 [tidak
lagi](https://web.archive.org/web/20260207211148/https://shattered.io/) dianggap sebagai hash function kriptografis yang kuat.
Anda mungkin menemukan tabel [masa hidup cryptographic hash
function](https://valerieaurora.org/hash.html) ini menarik. Namun, perhatikan bahwa
merekomendasikan hash function tertentu berada di luar cakupan kuliah ini. Jika Anda
melakukan pekerjaan di mana ini penting, Anda memerlukan pelatihan formal di bidang
security/cryptography.

## Aplikasi

- Git, untuk content-addressed storage. Gagasan [hash
function](https://en.wikipedia.org/wiki/Hash_function) adalah konsep yang lebih umum
(ada hash function non-kriptografis). Mengapa Git menggunakan
cryptographic hash function?
- Ringkasan singkat isi sebuah berkas. Perangkat lunak sering dapat diunduh
dari mirror (yang berpotensi kurang tepercaya), misalnya ISO Linux, dan akan
menyenangkan jika kita tidak harus mempercayainya. Situs resmi biasanya memposting hash
di samping tautan unduhan (yang menunjuk ke mirror pihak ketiga), sehingga
hash dapat diperiksa setelah mengunduh berkas.
- [Commitment scheme](https://en.wikipedia.org/wiki/Commitment_scheme).
Misalkan Anda ingin berkomitmen pada nilai tertentu, tetapi mengungkapkan nilai itu sendiri
nanti. Misalnya, saya ingin melakukan lemparan koin adil "dalam pikiran saya", tanpa
koin bersama tepercaya yang dapat dilihat kedua pihak. Saya dapat memilih nilai `r =
random()`, lalu membagikan `h = sha256(r)`. Kemudian, Anda dapat menyebut heads atau tails
(kita sepakati bahwa `r` genap berarti heads, dan `r` ganjil berarti tails). Setelah Anda
menyebut, saya dapat mengungkapkan nilai saya `r`, dan Anda dapat mengonfirmasi bahwa saya tidak curang dengan
memeriksa `sha256(r)` cocok dengan hash yang saya bagikan sebelumnya.

# Key derivation functions

Konsep yang terkait dengan cryptographic hash, [key derivation
function](https://en.wikipedia.org/wiki/Key_derivation_function) (KDF) digunakan
untuk sejumlah aplikasi, termasuk menghasilkan output berpanjang tetap
untuk digunakan sebagai key dalam algoritma kriptografis lain. Biasanya, KDF sengaja
dibuat lambat, untuk memperlambat serangan brute-force offline.

## Aplikasi

- Menghasilkan key dari passphrase untuk digunakan dalam algoritma kriptografis lain
(misalnya symmetric cryptography, lihat di bawah).
- Menyimpan kredensial login. Menyimpan password plaintext itu buruk; pendekatan
yang benar adalah menghasilkan dan menyimpan
[salt](https://en.wikipedia.org/wiki/Salt_(cryptography)) acak `salt = random()` untuk
setiap pengguna, menyimpan `KDF(password + salt)`, dan memverifikasi upaya login dengan
menghitung ulang KDF dari password yang dimasukkan dan salt yang tersimpan.

# Symmetric cryptography

Menyembunyikan isi pesan mungkin adalah konsep pertama yang Anda pikirkan ketika
memikirkan cryptography. Symmetric cryptography mencapai ini dengan
rangkaian fungsionalitas berikut:

```
keygen() -> key  (this function is randomized)

encrypt(plaintext: array<byte>, key) -> array<byte>  (the ciphertext)
decrypt(ciphertext: array<byte>, key) -> array<byte>  (the plaintext)
```

Fungsi encrypt memiliki sifat bahwa diberikan output (ciphertext), sulit
menentukan input (plaintext) tanpa key. Fungsi decrypt
memiliki sifat kebenaran yang jelas, bahwa `decrypt(encrypt(m, k), k) = m`.

Contoh symmetric cryptosystem yang banyak digunakan saat ini adalah
[AES](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

## Aplikasi

- Mengenkripsi berkas untuk penyimpanan di layanan cloud yang tidak tepercaya. Ini dapat
digabungkan dengan KDF, sehingga Anda dapat mengenkripsi berkas dengan passphrase. Hasilkan `key
= KDF(passphrase)`, lalu simpan `encrypt(file, key)`.

# Asymmetric cryptography

Istilah "asymmetric" merujuk pada adanya dua key, dengan dua peran berbeda.
Private key, seperti namanya, dimaksudkan untuk dijaga kerahasiaannya, sedangkan
public key dapat dibagikan secara publik dan tidak akan memengaruhi keamanan (berbeda dengan membagikan
key pada symmetric cryptosystem). Asymmetric cryptosystem menyediakan
rangkaian fungsionalitas berikut, untuk encrypt/decrypt dan sign/verify:

```
keygen() -> (public key, private key)  (this function is randomized)

encrypt(plaintext: array<byte>, public key) -> array<byte>  (the ciphertext)
decrypt(ciphertext: array<byte>, private key) -> array<byte>  (the plaintext)

sign(message: array<byte>, private key) -> array<byte>  (the signature)
verify(message: array<byte>, signature: array<byte>, public key) -> bool  (whether or not the signature is valid)
```

Fungsi encrypt/decrypt memiliki sifat serupa dengan padanannya dari
symmetric cryptosystem. Sebuah pesan dapat dienkripsi menggunakan public key.
Diberikan output (ciphertext), sulit menentukan input (plaintext)
tanpa private key. Fungsi decrypt memiliki sifat kebenaran
yang jelas, bahwa `decrypt(encrypt(m, public key), private key) = m`.

Enkripsi simetris dan asimetris dapat dibandingkan dengan gembok fisik. Sebuah
symmetric cryptosystem seperti kunci pintu: siapa pun yang memiliki kuncinya dapat mengunci dan
membukanya. Asymmetric encryption seperti gembok dengan kunci. Anda dapat memberikan
gembok yang terbuka kepada seseorang (public key), orang itu dapat memasukkan pesan ke dalam
kotak lalu memasang gembok tersebut, dan setelah itu, hanya Anda yang dapat membuka gembok
karena Anda menyimpan kuncinya (private key).

Fungsi sign/verify memiliki sifat yang sama seperti yang Anda harapkan dari tanda tangan
fisik, yaitu sulit memalsukan tanda tangan. Apa pun
pesannya, tanpa private key, sulit menghasilkan tanda tangan sehingga
`verify(message, signature, public key)` mengembalikan true. Dan tentu saja, fungsi
verify memiliki sifat kebenaran yang jelas bahwa `verify(message,
sign(message, private key), public key) = true`.

## Aplikasi

- [Enkripsi email PGP](https://en.wikipedia.org/wiki/Pretty_Good_Privacy).
Orang dapat memposting public key mereka secara daring (misalnya di keyserver PGP, atau di
[Keybase](https://keybase.io/)). Siapa pun dapat mengirimi mereka email terenkripsi.
- Private messaging. Aplikasi seperti [Signal](https://signal.org/) dan
[Keybase](https://keybase.io/) menggunakan asymmetric key untuk membangun saluran komunikasi
privat.
- Menandatangani perangkat lunak. Git dapat memiliki commit dan tag bertanda tangan GPG. Dengan public key
yang diposting, siapa pun dapat memverifikasi keaslian perangkat lunak yang diunduh.

## Distribusi key

Asymmetric-key cryptography luar biasa, tetapi memiliki tantangan besar dalam
mendistribusikan public key / memetakan public key ke identitas dunia nyata. Ada
banyak solusi untuk masalah ini. Signal memiliki satu solusi sederhana: trust on
first use, dan mendukung pertukaran public key out-of-band (Anda memverifikasi
"safety number" teman Anda secara langsung). PGP memiliki solusi berbeda, yaitu
[web of trust](https://en.wikipedia.org/wiki/Web_of_trust). Keybase memiliki solusi
lain lagi yaitu [social
proof](https://keybase.io/blog/chat-apps-softer-than-tofu) (beserta ide rapi lainnya).
Setiap model memiliki kelebihannya; kami (para pengajar) menyukai model
Keybase.

# Studi kasus

## Password manager

Ini adalah tool penting yang sebaiknya dicoba digunakan oleh semua orang (misalnya
[KeePassXC](https://keepassxc.org/), [pass](https://git.zx2c4.com/password-store/about/),
dan [1Password](https://1password.com)). Password manager memudahkan penggunaan password
unik berentropy tinggi yang dihasilkan secara acak untuk semua login Anda, dan menyimpan
semua password Anda di satu tempat, terenkripsi dengan symmetric cipher dengan key
yang dihasilkan dari passphrase menggunakan KDF.

Menggunakan password manager memungkinkan Anda menghindari penggunaan ulang password (sehingga Anda kurang terdampak
ketika situs web terkompromi), menggunakan password berentropy tinggi (sehingga Anda lebih kecil kemungkinannya
terkompromi), dan hanya perlu mengingat satu password berentropy tinggi.

## Autentikasi dua faktor

[Autentikasi dua
faktor](https://en.wikipedia.org/wiki/Multi-factor_authentication)
(2FA) mengharuskan Anda menggunakan passphrase ("sesuatu yang Anda ketahui") bersama dengan
authenticator 2FA (seperti [YubiKey](https://www.yubico.com/), "sesuatu yang Anda miliki")
untuk melindungi dari password yang dicuri dan
serangan [phishing](https://en.wikipedia.org/wiki/Phishing).

## Enkripsi seluruh disk

Menjaga seluruh disk laptop Anda terenkripsi adalah cara mudah melindungi data Anda
jika laptop Anda dicuri. Anda dapat menggunakan [cryptsetup +
LUKS](https://wiki.archlinux.org/index.php/Dm-crypt/Encrypting_a_non-root_file_system)
di Linux,
[BitLocker](https://fossbytes.com/enable-full-disk-encryption-windows-10/) di
Windows, atau [FileVault](https://support.apple.com/en-us/HT204837) di macOS.
Ini mengenkripsi seluruh disk dengan symmetric cipher, dengan key yang dilindungi
passphrase.

## Private messaging

Gunakan [Signal](https://signal.org/) atau [Keybase](https://keybase.io/). Keamanan
end-to-end di-bootstrap dari asymmetric-key encryption. Memperoleh
public key kontak Anda adalah langkah kritis di sini. Jika Anda menginginkan keamanan yang baik, Anda
perlu mengautentikasi public key secara out-of-band (dengan Signal atau Keybase), atau memercayai
social proof (dengan Keybase).

## SSH

Kita telah membahas penggunaan SSH dan SSH key pada [kuliah
sebelumnya](/2020/command-line/#remote-machines). Mari lihat aspek
cryptography-nya.

Ketika Anda menjalankan `ssh-keygen`, tool tersebut menghasilkan pasangan asymmetric key, `public_key,
private_key`. Ini dihasilkan secara acak, menggunakan entropy yang disediakan
sistem operasi (dikumpulkan dari peristiwa perangkat keras, dsb.). Public key
disimpan apa adanya (karena publik, menjaganya tetap rahasia tidak penting), tetapi
saat disimpan, private key sebaiknya terenkripsi di disk. Program `ssh-keygen`
meminta passphrase kepada pengguna, dan ini dimasukkan melalui key derivation
function untuk menghasilkan key, yang kemudian digunakan untuk mengenkripsi private key dengan
symmetric cipher.

Saat digunakan, setelah server mengetahui public key klien (tersimpan di
berkas `.ssh/authorized_keys`), klien yang terhubung dapat membuktikan identitasnya menggunakan
asymmetric signature. Ini dilakukan melalui
[challenge-response](https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication).
Pada tingkat tinggi, server memilih angka acak dan mengirimkannya ke klien.
Klien lalu menandatangani pesan ini dan mengirimkan tanda tangannya kembali ke server,
yang memeriksa tanda tangan tersebut terhadap public key yang tercatat. Ini secara efektif
membuktikan bahwa klien memiliki private key yang bersesuaian dengan
public key yang ada di berkas `.ssh/authorized_keys` server, sehingga server
dapat mengizinkan klien login.

{% comment %}
extra topics, if there's time

security concepts, tips
- biometrics
- HTTPS
{% endcomment %}

# Sumber daya

- [Catatan tahun lalu](/2019/security/): dari saat kuliah ini lebih berfokus pada security dan privacy sebagai pengguna komputer
- [Cryptographic Right Answers](https://latacora.micro.blog/2018/04/03/cryptographic-right-answers.html): menjawab "crypto apa yang harus saya gunakan untuk X?" untuk banyak X yang umum.

# Latihan

1. **Entropy.**
    1. Misalkan sebuah password dipilih sebagai konkatenasi empat kata kamus
       huruf kecil, di mana setiap kata dipilih secara acak seragam dari
       kamus berukuran 100.000. Contoh password semacam itu adalah
       `correcthorsebatterystaple`. Berapa bit entropy yang dimilikinya?
    1. Pertimbangkan skema alternatif di mana password dipilih sebagai rangkaian
       8 karakter alfanumerik acak (termasuk huruf kecil dan
       huruf besar). Contohnya adalah `rg8Ql34g`. Berapa bit entropy
       yang dimilikinya?
    1. Mana password yang lebih kuat?
    1. Misalkan penyerang dapat mencoba menebak 10.000 password per detik. Secara
       rata-rata, berapa lama waktu yang dibutuhkan untuk memecahkan masing-masing password?
1. **Cryptographic hash functions.** Unduh image Debian dari sebuah
   [mirror](https://www.debian.org/CD/http-ftp/) (misalnya [dari mirror
   Argentina ini](http://debian.xfree.com.ar/debian-cd/current/amd64/iso-cd/)).
   Periksa silang hash-nya (misalnya menggunakan perintah `sha256sum`) dengan hash
   yang diperoleh dari situs resmi Debian (misalnya [berkas
   ini](https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/SHA256SUMS)
   yang di-host di `debian.org`, jika Anda mengunduh berkas yang ditautkan dari
   mirror Argentina tersebut).
1. **Symmetric cryptography.** Enkripsi sebuah berkas dengan enkripsi AES, menggunakan
   [OpenSSL](https://www.openssl.org/): `openssl aes-256-cbc -salt -in {input
   filename} -out {output filename}`. Lihat isinya menggunakan `cat` atau
   `hexdump`. Dekripsi dengan `openssl aes-256-cbc -d -in {input filename} -out
   {output filename}` dan konfirmasi bahwa isinya cocok dengan aslinya menggunakan
   `cmp`.
1. **Asymmetric cryptography.**
    1. Siapkan [SSH
       key](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2)
       di komputer yang dapat Anda akses (bukan Athena, karena Kerberos berinteraksi
       secara aneh dengan SSH key). Pastikan
       private key Anda terenkripsi dengan passphrase, sehingga terlindungi saat
       disimpan.
    1. [Siapkan GPG](https://www.digitalocean.com/community/tutorials/how-to-use-gpg-to-encrypt-and-sign-messages)
    1. Kirim email terenkripsi ke Anish ([public key](https://keybase.io/anish)).
    1. Tandatangani sebuah commit Git dengan `git commit -S` atau buat tag Git bertanda tangan dengan
       `git tag -s`. Verifikasi tanda tangan pada commit dengan `git show
       --show-signature` atau pada tag dengan `git tag -v`.
