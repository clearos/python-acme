%global         srcname  acme

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-acme
Version:        0.13.0
Release:        1%{?dist}
Summary:        Python library for the ACME protocol
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/acme
Source0:        https://files.pythonhosted.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

%if 0%{?rhel}
Patch0:         epel7-setup.patch
%endif

BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  python-sphinx_rtd_theme
BuildRequires:  python-cryptography
BuildRequires:  pyOpenSSL >= 0.13
BuildRequires:  python-requests
BuildRequires:  python-pyrfc3339

%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
BuildRequires:  python3-cryptography
BuildRequires:  python3-pyOpenSSL >= 0.13
BuildRequires:  python3-requests
BuildRequires:  python3-pyrfc3339
%endif

# Required for testing
BuildRequires:  python-ndg_httpsclient
BuildRequires:  python-nose
BuildRequires:  python-tox
BuildRequires:  python-mock
BuildRequires:  pytz

%if %{with python3}
BuildRequires:  python3-ndg_httpsclient
BuildRequires:  python3-nose
BuildRequires:  python3-tox
BuildRequires:  python3-mock
BuildRequires:  python3-pytz
%endif

BuildArch:      noarch

%{!?py2_build: %global py2_build CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build}
%{!?py2_install: %global py2_install %{__python} setup.py install --skip-build --root %{buildroot}}
%{!?python2_sitelib: %global python2_sitelib %{python_sitelib}}

%package -n python2-acme
Requires: python-cryptography
Requires: python-ndg_httpsclient
Requires: python-pyasn1
Requires: pyOpenSSL >= 0.13
Requires: python-pyrfc3339
Requires: pytz
Requires: python-requests
Requires: python-six
%if %{with python3}
# Recommends not supported by rpm on EL7
#Recommends: python-acme-doc
%endif
Summary:        %{summary}
%{?python_provide:%python_provide python2-acme}


%description
Python libraries implementing the Automatic Certificate Management Environment
(ACME) protocol. It is used by the Let's Encrypt project.

%description -n python2-acme
Python 2 library for use of the Automatic Certificate Management Environment
protocol as defined by the IETF. It's used by the Let's Encrypt project.

%if %{with python3}
%package -n python3-acme
Requires: python3-cryptography
Requires: python3-ndg_httpsclient
Requires: python3-pyasn1
Requires: python3-pyOpenSSL
Requires: python3-pyrfc3339
Requires: python3-pytz
Requires: python3-requests
Requires: python3-six
#Recommends: python-acme-doc
Summary:        %{summary}
%{?python_provide:%python_provide python3-acme}

%description -n python3-acme
Python 3 library for use of the Automatic Certificate Management Environment
protocol as defined by the IETF. It's used by the Let's Encrypt project.
%endif

%package doc
Provides: bundled(jquery)
Provides: bundled(underscore)
Provides: bundled(inconsolata-fonts)
Provides: bundled(lato-fonts)
Provides: bundled(robotoslab-fonts)
Requires: fontawesome-fonts fontawesome-fonts-web
Summary:  Documentation for python-acme libraries

%description doc
Documentation for the ACME python libraries

%prep
%autosetup -p1 -n %{srcname}-%{version}


%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
mv %{buildroot}%{_bindir}/jws{,-2}
%if %{with python3}
%py3_install
mv %{buildroot}%{_bindir}/jws{,-3}
%endif
# man page is pretty useless but api pages are decent
# Issue opened upstream for improving man page
# Need to cd as parent makefile tries to build libraries
(  cd docs && make  html )
# Clean up stuff we don't need for docs
rm -rf docs/_build/html/{.buildinfo,man,_sources}
# Unbundle fonts already on system
# Lato ttf is in texlive but that adds a lot of dependencies (30+MB) for just a font in documentation
# and lato is not in it's own -fonts package, only texlive
rm -f docs/_build/html/_static/fonts/fontawesome*
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.eot docs/_build/html/_static/fonts/fontawesome-webfont.eot
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.svg docs/_build/html/_static/fonts/fontawesome-webfont.svg
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.ttf docs/_build/html/_static/fonts/fontawesome-webfont.ttf
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.woff docs/_build/html/_static/fonts/fontawesome-webfont.woff
# upstream state that certbot isn't ready for python3 yet so symlink the -2 version for now
ln -s %{_bindir}/jws-2 %{buildroot}%{_bindir}/jws

%check
%{__python2} setup.py test
%if %{with python3}
%{__python3} setup.py test
%endif
# Make sure the scripts use the expected python versions
grep -q %{__python2} %{buildroot}%{_bindir}/jws-2
%if %{with python3}
grep -q %{__python3} %{buildroot}%{_bindir}/jws-3
%endif

