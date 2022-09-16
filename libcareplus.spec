%define with_selinux 1

Version: 1.0.0
Name: libcareplus
Summary: LibcarePlus tools
Release: 13
Group: Applications/System
License: GPLv2
Url: https://gitee.com/openeuler/libcareplus
Source0: %{name}-%{version}.tar.gz

Patch0000: 0000-gensrc-skip-vector-instruction-in-str_do_gotpcrel.patch
Patch0001: 0001-gensrc-we-should-add-align-while-FLAGS_PUSH_SECTION-.patch
Patch0002: 0002-fix-cblock-parse-for-LCOLD-LHOT-.cold.NUM-.init_arra.patch
Patch0003: 0003-elf-add-section-adderss-for-STT_NOTYPE-type-of-symbo.patch
Patch0004: 0004-elf-strip-adapt-to-new-gcc-version-10.3.1.patch
Patch0005: 0005-gitignore-ignore-some-tests-and-binary.patch
Patch0006: 0006-libcare-patch-make-adapt-libcare-patch-make-to-meson.patch
Patch0007: 0007-kpatch_elf-compatible-with-older-versions-of-the-so-.patch
Patch0008: 0008-kpatch_parse-fix-failed-to-recognize-.cold.patch
Patch0009: 0009-help-modify-some-help-information.patch
Patch0010: 0010-libcare-patch-make-fix-some-bugs.patch
Patch0011: 0011-selinux-enable-libcare-ctl-to-mprotect-qemu-process.patch
Patch0012: 0012-libcare-dump-change-the-return-value.patch
Patch0013: 0013-modify-pkgbuild-to-make-kpatch-for-RPM-based-packages.patch
Patch0014: 0014-kpatch_process-fix-possible-double-free.patch
Patch0015: 0015-ptrace-fix-NULL-pointer-access-problem.patch
Patch0016: 0016-fix-patched-process-crashing-when-acccess-the-global.patch
Patch0017: 0017-fix-probably-restore-cc-symbol-link-fail-when-kill-p.patch
Patch0018: 0018-optimize-Remove-unnecessary-comparison-code.patch
Patch0019: 0019-Revert-fix-probably-restore-cc-symbol-link-fail-when.patch
Patch0020: 0020-fix-probably-restore-cc-symbol-link-fail-when-kill-p.patch
Patch0021: 0021-do-not-print-awk-warning-in-libcare-patch-make.patch

BuildRequires: elfutils-libelf-devel libunwind-devel gcc systemd

%if 0%{with selinux}
BuildRequires: checkpolicy
BuildRequires: selinux-policy-devel
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{with selinux}
Requires:      libcareplus-selinux = %{version}-%{release}
%endif

%description
LibcarePlus userland tools

%if 0%{with selinux}

%package selinux
Summary: SELinux package for LibcarePlus/QEMU integration
Group: System Environment/Base
Requires(post): selinux-policy-base, policycoreutils
Requires(postun): policycoreutils
%description selinux
This package contains SELinux module required to allow for
LibcarePlus interoperability with the QEMU run by sVirt.

%endif


%package devel
Summary: LibcarePlus development package
Group: System Environment/Development Tools
%description devel
LibcarePlus devel files.


%prep
%setup -q
%autopatch -p1

%build
cd src
sh ./config
cd ../
make -C src
%if 0%{with selinux}
make -C dist/selinux
%endif

%install
%{__rm} -rf %{buildroot}

make -C src install \
        DESTDIR=%{buildroot} \
        bindir=%{_bindir} \
        libexecdir=%{_libexecdir}

%if 0%{with selinux}
make -C dist/selinux install \
        DESTDIR=%{buildroot}
%endif


install -m 0644 -D dist/libcare.preset %{buildroot}%{_presetdir}/90-libcare.preset
install -m 0500 scripts/pkgbuild %{buildroot}%{_bindir}/libcare-pkgbuild
install -m 0500 scripts/de-offset-syms.awk %{buildroot}%{_bindir}/de-offset-syms.awk
install -m 0644 -D scripts/example_info %{buildroot}/usr/share/libcareplus/qemu_example_info

%pre
/usr/sbin/groupadd libcare -r 2>/dev/null || :
/usr/sbin/usermod -a -G libcare qemu 2>/dev/null || :

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/libcare-ctl
%{_presetdir}/90-libcare.preset

%files devel
%defattr(-,root,root)
%{_bindir}/libcare-cc
%{_bindir}/libcare-patch-make
%{_bindir}/libcare-dump
%{_bindir}/kpatch_gensrc
%{_bindir}/kpatch_strip
%{_bindir}/kpatch_make
%{_bindir}/libcare-server
%{_bindir}/libcare-client
%{_bindir}/libcare-pkgbuild
%{_bindir}/de-offset-syms.awk
/usr/share/libcareplus/qemu_example_info

%if 0%{with selinux}

%files selinux
%defattr(-,root,root,-)
%attr(0600,root,root) %{_datadir}/selinux/packages/libcare.pp

%post selinux
. /etc/selinux/config
FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

/usr/sbin/semodule -i %{_datadir}/selinux/packages/libcare.pp

