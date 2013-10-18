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

%define gcj_support 1

# If you don't want to build with maven, and use straight ant instead,
# give rpmbuild option '--without maven'

%define with_maven 0

%define section     free
%define parent plexus
%define subname i18n

Summary:	Plexus I18N Component
Name:		plexus-i18n
Version:	1.0
Release:	0.b6.5.0.1
License:	Apache Software License
Group:		Development/Java
Url:		http://plexus.codehaus.org/
Source0:	plexus-i18n-1.0-beta-6-src.tar.gz
# svn export svn://svn.plexus.codehaus.org/plexus/tags/plexus-i18n-1.0-beta-6
# tar czf plexus-i18n.tar.gz plexus-i18n-1.0-beta-6/
Source1:	plexus-i18n-1.0-build.xml
Source2:	plexus-i18n-1.0-project.xml
Source3:	plexus-i18n-settings.xml
Source4:	plexus-i18n-1.0-jpp-depmap.xml
%if ! %{gcj_support}
BuildArch:	noarch
%else
BuildRequires:	java-gcj-compat-devel
%endif
BuildRequires:	java-rpmbuild >= 0:1.6
BuildRequires:	ant >= 0:1.6
%if %{with_maven}
BuildRequires:	maven2 >= 2.0.4-10jpp
BuildRequires:	maven2-plugin-compiler
BuildRequires:	maven2-plugin-install
BuildRequires:	maven2-plugin-jar
BuildRequires:	maven2-plugin-javadoc
BuildRequires:	maven2-plugin-resources
BuildRequires:	maven2-plugin-surefire
BuildRequires:	maven2-plugin-release
BuildRequires:	plexus-maven-plugin
%endif
BuildRequires:	classworlds >= 0:1.1
BuildRequires:	plexus-container-default 
BuildRequires:	plexus-utils 
Requires:	classworlds >= 0:1.1
Requires:	plexus-container-default 
Requires:	plexus-utils 

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -qn plexus-i18n-1.0-beta-6
%remove_java_binaries
cp %{SOURCE1} build.xml
cp %{SOURCE2} project.xml
cp %{SOURCE3} settings.xml

%build
%if %{with_maven}
sed -i -e "s|<url>__JPP_URL_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__JAVADIR_PLACEHOLDER__</url>|<url>file://`pwd`/external_repo</url>|g" settings.xml
sed -i -e "s|<url>__MAVENREPO_DIR_PLACEHOLDER__</url>|<url>file://`pwd`/.m2/repository</url>|g" settings.xml
sed -i -e "s|<url>__MAVENDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/maven2/plugins</url>|g" settings.xml
sed -i -e "s|<url>__ECLIPSEDIR_PLUGIN_PLACEHOLDER__</url>|<url>file:///usr/share/eclipse/plugins</url>|g" settings.xml

export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository
mkdir -p $MAVEN_REPO_LOCAL

mkdir external_repo
ln -s %{_javadir} external_repo/JPP

mvn-jpp \
        -e \
        -s $(pwd)/settings.xml \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=%{SOURCE4} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%else
mkdir -p target/lib
build-jar-repository -s -p target/lib \
classworlds \
plexus/container-default \
plexus/utils \

%{ant} jar javadoc
%endif

%install
# jars
install -d -m 755 %{buildroot}%{_javadir}/plexus
install -pm 644 target/%{name}-%{version}-beta-6.jar \
  %{buildroot}%{_javadir}/plexus/i18n-%{version}.jar
%add_to_maven_depmap org.codehaus.plexus %{name} %{version} JPP/%{parent} %{subname}

(cd %{buildroot}%{_javadir}/plexus && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# poms
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 pom.xml \
    %{buildroot}%{_datadir}/maven2/poms/JPP.%{parent}-%{subname}.pom

# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/apidocs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name} 

%{gcj_compile}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%{_javadir}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%{gcj_files}

%files javadoc
%doc %{_javadocdir}/*

