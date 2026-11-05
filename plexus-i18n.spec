Name:		plexus-i18n
Version:	1.2.0
Release:	1
Summary:	Looks up localised messages from resource bundles
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/codehaus-plexus/plexus-i18n
Source0:	https://github.com/codehaus-plexus/plexus-i18n/archive/refs/tags/plexus-i18n-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:	mvn(org.codehaus.plexus:plexus:pom::)
BuildRequires:	mvn(javax.inject:javax.inject)
BuildRequires:	mvn(org.slf4j:slf4j-api)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name}

%description
Plexus I18N looks up messages from resource bundles, with a default
bundle and locale. Doxia's integration tools use it.

%prep
%autosetup -n plexus-i18n-plexus-i18n-%{version}

%files -f .mfiles
%doc README.md
