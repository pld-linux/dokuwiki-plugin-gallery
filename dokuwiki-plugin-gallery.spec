%define		subver	2016-12-22
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin	gallery
%define		php_min_version 5.1.0
Summary:	DokuWiki Plugin to embed an automatically created image gallery into a page
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/splitbrain/dokuwiki-plugin-gallery/archive/%{subver}/%{plugin}-%{version}.tar.gz
# Source0-md5:	2222b10270d5be1fddf1aa68b6f5183c
URL:		https://www.dokuwiki.org/plugin:gallery
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
Requires:	php(pcre)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
A basic gallery can be added by selecting a namespace like this:

{{gallery>namespace}}

%prep
%setup -qc
mv *-%{plugin}-*/* .

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/README
%{__rm} $RPM_BUILD_ROOT%{plugindir}/deleted.files

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.js
%{plugindir}/*.less
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/images
%{plugindir}/swipebox
