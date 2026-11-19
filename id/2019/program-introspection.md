---
layout: lecture-id
title: "Program Introspection"
presenter: Anish
date: 2019-01-29
order: 1
video:
  aspect: 62.5
  id: 74MhV-7hYzg
lang: id
permalink: /id/2019/program-introspection/
---

# Debugging

Ketika printf-debugging tidak cukup baik: gunakan debugger.

Debugger memungkinkan Anda berinteraksi dengan eksekusi sebuah program, memungkinkan Anda melakukan
hal-hal seperti:

- menghentikan eksekusi program ketika mencapai baris tertentu
- single-step melalui program
- memeriksa nilai variabel
- banyak fitur lanjutan lainnya

## GDB/LLDB

[GDB](https://www.gnu.org/software/gdb/) dan [LLDB](https://lldb.llvm.org/).
Mendukung banyak bahasa mirip C.

Mari lihat [example.c](/2019/files/example.c). Kompilasi dengan flag debug:
`gcc -g -o example example.c`.

Buka GDB:

`gdb example`

Beberapa perintah:

- `run`
- `b {name of function}` - menetapkan breakpoint
- `b {file}:{line}` - menetapkan breakpoint
- `c` - continue
- `step` / `next` / `finish` - step in / step over / step out
- `p {variable}` - mencetak nilai variabel
- `watch {expression}` - menetapkan watchpoint yang terpicu ketika nilai ekspresi berubah
- `rwatch {expression}` - menetapkan watchpoint yang terpicu ketika nilai dibaca
- `layout`

## PDB

[PDB](https://docs.python.org/3/library/pdb.html) adalah debugger Python.

Sisipkan `import pdb; pdb.set_trace()` di tempat Anda ingin masuk ke PDB, pada dasarnya
hibrida antara debugger (seperti GDB) dan shell Python.

## Developer Tool web browser

Contoh lain debugger, kali ini dengan antarmuka grafis.

# strace

Amati system call yang dilakukan sebuah program: `strace {program}`.

# Profiling

Jenis profiling: CPU, memori, dsb.

Profiler paling sederhana: `time`.

## Go

Jalankan kode test dengan CPU profiler: `go test -cpuprofile=cpu.out`

Analisis profile: `go tool pprof -web cpu.out`

Jalankan kode test dengan Memory profiler: `go test -memprofile=mem.out`

Analisis profile: `go tool pprof -web mem.out`

## Perf

Statistik performa dasar: `perf stat {command}`

Jalankan program dengan profiler: `perf record {command}`

Analisis profile: `perf report`
