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
    *
    * include/func_include.inc.php
    */

    //See later to change this
    define("INI_FILE_PKGS","/etc/pulse_pkgs_agent/pulse_agent_xmlrpc_pkgs.ini");

    function msg($msg, $type=NULL){
        if (!is_null ($type)) $GLOBALS['message'] = $type;
        if ($GLOBALS['message'] == "warning"){
            error_log (sprintf("Warning : [script %s] %s",
                                    $_SERVER['PHP_SELF'],
                                    $msg));
        }
        else{
            error_log (sprintf("Error : [script %s] %s",
                                    $_SERVER['PHP_SELF'],
                                    $msg));
        }
    }

    function test_sessiondata($messagetype="warning"){
        $GLOBALS['message'] = $messagetype;
        if (!isset($_SESSION['user'] )){
            msg("authentification username missing");
            return false;
        }
        if (!isset($_SESSION['password'] )){
            msg ("authentification password missing");
            return false;
        }
        if (!isset($_SESSION['remoteadress'] )){
            msg ("remoteadress missing");
            return false;
        }
        if (!isset($_SESSION['enablessl'] )){
            msg ("enablessl missing");
            return false;
        }
        if (!isset($_SESSION['host'] )){
            msg ("host missing");
            return false;
        }
        if (!isset($_SESSION['host'] )){
            msg ("port missing");
            return false;
        }
        return true;
    }

    function start_config() {
        # on charge la configuration
        $ini_array = parse_ini_file(INI_FILE_PKGS);
        $_SESSION = array_merge($_SESSION, $ini_array);
    }

    function is_session_started(){
        if ( php_sapi_name() !== 'cli' ) {
            if ( version_compare(phpversion(), '5.4.0', '>=') ) {
                return session_status() === PHP_SESSION_ACTIVE ? TRUE : FALSE;
            } else {
                return session_id() === '' ? FALSE : TRUE;
            }
        }
        return FALSE;
    }

    function display_http_response_code($code = NULL) {
        $text = 'Unknown http status code ';
        if ($code !== NULL) {
            switch ($code) {
                case 100: $text = 'Continue'; break;
                case 101: $text = 'Switching Protocols'; break;
                case 200: $text = 'OK'; break;
                case 201: $text = 'Created'; break;
                case 202: $text = 'Accepted'; break;
                case 203: $text = 'Non-Authoritative Information'; break;
                case 204: $text = 'No Content'; break;
                case 205: $text = 'Reset Content'; break;
                case 206: $text = 'Partial Content'; break;
                case 300: $text = 'Multiple Choices'; break;
                case 301: $text = 'Moved Permanently'; break;
                case 302: $text = 'Moved Temporarily'; break;
                case 303: $text = 'See Other'; break;
                case 304: $text = 'Not Modified'; break;
                case 305: $text = 'Use Proxy'; break;
                case 400: $text = 'Bad Request'; break;
                case 401: $text = 'Unauthorized'; break;
                case 402: $text = 'Payment Required'; break;
                case 403: $text = 'Forbidden'; break;
                case 404: $text = 'Not Found'; break;
                case 405: $text = 'Method Not Allowed'; break;
                case 406: $text = 'Not Acceptable'; break;
                case 407: $text = 'Proxy Authentication Required'; break;
                case 408: $text = 'Request Time-out'; break;
                case 409: $text = 'Conflict'; break;
                case 410: $text = 'Gone'; break;
                case 411: $text = 'Length Required'; break;
                case 412: $text = 'Precondition Failed'; break;
                case 413: $text = 'Request Entity Too Large'; break;
                case 414: $text = 'Request-URI Too Large'; break;
                case 415: $text = 'Unsupported Media Type'; break;
                case 500: $text = 'Internal Server Error'; break;
                case 501: $text = 'Not Implemented'; break;
                case 502: $text = 'Bad Gateway'; break;
                case 503: $text = 'Service Unavailable'; break;
                case 504: $text = 'Gateway Time-out'; break;
                case 505: $text = 'HTTP Version not supported'; break;
                default:
                    exit('Unknown http status code "' . htmlentities($code) . '"');
                break;
            }
        };
        return $text;
    }
    ?>
