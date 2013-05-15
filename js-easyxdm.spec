Summary:	jQuery JavaScript Library
Summary(pl.UTF-8):	Biblioteka JavaScriptu jQuery
Name:		js-easyxdm
Version:	2.4.11.104
Release:	2
License:	MIT
Group:		Applications/WWW
Source0:	https://github.com/downloads/oyvindkinsey/easyXDM/easyXDM-%{version}.zip
# Source0-md5:	6c451cfa4702d6f5259570e9ae17bce0
URL:		http://www.easyxdm.net/
BuildRequires:	js
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	unzip
BuildRequires:	yuicompressor
Requires:	webserver(access)
Requires:	webserver(alias)
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		easyxdm
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
easyXDM is a JavaScript library that enables you as a developer to
easily work around the limitation set in place by the Same Origin
Policy, in turn making it easy to communicate and expose JavaScript
API's across domain boundaries.

%prep
%setup -qc

# Apache1 config
cat > apache.conf <<'EOF'
Alias /js/easyXDM/ %{_appdir}/
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

# Apache2 config
cat > httpd.conf <<'EOF'
Alias /js/easyXDM/ %{_appdir}/
<Directory %{_appdir}>
	Require all granted
</Directory>
EOF

# Lighttpd config
cat > lighttpd.conf <<'EOF'
alias.url += (
    "/js/easyXDM/" => "%{_appdir}/",
)
EOF

%build
install -d build

# compress .js
yuicompressor --charset UTF-8 easyXDM.js -o build/easyXDM.js
js -C -f build/easyXDM.js

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}
cp -p build/easyXDM.js $RPM_BUILD_ROOT%{_appdir}

install -d $RPM_BUILD_ROOT%{_sysconfdir}
cp -a apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -a lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc MIT-license.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%dir %{_appdir}
%{_appdir}/*.js
