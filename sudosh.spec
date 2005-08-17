Summary:	sudo shell
Summary(pl):	Pow³oka sudo
Name:		sudosh
Version:	1.6.3
Release:	0.1
License:	Open Software License v2.0
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/sudosh/%{name}-%{version}.tar.gz
# Source0-md5:	700ee8c6060c1512ac0c2731b5727cc6
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

%description -l pl
sudosh to filtr wykorzystuj±cy zalety urz±dzeñ PTY, aby po¶redniczyæ
miêdzy klawiatur± u¿ytkownika a programem, w tym wypadku pow³ok±.
Zosta³ zaprojektowany w szczególno¶ci do u¿ywania z programem sudo i
umo¿liwia wywo³ywanie pow³oki roota z logowaniem. Jest zasadniczo
"kamer±" zapisuj±c± sesje pow³oki roota; ma tak¿e mo¿liwo¶æ
odtwarzania sesji tak, jak zosta³y oryginalnie zapisane. Zapisuje ca³e
wej¶cie i wyj¶cie, wej¶cie z klawiatury i informacje o czasie - tak,
¿e sesje mo¿na odtwarzaæ w oryginalnej postaci.

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
