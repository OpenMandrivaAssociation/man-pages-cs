%define LNG cs

Summary:	Czech Linux Manual Pages
Name:		man-pages-%LNG
Version:	0.18.20090209
Release:	%mkrel 8
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


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0.18.20090209-6mdv2011.0
+ Revision: 666365
- mass rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.18.20090209-5mdv2011.0
+ Revision: 609316
- rebuild

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0.18.20090209-4mdv2011.0
+ Revision: 609298
- fix build
- fix typos
- fix typo, duh!
- fix build
- rebuild
- rebuilt for 2010.1

  + Tomas Kindl <supp@mandriva.org>
    - unify buildroot usage
    - bump to version 0.18.20090209
     - SPEC cleanup

* Tue Oct 14 2008 Funda Wang <fwang@mandriva.org> 0.17.20080113-1mdv2009.1
+ Revision: 293464
- New version 0.17.20080113

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.17.20070905-2mdv2009.0
+ Revision: 223154
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.17.20070905-1mdv2008.1
+ Revision: 129693
- kill re-definition of %%buildroot on Pixel's request

* Thu Sep 06 2007 Funda Wang <fwang@mandriva.org> 0.17.20070905-1mdv2008.0
+ Revision: 80554
- New version 0.17.20070905

* Tue Jun 26 2007 Thierry Vignaud <tv@mandriva.org> 0.17.20070226-1mdv2008.0
+ Revision: 44467
- kill old icon
- new release

* Fri May 04 2007 Funda Wang <fwang@mandriva.org> 0.17.20070219-1mdv2008.0
+ Revision: 22586
- New upstream version.


* Fri Apr 04 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.16-1mdk
- new release
- remove patch 0 (merged upstream)

* Mon Jan 20 2003 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.14-4mdk
- build release

* Wed May 29 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.14-3mdk
- use new man-pages-LG template
    - don't rebuild whatis on install since
      - we've already build in package
      - cron will rebuild it nightly and so add other package french man pages
    - adapt to new man-pages-LG template
    - requires man => 1.5j-8mdk for new man-pages framework
    - remove old makewhatis.cs since default makewhatis is now able to parse
      non english man pages
    - use new std makewhatis to build whatis in spec and in cron entry 
    - whatis db goes into /var/cache/man (so enable ro /usr)
    - standard {Build,}Requires/buildroot/prereq/arc/provides/obsoletes
    - default description
    - remove translations

* Thu Mar 07 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.14-2mdk
- prevent conflicts with man
- provides manpages-%%LANG
- don't overwrite crontab if user atered it
- fix permission on /usr/share/man/cs/*

* Sun Jul 01 2001 Jesse Kuang <kjx@mandrakesoft.com> 0.14-1mdk
- upgrade from rawhide

* Tue May 01 2001 David BAUDENS <baudens@mandrakesoft.com> 0.12-10mdk
- Use %%_tmppath for BuildRoot

* Tue Jul 18 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.12-9mdk
- Big Move

* Mon Jun 26 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.12-8mdk
- use mandir macro in order to be ok when switching to /usr/share/man as
  following FHS

* Tue Apr 11 2000 Denis Havlik <denis@mandrakesoft.com> 0.12-7mdk
- spechelper, permissions,

* Tue Mar 28 2000 Denis Havlik <denis@mandrakesoft.com> 0.12-6mdk
- convert to new group scheme
- convert books-cs.gif -> .xpm

* Fri Nov 19 1999 Pablo Saratxaga <pablo@mandrakesoft.com> 0.12-5mdk
- moved makewhatis.cs from /usr/local/sbin to /usr/sbin

* Tue Jul 20 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- included some nice improvements from man-pages-pl

* Wed Jul 07 1999 Pablo Saratxaga <pablo@mandrakesoft.com>
- Adapted the rpm package of Pavel Janik to Mandrake

