#!/usr/bin/env bash
set -euo pipefail
cd /work
mkdir -p output .cache/ccache rpmbuild/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}
export CCACHE_DIR=/work/.cache/ccache CCACHE_BASEDIR=/work CCACHE_MAXSIZE=3G
export CCACHE_COMPILERCHECK=content
curl --fail --location --retry 3 \
 https://github.com/AyuGram/AyuGramDesktop/releases/download/v7.2.9/AyuGramDesktop-7.2.9-full.tar.gz \
 -o rpmbuild/SOURCES/AyuGramDesktop-7.2.9-full.tar.gz
cp ayugram-desktop.spec rpmbuild/SPECS/
/usr/bin/time -v rpmbuild -bb --noclean --define '_topdir /work/rpmbuild' \
 rpmbuild/SPECS/ayugram-desktop.spec 2>&1 | tee output/build.log
ccache --show-stats | tee output/ccache.log
cp rpmbuild/RPMS/x86_64/*.rpm output/
rpm -qp --qf '%{NAME} %{VERSION}-%{RELEASE} %{ARCH}\n' output/*.rpm | tee output/package.log
# Export the real build tree and cache, not just the installed executable.
tar -czf output/ayugram-7.2.9-fedora44-build-base.tar.gz \
 .cache/ccache rpmbuild/BUILD rpmbuild/SOURCES rpmbuild/SPECS
