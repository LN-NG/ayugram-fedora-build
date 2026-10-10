%global _lto_cflags %{nil}
%global debug_package %{nil}
%global _smp_build_ncpus 2
# AyuGram Desktop's constants...
%global appname AyuGramDesktop

# Reducing debuginfo verbosity to avoid possible building crash on low-memory devices
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')

Name: ayugram-desktop
Version: 7.2.9
Release: 1.local%{?dist}

# Application and 3rd-party modules licensing:
# * AyuGram Desktop - GPL-3.0-or-later with OpenSSL exception -- main tarball;
# * tg_owt - BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain -- static dependency;
# * rlottie - LGPL-2.1-or-later AND FTL AND BSD-3-Clause -- static dependency;
# * cld3  - Apache-2.0 -- static dependency;
# * open-sans-fonts  - Apache-2.0 -- bundled font;
# * vazirmatn-fonts - OFL-1.1 -- bundled font.
# * lib_icu - Unicode-3.0 -- static dependency;
# * kcoreaddons - MPL-1.1 AND CC0-1.0 AND Artistic-1.0-Perl AND QPL-1.0 -- static dependency;
# * expected-lite - BSL-1.0 -- only header lib
# * minizip - Zlib -- static dependency;
License: GPL-3.0-or-later AND BSD-3-Clause AND BSD-2-Clause AND Apache-2.0 AND MIT AND LicenseRef-Fedora-Public-Domain AND LGPL-2.1-or-later AND FTL AND MPL-1.1 AND OFL-1.1 AND Unicode-3.0 AND BSL-1.0 AND CC0-1.0 AND Zlib AND Artistic-1.0-Perl AND QPL-1.0
URL: https://github.com/AyuGram/%{appname}
Summary: Desktop Telegram client with good customization and Ghost mode

# Upstream doesn't provide full source tarball. AyuGram splited to many git submodules.
# Also it bundles some 3rd-party libraries. In most generating script does
# git clone --recursive --branch "v${VERSION}" ...

# create-ayugram-tarball-full.sh 6.3.10.
Source0: AyuGramDesktop-%{version}-full.tar.gz
Source1: tlottie-31f1b542f88e7b4be9a01e749920d857535fc715.tar.gz
Source2: tlottie-upstream.patch

# Fix searching protobuf cmake module
# Fix compilation with gcc16
# Fix saving hide premium statuses to config file
# AyuGram Desktop require more than 8 GB of RAM on linking stage.
# Disabling all low-memory architectures.
ExclusiveArch: x86_64 aarch64

BuildRequires: cmake(Microsoft.GSL)
BuildRequires: cmake(OpenAL)
BuildRequires: cmake(Qt6Concurrent)
BuildRequires: cmake(Qt6Core)
BuildRequires: cmake(Qt6Core5Compat)
BuildRequires: cmake(Qt6DBus)
BuildRequires: cmake(Qt6Gui)
BuildRequires: cmake(Qt6GuiPrivate)
BuildRequires: cmake(Qt6Network)
BuildRequires: cmake(Qt6OpenGL)
BuildRequires: cmake(Qt6OpenGLWidgets)
BuildRequires: cmake(Qt6Svg)
BuildRequires: cmake(Qt6WaylandClient)
BuildRequires: cmake(Qt6Widgets)
BuildRequires: cmake(Qt6WidgetsPrivate)
BuildRequires: cmake(fmt)
BuildRequires: cmake(range-v3)
BuildRequires: cmake(tg_owt)
BuildRequires: cmake(tl-expected)
BuildRequires: cmake(ada)

BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(gio-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(glibmm-2.68) >= 2.76.0
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(hunspell)
BuildRequires: pkgconfig(jemalloc)
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libcrypto)
BuildRequires: pkgconfig(liblz4)
BuildRequires: pkgconfig(liblzma)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libswresample)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libxxhash)
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
BuildRequires: pkgconfig(rnnoise)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(webkitgtk-6.0)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xcb-keysyms)
BuildRequires: pkgconfig(xcb-record)
BuildRequires: pkgconfig(xcb-screensaver)

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: ffmpeg-devel
BuildRequires: rust
BuildRequires: cargo
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: libappstream-glib
BuildRequires: libatomic
BuildRequires: libdispatch-devel
BuildRequires: libqrcodegencpp-devel
BuildRequires: libstdc++-devel
BuildRequires: minizip-compat-devel
BuildRequires: ninja-build
BuildRequires: python3
BuildRequires: patch
BuildRequires: tar
BuildRequires: pkgconfig(openh264)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(tde2e)

Requires: hicolor-icon-theme
Requires: qt6-qtimageformats%{?_isa}
Requires: webkitgtk6.0%{?_isa}

# Short alias for the main package...
Provides: ayugram = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: ayugram%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

Provides: bundled(tlottie) = 0.1.0~git31f1b542f8

%description
AyuGram Desktop is a Telegram desktop client with customization features.
This package is built from the pinned upstream 7.2.9 source release.

%prep
# Unpacking AyuGram Desktop source archive...
%autosetup -n %{appname}-%{version}-full -p1
mkdir tlottie-src
tar -xf %{SOURCE1} -C tlottie-src --strip-components=1
patch -p1 -d tlottie-src < %{SOURCE2}

# Unbundling libraries... except minizip
rm -rf Telegram/ThirdParty/{GSL,QR,dispatch,expected,fcitx5-qt,hime,hunspell,kimageformats,lz4,nimf,range-v3,xxHash}

%build
export CARGO_HOME=/work/.cache/cargo
export CARGO_BUILD_JOBS=2
cargo rustc --manifest-path tlottie-src/Cargo.toml --lib --release --locked \
    --features c-api --crate-type staticlib --target x86_64-unknown-linux-gnu \
    -- --print native-static-libs
mkdir -p tlottie-prefix/lib tlottie-prefix/include/tlottie
cp tlottie-src/target/x86_64-unknown-linux-gnu/release/libtlottie.a tlottie-prefix/lib/
cp tlottie-src/include/tlottie.h tlottie-prefix/include/tlottie/
# Building AyuGram Desktop using cmake...
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="$PWD/tlottie-prefix" \
    -DCMAKE_C_COMPILER_LAUNCHER=ccache \
    -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
    -DCMAKE_EXE_LINKER_FLAGS="-fuse-ld=mold" \
    -DCMAKE_SHARED_LINKER_FLAGS="-fuse-ld=mold" \
    -DCMAKE_AR=%{_bindir}/gcc-ar \
    -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
    -DCMAKE_NM=%{_bindir}/gcc-nm \
    -DTDESKTOP_API_ID=2040 \
    -DTDESKTOP_API_HASH=b18441a1ff607e10a989891a5462e627 \
    -DDESKTOP_APP_USE_PACKAGED:BOOL=ON \
    -DDESKTOP_APP_USE_PACKAGED_FONTS:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_WAYLAND_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_X11_INTEGRATION:BOOL=OFF \
    -DDESKTOP_APP_DISABLE_CRASH_REPORTS:BOOL=ON \
    -DDESKTOP_APP_DISABLE_QT_PLUGINS:BOOL=ON
%cmake_build

%install
%cmake_install

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/com.ayugram.desktop.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/com.ayugram.desktop.desktop

%files
%doc README.md changelog.txt
%license LICENSE LEGAL tlottie-src/LICENSE
%{_bindir}/AyuGram
%{_datadir}/applications/com.ayugram.desktop.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
%{_datadir}/dbus-1/services/com.ayugram.desktop.service
%{_metainfodir}/com.ayugram.desktop.metainfo.xml


%changelog
* Sun Oct 11 2026 Cloud Build <build@users.noreply.github.com> - 7.2.9-1.local
- Build pinned upstream release with its pinned tlottie dependency
