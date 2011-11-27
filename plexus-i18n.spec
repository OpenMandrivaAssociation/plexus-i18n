# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define with_maven 1
%define parent plexus
%define subname i18n

Name:           plexus-i18n
Version:        1.0
Release:        0.b10.2.3
Summary:        Plexus I18N Component
License:        ASL 2.0
Group:          Development/Java
URL:           http://plexus.codehaus.org/plexus-components/plexus-i18n
Source0:        plexus-i18n-1.0-beta-10-src.tar.bz2
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-i18n-1.0-beta-10/
# tar cjf plexus-i18n-1.0-beta-10-src.tar.bz2 plexus-i18n-1.0-beta-10/
Source1:        plexus-i18n-1.0-build.xml
Source5:        plexus-i18n-1.0-plexus-components.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-devel >= 1.6.0
%if %{with_maven}
BuildRequires:  maven2 >= 2.0.4-10jpp
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
BuildRequires:  plexus-maven-plugin
%endif
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  plexus-container-default 
BuildRequires:  plexus-utils 
Requires:  classworlds >= 0:1.1
Requires:  plexus-container-default 
Requires:  plexus-utils 
Requires(post):    jpackage-utils >= 0:1.7.2
Requires(postun):  jpackage-utils >= 0:1.7.2

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n plexus-i18n-1.0-beta-10
for j in $(find . -name "*.jar"); do
        mv $j $j.no
done
cp %{SOURCE1} build.xml
mkdir -p src/main/resources/META-INF/plexus

%build
%if %{with_maven}
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -Dmaven2.jpp.mode=true \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%else

mkdir -p target/lib
build-jar-repository -s -p target/lib \
classworlds \
plexus/container-default \
plexus/utils \

ant jar javadoc

# inject pom and component descriptor into the jar (can be done via ant, but
# since build.xml is autogenerated, it is best to do it here)
mkdir -p META-INF/plexus META-INF/maven/org.codehaus.plexus/plexus-i18n/
cp %{SOURCE5} META-INF/plexus/components.xml
cp pom.xml META-INF/maven/org.codehaus.plexus/plexus-i18n/
jar uvf target/%{name}-%{version}-beta-10.jar META-INF
rm -rf META-INF

%endif

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/plexus
install -pm 644 target/%{name}-%{version}-beta-10.jar \
  $RPM_BUILD_ROOT%{_javadir}/plexus/i18n-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}

(cd $RPM_BUILD_ROOT%{_javadir}/plexus && for jar in *-%{version}*; \
   do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
%if %{with_maven}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom
%endif

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%if %{with_maven}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%else
cp -pr target/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
%endif
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_javadir}/%{parent}/*
%if %{with_maven}
%{_datadir}/maven2/poms/*
%endif
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}

