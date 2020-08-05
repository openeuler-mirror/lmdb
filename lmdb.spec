Name:           lmdb
Version:        0.9.24
Release:        1
Summary:        An extraordinarily fast, memory-efficient database
License:        OpenLDAP
URL:            http://symas.com/lmdb/
Source0:        https://github.com/LMDB/lmdb/archive/LMDB_%{version}.tar.gz
Source1:        lmdb.pc.in

BuildRequires:  gcc, make, doxygen, git

Patch0:         lmdb-make.patch
Patch1:         lmdb-s390-check.patch

Provides:       %{name}-libs
Obsoletes:      %{name}-libs

%description
Symas LMDB is an extraordinarily fast, memory-efficient database
we developed for the OpenLDAP Project. With memory-mapped files,
it has the read performance of a pure in-memory database while
retaining the persistence of standard disk-based databases.

%package        devel
Summary:        Development libraries and files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The package contains lib and header files for developing application
that use %{name}

%package_help

%prep
%autosetup -n %{name}-LMDB_%{version} -p1 -Sgit

%build
pushd libraries/lib%{name}
%make_build XCFLAGS="%{optflags}"

doxygen
rm -f Doxyfile || :
rm -rf man || :
popd

%install
pushd libraries/lib%{name}
mkdir -m 0755 -p %{buildroot}{%{_exec_prefix}/bin,%{_exec_prefix}/include}
mkdir -m 0755 -p %{buildroot}{%{_exec_prefix}/%{_lib}/pkgconfig,%{_datadir}/man/man1}
make DESTDIR=%{buildroot} prefix=%{_exec_prefix} libdir=%{_exec_prefix}/%{_lib} mandir=%{_datadir}/man install
popd

sed -e 's:@PREFIX@:%{_exec_prefix}:g' \
    -e 's:@EXEC_PREFIX@:%{_exec_prefix}:g' \
    -e 's:@LIBDIR@:%{_exec_prefix}/%{_lib}:g' \
    -e 's:@INCLUDEDIR@:%{_exec_prefix}/include:g' \
    -e 's:@PACKAGE_VERSION@:%{version}:g' \
    %{SOURCE1} >lmdb.pc
install -Dpm 0644 -t %{buildroot}%{_exec_prefix}/%{_lib}/pkgconfig lmdb.pc

%check

pushd libraries/lib%{name}
rm -rf testdb || :
LD_LIBRARY_PATH=$PWD make test
popd

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_exec_prefix}/bin/*
%{_exec_prefix}/%{_lib}/*.so.*
%doc libraries/lib%{name}/CHANGES
%doc libraries/lib%{name}/COPYRIGHT
%license libraries/lib%{name}/LICENSE

%files devel
%{_exec_prefix}/include/*
%{_exec_prefix}/%{_lib}/*.so
%{_exec_prefix}/%{_lib}/pkgconfig/*.pc

%files help
%{_datadir}/man/man1/*
%doc libraries/lib%{name}/html
%doc libraries/lib%{name}/COPYRIGHT
%doc libraries/lib%{name}/CHANGES
%license libraries/lib%{name}/LICENSE

%changelog
* Tue Aug 04 2020 Leo Fang <leofang_94@163.com> - 0.9.24-1
- Upgrade to version 0.9.24 and add yaml file for lmdb

* Fri Sep 20 2019 caomeng<caomeng5@huawei.com> - 0.9.22-4
- Package init
