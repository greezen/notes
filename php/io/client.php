<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/7/29
 * Time: 21:16
 */

$addr = 'tcp://127.0.0.1:8800';

$fp = stream_socket_client($addr, $errno, $errstr, 1);
if (!$fp) {
    echo "$errstr ($errno)<br />\n";
} else {
    fwrite($fp, "GET / HTTP/1.0\r\n{$addr}\r\nAccept: */*\r\n\r\n");
    while (!feof($fp)) {
        echo fgets($fp, 1024);
    }
    fclose($fp);
    exit();
}