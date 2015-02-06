%define version 3.0
%define release  8

Name:		http-replicator
Version:	%version
Release:	%release
URL:		http://gertjan.freezope.org/replicator/
Source:		http://gertjan.freezope.org/replicator/%{name}_%{version}.tar.bz2
Source1:	%{name}.init.bz2
Group:		System/Servers
License:	GPL
Summary:	General purpose caching proxy server
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Buildarch:	noarch
Requires(pre):	rpm-helper

%description
Replicator is a replicating HTTP proxy server. Files that are downloaded
through the proxy are transparently stored in a private cache, so an exact copy
of accessed remote files is created on the local machine. It is in essence a
general purpose proxy server, but very well suited for maintaining a cache of
Mandriva Linux packages.

%prep
%setup -q

%build

%install
rm -Rf %{buildroot}
install -d %{buildroot}/{%{_bindir},%{_sysconfdir}/{sysconfig,cron.weekly,logrotate.d},%{_initrddir}}
install -m755 http-replicator  http-replicator_maintenance %{buildroot}/%{_bindir}
install -m 755 debian/cron.weekly %{buildroot}/%{_sysconfdir}/cron.weekly/%{name}
sed -i -e 's/default/sysconfig/g' %{buildroot}/%{_sysconfdir}/cron.weekly/%{name}
install -m 644 debian/logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/%{name}
install -m 644 debian/default %{buildroot}/%{_sysconfdir}/sysconfig/%{name}
sed -i -e 's/proxy/%{name}/g' %{buildroot}/%{_sysconfdir}/sysconfig/%{name}

bzcat %{SOURCE1} > %{buildroot}/%{_initrddir}/%{name}
install -d %{buildroot}/%{_var}/cache/%{name}

%pre
%_pre_useradd %{name} %{_var}/cache/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%clean
rm -Rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*
%attr(755,root,root) %{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/cron.weekly/%{name}
%dir %attr(755,%{name},adm) %{_var}/cache/%{name}
%doc README



%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0-7mdv2011.0
+ Revision: 619488
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 3.0-6mdv2010.0
+ Revision: 429478
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 3.0-5mdv2009.0
+ Revision: 247062
- rebuild

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 3.0-3mdv2008.1
+ Revision: 140755
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - import http-replicator


* Wed Sep 06 2006 Buchan Milne <bgmilne@mandriva.org> 3.0-3mdv2007.0
- Rebuild

* Thu Oct 13 2005 Rafael Garcia-Suarez <rgarciasuarez@mandriva.com> 3.0-2mdk
- Remove unused file /etc/http-replicator
- cron and init.d files must not be marked as config(noreplace)

* Mon Apr 25 2005 Buchan Milne <bgmilne@linux-mandrake.com> 3.0-1mdk
- New release 3.0
- mkrel
- s/akel/iva L/

* Tue Aug 03 2004 Buchan Milne <bgmilne@linux-mandrake.com> 2.1-0.rc1.1mdk
- First Mandrake package
