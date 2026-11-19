---
layout: lecture-id
title: "Virtual Machine dan Container"
presenter: Anish, Jon
date: 2019-01-15
order: 2
video:
  aspect: 56.25
  id: LJ9ki5zq6Ik
lang: id
permalink: /id/2019/virtual-machines/
---

# Virtual Machines

Virtual machine adalah komputer yang disimulasikan. Anda dapat mengonfigurasi guest virtual
machine dengan sistem operasi dan konfigurasi tertentu lalu menggunakannya tanpa
memengaruhi environment host Anda.

Untuk kelas ini, Anda dapat menggunakan VM untuk bereksperimen dengan sistem operasi, perangkat lunak,
dan konfigurasi tanpa risiko: Anda tidak akan memengaruhi environment pengembangan utama
Anda.

Secara umum, VM memiliki banyak kegunaan. VM umumnya digunakan untuk menjalankan perangkat lunak
yang hanya berjalan pada sistem operasi tertentu (misalnya menggunakan Windows VM di Linux
untuk menjalankan perangkat lunak khas Windows). VM sering digunakan untuk bereksperimen dengan
perangkat lunak yang berpotensi berbahaya.

## Fitur berguna

- **Isolasi**: hypervisor melakukan tugas yang cukup baik dalam mengisolasi guest dari
host, sehingga Anda dapat menggunakan VM untuk menjalankan perangkat lunak buggy atau tidak tepercaya secara
cukup aman.

- **Snapshot**: Anda dapat mengambil "snapshot" virtual machine Anda, menangkap
seluruh keadaan mesin (disk, memori, dsb.), membuat perubahan pada mesin Anda,
lalu memulihkan ke keadaan sebelumnya. Ini berguna untuk menguji
tindakan yang berpotensi destruktif, antara lain.

## Kekurangan

Virtual machine umumnya lebih lambat daripada berjalan di bare metal, sehingga bisa
tidak cocok untuk aplikasi tertentu.

## Persiapan

- **Sumber daya**: dibagi dengan mesin host; waspadai ini saat mengalokasikan
sumber daya fisik.

- **Networking**: banyak opsi, NAT default seharusnya berfungsi baik untuk sebagian besar use
case.

- **Guest addon**: banyak hypervisor dapat memasang perangkat lunak di guest untuk
memungkinkan integrasi yang lebih baik dengan sistem host. Anda sebaiknya menggunakan ini jika bisa.

## Sumber daya

- Hypervisor
    - [VirtualBox](https://www.virtualbox.org/) (open-source)
    - [Virt-manager](https://virt-manager.org/) (open-source, mengelola virtual machine KVM dan container LXC)
    - [VMWare](https://www.vmware.com/) (komersial, tersedia dari IS&T [untuk
    mahasiswa MIT](https://ist.mit.edu/vmware-fusion))

Jika Anda sudah familiar dengan hypervisor/VM populer Anda mungkin ingin mempelajari lebih lanjut cara melakukan ini dengan cara yang ramah command line. Salah satu opsi adalah toolkit [libvirt](https://wiki.libvirt.org/page/UbuntuKVMWalkthrough) yang memungkinkan Anda mengelola beberapa penyedia virtualisasi/hypervisor berbeda.

## Latihan

1. Unduh dan pasang sebuah hypervisor.

1. Buat virtual machine baru dan pasang distribusi Linux (misalnya
[Debian](https://www.debian.org/)).

1. Bereksperimenlah dengan snapshot. Coba hal yang selalu ingin Anda coba, seperti
   menjalankan `sudo rm -rf --no-preserve-root /`, dan lihat apakah Anda dapat pulih
   dengan mudah.

1. Baca apa itu [fork-bomb](https://en.wikipedia.org/wiki/Fork_bomb) (`:(){ :|:& };:`) dan jalankan di VM untuk melihat bahwa isolasi sumber daya (CPU, Memory, &c) bekerja.

1. Pasang guest addon dan bereksperimenlah dengan mode windowing berbeda, file
   sharing, dan fitur lain.

# Containers

Virtual Machine relatif berat; bagaimana jika Anda ingin menjalankan
mesin secara otomatis? Masuklah container!

 - Amazon Firecracker
 - Docker
 - rkt
 - lxc

Container _sebagian besar_ hanyalah kumpulan berbagai fitur keamanan Linux,
seperti virtual file system, virtual network interface, chroot,
trik virtual memory, dan sejenisnya, yang bersama-sama memberikan kesan
virtualisasi.

Tidak seaman atau seisolasi VM, tetapi cukup dekat dan semakin
baik. Biasanya performa lebih tinggi, dan jauh lebih cepat dimulai, tetapi tidak
selalu.

Peningkatan performa berasal dari fakta bahwa berbeda dengan VM yang menjalankan seluruh salinan sistem operasi, container berbagi kernel linux dengan host. Namun perhatikan bahwa jika Anda menjalankan container linux di Windows/macOS sebuah Linux VM perlu aktif sebagai lapisan perantara di antara keduanya.

![Docker vs VM](/2019/files/containers-vs-vms.png)
_Perbandingan antara container Docker dan Virtual Machine. Kredit: blog.docker.com_

Container praktis ketika Anda ingin menjalankan tugas otomatis dalam
setup terstandar:

 - Build system
 - Environment pengembangan
 - Server terpaket
 - Menjalankan program tidak tepercaya
   - Menilai kiriman mahasiswa
   - (Sebagian) cloud computing
 - Continuous integration
   - Travis CI
   - GitHub Actions

Lebih jauh lagi, perangkat lunak container seperti Docker juga telah digunakan secara ekstensif sebagai solusi untuk [dependency hell](https://en.wikipedia.org/wiki/Dependency_hell). Jika sebuah mesin perlu menjalankan banyak layanan dengan dependency yang saling bertentangan, layanan tersebut dapat diisolasi menggunakan container.

Biasanya, Anda menulis berkas yang mendefinisikan cara membangun container Anda.
Anda mulai dengan semacam _base image_ minimal (seperti Alpine Linux), lalu
daftar perintah untuk dijalankan guna menyiapkan environment yang Anda inginkan (memasang
paket, menyalin berkas, membangun sesuatu, menulis berkas config, dsb.). Biasanya,
ada juga cara untuk menentukan port eksternal apa pun yang seharusnya
tersedia, dan sebuah _entrypoint_ yang menentukan perintah apa yang harus dijalankan
ketika container dimulai (seperti skrip penilaian).

Dengan cara yang serupa dengan situs web repositori kode (seperti [GitHub](https://github.com/)) ada beberapa situs web repositori container (seperti [DockerHub](https://hub.docker.com/)) di mana banyak layanan perangkat lunak memiliki image yang sudah dibangun dan dapat dengan mudah di-deploy.

## Latihan

1. Pilih perangkat lunak container (Docker, LXC, …) dan pasang image Linux sederhana. Coba SSH ke dalamnya.

1. Cari dan unduh image container yang sudah dibangun untuk web server populer (nginx, apache, …)
