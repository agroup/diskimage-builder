Name:		diskimage-builder
Summary:	Image building tools for OpenStack
Version:	0.1.34
Release:	100.patches%{?dist}
License:	ASL 2.0
Group:		System Environment/Base
URL:		https://launchpad.net/diskimage-builder
Source0:	http://tarballs.openstack.org/diskimage-builder/%{name}-%{version}.tar.gz

Patch0001: 0001-svc-map-requires-PyYAML.patch
Patch0002: 0002-Enable-dracut-deploy-ramdisks.patch
Patch0003: 0003-Move-busybox-binary-dep-to-ramdisk-element.patch
Patch0004: 0004-Unset-trap-before-dracut-ramdisk-build-script-exits.patch
Patch0005: 0005-Install-lsb_release-from-package.patch
Patch0006: 0006-Simplify-Dracut-cmdline-script.patch
Patch0007: 0007-Use-binary-deps.d-for-dracut-ramdisks.patch
Patch0008: 0008-Remove-duplicate-binary-deps-from-dracut-ramdisk.patch
Patch0009: 0009-Enable-RHEL-Registration.patch
Patch0010: 0010-Update-RHEL-Registration.patch
Patch0011: 0011-Allow-source-repositories-to-be-disabled-completely.patch
Patch0012: 0012-Allow-injecting-arbitrary-yum-repo-configuration.patch
Patch0013: 0013-Convert-deploy-ramdisk-to-targetcli.patch
Patch0014: 0014-Add-Activation-Key-Support-For-Customer-Portal.patch
Patch0015: 0015-Fix-repo-enablement-for-RHEL-during-registration.patch
Patch0016: 0016-Deprecates-username-and-password-from-boot-time-regi.patch
Patch0017: 0017-Allow-for-disabling-rhel-registration.patch
Patch0018: 0018-Don-t-trace-RHEL-registration-scripts.patch
Patch0019: 0019-Ironic-Local-boot.patch

BuildArch: noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-d2to1
BuildRequires: python-pbr

Requires: kpartx
Requires: qemu-img
Requires: curl
Requires: python-argparse
Requires: python-babel
Requires: tar
Requires: dib-utils

%prep
%setup -q -n %{name}-%{version}

%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root=%{buildroot}

mkdir -p %{buildroot}%{_datadir}/%{name}/lib
mkdir -p %{buildroot}%{_datadir}/%{name}/elements

