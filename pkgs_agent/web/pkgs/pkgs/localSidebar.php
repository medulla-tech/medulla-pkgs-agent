<?php
/*
 * (c) 2008 Mandriva, http://www.mandriva.com
 *
 * $Id$
 *
 * This file is part of Pulse 2, http://pulse2.mandriva.org
 *
 * Pulse 2 is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * MMC is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with MMC; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston,
 * MA 02110-1301, USA
 */

$sidemenu= new SideMenu();
$sidemenu->setClass("pkgs");
$sidemenu->addSideMenuItem(new SideMenuItem(_T("Packages list", 'pkgs'), "pkgs", "pkgs", "index"));
$sidemenu->addSideMenuItem(new SideMenuItem(_T("Add a package", 'pkgs'), "pkgs", "pkgs", "add"));
$sidemenu->addSideMenuItem(new SideMenuItem(_T("Pending packages list", 'pkgs'), "pkgs", "pkgs", "pending"));
$sidemenu->addSideMenuItem(new SideMenuItem(_T("Rules list", 'pkgs'), "pkgs", "pkgs", "rulesList"));
$sidemenu->addSideMenuItem(new SideMenuItem(_T("Add a rule", 'pkgs'), "pkgs", "pkgs", "addRule"));

?>
