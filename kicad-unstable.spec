#
# spec file for package kicad-unstable
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           kicad-unstable
%define bzr_date 20150123
%define human_date 2015.01.23
%define bzr_rev 5386
Version:        %{bzr_date}_R%{bzr_rev}
Release:        1.1
Summary:        EDA software suite for the creation of schematics and PCB (development version)
License:        GPL-2.0+
Group:          Productivity/Scientific/Electronics
Url:            https://kicad-pcb.org
# https://launchpad.net/kicad/product
Source:         http://bazaar.launchpad.net/~kicad-product-committers/kicad/product/tarball/%{bzr_rev}#/kicad-%{version}.tar.gz
Source2:        boost_1_54_0.tar.bz2
%if 0%{?suse_version} > 1320
BuildRequires:  boost-devel >= 1.56
%endif
BuildRequires:  bzr
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkg-config
BuildRequires:  update-desktop-files
BuildRequires:  wxWidgets-devel >= 3.0
BuildRequires:  python-wxWidgets-devel >= 3.0
BuildRequires:  python-devel
BuildRequires:  swig
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glew)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(zlib)
# fix directory owner
BuildRequires:  hicolor-icon-theme
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       python-wxWidgets >= 3.0
Requires:       %{name}-library
Recommends:     %{name}-doc
Conflicts:      kicad
Conflicts:      kicad-gost

%description
Kicad is an open source (GPL) software for the creation of electronic schematic
diagrams and printed circuit with up to 32 copper layers and additional techinical layers.

KiCad includes a project manager and four main independent software tools:
- Eeschema: schematic editor.
- Pcbnew: printed circuit board editor.
- Gerbview: GERBER file viewer (photoplotter documents).
- Cvpcb: footprint selector for components association.

%prep
%setup -q -c kicad-%{version}
mv ~kicad-product-committers/kicad/product/* .
rm -r ~kicad-product-committers

# fix plugin directory
sed -i 's|KICAD_PLUGINS lib/kicad/plugins|KICAD_PLUGINS %{_lib}/kicad/plugins|' CMakeLists.txt
# fix documentation directory
# sed -i 's|KICAD_DOCS share/doc/kicad|KICAD_DOCS share/doc/packages/kicad|' CMakeLists.txt

# Set version
sed -i 's/^#   define KICAD_BUILD_VERSION.*/#   define KICAD_BUILD_VERSION "(%{human_date} BZR%{bzr_rev})"/' common/build_version.cpp

# boost
%if 0%{?suse_version} <= 1320
mkdir .downloads-by-cmake
cp %{SOURCE2} .downloads-by-cmake
%endif

%build
bzr whoami "obs <obs@localhost>"
%cmake \
    -DwxWidgets_USE_STATIC=OFF \
    -DwxWidgets_USE_UNICODE=ON \
    \
%if 0%{?suse_version} > 1320
    -DKICAD_SKIP_BOOST=ON \
%else
    -DKICAD_SKIP_BOOST=OFF \
%endif
    -DBUILD_GITHUB_PLUGIN=ON \
    -DKICAD_SCRIPTING=ON \
    -DKICAD_SCRIPTING_MODULES=ON \
    -DKICAD_SCRIPTING_WXPYTHON=ON

make %{?_smp_mflags}

%install
%cmake_install

%suse_update_desktop_file -r bitmap2component "Education;Engineering"
%suse_update_desktop_file -r cvpcb "Education;Engineering"
%suse_update_desktop_file -r eeschema "Education;Engineering"
%suse_update_desktop_file -r gerbview "Education;Engineering"
%suse_update_desktop_file -r kicad "Education;Engineering"
%suse_update_desktop_file -r pcbcalculator "Education;Engineering"
%suse_update_desktop_file -r pcbnew "Education;Engineering"
%fdupes -s %{buildroot}%{_datadir}/kicad/
%fdupes -s %{buildroot}%{_datadir}/icons/hicolor/

cat > %{name}.sh << 'EOF'
KIGITHUB="https://github.com/KiCad"
export KIGITHUB

EOF
install -Dm 644 %{name}.sh %{buildroot}%{_sysconfdir}/profile.d/%{name}.sh

