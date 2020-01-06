<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/8/3
 * Time: 22:38
 */

set_time_limit(0);
class SocketServer
{
    private static $socket;
    function SocketServer($port)
    {
        global $errno, $errstr;
        if ($port < 1024) {
            die("端口号必须大于 1024\n");
        }

        $socket = stream_socket_server("tcp://0.0.0.0:{$port}", $errno, $errstr);
        if (!$socket) die("$errstr ($errno)");

        while ($conn = stream_socket_accept($socket, -1)) { // 设置不超时
            static $id = 0;
            static $ct = 0;
            $ct_last = $ct;
            $ct_data = '';
            $buffer = '';
            $id++; 
            $count = 0;
            echo "客户端id: $id\n";
            while (!preg_match('/\r?\n/', $buffer)) { // 没有读到结束符，继续读
                $buffer = fread($conn, 1024);
                $count++;
                echo "读的次数: " . $count; // 打印读的次数
                $ct += strlen($buffer);
                $ct_data .= preg_replace('/\r?\n/', '', $buffer);
            }
            $ct_size = ($ct - $ct_last) * 8;
            echo "[$id] " . __METHOD__ . " > " . $ct_data . "\n";
            fwrite($conn, "Received {$ct_size} byte data.\r\n");
            fclose($conn);
        }

        fclose($socket);
    }
}
new SocketServer(2000);