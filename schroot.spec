#TODO: proper pam configuration file

Summary:	Execute commands under different root filesystems
Summary(pl.UTF-8):   Wykonywanie poleceń w innym głównym systemie
Name:		schroot
Version:	1.0.5
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/s/schroot/%{name}_%{version}.orig.tar.gz
# Source0-md5:	685c6e8c9a9d5de24e543031683b8e30
Patch0:		schroot-kill-procs.patch
URL:		http://packages.qa.debian.org/s/schroot.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	boost-any-devel
Buildrequires:	boost-mem_fn-devel
BuildRequires:	boost-program_options-devel
BuildRequires:	boost-ref-devel
BuildRequires:	boost-regex-devel
BuildRequires:	cppunit-devel
BuildRequires:	gettext-autopoint
BuildRequires:	gettext-devel
BuildRequires:	libuuid-devel
BuildRequires:	lockdev-devel
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Execute commands under different root filesystems.

%description -l pl.UTF-8
Wykonywanie poleceń w innym głównym systemie.

%prep
%setup -q
%patch0 -p1

%build
sed -e "s/@RELEASE_DATE@/`date '+%d %b %Y'`/" -e "s/@RELEASE_UDATE@/`date '+%s'`/" scripts/schroot_release.m4.in > m4/schroot_release.m4
%{__libtoolize}
%{__autopoint}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}

# workaround for g++ problems with arguments sequence
sed -r -i -e "s:^(ac_link=.*)(-o conftest.*)(conftest.*ac_ext)(.*):\1 \3 \2 \4:" configure

%configure

%{__make} CC="%{__cc}"


%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cat > do_chroot << 'EOF'
#!/bin/sh

exec schroot -p -q -- "`basename $0`" "$@"
EOF

install do_chroot $RPM_BUILD_ROOT%{_bindir}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README TODO debian/changelog
%{_mandir}/man?/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/exec.d
%dir %{_sysconfdir}/%{name}/setup.d
%dir %{_libdir}/%{name}
%dir /var/lib/%{name}
%dir /var/lib/%{name}/mount
%dir /var/lib/%{name}/session
%attr(4755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/do_chroot
%attr(755,root,root) %{_libdir}/%{name}/*
%attr(755,root,root) %{_sysconfdir}/%{name}/exec.d/*
%attr(755,root,root) %{_sysconfdir}/%{name}/setup.d/*
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) /etc/pam.d/%{name}
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
