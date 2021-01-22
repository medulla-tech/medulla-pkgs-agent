<?php
include("include/header.php");

$objectsearch=array("location_curent" => isset($_SESSION['location']) ? $_SESSION['location'] : "",
                    "imaging_location"=> isset($_SESSION['imaging_location']) ? $_SESSION['imaging_location'] : "",
                    "UserLocations" => isset($_SESSION['pulse2.getUserLocations']) ? $_SESSION['pulse2.getUserLocations'] : "",
                     "login" => isset($_SESSION['login']) ? $_SESSION['login'] : "",
                     "pass" => isset($_SESSION['pass']) ? $_SESSION['pass'] : "",
                     "aclattr" => isset($_SESSION['aclattr']) ? $_SESSION['aclattr'] : "",
                     "acltab" => isset($_SESSION['acltab']) ? $_SESSION['acltab'] : ""
                    );

$shares = pkgs_get_shares();
$select = new SelectItem("share");
//xmlrpc_pkgs_search_share($objectsearch);

$ars_id = [];
$ars_name = [];
$share_path = [];
$name = [];
$type = [];
$enabled = [];
$id = [];
$comments = [];
$uri = [];


foreach ($shares as $share){
  $ars_id[] = $share['ars_id'];
  $ars_name[] = $share['ars_name'];
  $share_path[] = $share['share_path'];
  $name[] = $share['name'];
  $type[] = $share['type'];
  $enabled[] = $share['enabled'];
  $id[] = $share['id'];
  $comments[] = $share['comments'];
  $uri[] = $share['uri'];
}

$path_json = json_encode($share_path);
$select->setElements($name);
$select->setElementsVal($uri);
$select->display();

?>

<script>
index = 0;
paths = <?php echo $path_json;?>;
urladd = jQuery("#menu-add").attr('href');
_urladd = urladd + "?path="+paths[index];
jQuery("#menu-add").attr('href', _urladd);
jQuery("#share").on("change", function(){
  index = jQuery("#share option:selected").index()
  _urladd = urladd + "?path="+paths[index];
  jQuery("#menu-add").attr('href', _urladd);
});
</script>
