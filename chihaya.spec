%define debug_package %{nil}

%define  uid   chihaya
%define  gid   chihaya
%define  nuid  972
%define  ngid  972



Name:     chihaya
Version:  2.1.2
Release:  3%{?dist}
Summary:  Chihaya Bittorrent Tracker Written in GoLang
Epoch:    1
Packager: idcm <idcm@live.cn>
License:  2 Clause BSD
Group:    System Environment/Daemons
URL:      https://github.com/idcm/chihaya/tags
Source0:  https://github.com/idcm/chihaya/archive/%{version}.tar.gz
Source1:  chihaya.service
Source2:  chihaya.sysconfig
Source3:  example_config.yaml

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires:     golang
BuildRequires:     git
BuildRequires:     systemd
Requires(post):    systemd
Requires(preun):   systemd
Requires(postun):  systemd



%description
Chihaya an opensource and public tracker written in GoLang.
An example command to scrap the stats from the service:
 curl http://localhost:6880/stats?flatten=1
** Use Firewall since the service is open by default for to anyone!!

%prep
%setup -q -n %{name}-%{version}

%build
go build ./cmd/chihaya

%install
rm -rf %{buildroot}

install -p -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}

# install binary
install -p -D -m 0755 %{_builddir}/%{name}-%{version}/chihaya %{buildroot}%{_bindir}/%{name}

# install unit file
install -p -D -m 0644 \
   %{SOURCE1} \
   %{buildroot}%{_unitdir}/chihaya.service

# install configuration
install -p -D -m 0644 \
   %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/%{name}/%{name}.yaml

install -p -D -m 0644 \
   %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/sysconfig/chihaya

%clean
rm -rf %{buildroot}

%pre
# Create user and group if nonexistent
# Try using a common numeric uid/gid if possible
if [ ! $(getent group %{gid}) ]; then
   if [ ! $(getent group %{ngid}) ]; then
      groupadd -r -g %{ngid} %{gid} > /dev/null 2>&1 || :
   else
      groupadd -r %{gid} > /dev/null 2>&1 || :
   fi
fi
if [ ! $(getent passwd %{uid}) ]; then
   if [ ! $(getent passwd %{nuid}) ]; then
      useradd -M -r -s /sbin/nologin -u %{nuid} -g %{gid} %{uid} > /dev/null 2>&1 || :
   else
      useradd -M -r -s /sbin/nologin -g %{gid} %{uid} > /dev/null 2>&1 || :
   fi
fi

%post
%systemd_post chihaya.service

%preun
%systemd_preun chihaya.service

%postun
%systemd_postun_with_restart chihaya.service

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/sysconfig/chihaya
%config(noreplace) %{_sysconfdir}/%{name}
%{_unitdir}/chihaya.service

%changelog
* Tue Jan 07 2020 Eliezer Croitoru <eliezer@ngtech.co.il>
- Release 2.0.0 Stable.
