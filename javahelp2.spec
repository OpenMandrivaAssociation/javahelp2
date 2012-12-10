Summary:	JavaHelp
Name:		javahelp2
Version:	2.0.05
Release:	%mkrel 7
Epoch:		0
Group:		Development/Java
License:	GPLv2 with exceptions
Url:		https://javahelp.dev.java.net/
Source0:	https://javahelp.dev.java.net/files/documents/5985/59373/%{name}-src-%{version}.zip
Source1:	%{name}-jhindexer.sh
Source2:	%{name}-jhsearch.sh
BuildArch:	noarch
Requires:	jpackage-utils >= 0:1.5.32
BuildRequires:	java-rpmbuild >= 0:1.5.32
BuildRequires:	jsp >= 0:2.0
BuildRequires:	xml-commons-jaxp-1.3-apis
BuildRequires:	tomcat5-servlet-2.4-api
BuildRequires:	xerces-j2
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JavaHelp software is a full-featured, platform-independent, extensible
help system that enables developers and authors to incorporate online
help in applets, components, applications, operating systems, and
devices. Authors can also use the JavaHelp software to deliver online
documentation for the Web and corporate Intranet.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Development/Java

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}-%{version}
# fix files perms
chmod -R go=u-w *
# remove windows files
for file in `find . -type f -name .bat`; do rm -f $file; done

#
# This class provides native browser integration and would require
# JDIC project to be present. Currently there is no such jpackage.org
# package, so deleting the class. When JDIC package is created,
# add BuildProvides and remove the "rm" call.
#
rm jhMaster/JavaHelp/src/new/javax/help/plaf/basic/BasicNativeContentViewerUI.java

mkdir javahelp_nbproject/lib
ln -s %{_javadir}/jsp.jar javahelp_nbproject/lib/jsp-api.jar
ln -s %{_javadir}/servletapi5.jar javahelp_nbproject/lib/servlet-api.jar

%build
export CLASSPATH=$(build-classpath ant/ant-nodeps)
%ant -f javahelp_nbproject/build.xml -Djdic-jar-present=true -Djdic-zip-present=true -Dservlet-jar-present=true -Dtomcat-zip-present=true release javadoc

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_javadir}
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_datadir}/%{name}
install -m 755 %{SOURCE1} %{buildroot}%{_bindir}/jh2indexer
install -m 755 %{SOURCE2} %{buildroot}%{_bindir}/jh2search

install -m 644 javahelp_nbproject/dist/lib/jhall.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar
#cp -pr jhMaster/JavaHelp/doc/public-spec/dtd %{buildroot}%{_datadir}/%{name}
#cp -pr jhMaster/JavaHelp/demos %{buildroot}%{_datadir}/%{name}
cp -pr javahelp_nbproject/dist/lib/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
# create unversioned symlinks
(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} ${jar/-%{version}/}; done)

%clean
rm -rf %{buildroot}

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/*
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%dir %{_datadir}/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.0.05-7mdv2011.0
+ Revision: 619783
- the mass rebuild of 2010.0 packages

* Sun Sep 27 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0:2.0.05-6mdv2010.0
+ Revision: 449816
- add missing buildrequires on tomcat5-servlet-2.4-api, xml-commons-jaxp-1.3-apis and xerces-j2
- spec file clean
- rebuild for new era

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0:2.0.05-4mdv2009.0
+ Revision: 247393
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:2.0.05-2mdv2008.1
+ Revision: 120928
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Nov 21 2007 Nicolas Vigier <nvigier@mandriva.com> 0:2.0.05-1mdv2008.1
+ Revision: 111054
- build with java >= 1.6.0
- fix ant error (fix by Alexander Kurtakov)
- fix release, license, group tags
- add buildrequires
- import javahelp2


* Thu Nov 14 2007 Jaroslav Tulach <jtulach@netbeans.org> 0:2.0.05-1mdv
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
