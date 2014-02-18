#
# Conditional build:
%bcond_with	tests	# do not perform "make test" (they use network)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	libcloud
Summary:	Unified Python API for cloud service providers
Name:		python-%{module}
Version:	0.14.1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	ftp://apache.cs.utah.edu/apache.org/libcloud/apache-%{module}-%{version}.tar.bz2
# Source0-md5:	0270c54b3f61a60a008271d92addb7b8
Patch0:		cacerts_path.patch
URL:		https://libcloud.apache.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%{?with_tests:BuildRequires:	python-mock}
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
%{?with_tests:BuildRequires:	python3-mock}
BuildRequires:	python3-modules
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libcloud is a Python library for interacting with many of the popular
cloud service providers using a unified API. It was created to make it
easy for developers to build products that work between any of the
services that it supports.

Resource you can manage with Libcloud are divided in the following
categories:

- Cloud Servers and Block Storage - services such as Amazon EC2 and
  Rackspace CloudServers
- Cloud Object Storage and CDN - services such as Amazon S3 and
  Rackspace CloudFiles
- Load Balancers as a Service - services such as Amazon Elastic Load
  Balancer and GoGrid LoadBalancers
- DNS as a Service - services such as Amazon Route 53 and Zerigo

%package -n python3-%{module}
Summary:	Unified Python API for cloud service providers
Group:		Libraries/Python

%description -n python3-%{module}
Libcloud is a Python library for interacting with many of the popular
cloud service providers using a unified API. It was created to make it
easy for developers to build products that work between any of the
services that it supports.

Resource you can manage with Libcloud are divided in the following
categories:

- Cloud Servers and Block Storage - services such as Amazon EC2 and
  Rackspace CloudServers
- Cloud Object Storage and CDN - services such as Amazon S3 and
  Rackspace CloudFiles
- Load Balancers as a Service - services such as Amazon Elastic Load
  Balancer and GoGrid LoadBalancers
- DNS as a Service - services such as Amazon Route 53 and Zerigo

%prep
%setup -q -n apache-%{module}-%{version}

%patch0 -p1

cp libcloud/test/secrets.py-dist libcloud/test/secrets.py

%{__sed} -i -e '1s,^#!.*python,#!%{__python},' demos/*.py example_*.py

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a example_*.py demos $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a example_*.py demos $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst NOTICE README.rst
%{py_sitescriptdir}/%{module}
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst NOTICE README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif
