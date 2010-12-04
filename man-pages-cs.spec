%define LNG cs

Summary:	Czech Linux Manual Pages
Name:		man-pages-%LNG
Version:	0.18.20090209
Release:	%mkrel 4
License:	Distributable
Group:		System/Internationalization
URL:		http://tropikhajma.sweb.cz/man-pages-cs/
Source:		http://tropikhajma.sweb.cz/%{name}/%{name}-%{version}.tar.lzma
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	man => 1.5j-8mdk
BuildRequires:	sed 
BuildRequires:	grep 
Requires:	locales-%LNG, 
Requires:	man => 1.5j-8mdk
Autoreqprov:	false
BuildArch:	noarch
Obsoletes:	man-%LNG, manpages-%LNG
Provides:	man-%LNG, manpages-%LNG

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
%setup -q -n %name-%version

%build
# Preserve better versions...
rm ./procps/kill.1
rm ./procps/uptime.1
rm ./man-pages/man1/du.1 
rm ./man-pages/man1/dir.1
rm ./man-pages/man1/vdir.1 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_mandir}/%LNG/
make install DESTDIR=%{buildroot} MANDIR=%{_mandir}/%LNG/

LANG=%LNG DESTDIR=%{buildroot} %{_sbindir}/makewhatis %{buildroot}/%_mandir/%LNG

mkdir -p %{buildroot}%{_sysconfdir}/cron.weekly

cat > %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG %{_sbindir}/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x %{buildroot}%{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron

mkdir -p  %{buildroot}/var/cache/man/%LNG

touch %{buildroot}/var/cache/man/%LNG/whatis

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/cache/man/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/cache/man/%LNG
   fi
fi

%post
%create_ghostfile /var/cache/man/%LNG/whatis root root 644

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,man,755)
%doc README* Changelog CONTRIB.old
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%ghost %config(noreplace) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%_mandir/%LNG/whatis
%config(noreplace) %attr(755,root,root) %{_sysconfdir}/cron.weekly/makewhatis-%LNG.cron
