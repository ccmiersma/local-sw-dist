%define author Christopher Miersma

# This defines the target stable release for a given version.
#Increment it for small packaging changes within a stable release.
#Reset it to 1, when you begin work on a new version, bugfix etc.
%define rel_num 1
Name:		local-sw-dist
#Update the version to track changes to the specfile with major versions
Version:        0.3.0

#The following parameters can be defined at the command line, but default as below.
%{!?rel:%define rel false}
%{!?local_source:%define local_source false}
%{!?tag:%define tag release-%{version}}

%{!?local_prefix:%define local_prefix local}
%if "%{local_prefix}" != "false"
%define _prefix /opt/%{local_prefix}
%define _datadir %{_prefix}/share
%define _mandir %{_datadir}/man
%define _bindir %{_prefix}/bin
%define _sbindir %{_prefix}/sbin
%define _libdir %{_prefix}/lib
%define _libexecdir %{_prefix}/libexec
%define _includedir %{_prefix}/include
%endif

#If this is not specifically defined as a release, the rel_num will be the upcoming release
#minus 1 with rc and a date stamp. A clean release package for stable release can be defined
#by passing "-D 'rel true'" If you need to re-release a package because of specfile or other
#packaging issues, you must update the default rel_num in the specfile.
%if "%{rel}" == "false"
Release:        %(echo $((%{rel_num} - 1)))rc%(date +"%Y%m%d%H%M")%{?dist}
%else
Release:        %{rel_num}%{?dist}
%endif

Summary:	Local Software Distribution
Group:		local
License:	MIT
URL:		https://gitlab.com/ccmiersma/%{name}/
Source0:	%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  pandoc

%define vcsurl git@gitlab.com:/ccmiersma/%{name}.git

%description
This package will install the base environment for a custom software distribution.
This can serve as a starting point for a complete integrated set of scripts, configurations,
and custom applications local to your organization.

%prep
%if "%{local_source}" == "false"

# This section works to grab the source file from the git repository.
# If you wish to build from a local tar file that you have downloaded or extracted
# from the SRPM, run rpmbuild with -D 'local_source true'
rm -rf ./%{name}-%{version}/
git archive --prefix=%{name}-%{version}/ --format tar %{tag} --remote %{vcsurl} | gzip > %{name}-%{version}.tar.gz

tar xvfz %{name}-%{version}.tar.gz
mv -f %{name}-%{version}.tar.gz ../SOURCES

%setup -T -D

%else
# local_source is not false, so we build from local SOURCE0
# By default local_source is false, so we skip this.
%setup

%endif

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
mkdir -p ${RPM_BUILD_ROOT}%_mandir
mkdir -p ${RPM_BUILD_ROOT}%_bindir
mkdir -p ${RPM_BUILD_ROOT}%_sbindir
mkdir -p ${RPM_BUILD_ROOT}%_libdir/scripts
mkdir -p ${RPM_BUILD_ROOT}%_libexecdir 
mkdir -p ${RPM_BUILD_ROOT}%_includedir 
mkdir -p ${RPM_BUILD_ROOT}%_sysconfdir/profile.d/ 
mkdir -p ${RPM_BUILD_ROOT}%_sysconfdir/opt/%{local_prefix}/
mkdir -p ${RPM_BUILD_ROOT}/var/opt/%{local_prefix}

mkdir -p ${RPM_BUILD_ROOT}%_mandir/man7
mkdir -p ${RPM_BUILD_ROOT}%_prefix/app
mkdir -p ${RPM_BUILD_ROOT}%_prefix/webapps
mkdir -p ${RPM_BUILD_ROOT}%_prefix/lib64
mkdir -p ${RPM_BUILD_ROOT}%_sysconfdir/sysconfig/


#Pre-config file in sysconfig.
cp environment ${RPM_BUILD_ROOT}%_sysconfdir/sysconfig/local/environment

# The script library with all the defaults
cp local-sw-dist.lib.sh ${RPM_BUILD_ROOT}%_libdir/scripts/


# The glue that holds it together outside the root.
cp local.sh ${RPM_BUILD_ROOT}/etc/profile.d/


cp %{name}.7.gz ${RPM_BUILD_ROOT}%_mandir/man7/



# This automatically builds a file list from files and symlinks.
find ${RPM_BUILD_ROOT} -type f -o -type l | sed -e "s#${RPM_BUILD_ROOT}##g"|sed -e "s#\(.*\)#\"\1\"#" > %{name}-filelist

%clean
%__rm -rf ${RPM_BUILD_ROOT}
#%__rm -rf %_builddir/*

%files -f %{name}-filelist
%defattr(-,root,root, -)
%dir %_prefix
%dir %_datadir
%dir %_mandir
%dir %_bindir
%dir %_sbindir
%dir %_libdir
%dir %_libdir/scripts
%dir %_libexecdir 
%dir %_includedir
%dir %_sysconfdir/opt/%{local_prefix}/
%dir %_sysconfdir/sysconfig/local/
%dir /var/opt/%{local_prefix}
%dir %_mandir/man7
%dir %_prefix/app
%dir %_prefix/webapps
%dir %_prefix/lib64
%config(noreplace) %_sysconfdir/sysconfig/local/environment
%config(replace) %_sysconfdir/profile.d/local.sh
%docdir %{_mandir} 

# The post and postun update the man page database
%post

mandb

%postun

mandb

%changelog
* Sat Mar 25 2017 Christopher Miersma - 0.3.0-1
- Simplified script and config structure.
* Sat Mar 25 2017 Christopher Miersma - 0.2.1-1
- Add webapps folder
* Fri Mar 24 2017 Christopher Miersma - 0.2.0-1
- Get all the variables covered properly and default to turning on.
* Thu Jan 19 2017 Christopher Miersma - 0.1.0-1
- Initial Release
