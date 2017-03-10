%{?_javapackages_macros:%_javapackages_macros}

Summary:	A Java Implementation of a Mork Parse
Name:		jmork
Version:	1.0.6
Release:	1
License:	Eclipse Public License
Group:		Development/Java
URL:		https://github.com/ibauersachs/jmork
Source0:	https://github.com/ibauersachs/%{name}/archive/%{name}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)

%description
Mork is a text "database" format used by Mozilla applications like Firefox
and Thunderbird to store some data. Mainly the URL History of Firefox and
the address book of Thunderbird is stored in the (rather weird) Mork format.

This is a Java Implementation which can be used to parse .mab Files on a raw
level.

The current version of the data format is v1.4.

%files -f .mfiles

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{name}-%{version}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive" "
<index>true</index>"
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]" "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>

		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Set the right name to fit the packaging guidelines
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

