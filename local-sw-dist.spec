%define author Christopher Miersma


%{!?local_prefix:%define local_prefix local}
%if "%{local_prefix}" != "false"
%define _prefix /opt/%{local_prefix}
%define _sysconfdir /etc/%{_prefix}
%define _datadir %{_prefix}/share
%define _docdir %{_datadir}/doc
%define _mandir %{_datadir}/man
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/libexec
%define _includedir %{_prefix}/include
%endif

Name:		local-sw-dist
Version:        0.3.1
Release:        1%{?dist}%{?local_prefix}

Summary:	Local Software Distribution
Group:		local
License:	MIT
URL:		https://gitlab.com/ccmiersma/%{name}/
Source0:	%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  pandoc


%description
This package will install the base environment for a custom software distribution.
This can serve as a starting point for a complete integrated set of scripts, configurations,
and custom applications local to your organization.


%prep
%setup


%build


echo "Creating man page from README..."

# If a README.md is found, create a man page
if [ -e "README.md" ]; then
  cat README.md | \
  sed -e 1i"\%% %{name}(7)\n\%% %{author} \n\%% $(date +\%B\ \%Y)\n#NAME\n%{name} - %{summary}\n" | \
  pandoc -s -t man - | \
  gzip > %{name}.7.gz
fi

%install

mkdir -p ${RPM_BUILD_ROOT}%_prefix
mkdir -p ${RPM_BUILD_ROOT}%_datadir
mkdir -p ${RPM_BUILD_ROOT}%_docdir
mkdir -p ${RPM_BUILD_ROOT}%_mandir
mkdir -p ${RPM_BUILD_ROOT}%_bindir
mkdir -p ${RPM_BUILD_ROOT}%_sbindir
mkdir -p ${RPM_BUILD_ROOT}%_libdir/scripts
mkdir -p ${RPM_BUILD_ROOT}%_libexecdir 
mkdir -p ${RPM_BUILD_ROOT}%_includedir 
mkdir -p ${RPM_BUILD_ROOT}/etc/profile.d/ 
mkdir -p ${RPM_BUILD_ROOT}%_sysconfdir/
mkdir -p ${RPM_BUILD_ROOT}/var/opt/%{local_prefix}

mkdir -p ${RPM_BUILD_ROOT}%_mandir/man7
mkdir -p ${RPM_BUILD_ROOT}%_prefix/app
mkdir -p ${RPM_BUILD_ROOT}%_prefix/webapps
mkdir -p ${RPM_BUILD_ROOT}%_prefix/lib64
mkdir -p ${RPM_BUILD_ROOT}/etc/sysconfig/local


#Pre-config file in sysconfig.
cp environment ${RPM_BUILD_ROOT}/etc/sysconfig/local/environment

# The script library with all the defaults
cp local-sw-dist.lib.sh ${RPM_BUILD_ROOT}%_libdir/scripts/


# The glue that holds it together outside the root.
cp local.sh ${RPM_BUILD_ROOT}/etc/profile.d/


cp %{name}.7.gz ${RPM_BUILD_ROOT}%_mandir/man7/

cp README.md ${RPM_BUILD_ROOT}%_docdir/


#Manually defined files and dirs that need special designation.
#This will end up in the files section.
cat > %{name}-defined-files-list << EOF
%dir %_prefix
%dir %_datadir
%dir %_docdir
%dir %_mandir
%dir %_bindir
%dir %_sbindir
%dir %_libdir
%dir %_libdir/scripts
%dir %_libexecdir 
%dir %_includedir
%dir %_sysconfdir/
%dir /etc/sysconfig/local/
%dir /var/opt/%{local_prefix}
%dir %_mandir/man7
%dir %_prefix/app
%dir %_prefix/webapps
%dir %_prefix/lib64
%config(noreplace) /etc/sysconfig/local/environment
%config /etc/profile.d/local.sh
%docdir %{_mandir}
%docdir %{_docdir}
EOF
#Convoluted stuff to combine the manual list above with any new files we find, into a correct list with no duplicates
find ${RPM_BUILD_ROOT} -type f -o -type l | sed -e "s#${RPM_BUILD_ROOT}##g"|sed -e "s#\(.*\)#\"\1\"#" > %{name}-all-files-list
cat %{name}-defined-files-list | cut -f2 -d' ' | sed -e "s#\(.*\)#\"\1\"#" | sort > %{name}-defined-files-list.tmp
cat %{name}-all-files-list | sort > %{name}-auto-files-list.tmp
diff -e %{name}-defined-files-list.tmp %{name}-auto-files-list.tmp | grep "^\"" > %{name}-auto-files-list
cat %{name}-defined-files-list %{name}-auto-files-list > %{name}-files-list

%clean
%__rm -rf ${RPM_BUILD_ROOT}

%files -f %{name}-files-list
%defattr(-,root,root, -)


# The post and postun update the man page database
%post

mandb

%postun

mandb

%changelog
* Fri Jun 09 2017 Christopher Miersma <ccmiersma@gmail.com> 0.3.1-1
- new package built with tito

* Sat Mar 25 2017 Christopher Miersma - 0.3.0-1
- Simplified script and config structure.
* Sat Mar 25 2017 Christopher Miersma - 0.2.1-1
- Add webapps folder
* Fri Mar 24 2017 Christopher Miersma - 0.2.0-1
- Get all the variables covered properly and default to turning on.
* Thu Jan 19 2017 Christopher Miersma - 0.1.0-1
- Initial Release
