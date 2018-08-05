<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/8/5
 * Time: 15:30
 */

function debug ($msg)
{
//	echo $msg;
    error_log($msg, 3, '/tmp/socket.log');
}
if ($argv[1]) {
    $socket_client = stream_socket_client('tcp://0.0.0.0:2000', $errno, $errstr, 30);
//	stream_set_blocking($socket_client, 0);
    if (!$socket_client) {
        die("$errstr ($errno)");
    } else {
        $msg = trim($argv[1]);
        for ($i = 0; $i < 10; $i++) {
            $res = fwrite($socket_client, "$msg($i)");
            usleep(100000);
            debug(fread($socket_client, 1024));
        }
        fclose($socket_client);
    }
}
else {

    $phArr = array();
    for ($i = 0; $i < 10; $i++) {
        $phArr[$i] = popen("php ".__FILE__." '{$i}:test'", 'r');
    }
    foreach ($phArr as $ph) {
        pclose($ph);
    }

//	for ($i = 0; $i < 10; $i++) {
//		system("php ".__FILE__." '{$i}:test'");
//	}
}