%define		plugin	gallery
%define		php_min_version 5.0.0
%include	/usr/lib/rpm/macros.php
Summary:	DokuWiki Plugin to embed an automatically created image gallery into a page
Name:		dokuwiki-plugin-%{plugin}
Version:	20100430
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://github.com/splitbrain/dokuwiki-plugin-%{plugin}/tarball/master/%{plugin}-%{version}.tgz
# Source0-md5:	d368c8dff315fc1f7bde4d065279d224
URL:		http://www.dokuwiki.org/plugin:gallery
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20091225
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-pcre
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
%{plugindir}/*.css
%{plugindir}/*.js
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/images
