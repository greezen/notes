<?php
/**
 * 需要libevent和event扩展支持
 * @link https://github.com/expressif/pecl-event-libevent.git
 * User: greezen
 * Date: 2018/8/5
 * Time: 15:29
 */

set_time_limit(0);
class EpollSocketServer
{
    private static $socket;
    private static $connections;
    private static $buffers;
    private static $base = null;

    function __construct ($port)
    {
        global $errno, $errstr;

        if (!extension_loaded('event')) {
            die("请先安装event扩展\n");
        }

        if ($port < 1024) {
            die("端口号必须大于 1024\n");
        }

        $socket_server = stream_socket_server("tcp://0.0.0.0:{$port}", $errno, $errstr);
        if (!$socket_server) die("$errstr ($errno)");

        stream_set_blocking($socket_server, 0); // 非阻塞

        self::$base = new EventBase();
        $event = new Event(self::$base, $socket_server, Event::READ | Event::PERSIST, array(__CLASS__, 'ev_accept'));
        $event->add();
        self::$base->loop();

        self::$connections = array();
        self::$buffers = array();
    }

    // 新请求事件回调
    static function ev_accept($socket, $flag, $base)
    {
        static $id = 0;

        $connection = stream_socket_accept($socket);
        stream_set_blocking($connection, 0);// 非阻塞

        $id++;
        $buffer = new EventBufferEvent(self::$base, $connection, EventBufferEvent::READING, array(__CLASS__, 'ev_read'), array(__CLASS__, 'ev_write'), array(__CLASS__, 'ev_event'));
        $buffer->setTimeouts(1, 1);// 设置读写超时时间
        $buffer->setWatermark(Event::READ, 0, 0xffffff);
        // $buffer->setPriority(10); // 设置优先级
        $buffer->enable(Event::READ | Event::PERSIST |Event::WRITE); // 设置监听的事件

        // 保存connection和buffer
        self::$connections[$id] = $connection;
        self::$buffers[$id] = $buffer;
    }

    // 事件状态改变回调
    static function ev_event($buffer, $error, $id)
    {
        if (isset(self::$connections[$id]) && is_resource(self::$connections[$id])) {
            fclose(self::$connections[$id]);
        }
        unset(self::$buffers[$id], self::$connections[$id]);
    }

    // 读事件回调
    static function ev_read($buffer, $id)
    {
        static $ct = 0;
        $ct_last = $ct;
        $ct_data = '';
        while ($read = $buffer->read(1024)) {
            $ct += strlen($read);
            $ct_data .= $read;
        }
        $ct_size = ($ct - $ct_last) * 8;
        echo "[$id] " . __METHOD__ . " > " . $ct_data . "\n";
        $buffer->write("Received $ct_size byte data.\r\n");
    }

    // 写事件回调
    static function ev_write($buffer, $id)
    {
        echo "[$id] " . __METHOD__ . "\n";
    }
}
new EpollSocketServer(2000);