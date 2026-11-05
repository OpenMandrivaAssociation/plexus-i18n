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
# Sisu loads @Named classes from this index. The indexer plugin is not packaged.
python - <<'PY'
import re
from pathlib import Path
root = Path("src/main/java")
names = []
for path in sorted(root.rglob("*.java")):
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"\b(?:class|interface|enum)\s+([A-Za-z0-9_]+)", text)
    if not match:
        continue
    if "@Named" not in text[:match.start()]:
        continue
    pkg = re.search(r"(?m)^package\s+([A-Za-z0-9_.]+)\s*;", text)
    if not pkg:
        continue
    names.append(pkg.group(1) + "." + match.group(1))
if names:
    dest = Path("src/main/resources/META-INF/sisu")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "javax.inject.Named").write_text("\n".join(names) + "\n", encoding="utf-8")
PY

%files -f .mfiles
%doc README.md
