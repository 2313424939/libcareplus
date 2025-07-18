# LibcarePlus 核心技术文档与实现流程图

---

## 1. 补丁生成流程（libcare-patch-make）

- 使用 `libcare-cc` 替换编译器，分别对原始和修补后的源码生成汇编文件。
- 对比汇编文件，提取差异，生成带有补丁信息的特殊 ELF section。
- 通过 `libcare-patch-make` 脚本自动化上述流程，最终输出二进制补丁文件（.patch）。

#### 主要命令
```sh
$ KPATCH_STAGE=configure CC=libcare-cc ./configure
$ libcare-patch-make first.patch second.patch
```

---

## 2. 补丁应用与管理（libcare-ctl）

- `patch`：将补丁注入目标进程（通过 ELF 共享库方式加载，重定向原有函数到新实现）。
- `unpatch`：回滚补丁，恢复原始代码。
- `info`：查询进程已加载补丁信息。

#### 主要命令
```sh
$ libcare-ctl patch -p <PID> some_patch_file.kpatch
$ libcare-ctl unpatch -p <PID> <BuildID>
$ libcare-ctl info -p <PID>
```

---

## 3. 代码实现流程图（Mermaid 格式）

### 3.1 补丁生成流程
```mermaid
flowchart TD
    A[原始源码] --> B[libcare-cc (KPATCH_STAGE=original)]
    B --> C[生成原始汇编]
    C --> D[应用补丁源码]
    D --> E[libcare-cc (KPATCH_STAGE=patched)]
    E --> F[生成补丁汇编]
    F --> G[kpatch_gensrc (对比汇编差异)]
    G --> H[libcare-patch-make (生成二进制补丁)]
```

### 3.2 补丁应用流程
```mermaid
flowchart TD
    A[目标进程] --> B[libcare-ctl patch]
    B --> C[加载补丁ELF (注入内存)]
    C --> D[重定向函数入口]
    D --> E[进程热补丁生效]
```

---

> 本文档梳理自项目 docs 目录及核心脚本，流程图可直接用于 mermaid 渲染。
