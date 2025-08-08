%define rpmhome /usr/lib/rpm

Name: debugedit
Version: 5.1
Release: 1
Summary: Tools for debuginfo creation
License: GPLv3+ AND GPLv2+ AND LGPLv2+
URL: https://github.com/sailfishos/debugedit
Source0: %{name}-%{version}.tar.bz2

BuildRequires: pkgconfig(libelf)
BuildRequires: pkgconfig(libdw)
BuildRequires: xxhash-devel
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

Patch0: 0001-openSUSE-finddebuginfo-patch.patch
Patch1: 0002-OpenSUSE-finddebuginfo-absolute-links.patch
Patch2: 0003-OpenSUSE-debugsubpkg.patch
Patch3: 0004-Compatibility-with-older-dd.patch
Patch4: 0005-Remove-manpages.patch
Patch5: 0006-PR32760-find-debuginfo-handle-static-libraries.patch

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
%{_bindir}/debugedit
%{_bindir}/sepdebugcrcfix
%{_bindir}/find-debuginfo
%{_bindir}/find-debuginfo.sh
