%global         srcname  acme

Name:           python-acme
Version:        0.1.0
Release:        2%{?dist}
Summary:        Python library for the ACME protocol
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/acme
Source0:        https://pypi.python.org/packages/source/a/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-sphinx
BuildRequires:  python-sphinxcontrib-programoutput
BuildRequires:  python-cryptography
BuildRequires:  pyOpenSSL
BuildRequires:  python-requests
BuildRequires:  python-pyrfc3339
BuildRequires:  python-werkzeug

BuildRequires:  python3-devel
BuildRequires:  python3-cryptography
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-requests
BuildRequires:  python3-pyrfc3339
BuildRequires:  python3-werkzeug

# Required for testing
BuildRequires:  python-ndg_httpsclient
BuildRequires:  python-nose
BuildRequires:  python-tox

BuildRequires:  python3-ndg_httpsclient
BuildRequires:  python3-nose
BuildRequires:  python3-tox

BuildArch:      noarch

%package -n python2-acme
Requires: python-cryptography
Requires: python-ndg_httpsclient
Requires: python-pyasn1
Requires: pyOpenSSL
Requires: python-pyrfc3339
Requires: pytz
Requires: python-requests
Requires: python-six
Requires: python-werkzeug
Recommends: python-acme-doc
Summary:        %{summary}
%{?python_provide:%python_provide python2-acme}


%description
Python libraries implementing the Automatic Certificate Management Environment
(ACME) protocol. It is used by the Let's Encrypt project.

%description -n python2-acme
Python 2 library for use of the Automatic Certificate Management Environment
protocol as defined by the IETF. It's used by the Let's Encrypt project.

%package -n python3-acme
Requires: python3-cryptography
Requires: python3-ndg_httpsclient
Requires: python3-pyasn1
Requires: python3-pyOpenSSL
Requires: python3-pyrfc3339
Requires: python3-pytz
Requires: python3-requests
Requires: python3-six
Requires: python3-werkzeug
Recommends: python-acme-doc
Summary:        %{summary}
%{?python_provide:%python_provide python3-acme}

%description -n python3-acme
Python 3 library for use of the Automatic Certificate Management Environment
protocol as defined by the IETF. It's used by the Let's Encrypt project.

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
%autosetup -n %{srcname}-%{version}


%build
%py2_build
%py3_build

# build documentation
%{__python2} setup.py install --user
make -C docs html PATH=$HOME/.local/bin:$PATH

# Clean up stuff we don't need for docs
rm -rf docs/_build/html/{.buildinfo,_sources}

%install
# Do python3 first so bin ends up from py2
%py3_install
%py2_install

# Unbundle fonts already on system
# Lato ttf is in texlive but that adds a lot of dependencies (30+MB) for just a font in documentation
# and lato is not in it's own -fonts package, only texlive
rm -f docs/_build/html/_static/fonts/fontawesome*
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.eot docs/_build/html/_static/fonts/fontawesome-webfont.eot
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.svg docs/_build/html/_static/fonts/fontawesome-webfont.svg
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.ttf docs/_build/html/_static/fonts/fontawesome-webfont.ttf
ln -sf /usr/share/fonts/fontawesome/fontawesome-webfont.woff docs/_build/html/_static/fonts/fontawesome-webfont.woff


%check
%{__python2} setup.py test
%{__python3} setup.py test
# Make sure the script uses the expected python version
grep -q %{__python2} %{buildroot}%{_bindir}/jws

%files -n python2-acme
%license LICENSE.txt
%{python2_sitelib}/%{srcname}
%{python2_sitelib}/%{srcname}-%{version}*.egg-info
%{_bindir}/jws

%files -n python3-acme
%license LICENSE.txt
%{python3_sitelib}/%{srcname}
%{python3_sitelib}/%{srcname}-%{version}*.egg-info

%files doc
%license LICENSE.txt
%doc README.rst
%doc docs/_build/html

%changelog
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
