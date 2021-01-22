<?php
session_start();

if(!defined("PROTOCOL"))
  define("PROTOCOL", (isset($_SERVER['HTTPS'])) ? "https" : "http");
if(!defined("BASE_URL"))
define("BASE_URL", PROTOCOL."://".$_SERVER['HTTP_HOST'].'/pkgs');
if(!defined("BASE_DIR"))
  define("BASE_DIR", $_SERVER['CONTEXT_DOCUMENT_ROOT']);

function absurl($dest){
  $dest = preg_replace('#(\.\.\/)#', '', $dest);


  if ($dest[0] == "/"){
    return BASE_URL.$dest;
  }
  else{
    return BASE_URL.'/'.$dest;
  }
}

function abspath($dest){
  $dest = preg_replace('#(\.\.\/)#', '', $dest);

  if ($dest[0] == "/"){
    return BASE_DIR.$dest;
  }
  else{
    return BASE_DIR.'/'.$dest;
  }
}

include_once(abspath("include/i18n.inc.php"));
include_once(abspath("include/PageGenerator.php"));
include_once(abspath("include/FormGenerator.php"));
include_once(abspath("include/xmlrpc.inc.php"));
include_once(abspath("include/functions.php"));


?>

<nav>
  <ul>
    <li><a href="<?php echo absurl("pkgs/pkgs/add.php");?>">new package</a></li>

  </ul>
</nav>
