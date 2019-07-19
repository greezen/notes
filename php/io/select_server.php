<?php
/**
 * Created by PhpStorm.
 * User: greezen
 * Date: 2018/8/4
 * Time: 15:48
 */

set_time_limit(0);
class SelectSocketServer
{
    private static $socket;
    private static $timeout = 60;
    private static $maxconns = 10;
    private static $connections = array();

    function __construct($port)
    {
        global $errno, $errstr;
        if ($port < 1024) {
            die("端口号必须大于 1024\n");
        }

        $socket = socket_create_listen($port);
        if (!$socket) die("监听端口 {$port} 失败");

        socket_set_nonblock($socket); // 非阻塞

        while (true)
        {
            $readfds = array_merge(self::$connections, array($socket));
            $writefds = array();
            $e = null;

            // 选择一个连接，获取读、写连接通道
            if (socket_select($readfds, $writefds, $e, self::$timeout))
            {
                // 如果是当前服务端的监听连接
                if (in_array($socket, $readfds)) {
                    // 接受客户端连接
                    $newconn = socket_accept($socket);
                    $i = (int) $newconn;
                    $reject = '';
                    if (count(self::$connections) >= self::$maxconns) {
                        $reject = "服务器满员了,请稍候再试.\n";
                    }
                    // 将当前客户端连接放入链接池
                    self::$connections[$i] = $newconn;
                    // 输入的连接资源缓存容器
                    $writefds[$i] = $newconn;
                    // 连接不正常
                    if ($reject) {
                        socket_write($writefds[$i], $reject);
                        unset($writefds[$i]);
                        self::close($i);
                    } else {
                        echo "客户端id:  {$i} .\n";
                    }
                    // 从可读连接池中删除
                    $key = array_search($socket, $readfds);
                    unset($readfds[$key]);
                }

                // 轮循读通道
                foreach ($readfds as $rfd) {
                    // 客户端连接
                    $i = (int) $rfd;
                    // 从通道读取
                    $line = @socket_read($rfd, 2048, PHP_NORMAL_READ);
                    if ($line === false) {
                        // 读取不到内容，结束连接
                        echo "连接关闭 $i.\n";
                        self::close($i);
                        continue;
                    }
                    $tmp = substr($line, -1);
                    if ($tmp != "\r" && $tmp != "\n") {
                        // 等待更多数据
                        continue;
                    }
                    // 处理逻辑
                    $line = trim($line);
                    if ($line == "quit") {
                        echo "客户端 $i 退出.\n";
                        self::close($i);
                        break;
                    }
                    if ($line) {
                        echo "客户端 $i >>" . $line . "\n";
                    }
                }

                // 轮循写通道
                foreach ($writefds as $wfd) {
                    $i = (int) $wfd;
                    $w = socket_write($wfd, "欢迎新童鞋 $i!\n");
                }
            }
        }
    }

    function close ($i)
    {
        socket_shutdown(self::$connections[$i]);
        socket_close(self::$connections[$i]);
        unset(self::$connections[$i]);
    }
}
new SelectSocketServer(2000);