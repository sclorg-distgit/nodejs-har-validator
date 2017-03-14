%{?scl:%scl_package nodejs-%{srcname}}
%{!?scl:%global pkg_name %{name}}

# needed for building on el6
%{?nodejs_find_provides_and_requires}

%global enable_tests 0
%global srcname har-validator

%global commit0 a71163c62b8786a41d503248fb60893598f3c26f
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global owner ahmadnassri

Name:           %{?scl_prefix}nodejs-%{srcname}
Version:        2.0.3
Release:        4%{?dist}
Summary:        Extremely fast HTTP Archive (HAR) validator using JSON Schema
License:        ISC
URL:            https://github.com/%{owner}/%{srcname}
Source0:        https://github.com/%{owner}/%{srcname}/archive/%{commit0}.tar.gz#/%{srcname}-%{shortcommit0}.tar.gz
# https://github.com/ahmadnassri/har-validator/pull/15
Patch0:         nodejs-har-validator-should8.patch

BuildArch:      noarch

%if 0%{?rhel} == 6
ExclusiveArch:  %{ix86} x86_64 %{arm} noarch
%else
ExclusiveArch:  %{nodejs_arches} noarch
%endif

BuildRequires:  %{?scl_prefix}nodejs-devel

%if 0%{?enable_tests}
BuildRequires:  %{?scl_prefix}npm(mocha)
BuildRequires:  %{?scl_prefix}npm(require-directory)
BuildRequires:  %{?scl_prefix}npm(pinkie-promise)
BuildRequires:  %{?scl_prefix}npm(is-my-json-valid)
BuildRequires:  %{?scl_prefix}npm(should) >= 8.0.0
%endif

%description
%{summary}.

%prep
%setup -q -n %{srcname}-%{commit0}
rm -rf node_modules

%nodejs_fixdep chalk
%nodejs_fixdep commander '2.x'

%build
#nothing to do

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{srcname}

cp -pr package.json lib/ bin/ \
    %{buildroot}%{nodejs_sitelib}/%{srcname}

mkdir -p %{buildroot}%{_bindir}
ln -s %{nodejs_sitelib}/%{srcname}/bin/har-validator \
    %{buildroot}%{_bindir}/har-validator

%nodejs_symlink_deps

%if 0%{?enable_tests}

%check
%nodejs_symlink_deps --check
mocha
%endif

%files
%{!?_licensedir:%global license %doc}
%doc README.md
%license LICENSE
%{nodejs_sitelib}/%{srcname}
%{_bindir}/har-validator

%changelog
* Mon Jan 16 2017 Zuzana Svetlikova <zsvetlik@redhat.com> - 2.0.3-4
- Rebuild for rhscl

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Dec 19 2015 Tom Hughes <tom@compton.nu> - 2.0.3-2
- Patch tests to work with should 8.x

* Sun Dec 06 2015 Piotr Popieluch <piotr1212@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Wed Nov 18 2015 Piotr Popieluch <piotr1212@gmail.com> - 2.0.2-1
- Initial package
