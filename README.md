# AyuGram 7.2.9 for Fedora 44 x86_64

Generic cloud RPM build based on the RPM Fusion 6.7.8 packaging recipe.
Source: upstream official full release archive, tag v7.2.9, commit
d4b7546e77f93ac4c9bb53a3fcf7e9ffbbecf1b5.
The obsolete protobuf/GCC16/settings patches are not needed by this release.
System dependencies come from Fedora and RPM Fusion Free repositories.
The API application constants used by the spec are the public constants from
upstream's Linux build instructions; no user credentials or profiles are used.

Build: GCC, mold, Release, no LTO, two compile jobs, 3 GB ccache.
The RPM keeps the standard AyuGram package name and executable path for upgrades.
No package is automatically installed by GitHub Actions.

The build-base artifact includes ccache, source archive, RPM spec and the actual
rpmbuild BUILD tree. Extract at a workspace mounted as `/work` in the same Fedora
container with matching dependencies. An arbitrary relocation of a configured
CMake build tree is not supported. Toolchain versions are in toolchain.txt.
For a clean rebuild with cache, use scripts/container.sh. For a direct incremental
build, run cmake --build against the configured build directory inside
rpmbuild/BUILD; the directory path is printed in the build log. Ccache saves time;
remaining compilation and linking still need memory.

The tlottie static library is built from the commit and patch-set revisions pinned
by the upstream 7.2.9 Dockerfile: 31f1b542f88e7b4be9a01e749920d857535fc715
and desktop-app/patches 519aaa084608fa6f9a2bfbd1959d133c44d94227.
Its MIT license is included in the RPM; Cargo downloads and compiled tlottie
artifacts are part of the cache/build-base export. No system tlottie is replaced.
