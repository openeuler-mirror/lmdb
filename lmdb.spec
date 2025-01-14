%global commit_hash d87d682b6db9c04c1bee34e5cadbbcae4e6d9a67
Name:           lmdb
Version:        0.9.30
Release:        2
Summary:        An extraordinarily fast, memory-efficient database
License:        OLDAP-2.8
URL:            http://symas.com/lmdb/
Source0:        https://git.openldap.org/openldap/openldap/-/archive/LMDB_%{version}.tar.gz
Source1:        lmdb.pc.in

BuildRequires:  gcc, make, doxygen, 

Patch0:         lmdb-make.patch
Patch1:         lmdb-s390-check.patch

Provides:       %{name}-libs
Obsoletes:      %{name}-libs < %{version}-%{release}

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
%autosetup -n openldap-LMDB_%{version}-%{commit_hash} -p1

%build
pushd libraries/lib%{name}
%set_build_flags
%make_build XCFLAGS="%{build_cflags}"

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

%ldconfig_scriptlets libs

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
* Fri Nov 25 2022 wangjiang <wangjiang37@h-partners.com> - 0.9.30-2
- fix obsoletes in spec

* Fri Nov 04 2022 wangjiang <wangjiang37@h-partners.com> - 0.9.30-1
- upgrade version to 0.9.30

* Tue May 10 2022 mylee <liweiganga@uniontech.com> - 0.9.29-3
- fix spec changelog date

* Thu Apr 14 2022 renhongxun <renhongxun@h-partners.com> - 0.9.29-2
- update license from openLDAP to OLDAP-2.8

* Thu Nov 25 2021 liudabo <liudabo1@huawei.com> - 0.9.29-1
- upgrade version to 0.9.29

* Fri Jul 30 2021 chenyanpanHW <chenyanpan@huawei.com> - 0.9.27-2
- DESC: delete -Sgit from %autosetup, and delete BuildRequires git

* Tue Jan 26 2021 liudabo <liudabo1@huawei.com> - 0.9.27-1
- upgrade version to 0.9.27

* Tue Jul 28 2020 xinghe <xinghe1@huawei.com> - 0.9.25-1
- update version to 0.9.25

* Fri Sep 20 2019 caomeng <caomeng5@huawei.com> - 0.9.22-4
- Package init

