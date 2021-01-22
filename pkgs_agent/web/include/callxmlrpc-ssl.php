<?php
    /*
    *
    * (c) 2016 siveo, http://www.siveo.net
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
    * file : include/callxmlrpc-ssl.php
    */
    require_once("func_include.inc.php");

    echo '';

    function xmlCall($method, $params = null) {
        $GLOBALS['message'] = "warning";
        if ( is_session_started() === FALSE ) {
            # session n'existe pas on charge la session
            session_start();
            start_config();
        }
        if (!test_sessiondata("warning")){
            # session existe il manque des informations
            start_config();
        }
        if (!test_sessiondata("error")){
            msg("terminate script on error session value","error");
        }
        $_SESSION['auth'] = base64_encode($_SESSION['user'].":".$_SESSION['password']);

        $functrim = function($value) {return trim($value);};
        $array_ip_accept=explode ("," , $_SESSION['remoteadress']);

        $array_ip_accept_remote = array_map($functrim, $array_ip_accept);
        //echo $_SERVER['REMOTE_ADDR'];
        if (! in_array($_SERVER['REMOTE_ADDR'], $array_ip_accept_remote)) {
            msg("terminate script on error remote ip forbiden","error");
            exit(0);
        }

       $auth = $_SESSION['auth'];
       $request = xmlrpc_encode_request($method, $params);
       $header = (version_compare(phpversion(), '5.2.8'))
                    ? array("Content-Type: text/xml","Authorization: Basic $auth")
                    : "Content-Type: text/xml\r\nAuthorization: Basic $auth" ; //[1]
        if ($_SESSION['enablessl']){
            $contextstruct=array(
                "http" => array("method" => "POST",
                                "header" => $header,
                                "ignore_errors" => true,
                                "timeout" => (float)30.0,
                                "content" => $request,),
                "ssl"=>array("allow_self_signed"=>true,
                            "verify_peer"=>false,
                            "verify_peer_name"=>false,));
            $uri = sprintf("https://%s:%s/",$_SESSION['host'],$_SESSION['port']);
        }
        else{
            $contextstruct=array(
                "http" => array("method" => "POST",
                                "header" => $header,
                                "ignore_errors" => true,
                                "timeout" => (float)30.0,
                                "content" => $request,));
            $uri = sprintf("http://%s:%s/",$_SESSION['host'],$_SESSION['port']);
        }
        # creation du context
        $context = stream_context_create($contextstruct);
        $file = @file_get_contents($uri, false, $context);
        # on recupere le code html en analisant le header de retour
        if (http_response_code() != 200){
            # on a pas 200 on envoi 1 log avec le code erreur
            msg(display_http_response_code($code), "error");
        }else
        {
            $response = xmlrpc_decode($file);
            //var_dump ( $response);
            if ($response && @xmlrpc_is_fault($response)) {
                $errObj = new ErrorHandlingmsg($response);
                return FALSE;
            } else {
                return $response;
            }
        }
        return false;
    }

class ErrorHandlingmsg {
    var $msg;
    var $faultString;
    var $faultTraceback;
    var $faultCode;

    function ErrorHandlingmsg($rep) {
        $this->faultCode = $rep['faultCode'];
        $this->faultString =  $rep['faultString'];
        $this->faultTraceback = $rep['faultTraceback'];
            $str= '<pre id=\'textclipboard\'>';
            $str .= gmdate("d M Y H:i:s") . "\n\n";
            $str .= "PHP XMLRPC call: " . $this->faultString  . "\n\n";
            $str .= "Python Server traceback:\n";
            $str .= htmlentities($this->faultTraceback)."\n";
            $str .= '</pre>';
            $this->msg = $str;

        $order   = array("\r\n", "\n", "\r");
        $replace = '<br />';
        $this->msg =  str_replace($order, $replace, $this->msg);
        $order   = array("\"");
        $replace = "'";
        $this->msg = str_replace($order, $replace, $this->msg);

        echo '<script>
//             navigator.permissions.query({name: "clipboard-write"}).then(result => {
//                  if (result.state == "granted" || result.state == "prompt") {
//                      console.log(" write to the clipboard now")
//                  }
//             });
                var msg= "'.$this->msg.'";
                $("<div></div>").dialog({
                    modal: true,
                    width: "auto",
                    height: "auto",
                    show: "slide",
                    title: "Error Call function '. $this->faultString.'",
                    open: function() {
                    var markup = msg;
                    $(this).html(markup);
                    },
                    buttons: {
                        Ok: function() {
                            $( this ).dialog( "close" );
                        }
                        //,Clipboard: function() {
                            // API pas encore sur tout les navigateur.
//                             navigator.clipboard.writeText(msg).then(function() {
//                                     /* presse-papiers modifié avec succès */
//                                     console.log(" presse-papiers modifié avec succès ")
//                                     }, function() {
//                                         console.log("Vérify browser permission clipboard-write ");
//                                     });
                        //}
                    }
                });  //end confirm dialog
            </script>';
    }
}
