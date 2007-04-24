Summary:	sudo shell
Summary(pl.UTF-8):	Powłoka sudo
Name:		sudosh
# NB! read changelog before attempting to upgrade to 1.8.x series
Version:	2.0.00
Release:	0.1
License:	Open Software License v2.0
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/sudosh/%{name}-%{version}.tar.gz
# Source0-md5:	bc810e73d615821de0c7ceb716212428
Patch0:		%{name}-Makefile.am-install.patch
URL:		http://sourceforge.net/projects/sudosh/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires(preun):	sed >= 4.0
Requires(post):	grep
Requires:	sudo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_shell		%{_bindir}/eash

%description
sudosh is a filter that takes advantage of PTY devices in order to sit
between the user's keyboard and a program, in this case a shell. It
was designed specifically to be used in conjunction with sudo, and
allows the execution of a root shell with logging. It is basically a
VCR and will record root shell sessions and also has the ability to
play back the sessions as they were originally recorded. It records
all input/output, keyboard input, and timing information so that the
session can be played back in the original format.

%description -l pl.UTF-8
sudosh to filtr wykorzystujący zalety urządzeń PTY, aby pośredniczyć
między klawiaturą użytkownika a programem, w tym wypadku powłoką.
Został zaprojektowany w szczególności do używania z programem sudo i
umożliwia wywoływanie powłoki roota z logowaniem. Jest zasadniczo
"kamerą" zapisującą sesje powłoki roota; ma także możliwość
odtwarzania sesji tak, jak zostały oryginalnie zapisane. Zapisuje całe
wejście i wyjście, wejście z klawiatury i informacje o czasie - tak,
że sesje można odtwarzać w oryginalnej postaci.

%prep
%setup -q -n eas-%{version}
%patch -p0

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/var/log/%{name},%{_bindir},%{_sysconfdir}/certs}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	umask 022
	echo '%{_shell}' > /etc/shells
else
	grep -q '^%{_shell}$' /etc/shells || echo '%{_shell}' >> /etc/shells
fi

%preun
if [ "$1" = "0" ]; then
	%{__sed} -i -e '/^%(echo %{_shell} | sed -e 's,/,\\/,g')$/d' /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/certs/*.pem
%dir %{_sysconfdir}/css
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/css/*.css 
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/easd_config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/eash_config

%attr(1733,root,root) %dir /var/log/%{name}
