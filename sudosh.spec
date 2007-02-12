Summary:	sudo shell
Summary(pl.UTF-8):   Powłoka sudo
Name:		sudosh
Version:	1.8.2
Release:	0.1
License:	Open Software License v2.0
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/sudosh/%{name}-%{version}.tar.gz
# Source0-md5:	7121efdac817e4a27111869f27fabea0
Patch0:		%{name}-DESTDIR.patch
URL:		http://sourceforge.net/projects/sudosh/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
Requires(post,preun):	sed >= 4.0
Requires(post):	grep
Requires:	sudo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin

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
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/var/log/%{name},%{_sysconfdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f /etc/shells ]; then
	umask 022
	echo '%{_bindir}/sudosh' >> /etc/shells
else
	grep -q '^%{_bindir}/sudosh$' /etc/shells || echo '%{_bindir}/sudosh' >> /etc/shells
fi

%preun
if [ "$1" = "0" ]; then
	sed -i -e '/^%(echo %{_bindir} | sed -e 's,/,\\/,g')\/sudosh$/d' /etc/shells
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS PLATFORMS README
%attr(755,root,root) %{_bindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%{_mandir}/man[158]/*
%attr(1733,root,root) %dir /var/log/%{name}
