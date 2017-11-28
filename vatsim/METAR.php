<?php
//Retrieves the METAR
function getMetar($icao){
    $metar = file_get_contents("http://metar.vatsim.net/".$icao);
    return $metar;
}
//Checks if there is any activity at an airport
function checkAirport($icao){
    $a = $icao;
    $details = file_get_contents("http://api.vateud.net/online/pilots/".$a.".json");
    return $details;
}
//Used with GetCurrentATC(), checks if the page returns code 200 (aka. the page actually loads something in)
function get_http_response_code($url){
    $headers = get_headers($url);
    return substr($headers[0], 9, 3);
}
 

//Uses the VATEUD API to get all data from the given FIR
function GetCurrentATC($FIR){
	$ATC=[];
    $json = file_get_contents("http://api.vateud.net/online/atc/".$FIR.".json");
    $details = json_decode($json, true);
	foreach ($details as $detail) {
		$ATC[] = $detail["name"];
	}
	return $ATC;
	#echo $details[0];
}
//Defines all the airports to be used in this script
$ICAOs=explode(",",$_GET["ICAO"]);#[
   # 1 => "lebl",
  #  2 => "lepa",
   # 3 => "leib",
   # 4 => "lemh",
   # 5 => "levc"
#];
 
//Creates an array to save all the METARs in
$metars = [];
// Checks if the page loads, then checks if an airport has activity, then retrieves the METARs where needed. If the VATEUD API doesn't retrieve any data (because 99% it's broken, it retrieves all the METARs)
if (get_http_response_code("http://api.vateud.net") == 200) {
	foreach ($ICAOs as $ICAO){
		$temp=json_decode(checkAirport($ICAO));
		if (!empty($temp)){
			$metars[]=getMetar($ICAO);
		}
	}
}
else{
    foreach ($ICAOs as $ICAO){
        $metars[] = getMetar($ICAO);
    }
}
 
// Joins all the retrieved METARs into one string.
$result_string = join('   |   ', $metars);
$str=str_replace("\r\n","",$result_string);
print $str
?>
