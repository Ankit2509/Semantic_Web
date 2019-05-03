	
<?php

header("Access-Control-Allow-Origin: *");
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
     // The request is using the POST method
$jsondata = "php://input";
$phpjsonstring = file_get_contents( $jsondata ); // Get content of posted JSON String
    
$fp = fopen('results.txt', 'w');

fwrite($fp, $phpjsonstring);
fclose($fp);

}
$str = file_get_contents('results.txt');
echo $str;
?>

