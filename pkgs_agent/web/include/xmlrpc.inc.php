<?
/*
*
* (c) 2016-2020 siveo, http://www.siveo.net
*
* This file is part of Pulse 2, http://www.siveo.net
*
* MMC is free software; you can redistribute it and/or modify
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
* Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
* file : include/xmlrpc.inc.php
*/

require("callxmlrpc-ssl.php");

function test($param=[]){
	return xmlCall("add",$param );
}

function pkgs_time(){
	return xmlCall("pkgsf.time",array());
}
function pkgs_list_all(){
	return xmlCall("pkgsf.list_all",array());
}

function pkgs_xmpp_test(){
	return xmlCall("xmppf.test",array());
}

function pkgs_pkgs_test(){
	return xmlCall("pkgsf.test",array());
}

function pkgs_get_shares(){
	return xmlCall("pkgsf.get_shares",array());
}
?>
