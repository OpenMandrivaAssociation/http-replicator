%define version 3.0
%define release  %mkrel 3

Name:		http-replicator
Version:	%version
Release:	%release
URL:		http://gertjan.freezope.org/replicator/
Source:		http://gertjan.freezope.org/replicator/%{name}_%{version}.tar.bz2
Source1:	%{name}.init.bz2
Group:		System/Servers
License:	GPL
Summary:	General purpose caching proxy server
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

