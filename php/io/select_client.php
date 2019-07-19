<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/8/4
 * Time: 16:02
 */

function debug ($msg)
{
//	echo $msg;
    error_log($msg, 3, '/tmp/socket.log');
}
if ($argv[1]) {

    $socket_client = stream_socket_client('tcp://0.0.0.0:2000', $errno, $errstr, 30);

//	stream_set_timeout($socket_client, 0, 100000);

    if (!$socket_client) {
        die("$errstr ($errno)");
    } else {
        $flag = fread($socket_client, 29);
        if ($flag != 'Server full, Try again later.') {
            $msg = trim($argv[1]);
            for ($i = 0; $i < 10; $i++) {
                $res = fwrite($socket_client, "$msg($i)\n");
                usleep(1000000);
            }
            fwrite($socket_client, "quit\n"); // add end token
            debug(fread($socket_client, 1024));
            fclose($socket_client);
        } else {
            echo $flag . PHP_EOL;
        }

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