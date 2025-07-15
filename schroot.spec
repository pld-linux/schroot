#TODO:
# - proper pam configuration file
# - is schroot-kill-procs.patch still needed?

Summary:	Execute commands under different root filesystems
Summary(pl.UTF-8):	Wykonywanie poleceń w innym głównym systemie
Name:		schroot
Version:	1.6.12
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://ftp.debian.org/debian/pool/main/s/schroot/%{name}_%{version}.orig.tar.xz
# Source0-md5:	99d5ddca2a0c977ffabea47ed486755a
Patch0:		%{name}-kill-procs.patch
Patch1:		%{name}-cmake.patch
URL:		https://tracker.debian.org/pkg/schroot
BuildRequires:	boost-devel >= 1.35.0
BuildRequires:	cmake
BuildRequires:	cppunit-devel
BuildRequires:	doxygen
BuildRequires:	gettext-autopoint
BuildRequires:	gettext-tools
BuildRequires:	libuuid-devel
BuildRequires:	lockdev-devel
BuildRequires:	pam-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Execute commands under different root filesystems.

%description -l pl.UTF-8
Wykonywanie poleceń w innym głównym systemie.

%package devel
Summary:	Header files for schroot
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for schroot.

%description devel -l pl.UTF-8
Pliki nagłówkowe schroot

%package static
Summary:	Static schroot library
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description static
Static schroot library.

%description static -l pl.UTF-8
Biblioteka statyczna schroot

%package -n bash-completion-schroot
Summary:	bash-completion for schroot command
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów polecenia schroot
Group:		Applications/Shells
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-schroot
This package provides bash-completion for schroot command.

%description -n bash-completion-schroot -l pl.UTF-8
Pakiet ten dostarcza bashowe uzupełnianie parametrów polecenia
schroot.

%prep
%setup -q
#%patch0 -p1
%patch -P1 -p1

%build
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cat > do_chroot << 'EOF'
#!/bin/sh

exec schroot -p -q -- "`basename $0`" "$@"
EOF

install do_chroot $RPM_BUILD_ROOT%{_bindir}

%find_lang %{name} --all-name

install -d $RPM_BUILD_ROOT%{bash_compdir}
%{__mv} $RPM_BUILD_ROOT/etc/bash_completion.d/schroot $RPM_BUILD_ROOT%{bash_compdir}/schroot

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README README.md TODO
%{_mandir}/man?/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/buildd
%dir %{_sysconfdir}/%{name}/chroot.d
%dir %{_sysconfdir}/%{name}/default
%dir %{_sysconfdir}/%{name}/desktop
%dir %{_sysconfdir}/%{name}/minimal
%dir %{_sysconfdir}/%{name}/sbuild
%dir %{_sysconfdir}/%{name}/setup.d
%dir %{_libexecdir}/%{name}
%dir %{_datarootdir}/%{name}
%dir %{_datarootdir}/%{name}/setup
%dir %{_sharedstatedir}/%{name}
%dir %{_sharedstatedir}/%{name}/session
%dir %{_sharedstatedir}/%{name}/union
%dir %{_sharedstatedir}/%{name}/unpack
%attr(4755,root,root) %{_bindir}/%{name}
%attr(755,root,root) %{_bindir}/do_chroot
%attr(755,root,root) %{_libexecdir}/%{name}/*
%{_sysconfdir}/%{name}/buildd/*
%{_sysconfdir}/%{name}/default/*
%{_sysconfdir}/%{name}/desktop/*
%{_sysconfdir}/%{name}/minimal/*
%{_sysconfdir}/%{name}/sbuild/*
%attr(755,root,root) %{_sysconfdir}/%{name}/setup.d/*
%{_datarootdir}/%{name}/setup/*
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) /etc/pam.d/%{name}
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf

%files devel
%defattr(644,root,root,755)
%dir %{_includedir}/sbuild
%{_includedir}/sbuild/*.h
%{_pkgconfigdir}/sbuild.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libsbuild.a

%files -n bash-completion-schroot
%defattr(644,root,root,755)
%{bash_compdir}/schroot
