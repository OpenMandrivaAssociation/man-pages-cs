%define LNG cs

Summary:	Czech Linux Manual Pages
Name:		man-pages-%LNG
Version:	0.18.20090209
Release:	%mkrel 2
License:	Distributable
Group:		System/Internationalization
URL:		http://tropikhajma.sweb.cz/man-pages-cs/
Source:		http://tropikhajma.sweb.cz/%{name}/%{name}-%{version}.tar.lzma
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
	Section 5:  File formats and protocols (e.g., wtmp, /etc/passwd, nfs)
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
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/%LNG/
make install DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}/%LNG/

LANG=%LNG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT/%_mandir/%LNG

mkdir -p $RPM_BUILD_ROOT/etc/cron.weekly

cat > $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LNG.cron << EOF
#!/bin/bash
LANG=%LNG /usr/sbin/makewhatis %_mandir/%LNG
exit 0
EOF
chmod a+x $RPM_BUILD_ROOT/etc/cron.weekly/makewhatis-%LNG.cron

mkdir -p  $RPM_BUILD_ROOT/var/cache/man/%LNG

%postun
# 0 means deleting the package
if [ "$1" = "0" ]; then
   ## Force removing of /var/cache/man/%LNG, if there isn't any man page
   ## directory /%_mandir/%LNG
   if [ ! -d %_mandir/%LNG ] ; then
       rm -rf /var/cache/man/%LNG
   fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,man,755)
%doc README* Changelog CONTRIB.old
%dir %_mandir/%LNG
%dir /var/cache/man/%LNG
%verify (not md5 mtime size) /var/cache/man/%LNG/whatis
%_mandir/%LNG/man*
%config(noreplace) %attr(755,root,root)/etc/cron.weekly/makewhatis-%LNG.cron