install -p -D -m 644 lib/* %{buildroot}%{_datadir}/%{name}/lib
cp -vr elements/ %{buildroot}%{_datadir}/%{name}

# explicitly remove config-applier since it does a pip install
rm -rf %{buildroot}%{_datadir}/%{name}/elements/config-applier

# This file is being split out of diskimage-builder, so remove it to
# avoid conflicts with the new package.
rm -f %{buildroot}%{_bindir}/dib-run-parts

# Patch 0002-Move-install-bin-from-rpm-distro-to-yum.patch
# creates a new file, but the perms are not set correctly when patch runs
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/yum/pre-install.d/01-yum-install-bin
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/extra-data.d/scripts/module/deploy-cmdline.sh
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/extra-data.d/scripts/module/module-setup.sh
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/install.d/20-install-dracut-deps
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/post-install.d/99-build-dracut-ramdisk
# Patch 0007-Use-binary-deps.d-for-dracut-ramdisks.patch has the same issue
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/ramdisk-base/post-install.d/01-ensure-binaries
# As does patch 0009-Enable-RHEL-Registration.patch
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/rhel-common/finalise.d/99-unregister
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/rhel-common/os-refresh-config/pre-configure.d/06-rhel-registration
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/rhel-common/pre-install.d/00-rhel-registration
# For 0012-Allow-injecting-arbitrary-yum-repo-configuration.patch
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/yum/extra-data.d/99-yum-repo-conf
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/yum/cleanup.d/99-remove-yum-repo-conf
# For Patch0013: 0013-Convert-deploy-ramdisk-to-targetcli.patch
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/extra-data.d/scripts/targetcli-wrapper
chmod +x %{buildroot}/%{_datadir}/%{name}/elements/dracut-ramdisk/extra-data.d/scripts/module/python-deps

%description
Components of TripleO that are responsible for building disk images.

%files
%doc LICENSE
%doc docs/ci.md
%{_bindir}/*
%{python_sitelib}/diskimage_builder*
%{_datadir}/%{name}/lib
%{_datadir}/%{name}/elements

%changelog
* Tue Jan 20 2015 James Slagle <jslagle@redhat.com> 0.1.34-100.patches
- Update patch 0019-Ironic-Local-boot.patch

* Mon Jan 19 2015 James Slagle <jslagle@redhat.com> 0.1.34-99.patches

* Mon Jan 05 2015 James Slagle <jslagle@redhat.com> 0.1.34-19
- Don't trace RHEL registration scripts
- Allow for disabling rhel registration
- Deprecates username and password from boot time registration
- Fix repo enablement for RHEL during registration

* Tue Dec 09 2014 James Slagle <jslagle@redhat.com> 0.1.34-18
- Allow for disabling rhel registration

* Tue Dec 08 2014 James Slagle <jslagle@redhat.com> 0.1.34-17
- Make files created by patch 0012-Allow-injecting-arbitrary-yum-repo-configuration.patch +x

* Sun Dec 07 2014 James Slagle <jslagle@redhat.com> 0.1.34-16
- Make files created by patch 0013-Convert-deploy-ramdisk-to-targetcli.patch +x

* Sat Dec 06 2014 James Slagle <jslagle@redhat.com> 0.1.34-15
- Convert deploy ramdisk to targetcli

* Thu Dec 04 2014 James Slagle <jslagle@redhat.com> 0.1.34-14
- Allow injecting arbitrary yum repo configuration

* Fri Nov 21 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-13
- Allow source-repositories to be disabled completely

* Thu Nov 20 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-12
- Update RHEL Registration

* Tue Nov 18 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-11
- Enable RHEL Registration

* Fri Nov 14 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-10
- Remove duplicate binary-deps from dracut-ramdisk

* Fri Nov 14 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-9
- Fix perms on binary-deps patch

* Fri Nov 14 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-8
- Use binary-deps.d for dracut ramdisks

* Thu Nov 13 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-7
- Simplify Dracut cmdline script

* Tue Nov 11 2014 Ben Nemec <bnemec@redhat.com> 0.1.34-6
- Install lsb_release from package

* Thu Oct 23 2014 James Slagle <jslagle@redhat.com> 0.1.34-5
- Unset trap before dracut ramdisk build script exits

* Wed Oct 22 2014 James Slagle <jslagle@redhat.com> 0.1.34-4
- Move busybox binary-dep to ramdisk element

* Tue Oct 21 2014 James Slagle <jslagle@redhat.com> 0.1.34-3
- Remove requirement on busybox, we use dracut now.

* Mon Oct 20 2014 James Slagle <jslagle@redhat.com> 0.1.34-2
- Enable dracut deploy ramdisks

* Mon Oct 20 2014 James Slagle <jslagle@redhat.com> 0.1.34-1
- Update to upstream 0.1.34

* Fri Oct 17 2014 James Slagle <jslagle@redhat.com> 0.1.33-4
- svc-map requires PyYAML

* Fri Oct 17 2014 James Slagle <jslagle@redhat.com> 0.1.33-3
- Make sure file added by patch is +x

* Wed Oct 15 2014 James Slagle <jslagle@redhat.com> 0.1.33-2
- Move install bin from rpm-distro to yum
- Check for epel before installing it

* Wed Oct 15 2014 James Slagle <jslagle@redhat.com> 0.1.33-1
- Update to upstream 0.1.33

* Wed Oct 01 2014 James Slagle <jslagle@redhat.com> 0.1.32-1
- Update to upstream 0.1.32

* Mon Sep 29 2014 James Slagle <jslagle@redhat.com> 0.1.31-1
- Update to upstream 0.1.31

* Mon Sep 15 2014 James Slagle <jslagle@redhat.com> 0.1.30-1
- Update to upstream 0.1.30

* Thu Sep 11 2014 James Slagle <jslagle@redhat.com> - 0.1.15-4
- Switch to rdopkg

* Wed Jul 02 2014 James Slagle <jslagle@redhat.com> - 0.1.15-3
- Add patch Remove-fixfiles-from-rpm-distro-finalize.patch

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 30 2014 Ben Nemec <bnemec@redhat.com> - 0.1.15-1
- Update to 0.1.15
- Remove dib-run-parts from this package
- Add dependency on dib-utils (the new home of dib-run-parts)

* Wed Apr 16 2014 Ben Nemec <bnemec@redhat.com> - 0.1.13-1
- Update to 0.1.13
- Remove mariadb-rdo-package patch that merged upstream

* Wed Mar 26 2014 Jeff Peeler <jpeeler@redhat.com> 0.1.9-1
- rebase to 0.1.9

* Tue Feb 18 2014 Jeff Peeler <jpeeler@redhat.com> 0.1.5-3
- add tar requires (rhbz#1066680)

* Mon Jan 27 2014 Jeff Peeler <jpeeler@redhat.com> 0.1.5-2
- add new requires: python-argparse, python-babel

* Mon Jan 27 2014 Jeff Peeler <jpeeler@redhat.com> 0.1.5-1
- rebase to 0.1.5 + patch to fix RHEL 6.5 boot (rhbz#1057217)

* Wed Oct 9 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.5-1
- rebase to 0.0.5

* Mon Sep 16 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-7
- add patch to allow proper Fedora image creation when using vm element

* Fri Sep 13 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-6
- add patches to ccd7b86b606e678bf7281baff05c420b089c5d8f (fixes kpartx issue)

* Thu Sep 5 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-5
- rebase to a495079695e914fa7ec93292497bfc2471f41510
- Source moved from stackforge to openstack
- added curl requires
- switched to pbr
- remove all sudo related files as they are no longer used

* Tue Aug 13 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-4
- removed config-applier element

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-2
- rebased and dropped patches

* Mon Jul 29 2013 Jeff Peeler <jpeeler@redhat.com> 0.0.1-1
- initial package straight from github commit sha