%define LNG cs
Summary: Czech Linux Manual Pages
Name: man-pages-%LNG
Version: 0.17.20080113
Release: %mkrel 1
License: Distributable
Group: System/Internationalization
URL: http://sweb.cz/tropikhajma/man-pages-cs/index.html
Source: http://sweb.cz/tropikhajma/man-pages-cs/%name-%version.tar.lzma
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: man => 1.5j-8mdk
BuildRequires: sed grep man
Requires: locales-%LNG, man => 1.5j-8mdk
Autoreqprov: false
BuildArch: noarch
Obsoletes: man-%LNG, manpages-%LNG
Provides: man-%LNG, manpages-%LNG

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
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%_mandir/%LNG/
mkdir -p $RPM_BUILD_ROOT/var/cache/man/%LNG/cat{1,2,3,4,5,6,7,8,9,n}

for i in 1 2 3 4 5 6 7 8; do
    mkdir $RPM_BUILD_ROOT/%_mandir/%LNG/man$i
done
	
for podadresar in $(find . -maxdepth 1 -mindepth 1 -type d -print); do
  if [ $podadresar == "./latest" ]
  then
    continue
  fi
    # as there are no translations of same name pages, all can be put to single directory sorted by sections
  for soubor in $(ls $podadresar | sort); do
    zakljmeno=`echo $soubor | sed s/^[0123456789]\\\{8\\\}\\.//g | sed s/\\.[0-9]\\\{4\\\}-[0-9][0-9]-[0-9][0-9]\\.[a-f0-9]\\\{32\\\}$//g`;
    cislosekce=${zakljmeno: -1};
    cp -p $podadresar/$soubor $RPM_BUILD_ROOT/%_mandir/%LNG/man$cislosekce/$zakljmeno
  done
done

LANG=%LNG DESTDIR=$RPM_BUILD_ROOT /usr/sbin/makewhatis $RPM_BUILD_ROOT%_mandir/%LNG

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
