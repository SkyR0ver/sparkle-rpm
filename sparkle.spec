%global _pkgdir /opt/%{name}
%global _icondir %{_datadir}/icons/hicolor/512x512/apps

# Debug information for Electron apps is not available because prebuilt Electron
# binaries is used, whose debug info has been stripped already.
%global debug_package %{nil}

Name: sparkle
Version: 1.26.6
Release: %autorelease
Summary: Another Mihimo GUI

License: GPL-3.0-only
URL: https://github.com/xishang0128/sparkle

Source0: %{url}/archive/refs/tags/%{version}.tar.gz 
Source1: %{name}.desktop

BuildRequires: gcc-c++
BuildRequires: pnpm
BuildRequires: libxcrypt-compat

Requires(post): %{_bindir}/update-alternatives
Requires(preun): %{_bindir}/update-alternatives

%description
%{summary}, forked from Mihomo Party by xishang0128.


%prep
%autosetup


%build
pnpm install
pnpm build:linux -c.productName sparkle --dir


%install
# Clean prebuilt node binaries depending on other platforms or musl
UNPACKED_MODULE_DIR=dist/linux*-unpacked/resources/app.asar.unpacked/node_modules
rm -r ${UNPACKED_MODULE_DIR}/@tailwindcss/oxide-linux-*-musl
rm -r ${UNPACKED_MODULE_DIR}/lightningcss-linux-*-musl
%ifarch x86_64
ARCH=x64
%elifarch aarch64
ARCH=arm64
%endif
find ${UNPACKED_MODULE_DIR}/koffi/build/koffi -mindepth 1 -maxdepth 1 -type d ! -name "linux_${ARCH}" -exec rm -r {} +

# Modify file modes
chmod 4755 dist/linux*-unpacked/chrome-sandbox
chmod +sx dist/linux*-unpacked/resources/sidecar/mihomo
chmod +sx dist/linux*-unpacked/resources/sidecar/mihomo-alpha
chmod -R go-w dist/linux*-unpacked/resources/files/sub-store-frontend

# Install everything to /opt/sparkle
mkdir -p %{buildroot}%{_pkgdir}
cp -rp dist/linux*-unpacked/* %{buildroot}%{_pkgdir}

# Install icon
mkdir -p %{buildroot}%{_icondir}
install -Dp -m0644 build/icon.png %{buildroot}%{_icondir}/%{name}.png

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_datadir}/applications/%{name}.desktop


%post
# Create symlink
mkdir -p %{_bindir}
update-alternatives --install %{_bindir}/sparkle sparkle %{_pkgdir}/sparkle 100


%preun
if [ $1 -eq 0 ]; then
    update-alternatives --remove sparkle %{_pkgdir}/sparkle
fi


%files
%license LICENSE
%{_pkgdir}
%ghost %{_bindir}/sparkle
%{_datadir}/applications/%{name}.desktop
%{_icondir}/%{name}.png


%changelog
%autochangelog