# Load the policy if SELinux is enabled
if ! /usr/sbin/selinuxenabled; then
    # Do not relabel if selinux is not enabled
    exit 0
fi

/usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null

rm -f ${FILE_CONTEXT}.pre

exit 0

%postun selinux
if [ $1 -eq 0 ]; then
    . /etc/selinux/config
    FILE_CONTEXT=/etc/selinux/${SELINUXTYPE}/contexts/files/file_contexts
    cp ${FILE_CONTEXT} ${FILE_CONTEXT}.pre

    # Remove the module
    /usr/sbin/semodule -n -r libcare > /dev/null 2>&1

    /usr/sbin/fixfiles -C ${FILE_CONTEXT}.pre restore 2> /dev/null
fi
exit 0

%endif

%changelog
* Fri Sep 16 2022 yezengruan <yezengruan@huawei.com> 1.0.0-13
- do not print awk warning in libcare-patch-make

* Wed Jun 15 2022 yezengruan <yezengruan@huawei.com> 1.0.0-12
- kpatch_process: fix possible double free.
- ptrace: fix NULL pointer access problem
- fix patched process crashing when acccess the global var
- fix probably restore cc symbol link fail when kill patch building uncourteous
- optimize: Remove unnecessary comparison code

* Wed May 11 2022 Cichen Wang <wangcichen_yewu@cmss.chinamobile.com> 1.0.0-11
- modify scripts/pkgbuild to make kpatch'es for the RPM-based packages

* Tue May 10 2022 yezengruan <yezengruan@huawei.com> 1.0.0-10
- libcare-dump: change the return value
- gensrc: skip vector instruction in str_do_gotpcrel

* Wed Apr 27 2022 yezengruan <yezengruan@huawei.com> 1.0.0-9
- update the format of changelog

* Tue Mar 29 2022 yezengruan <yezengruan@huawei.com> 1.0.0-8
- selinux: enable libcare-ctl to mprotect qemu process

* Mon Mar 21 2022 yezengruan <yezengruan@huawei.com> 1.0.0-7
- libcare-patch-make: fix some bugs

* Tue Mar 15 2022 yezengruan <yezengruan@huawei.com> 1.0.0-6
- help: modify some help information

* Wed Mar 02 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-5
- kpatch_elf: compatible with older versions of the so naming rules
- kpatch_parse: fix failed to recognize .cold

* Mon Feb 28 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-4
- libcare-patch-make: adapt libcare-patch-make to meson
- gitignore: ignore some tests and binary
- elf/strip: adapt to new gcc version(10.3.1)

* Tue Feb 22 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-3
- libcareplus.spec:remove libcare.service and libcare.socket

* Tue Feb 22 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-2
- gensrc: we should add align while FLAGS_PUSH_SECTION flag is set
- elf: add section adderss for STT_NOTYPE type of symbol

* Tue Feb 22 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-1
- fix cblock parse for LCOLD/LHOT/.cold.NUM, .init_array and support gnu_unique_object

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 1.0.0-0
- package init 1.0.0-0

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-15
- kpatch_user: init pid in cmd_info_user

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-14
- some bugfix
- support aarch64 UT
- fix memory RWX problem

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-13
- add libcare-dump tool
- support test sets running on x86
- some bugfixs

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-12
- src/Makefile: execute config scripts before building
- kpatch_gensrc.c: support ignoring functions which we don't need
- arch/aarch64/arch_parse: modify is_variable_start for arm asm
- libcare-ctl: implement applied patch list
- libcare-ctl: introduce patch-id
- arch/aarch64/arch_elf: Add LDR and B instruction relocation
- arch/aarch64/arch_parse: improve VAR_CBLOCK start indentify
- tls: add support for TLS symbol with IE model
- arch64/arch_elf: add R_AARCH64_LDST32_ABS_LO12_NC relocation type for aarch64
- process: fix region start calculation
- aarch64/arch_elf: Add ldr and ldrb relocation for aarch6

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-11
- kpatch_cc: support gcc -MQ option
- libcare-cc: add gcc iquote option support

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-10
- kpatch_user.c: fix gcc warning

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-9
- libcare-patch-make: add `-j|--jobs` option

* Mon Feb 07 2022 imxcc <xingchaochao@huawei.com> - 0.1.4-8
- updated the README.en.md file

* Wed Sep 08 2021 imxcc <xingchaochao@huawei.com> - 0.1.4-7
- selinux: Allow init_t create lnk file

* Thu Sep 02 2021 imxcc <xingchaochao@huawei.com> - 0.1.4-6
- enable selinux

* Sat Aug 21 2021 caodongxia <caodongxia@huawei.com> - 0.1.4-5
- fixes uninstall warning

* Tue Jun 08 2021 wulei <wulei80@huawei.com> - 0.1.4-4
- fixes failed: gcc: command not found

* Tue Feb 09 2021 Jiajie Li <lijiajie11@huawei.com> - 0.1.4-3
- Add basic support libcareplus on aarch64

* Mon Dec 28 2020 sunguoshuai <sunguoshuai@huawei.com> - 0.1.4-2
- Del the {dist} in release.

* Tue Dec 8 2020 Ying Fang <fangying1@huawei.com> - 0.1.4-1
- Init the libcareplus package spec
