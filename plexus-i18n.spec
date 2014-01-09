%{?_javapackages_macros:%_javapackages_macros}
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

%define parent plexus
%define subname i18n

Name:           plexus-i18n
Version:        1.0
Release:        0.5.b10.2.1%{?dist}
Summary:        Plexus I18N Component
License:        ASL 2.0

URL:           http://plexus.codehaus.org/plexus-components/plexus-i18n
Source0:        plexus-i18n-1.0-beta-10-src.tar.bz2
# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-i18n-1.0-beta-10/
# tar cjf plexus-i18n-1.0-beta-10-src.tar.bz2 plexus-i18n-1.0-beta-10/

Patch0:         %{name}-migration-to-component-metadata.patch
Patch1:         %{name}-plexus-container-default-missing.patch

BuildArch:      noarch
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  ant >= 0:1.6
BuildRequires:  java-devel >= 1.6.0
BuildRequires:  maven-local
BuildRequires:  maven-compiler-plugin
BuildRequires:  maven-install-plugin
BuildRequires:  maven-jar-plugin
BuildRequires:  maven-javadoc-plugin
BuildRequires:  maven-resources-plugin
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven-doxia-sitetools
BuildRequires:  plexus-containers-component-metadata
BuildRequires:  classworlds >= 0:1.1
BuildRequires:  plexus-containers-container-default
BuildRequires:  plexus-utils
Requires:  classworlds >= 0:1.1
Requires:  plexus-containers-container-default
Requires:  plexus-utils

%description
The Plexus project seeks to create end-to-end developer tools for 
writing applications. At the core is the container, which can be 
embedded or for a full scale application server. There are many 
reusable components for hibernate, form processing, jndi, i18n, 
velocity, etc. Plexus also includes an application server which 
is like a J2EE application server, without all the baggage.


%package javadoc
Summary:        Javadoc for %{name}


%description javadoc
Javadoc for %{name}.


%prep
%setup -q -n plexus-i18n-1.0-beta-10
%patch0 -p1
%patch1 -p1

%build
mvn-rpmbuild -e install javadoc:aggregate

%install
# jars
install -Dpm 644 target/%{name}-%{version}-beta-10.jar \
     %{buildroot}/%{_javadir}/%{parent}/%{subname}.jar

# poms
install -Dpm 644 pom.xml %{buildroot}/%{_mavenpomdir}/JPP.%{name}.pom
%add_maven_depmap JPP.%{name}.pom %{parent}/%{subname}.jar

# javadoc
install -d -m 755 %{buildroot}/%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* %{buildroot}/%{_javadocdir}/%{name}
%if 0%{?fedora}
%else
# rpm5 parser...
sed -i 's|1.0-beta-10|1.0.beta.10|g;' %{buildroot}%{_mavendepmapfragdir}/*
%endif

%pre javadoc
# workaround for rpm bug, can be removed in F-19
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%files
%{_javadir}/%{parent}/%{subname}.jar
%{_mavenpomdir}/JPP.%{name}.pom
%{_mavendepmapfragdir}/%{name}

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.b10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.4.b10.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0-0.3.b10.2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 22 2012 Jaromir Capik <jcapik@redhat.com> - 1.0-0.2.b10.2
- Migration to plexus-containers-container-default

* Mon Nov 12 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.1.b10.2
- Fix Release tag

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.b10.2.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Jaromir Capik <jcapik@redhat.com> - 1.0-0.b10.2.4
- Missing plexus-container-default dependency added in the pom.xml

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.b10.2.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jul 28 2011 Jaromir Capik <jcapik@redhat.com> - 1.0-0.b10.2.2
- Migration to maven3
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Minor spec file changes according to the latest guidelines

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b10.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.b10.2
- BR java-devel 1.6.0.

* Wed Dec 23 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.0-0.b10.1
- Update to beta 10.
- Drop gcj and fix BRs.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b6.5.3.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b6.5.3.2
- Added pom.xml and components.xml to META-INF

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.0-0.b6.5.3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.0-0.b6.5.3
- drop repotag

* Wed Feb 27 2008 Deepak Bhole <dbhole@redhat.com> - 0:1.0-0.b6.5jpp.2
- Build with maven

* Tue Jan 22 2008 Permaine Cheung <pcheung@redhat.com> - 0:1.0-0.b6.5jpp.1
- Update to the same version as upstream

* Thu Apr 26 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.5jpp
- Reupload to fix metadata

* Sat Mar 24 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.4jpp
- Optionally build without maven
- Add gcj_support option
 
* Mon Feb 19 2007 Tania Bento <tbento@redhat.com> - 0:1.0-0.b6.3jpp.1
- Fixed %%Release tag.
- Changed the svn URL.
- Added instruction on how to tar the files extracted with svn export.
- Fixed %%BuildRoot tag.
- Removed %%post and %%postun sections for javadoc and made necessary changes.
- Added gcj support.

* Wed Oct 25 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.3jpp
- Fix components.xml
 
* Tue May 30 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.2jpp
- First JPP-1.7 release
- Drop maven support - waiting for maven2

* Mon Nov 07 2005 Ralph Apel <r.apel at r-apel.de> - 0:1.0-0.b6.1jpp
- First JPackage build
