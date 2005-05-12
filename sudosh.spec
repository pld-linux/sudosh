Summary:	sudo shell
Summary(pl):	Pow³oka sudo
Name:		sudosh
Version:	1.6.2
Release:	0.1
License:	Open Software License v2.0
Group:		Applications/Shells
Source0:	http://dl.sourceforge.net/sudosh/%{name}-%{version}.tar.gz
# Source0-md5:	eaae26de9184094f8d828f591ee519c0
URL:		http://sourceforge.net/projects/sudosh/
Requires:	sudo
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/log/%{name}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS PLATFORMS README
%attr(755,root,root) %{_bindir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%attr(1733,root,root) %dir /var/log/%{name}
