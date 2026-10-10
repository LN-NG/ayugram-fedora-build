#!/usr/bin/env bash
set -euo pipefail
dnf install -y https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-44.noarch.rpm
dnf install -y dnf5-plugins rpm-build redhat-rpm-config ccache mold time curl shadow-utils git
dnf builddep -y /work/ayugram-desktop.spec
# Make the exact installed toolchain/dependency versions available with the seed.
mkdir -p /work/output
rpm -qa --qf '%{NAME} %{VERSION}-%{RELEASE} %{ARCH}\n' | sort > /work/output/toolchain.txt
useradd --create-home builder
chown -R builder:builder /work
exec runuser -u builder -- bash scripts/build.sh