%files -n python2-acme
%license LICENSE.txt
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}*.egg-info
%{_bindir}/jws
%{_bindir}/jws-2

%if %{with python3}
%files -n python3-acme
%license LICENSE.txt
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}*.egg-info
%{_bindir}/jws-3
%endif

%files doc
%license LICENSE.txt
%doc README.rst
%doc docs/_build/html

%changelog
* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 0.13.0-1
- Update to 0.13.0

* Fri Mar 03 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-3
- upstream request not to use py3 yet so switch jws to py2
- include a py3 option for testing

* Fri Mar 03 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-2
- Build for python rpm macro change

* Fri Mar 03 2017 James Hogarth <james.hogarth@gmail.com> - 0.12.0-1
- Update to 0.12.0
- Change %{_bindir}/jws to be python3 on Fedora

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.11.1-1
- Upgrade to 0.11.1

* Thu Jan 05 2017 Adam Williamson <awilliam@redhat.com> - 0.9.3-2
- Backport upstream fix for tests with OpenSSL 1.1
- Backport upstream removal of sphinxcontrib-programoutput usage
- Re-enable doc generation

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com>
- Rebuild for Python 3.6
- Removing the docs subpackage for now until the dependency works in rawhide

* Fri Oct 14 2016 Nick Bebout <nb@fedoraproject.org> - 0.9.3-1
- Upgrade to 0.9.3
* Thu Oct 13 2016 Nick Bebout <nb@fedoraproject.org> - 0.9.2-1
- Upgrade to 0.9.2
* Fri Oct 07 2016 Nick Bebout <nb@fedoraproject.org> - 0.9.1-1
- Upgrade to 0.9.1
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Wed Jun 15 2016 Nick Bebout <nb@fedoraproject.org> - 0.8.1-1
- Upgrade to 0.8.1
* Fri Jun 03 2016 James Hogarth <james.hogarth@gmail.com> - 0.8.0-1
- update to 0.8.0 release
* Mon May 30 2016 Nick Bebout <nb@fedoraproject.org> - 0.7.0-1
- Upgrade to 0.7.0
* Thu May 12 2016 Nick Bebout <nb@fedoraproject.org> - 0.6.0-1
- Upgrade to 0.6.0
* Wed Apr 06 2016 Nick Bebout <nb@fedoraproject.org> - 0.5.0-1
- Upgrade to 0.5.0
* Sat Mar 05 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-3
- Package does not require python-werkzeug anymore, upstream #2453
* Fri Mar 04 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-2
- Fix build on EL7 where no newer setuptools is available
* Fri Mar 04 2016 Robert Buchholz <rbu@fedoraproject.org> - 0.4.2-1
- Upgrade to 0.4.2
* Tue Mar 1 2016 Nick Le Mouton <nick@noodles.net.nz> - 0.4.1-1
- Upgrade to 0.4.1
* Thu Feb 11 2016 Nick Bebout <nb@fedoraproject.org> - 0.4.0-1
- Upgrade to 0.4.0
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
* Thu Jan 28 2016 Nick Bebout <nb@fedoraproject.org> - 0.3.0-1
- Upgrade to 0.3.0
* Thu Jan 21 2016 Nick Bebout <nb@fedoraproject.org> - 0.2.0-1
- Upgrade to 0.2.0
* Wed Dec 16 2015 Nick Bebout <nb@fedoraproject.org> - 0.1.1-1
- Upgrade to 0.1.1
* Fri Dec 04 2015 James Hogarth <james.hogarth@gmail.com> - 0.1.0-3
- Restore missing dependencies causing a FTBFS with py3 tests
- Add the man pages
* Thu Dec 03 2015 Robert Buchholz <rbu@goodpoint.de> - 0.1.0-4
- Specify more of the EPEL dependencies
* Thu Dec 03 2015 Robert Buchholz <rbu@goodpoint.de> - 0.1.0-3
- epel7: Only build python2 package
* Thu Dec 03 2015 James Hogarth <james.hogarth@gmail.com> - 0.1.0-2
- Fix up the removal of the dev release snapshot
* Thu Dec 03 2015 James Hogarth <james.hogarth@gmail.com> - 0.1.0-1
- Update to new upstream release for the open beta
* Mon Nov 30 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-3-dev20151123
- Update spec with comments from review
* Sat Nov 28 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-2.dev20151123
- Update spec with comments from review
- Add python3 library
* Fri Nov 27 2015 James Hogarth <james.hogarth@gmail.com> - 0.0.0-1.dev20151123
- initial packaging
