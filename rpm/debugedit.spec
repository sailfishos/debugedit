%define rpmhome /usr/lib/rpm

Name: debugedit
Version: 5.1
Release: 1
Summary: Tools for debuginfo creation
License: GPLv3+ AND GPLv2+ AND LGPLv2+
URL: https://github.com/sailfishos/debugedit
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make gcc
BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libdw)
BuildRequires: xxhash-devel

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
# For run_job, sed
Requires: sed
# For append_uniq, grep
Requires: grep

Patch0: 0001-OpenSUSE-finddebuginfo-patch.patch
Patch1: 0002-OpenSUSE-finddebuginfo-absolute-links.patch
Patch2: 0003-OpenSUSE-debugsubpkg.patch
Patch3: 0004-Compatibility-with-older-dd.patch
Patch5: 0005-Remove-dwz-support.patch
Patch6: 0006-Remove-.gdb_index-support.patch

%description
The debugedit project provides programs and scripts for creating
debuginfo and source file distributions, collect build-ids and rewrite
source paths in DWARF data for debugging, tracing and profiling.

It is based on code originally from the rpm project plus libiberty and
binutils.  It depends on the elfutils libelf and libdw libraries to
read and write ELF files, DWARF data and build-ids.

%prep
%autosetup -p1 -n %{name}-%{version}/upstream

%build
autoreconf -f -v -i
%configure
%make_build

%install
%make_install

# Temp symlink to make sure things don't break.
pushd %{buildroot}%{_bindir}
ln -s find-debuginfo find-debuginfo.sh
popd

%files
%license COPYING COPYING3 COPYING.LIB
%doc README
%{_bindir}/debugedit
%{_bindir}/sepdebugcrcfix
%{_bindir}/find-debuginfo
%{_bindir}/find-debuginfo.sh
%{_mandir}/man1/debugedit.1*
%{_mandir}/man1/sepdebugcrcfix.1*
%{_mandir}/man1/find-debuginfo.1*
