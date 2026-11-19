---
layout: page
title: Edisi Sebelumnya
description: >
  Temukan semua edisi Missing Semester sebelumnya.
lang: id
permalink: /id/past/
---

{% comment %} pop to remove default "posts" collection {% endcomment %}
{% assign sorted_collections = site.collections | sort: 'label' | pop | reverse %}
<ul>
{% for collection in sorted_collections %}
    <li><a href="/{{ collection.label }}/">{{ collection.label }}</a></li>
{% endfor %}
</ul>

Kuliah setiap tahun sepenuhnya mandiri. Kami menyarankan memulai dengan versi materi yang paling baru. Ada variasi topik yang dibahas dari tahun ke tahun, sehingga kami tetap menyediakan catatan dan video untuk versi kursus sebelumnya.
