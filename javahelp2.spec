%{?_javapackages_macros:%_javapackages_macros}
# Copyright (c) 2000-2005, JPackage Project
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

Name:		javahelp2
Version:	2.0.05
Release:	18
Summary:	JavaHelp is a full-featured, platform-independent, extensible help system 
Group:		Development/Java
License:	GPLv2 with exceptions
Url:		https://javahelp.java.net/
Source0:	https://javahelp.dev.java.net/files/documents/5985/59373/%{name}-src-%{version}.zip
Source1:	%{name}-jhindexer.sh
Source2:	%{name}-jhsearch.sh
BuildArch:	noarch

BuildRequires:	javapackages-local
BuildRequires:	java-devel >= 1:1.6.0

BuildRequires:	ant
BuildRequires:	tomcat-servlet-3.0-api
BuildRequires:	tomcat-jsp-2.2-api


%description
JavaHelp software is a full-featured, platform-independent, extensible
help system that enables developers and authors to incorporate online
help in applets, components, applications, operating systems, and
devices. Authors can also use the JavaHelp software to deliver online
documentation for the Web and corporate Intranet.

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
# fix files perms
chmod -R go=u-w *
# remove windows files
find . -name "*.bat" -delete
#
# This class provides native browser integration and would require
# JDIC project to be present. Currently there is no such jpackage.org
# package, so deleting the class. When JDIC package is created,
# add BuildProvides and remove the "rm" call.
#
rm jhMaster/JavaHelp/src/new/javax/help/plaf/basic/BasicNativeContentViewerUI.java

mkdir javahelp_nbproject/lib
ln -s %{_javadir}/tomcat-jsp-api.jar javahelp_nbproject/lib/jsp-api.jar
ln -s %{_javadir}/tomcat-servlet-api.jar javahelp_nbproject/lib/servlet-api.jar

%build

ant -f javahelp_nbproject/build.xml \
 -Djavac.source=1.6 -Djavac.target=1.6 \
 -Djdic-jar-present=true -Djdic-zip-present=true \
 -Dservlet-jar-present=true -Dtomcat-zip-present=true \
 -Djavadoc.additionalparam="-Xdoclint:none" \
 release javadoc

%install
# see https://svn.java.net/svn/javahelp~svn/trunk/jhMaster/jhall.pom
%mvn_file javax.help:javahelp %{name}
%mvn_artifact javax.help:javahelp:%{version} javahelp_nbproject/dist/lib/jhall.jar
%mvn_install -J javahelp_nbproject/dist/lib/javadoc

install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}
#cp -pr jhMaster/JavaHelp/doc/public-spec/dtd $RPM_BUILD_ROOT%%{_datadir}/%%{name}
#cp -pr jhMaster/JavaHelp/demos $RPM_BUILD_ROOT%%{_datadir}/%%{name}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/jh2indexer
install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/jh2search

%files -f .mfiles
%{_bindir}/*
%dir %{_datadir}/%{name}

%files javadoc -f .mfiles-javadoc

%changelog
* Thu Jul 02 2015 gil cattaneo <puntogil@libero.it> 2.0.05-18
- fix FTBFS
- adapt to current guideline
- fix doclint issues
- fix some rpmlint problems
- update URL field
- add maven metadata

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Aug 05 2013 Omair Majid <omajid@redhat.com> - 2.0.05-15
- Update package to comply with latest guidelines
- Fix build dependencies

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 09 2012 Omair Majid <omajid@redhat.com> - 2.0.05-12
- Build with servlet api 6.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 27 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 2.0.05-7
- Fix FTBFS: added BR: servletapi5.
- Fixed wrapper scripts, resolves BZ#479341.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.05-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Apr 30 2008 Jaroslav Tulach <jtulach@netbeans.org> 2.0.05-5
- Removed epoch and did other stuff as per Fedora review

* Wed Apr 30 2008 Jaroslav Tulach <jtulach@netbeans.org> 2.0.05-4
- Converting to Fedora

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 2.0.05-2mdv2008.1
+ Revision: 120928
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Nov 21 2007 Nicolas Vigier <nvigier@mandriva.com> 0:2.0.05-1mdv2008.1
+ Revision: 111054
- build with java >= 1.6.0
- fix ant error (fix by Alexander Kurtakov)
- fix release, license, group tags
- add buildrequires
- import javahelp2


* Wed Nov 14 2007 Jaroslav Tulach <jtulach@netbeans.org> 0:2.0.05-1mdv
- Converted to version 2.0.05
- Removed demo and manual packages as they are not in current sources

* Wed Dec 20 2006 Jaroslav Tulach <Jaroslav.Tulach@Sun.COM> 0:2.0.02-2jpp
- Change License
- Include Sources
- Build from source
- Move to Free Section
- Temporarely remove the JDIC support (until we have a jdic package)

* Sat Dec 04 2004 Paolo Dona' <vik@3jv.com> 0:2.0.02-1jpp
- upgrade to 2.0_02

* Thu Feb 12 2004 Ralph Apel <r.apel@r-apel.de> 0:2.0.01-1jpp
- change pkg name to javahelp2
- change version notation to 2.0.01
- install scripts as jh2indexer and jh2search

* Wed Jan 14 2004 Ralph Apel <r.apel@r-apel.de> 0:2.0_01-1jpp
- upgrade to 2.0_01

* Mon Mar 24 2003 David Walluck <david@anti-microsoft.org> 0:1.1.3-2jpp
- update for JPackage 1.5

* Mon Mar 24 2003 David Walluck <david@anti-microsoft.org> 1.1.3-1jpp
- 1.1.3
- no more bzip2 on scripts
- fix Id tag in scripts

* Sat May 11 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-8jpp
- 1.1.2.01
- vendor, distribution, group tags
- updated scripts

* Fri Apr 05 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-7jpp 
- nosrc package
- section macro

* Thu Jan 17 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-6jpp
- javadoc in %%{_javadocdir} again 
- additional sources in individual archives

* Fri Jan 4 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-5jpp
- javadoc back to /usr/share/doc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- removed redundant jh.jar, jhbasic.jar and jsearch.jar
- changed jhall.jar name to javasearch.jar
- changed jhtools.jar name to javasearch-tools.jar
- javasearch-tools.jar in javasearch-tools package
- used jpackage scripts
- removed windows files from demo
- standardised summary

* Fri Dec 7 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-4jpp
- javadoc into javadoc package

* Sun Oct 28 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-3jpp
- first unified release
- fixed perm problems

* Tue Oct 09 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-2mdk
- split demo package 
- demo files in %%{_datadir}/%%{name}
- s/jPackage/JPackage/
- spec cleanup

* Tue Jul 24 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.2-1mdk
- used original archives
- s/Copyright/License
- truncated despcription length to 72 columns
- versionning
- no more source package
- merged demo and manual packages

* Sat Mar 10 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.1.1-2mdk
- vendor tag
- packager tag
- sources in /usr/src/java

* Sun Feb 04 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 1.1.1-1mdk
- first Mandrake release

