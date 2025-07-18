# kpatch 文件结构分析与解析流程

---

## 1. 问题背景

在使用 `readelf -S d854b4e0dd23453c2f8b909fda86017224f4592b.kpatch` 命令时，出现如下错误：

```
readelf: d854b4e0dd23453c2f8b909fda86017224f4592b.kpatch：错误：不是 ELF 文件 - 它开头的 magic 字节错误
```

---

## 2. 文件结构分析

通过十六进制查看 `.kpatch` 文件内容，发现其结构如下：

- 文件头部为 `KPATCH1\0`（`4b 50 41 54 43 48 31 00`），紧跟版本号等元数据，并非 ELF 标准头（`7f 45 4c 46`）。
- 在偏移量 `0x1f8`（504 字节）处，才出现 ELF 文件的 magic 字节 `7f 45 4c 46`。

这说明 `.kpatch` 文件是自定义格式，前部为补丁元信息，真正的 ELF 补丁内容嵌套在文件内部。

---

## 3. 正确解析方法

直接用 `readelf` 解析整个 `.kpatch` 文件会失败。应先提取内部的 ELF 部分，再用 `readelf` 工具分析。

### 操作步骤

```sh
# 提取从 0x1f8（504）字节开始的 ELF 部分
dd if=d854b4e0dd23453c2f8b909fda86017224f4592b.kpatch bs=1 skip=504 of=patch.elf

# 用 readelf 解析提取出的 ELF 文件
readelf -S patch.elf
```

---

## 4. 设计说明

- `.kpatch` 文件采用自定义头部，便于携带补丁元信息和校验数据。
- 补丁的实际 ELF 二进制内容嵌入在文件内部，需按偏移提取。
- libcareplus 框架会自动解析 `.kpatch` 文件结构并加载内部 ELF 补丁。

---

> 本文档梳理了 kpatch 文件结构及正确的分析方法，便于后续补丁调试与开发。
