%define rpmhome /usr/lib/rpm

Name: debugedit
Version: 5.0
Release: 1
Summary: Tools for debuginfo creation
License: GPL-3.0-or-later AND GPL-2.0-or-later AND LGPL-2.0-or-later
URL: https://sourceware.org/debugedit/
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make gcc
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libdw)
BuildRequires: gnupg2

# For the testsuite.
BuildRequires: autoconf
BuildRequires: automake

# The find-debuginfo.sh script has a couple of tools it needs at runtime.
# For strip_to_debug, eu-strip
Requires: elfutils
# For add_minidebug, readelf, awk, nm, sort, comm, objcopy, xz
Requires: binutils, gawk, coreutils, xz
# For find and xargs
Requires: findutils
# For do_file, gdb_add_index
# We only need gdb-add-index, so suggest gdb-minimal (full gdb is also ok)
Requires: /usr/bin/gdb-add-index
Suggests: gdb-minimal
# For run_job, sed
Requires: sed
# For append_uniq, grep
Requires: grep

Patch1: 0001-use-READELF-not-readelf.patch
Patch2: 0001-tests-Handle-zero-directory-entry-in-.debug_line-DWA.patch
Patch4: 0002-configure.ac-Use-AC_LINK_IFELSE-for-gz-none-check.patch
Patch5: 0003-configure.ac-Use-AC_LANG_PROGRAM-for-AC_LINK_IFELSE-.patch
Patch6: 0004-scripts-find-debuginfo.in-Add-q-quiet.patch
Patch7: 0001-find-debuginfo-Prefix-install_dir-to-PATH.patch
Patch8: 0001-find-debuginfo-Add-v-verbose-for-per-file-messages.patch
Patch9: 0001-debugedit-Add-support-for-.debug_str_offsets-DW_FORM.patch

Patch10: 0001-openSUSE-finddebuginfo-patch.patch
Patch11: 0002-OpenSUSE-finddebuginfo-absolute-links.patch
Patch12: 0003-OpenSUSE-debugsubpkg.patch
Patch13: 0009-Compatibility-with-older-dd.patch
Patch14: 0014-Don-t-build-manpages.patch
Patch15: 0015-Remove-dwz-support.patch

%description
The debugedit project provides programs and scripts for creating
debuginfo and source file distributions, collect build-ids and rewrite
source paths in DWARF data for debugging, tracing and profiling.

It is based on code originally from the rpm project plus libiberty and
binutils.  It depends on the elfutils libelf and libdw libraries to
read and write ELF files, DWARF data and build-ids.

%prep
%autosetup -n rpm-%{version}/upstream -p1

%build
autoreconf -f -v -i
%configure
%make_build

%install
%make_install

# Temp symlink to make sure things don't break.
pushd %{buildroot}%{_bindir}
ln -s find-debuginfo find-debuginfo.sh

# Another symlink for backwards Compatibility
mkdir -p ${RPM_BUILD_ROOT}%{rpmhome}
ln -s find-debuginfo ${RPM_BUILD_ROOT}%{rpmhome}/find-debuginfo.sh
popd

%files
%license COPYING COPYING3 COPYING.LIB
%doc README
%{_bindir}/debugedit
%{_bindir}/sepdebugcrcfix
%{_bindir}/find-debuginfo
%{_bindir}/find-debuginfo.sh
%{rpmhome}/find-debuginfo.sh