%files
%defattr(-,root,root)
%doc COPYRIGHT.txt CHANGELOG.txt
%{_bindir}/*
%{_libdir}/kicad/
%{_datadir}/kicad/
%{_datadir}/doc/kicad/
%{_libdir}/kicad/plugins/netlist_form_pads-pcb.xsl
%dir %{_libdir}/kicad/
%dir %{_libdir}/kicad/plugins/
%{python_sitelib}/*
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/kicad.xml
%{_datadir}/mimelnk/application/x-kicad-*.desktop
%dir %{_datadir}/mimelnk/
%dir %{_datadir}/mimelnk/application/
%{_datadir}/icons/hicolor/*/mimetypes/application-x-*
%{_datadir}/icons/hicolor/*/apps/*.*
%config %{_sysconfdir}/profile.d/%{name}.sh

%changelog
* Thu Dec  4 2014 dmitry_r@opensuse.org
- Use system boost libraries for openSUSE > 13.2
* Fri Sep 12 2014 dmitry_r@opensuse.org
- Update to current sources
- Use %%cmake macro
- Enable python scripting
* Tue Feb 25 2014 dmitry_r@opensuse.org
- Update to version 20140120
  * Bug fixes
* Wed Aug  7 2013 dmitry_r@opensuse.org
- Removed templates to avoid conflict with kicad-library package
  * kikad-no-templates-install.patch
- Removed obsolete kicad-2012.01.19-build-with-old-wxwidgets.patch
* Wed Jul 17 2013 dmitry_r@opensuse.org
- Update to version 20130707
  * no changelog available
  * removed obsolete kicad-2012.01.19-gcc-4.7.patch
* Thu Jun 27 2013 dmitry_r@opensuse.org
- Change package license to GPL-2.0+ [bnc#796377]
* Mon Apr  8 2013 werner.ho@gmx.de
- new version 20130330
- removed version patch
* Wed Jan 23 2013 dmitry_r@opensuse.org
- Update to version 20120521
  * various bugfixes, no detailed changelog available
- Change package license to GPL-3.0 [bnc#796377]
- Build with Unicode support
- Add switcher for build with GOST support
- Fix displayed version
  * kicad-version.patch
* Tue Aug 28 2012 scorot@free.fr
- fix build with old wxWindow on SLE 11
* Wed Jun 27 2012 scorot@free.fr
- add patch from debian to fix build with gcc-4.7
* Sat Feb 11 2012 werner.ho@gmx.de
- new version 2012-01-19
* Tue Jan 17 2012 werner.ho@gmx.de
- new version 2011-12-28
* Sun Aug 21 2011 werner.ho@gmx.de
- new version 2011-07-08
* Fri May 27 2011 werner.ho@gmx.de
- new version 2011-04-29
* Mon Mar 28 2011 stefan.bruens@rwth-aachen.de
- explicit request for DOUBLEBUFFER and DEPTH>=16
  fixes SwapBuffer() crash on Intel and Radeon GPUs
* Tue Mar 15 2011 werner.ho@gmx.de
- build fix for openSUSE 11.4
* Sun Nov  7 2010 werner.ho@gmx.de
- added l10n files and patch fixes bug [#650383]
* Fri Jul 23 2010 mhopf@novell.com
- Update to 2010-05-05-stable
* Mon Apr 12 2010 mhopf@novell.com
- Make it build with older wxGTK (wxAuiToolBar)
* Mon Apr 12 2010 mhopf@novell.com
- Update to 2010-04-06-SVN2508
  Currently only builds on 11.2
* Wed Jun 17 2009 Werner Hoch <werner.ho@gmx.de> - 2009.02.06
- new version 2009.02.06
* Sat Dec 20 2008 Werner Hoch <werner.ho@gmx.de> - 2008.08.25
- build fix for openSUSE 11.1
- added freeglut-devel and update_desktop_file
- directory fixes
* Sat Oct  4 2008 Werner Hoch <werner.ho@gmx.de> - 2008.08.25
- new version 2008.08.25
* Tue Mar 25 2008 Werner Hoch <werner.ho@gmx.de>
- new version 2008.03.20
* Tue Dec 25 2007 Werner Hoch <werner.ho@gmx.de>
- adapted spec file from kicad-2007.07.09-2.fc8.src.rpm
- removed french project descriptions
- use cmake build process
- new version 2007.11.29
  Mon Oct 15 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.07.09-2
- Update desktop file
  Thu Oct 04 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.07.09-1
- New upstream version
- Merge previous patches
- Remove X-Fedora, Electronics and Engineering categories
- Update desktop file
  Mon Aug 27 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-4
- License tag clarification
  Thu Aug 23 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-3
- Rebuild
  Wed Feb 14 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-2
- Fix desktop entry. Fix #228598
  Thu Feb  8 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2007.01.15-1
- New upstream version
  Thu Feb  8 2007 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.08.28-4
- Add patch to build with RPM_OPT_FLAGS and remove -s from LDFLAGS
  Contribution of Ville Skyttä <ville[DOT]skytta[AT]iki[DOT]fi>
  Fix #227757
- Fix typo in french summary
* Thu Dec 28 2006 Jason L Tibbitts III <tibbs@math.uh.edu> 2006.08.28-3
- Rebuild with wxGTK 2.8.
* Thu Oct  5 2006 Christian Iseli <Christian.Iseli@licr.org> 2006.08.28-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21
  Fri Sep 22 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.08.28-1
- New upstream version
- Use macro style instead of variable style
- Install missing modules. Fix #206602
  Fri Sep  1 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-6
- FE6 rebuild
  Mon Jul 10 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-5
- Removing backup files is no more needed.
  Mon Jul 10 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-4
- Remove BR libGLU-devel that is no more needed (bug #197501 is closed)
- Fix files permissions.
  Mon Jul  3 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-3
- s/mesa-libGLU-devel/libGLU-devel/
  Mon Jul  3 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-2
- BR mesa-libGLU-devel
  Wed Jun 28 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.06.26-1
- New upstream version
  Tue Jun 13 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006.04.24-5
- Change name
- Use %%%%{_docdir} instead of %%%%{_datadir}/doc
- Use %%%%find_lang
- Update desktop database
- Convert MSDOS EOL to Unix EOL
- Remove BR utrac
  Mon Jun 12 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-4
- Patch to suppress extra qualification compile time error on FC5
- BR utrac to convert MSDOS files before applying patch
  This will be remove for the next upstream version.
  Tue May 23 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-3
- Install help in /usr/share/doc/kicad/ as the path is hardcoded
  in gestfich.cpp
- Add desktop file
  Mon May 22 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-2
- Add a second tarball that contains many things that are not included in
  the upstream source tarball such components and footprints librairies,
  help, localisation, etc.
  Sun May 21 2006 Alain Portal <aportal[AT]univ-montp2[DOT]fr> 2006-04-24-0-1
- Initial Fedora RPM
