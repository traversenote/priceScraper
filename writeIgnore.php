<?php

//Get record

if (isset($_POST['id'])) {
	$id = $_POST['id'];
}else{
	$id = 0000;
}
if (isset($_POST['action'])) {
	$ignoreState = $_POST['action'];
}else{
	$ignoreState = 0;
}

// open file


$json = file_get_contents('prices.json', 'r') or die ("unable to open file");
#$ignoreFile = file_get_contents('results.json', 'w+') or die ("unable to open file");

//Decode JSON
$jsonData = json_decode($json,true);
$jsonFile = 'prices.json';
//Print data
//echo "\n".$id." will be set to ".$ignoreState."\n";
for($i=0; $i < count($jsonData); $i++){
	if($jsonData[$i]["productID"] == $id){
		$jsonData[$i]["dateIgnored"] = (string)date("M d Y");
		$jsonData[$i]["ignoreStatus"] = $ignoreState;
		//print(" PHP Got ".$jsonData[$i]["productID"]." ".$ignoreState." ");
		if (is_writable($jsonFile)) {
		    // no worries, just keep trucking
		    echo file_put_contents($jsonFile, json_encode($jsonData));
		    echo "\n Looks like stuff got written";
		} else {
		    $body  = "Error writing file: prices.json"."\n";
		    $body .= "Date Time: ".date('Y-m-d H:i:s')."\n";
		    $body .= "--------------------------------------------------------\n";
		    $body .= "Data to have been written: ".$jsonData[$i]["productID"]."\n";
		    echo $body;

		}
		
//		file_put_contents('prices.json', json_encode("You just don't care"));
		usleep(300000);
	}
}
?>
