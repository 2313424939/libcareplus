# LibcarePlus 项目技术文档与详细设计文档

---

## 1. 项目简介

LibcarePlus 是一个通用的用户态热补丁框架，可用于对 Linux 可执行程序或动态链接库进行热补丁，无需重启应用程序。它基于 LibCare 项目独立发展，支持 x86_64、aarch64 等主流架构。

- 官方主页：[https://github.com/cloudlinux/libcare](https://github.com/cloudlinux/libcare)
- 主要应用场景：关键安全更新（如 glibc GHOST 漏洞）、严重 bug 热修复等。

---

## 2. 软件架构

LibcarePlus 主要由以下部分组成：

- 补丁生成工具链（libcare-cc、libcare-patch-make 等）
- 补丁应用控制工具（libcare-ctl）
- 补丁格式与加载机制（基于 ELF 格式，支持 BuildID 匹配）
- 支持多架构（x86_64、aarch64 等）

### 2.1 补丁生成流程

1. 使用 `libcare-cc` 替换编译器，分别对原始和修补后的源码生成汇编文件。
2. 对比汇编文件，提取差异，生成带有补丁信息的特殊 ELF section。
3. 通过 `libcare-patch-make` 脚本自动化上述流程，最终输出二进制补丁文件（.patch）。

### 2.2 补丁应用流程

1. 通过 `libcare-ctl patch -p <PID>` 将补丁注入目标进程。
2. 补丁以 ELF 共享库方式加载到进程内存，重定向原有函数到新实现。
3. 支持补丁回滚（unpatch）和补丁信息查询（info）。

---

## 3. 详细设计

### 3.1 补丁制作工具链

- `libcare-cc`：编译器包装器，负责生成中间汇编文件。
- `libcare-patch-make`：自动化补丁制作流程，支持参数：
  - `--help/-h`：显示帮助
  - `--update`：仅更新 kpatches
  - `--clean`：清理构建
  - `--srcdir DIR`：切换源码目录

#### 使用示例：
```sh
$ cd project_dir
$ KPATCH_STAGE=configure CC=libcare-cc ./configure
$ libcare-patch-make first.patch second.patch
```

### 3.2 补丁应用与管理

- `libcare-ctl`：补丁应用与管理工具，支持：
  - `patch`：应用补丁
  - `unpatch`：回滚补丁
  - `info`：查询补丁信息
  - 常用参数：
    - `-v`：详细输出
    - `-h`：帮助
    - `-p <PID|all>`：指定进程

#### 应用补丁示例：
```sh
$ libcare-ctl patch -p <PID> some_patch_file.kpatch
```

#### 回滚补丁示例：
```sh
$ libcare-ctl unpatch -p <PID> <BuildID>
```

#### 查询补丁信息：
```sh
$ libcare-ctl info -p <PID>
```

### 3.3 补丁格式

- 补丁为 ELF 格式，类型为 REL，包含目标 BuildID、补丁元信息等。
- 加载时分配内存、解析重定位、覆盖原函数入口。
- 回滚时恢复原始代码，释放补丁内存。

---

## 4. 目录结构说明

- `src/`：核心源码与工具实现
- `docs/`：技术文档与详细设计说明
- `scripts/`：补丁制作、构建相关脚本
- `patches/`、`packages/`：补丁与包管理相关内容
- `samples/`：示例工程与补丁样例
- `tests/`：测试用例

---

## 5. 参考文档与扩展阅读

- [docs/internals.rst](docs/internals.rst)：详细内部原理与流程
- [docs/libcare-patch-make.rst](docs/libcare-patch-make.rst)：补丁制作工具说明
- [docs/libcare-ctl.rst](docs/libcare-ctl.rst)：补丁应用工具说明
- [README.md / README.en.md / README.rst](README.md)：项目简介与快速入门
- [samples/ghost/README.rst](samples/ghost/README.rst)：GHOST 漏洞补丁示例
- [samples/server/README.rst](samples/server/README.rst)：服务端补丁示例

---

## 6. 贡献指南

欢迎任何开发者参与贡献，可通过 Issue 或 Pull Request 参与开发。

---

> 本文档由 Copilot 自动梳理，内容参考项目源码与文档，建议结合实际代码与文档进一步完善。
