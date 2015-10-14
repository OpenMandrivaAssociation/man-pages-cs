%define LNG cs

Summary:	Czech Linux Manual Pages
Name:		man-pages-%{LNG}
Version:	0.18.20090209
Release:	19
License:	Distributable
Group:		System/Internationalization
Url:		http://tropikhajma.sweb.cz/man-pages-cs/
Source0:	http://tropikhajma.sweb.cz/%{name}/%{name}-%{version}.tar.lzma
BuildArch:	noarch

BuildRequires:	grep
BuildRequires:	man
BuildRequires:	sed
Requires:	locales-%{LNG}
Requires:	man
Autoreqprov:	false
Conflicts:	filesystem < 3.0-17

%description
A large collection of man pages (reference material) from the Linux
Documentation Project (LDP), translated to Czech.  The man pages are
organized into the following sections:

	Section 1:  User commands (intro only)
	Section 2:  System calls
	Section 3:  Libc calls
	Section 4:  Devices (e.g., hd, sd)
	Section 5:  File formats and protocols (e.g., wtmp, %{_sysconfdir}passwd, nfs)
	Section 6:  Games (intro only)
	Section 7:  Conventions, macro packages, etc. (e.g., nroff, ascii)
	Section 8:  System administration (intro only)

%prep
%setup -q

%build
# Preserve better versions...
rm ./procps/kill.1
rm ./procps/uptime.1
rm ./man-pages/man1/du.1
rm ./man-pages/man1/dir.1
rm ./man-pages/man1/vdir.1

%install
mkdir -p %{buildroot}/%{_mandir}/%{LNG}/
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}/%{LNG}/

LANG=%{LNG} DESTDIR=%{buildroot} %{_bindir}/mandb %{buildroot}/%{_mandir}/%{LNG}

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly

cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron << EOF
#!/bin/bash
LANG=%{LNG} %{_bindir}/mandb %{_mandir}/%{LNG}
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

mkdir -p  %{buildroot}/var/cache/man/%{LNG}

touch %{buildroot}/var/cache/man/%{LNG}/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/cache/man/%{LNG}, if there isn't any man page
   ## directory /%{_mandir}/%{LNG}
   if [ ! -d %{_mandir}/%{LNG} ] ; then
       rm -rf /var/cache/man/%{LNG}
   fi
fi

%post
%create_ghostfile /var/cache/man/%{LNG}/whatis root root 644

%files
%doc README* Changelog CONTRIB.old
%dir /var/cache/man/%{LNG}
%ghost %config(noreplace) /var/cache/man/%{LNG}/whatis
%{_mandir}/%{LNG}/man*
%{_mandir}/%{LNG}/cat*
%{_mandir}/%{LNG}/index.db*
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%{LNG}.cron

