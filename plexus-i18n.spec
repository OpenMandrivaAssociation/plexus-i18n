%{?_javapackages_macros:%_javapackages_macros}
%define parent plexus
%define subname i18n

Name:           plexus-i18n
Version:        1.0
Release:        0.6.b10.3
Summary:        Plexus I18N Component
License:        ASL 2.0
Group:          Development/Java
URL:            http://plexus.codehaus.org/plexus-components/plexus-i18n
BuildArch:      noarch

# svn export http://svn.codehaus.org/plexus/plexus-components/tags/plexus-i18n-1.0-beta-10/
# tar cjf plexus-i18n-1.0-beta-10-src.tar.bz2 plexus-i18n-1.0-beta-10/
Source0:        plexus-i18n-1.0-beta-10-src.tar.bz2

Patch0:         %{name}-migration-to-component-metadata.patch
Patch1:         %{name}-plexus-container-default-missing.patch

BuildRequires:  maven-local
BuildRequires:  mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:  mvn(org.codehaus.plexus:plexus-components:pom:)
BuildRequires:  mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:  mvn(org.codehaus.plexus:plexus-utils)

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

# doesn't like - in EVR
sed -i 's/1.0-beta-10/1.0.beta.10/' pom.xml
%patch0 -p1
%patch1 -p1

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.b10.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0-0.5.b10.3
- Update to current packaging guidelines

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

