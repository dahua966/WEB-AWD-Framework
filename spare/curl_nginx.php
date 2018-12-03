<?php
function curl_nginx($remoteDomain){
	$headers = getallheaders();
	$extraHeaders = array();
	$headers['Host'] = $remoteDomain;
	if (isset($headers['Referer'])) {
	    $headers['Referer'] = str_replace($_SERVER["HTTP_HOST"], $remoteDomain, $headers['Referer']);
	}
	if (isset($headers['Origin'])) {
	    $headers['Origin'] = str_replace($_SERVER["HTTP_HOST"], $remoteDomain, $headers['Origin']);
	}
	foreach ($headers as $key => $value) {
		if(in_array($key, array('User-Agent','Accept','Accept-Language','Accept-Encoding','Referer','Origin')))
			$extraHeaders[] = $key.': '.$value;
	}
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_URL, 'http://'.$remoteDomain.$_SERVER["REQUEST_URI"]);

	if ($_SERVER['REQUEST_METHOD'] == 'POST'){
		$post_data = file_get_contents('php://input');
		if(isset($_FILES)){
			$filename = array_keys($_FILES)[0];
			$post_data = $_POST;
			$post_data[$filename] = '@'.$_FILES[$filename]['tmp_name'];
		}
	    curl_setopt($ch, CURLOPT_POST, TRUE);
	    @curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
	}
	curl_setopt($ch, CURLOPT_HTTPHEADER, $extraHeaders);
	if (isset($headers['Cookie'])){
	    curl_setopt($ch, CURLOPT_COOKIE, $headers['Cookie']);
	}
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	$response = curl_exec($ch);
	curl_close($ch);
	echo $response;
	exit();
}