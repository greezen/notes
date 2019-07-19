<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/7/21
 * Time: 22:26
 */

//$re = new Reactor();

$addr = 'tcp://127.0.0.1:8800';
$server = stream_socket_server($addr,$errno,$errstr) or die($errstr);

while ($conn = stream_socket_accept($server)) {
    if (pcntl_fork() == 0) {
        $request = fread($conn, 1024);
        $response = date('Y-m-d H:i:s');
        fwrite($conn, $response);
        fclose($conn);
        exit(0);
    }
}