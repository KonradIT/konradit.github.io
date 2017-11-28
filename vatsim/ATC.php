<?php

//Checks if the page returns code 200 (aka. the page actually loads something in)
function get_http_response_code($url){
    $headers = get_headers($url);
    return substr($headers[0], 9, 3);
}

//Uses the VATEUD API to get all data from the given FIR
function GetCurrentATC($FIR,$ID){
	$ATC=[];
    $json = file_get_contents("http://api.vateud.net/online/atc/".$FIR.".json");
    $details = json_decode($json, true);
	$count=0;
	foreach ($details as $detail) {
		if (!preg_match('/ATIS$/', $detail["callsign"]) and $detail["facility"]!=0 and $detail["cid"]!=$ID){
			$ATC[] = $detail["callsign"]."     -     ".$detail["frequency"];
			if ($count<1){
				$count=$count+1;
			}
		}
	}
	while ($count<5 and $count>0) {
		$ATC[] = "";
		$count=$count+1;
	}
	return $ATC;
}
$OnlineATC = [];
$ICAOs=explode(",",$_GET["ICAO"]);
if (isset($_GET["CID"])){
	$CID=$_GET["CID"];
}
else {
	$CID=0;
}
// Checks if the page loads.
if (get_http_response_code("http://api.vateud.net") == 200) {
	foreach ($ICAOs as $ICAO){
		$online=GetCurrentATC($ICAO,$CID);
		if (!empty($online)) {
			foreach ($online as $ATC){
				$OnlineATC[]=$ATC;
			}
		}
	}
}
else{
    echo "VATEUD's API is offline.\nATC data not available.";
    }
if (empty($OnlineATC)){
	echo "      \tNo other ATC online\t      \n\n\n\n";
}
 
// Joins all the retrieved ATCs into one string.
$result_string = join("\n", $OnlineATC);
//Echoes the actualy string, also adds an break at the end
echo $result_string;
