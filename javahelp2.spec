Summary:	JavaHelp
Name:		javahelp2
Version:	2.0.05
Release:	8
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
#BuildRequires:	ant-nodeps

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

