<?php
/**
 * (c) 2004-2007 Linbox / Free&ALter Soft, http://linbox.com
 * (c) 2007-2009 Mandriva, http://www.mandriva.com
 *
 * $Id$
 *
 * This file is part of Mandriva Management Console (MMC).
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
 * along with MMC.  If not, see <http://www.gnu.org/licenses/>.
 */

function clean($val) { return urlencode(urldecode($val)); }

function to_s($obj) { return $obj->toS(); }
function to_rpc($obj) { return $obj->toRPC(); }
function to_xml($obj) { return $obj->toXML(); }

function getCookie($path) { // TODO generic!
    if (count($path) == 1) {
        return $_COOKIE[$path[0]];
    } elseif (count($path) == 2) {
        return $_COOKIE[$path[0]][$path[1]];
    } elseif (count($path) == 3) {
        return $_COOKIE[$path[0]][$path[1]][$path[2]];
    } elseif (count($path) == 4) {
        return $_COOKIE[$path[0]][$path[1]][$path[2]][$path[3]];
    }
    return false;
}

function myXmlCall($func, $params = null) {
    return xmlCall($func, convert($params));
}

function convert($str) {
    if ($str) {
        if (is_array($str)) {
            return array_map('convert', $str);
        } else {
            return preg_replace('`<`', '&lt;', preg_replace('`>`', '&gt;', $str));
        }
    } else {
        return $str;
    }
}

function quickGet($name, $p_first = false, $urldecode = True) {
    if ($p_first) {
        if (isset($_POST[$name]) && strlen($_POST[$name])) {
            $res = stripslashes($_POST[$name]);
        } elseif (isset($_GET[$name]) && strlen($_GET[$name])) {
            $res = $_GET[$name];
        } else {
            $res = null;
        }
    } else {
        if (isset($_GET[$name])) {
            $res = $_GET[$name];
        } elseif (isset($_POST[$name])) {
            $res = stripslashes($_POST[$name]);
        } else {
            $res = null;
        }
    }
    if ($urldecode) {
        return urldecode($res);
    } else {
        return $res;
    }
}

function quickSet($name, $value) {
    $_GET[$name] = $value;
}

function idGet() {
    return quickGet('id');
}

function right_top_shortcuts_display() {
    if (
        (isset($_GET['cn']) and isset($_GET['objectUUID'])) or
        (isset($_GET['uuid']) and $_GET['uuid'] != "") or
        (isset($_GET['action']) and in_array($_GET['action'], array('BrowseFiles', 'BrowseShareNames', 'hostStatus')))
    ) { // Computers
        include_once('modules/pulse2/includes/menu_action.php');
    } elseif (isset($_GET['gid'])) { // Groups
        include_once('modules/pulse2/includes/menu_group_action.php');
    }
}

/*
 * Used to get $list and $values variables to
 * build an ajaxFilter or SelectItem element
 *
 * @param bool AllEntitiesValue: If True, include 'All my entities' value in element list
 * @return array list and values params
 */

function getEntitiesSelectableElements($AllEntitiesValue = False) {
    $list = array();
    $values = array();
    $locations = getUserLocations();

    if ($AllEntitiesValue) {
        if (count($locations) > 1) {
            $list['Pulse2ALL'] = _T('All my entities', 'pulse2');
            $values['Pulse2ALL'] = '';
        }
    }
    foreach ($locations as $loc) {
        $values[$loc['uuid']] = $loc['uuid'];
        if (isset($loc['completename'])) {
            $list[$loc['uuid']] = $loc['completename'];
        } else {
            $list[$loc['uuid']] = $loc['name'];
        }
    }


    return array($list, $values);
}

/*
 *  Convert timestamp to date
 */

function timestamp_to_date($timestamp) {
        return date('Y/m/d', $timestamp);
}

/*
 *  Convert timestamp to datetime
 */
function timestamp_to_datetime($timestamp) {
        return gmdate('Y-m-d H:i:s', $timestamp);
}
/*
 * get UUID list of machines registered as Pull Machines
 */

function get_pull_targets() {
    if (!isset($_SESSION['pull_targets'])) {
        $_SESSION['pull_targets'] = array();
        if (in_array("msc", $_SESSION["modulesList"])) {
            $_SESSION['pull_targets'] = xmlcall('msc.get_pull_targets');
        }
    }
    return $_SESSION['pull_targets'];
}
?>
