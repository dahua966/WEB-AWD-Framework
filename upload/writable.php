<?php
ini_set('display_errors','On');
error_reporting(-1);

function new_is_writable($file) {
    if (is_dir($file)){
        $dir = $file;
        if ($fp = @fopen("$dir/test.txt", 'w')) {
            @fclose($fp);
            @unlink("$dir/test.txt");
            $writeable = 1;
        } else {
            $writeable = 0;
        }
    }
    return $writeable;
}

function read_all ($dir){
    if(!is_dir($dir)) return false;
    
    $handle = opendir($dir);

    if($handle){
        while(($fl = readdir($handle)) !== false){
            if (substr($dir,-1) === DIRECTORY_SEPARATOR){
                $temp = $dir.$fl;
            }
            else{
                $temp = $dir.DIRECTORY_SEPARATOR.$fl;
            }
            if(is_dir($temp) && $fl!='.' && $fl != '..' && new_is_writable($temp)){
                print $temp."<br/>";
                read_all($temp);
            }
        }
    }
}
// $dir = isset($argv[1]) ? $argv[1] : '/var/www/html';
$dir = isset($_GET[123]) ? $_GET[123] : '/var/www/html';
print exec('whoami')." is scanning dir: ".$dir."<br/>";
read_all($dir);
?>