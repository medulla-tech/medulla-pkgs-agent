%define tarname		pulse-pkgs-agent
%define git                    SHA
%define use_git         1
%define branch integration
%define filetree_version 0.2

Summary:	Pulse Pkgs agent
Name:		pulse-pkgs-agent
Version:	0.0
%if ! %use_git
Release:        1%{?dist}
%else
Release:        0.%git.1%{?dist}
%endif

Source0:        %name-%version.tar.gz
License:	MIT

Group:		Development/Python
Url:		http://www.siveo.net

Requires:   php-xmlrpc
Requires:   python-twisted-web
Requires:   python-twisted-core

%description
Pulse XMPP Agent

%files 
%_sbindir/pulse_agent_xmlrpc_pkgs.py
%_datadir/pkgs/
%{python2_sitelib}/pulse_pkgs_agent

#--------------------------------------------------------------------

%prep
%setup -q

# Remove bundled egg-info

%build
# Nothing to do

%install
mkdir -p %buildroot%_sbindir/
cp pkgs_agent/bin/pulse_agent_xmlrpc_pkgs.py %buildroot%_sbindir/

mkdir -p %buildroot%{python2_sitelib}/pulse_pkgs_agent
cp pkgs_agent/__init__.py %buildroot%{python2_sitelib}/pulse_pkgs_agent
cp -fr cp pkgs_agent/lib %buildroot%{python2_sitelib}/pulse_pkgs_agent

mkdir -p %buildroot%_datadir/pkgs/
cp -fr ./pkgs_agent/web/* %buildroot%_datadir/pkgs/
