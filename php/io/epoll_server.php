<?php
/**
 * Created by PhpStorm.
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
            die("Please install event extension firstly\n");
        }

        if ($port < 1024) {
            die("Port must be a number which bigger than 1024\n");
        }

        $socket_server = stream_socket_server("tcp://0.0.0.0:{$port}", $errno, $errstr);
        if (!$socket_server) die("$errstr ($errno)");

        stream_set_blocking($socket_server, 0); // 非阻塞

        self::$base = new EventBase();
        $event = new Event(self::$base, $socket_server, Event::READ | Event::PERSIST, array(__CLASS__, 'ev_accept'));
        $event->add();
        self::$base->loop();

//        event_set($event, $socket_server, Event::READ | EVENT::WRITE, array(__CLASS__, 'ev_accept'), $base);
//        event_base_set($event, $base);
//        event_add($event);
//        event_base_loop($base);

        self::$connections = array();
        self::$buffers = array();
    }

    static function ev_accept($socket, $flag, $base)
    {
        static $id = 0;

        $connection = stream_socket_accept($socket);
        stream_set_blocking($connection, 0);

        $id++; // increase on each accept
        $buffer = new EventBufferEvent(self::$base, $connection, EventBufferEvent::READING, array(__CLASS__, 'ev_read'), array(__CLASS__, 'ev_write'), array(__CLASS__, 'ev_error'));
        $buffer->setTimeouts(1, 1);
        $buffer->setWatermark(Event::READ, 0, 0xffffff);
        $buffer->setPriority(10);
        $buffer->enable(Event::READ | Event::PERSIST |Event::WRITE);

        // we need to save both buffer and connection outside
        self::$connections[$id] = $connection;
        self::$buffers[$id] = $buffer;
    }

    static function ev_error($buffer, $error, $id)
    {
//        event_buffer_disable(self::$buffers[$id], EV_READ | EV_WRITE);
        //$buffer->disable(Event::READ | Event::WRITE);
        //$buffer->free();
//        event_buffer_free(self::$buffers[$id]);
//        var_dump($buffer->read(1024));
        if (isset(self::$connections[$id]) && is_resource(self::$connections[$id])) {
            fclose(self::$connections[$id]);
        }
        //unset(self::$buffers[$id], self::$connections[$id]);
    }

    static function ev_read($buffer, $id)
    {
        static $ct = 0;
        $ct_last = $ct;
        $ct_data = '';
        //while ($read = event_buffer_read($buffer, 1024)) {
        while ($read = $buffer->read(1024)) {
            $ct += strlen($read);
            $ct_data .= $read;
        }
        $ct_size = ($ct - $ct_last) * 8;
        echo "[$id] " . __METHOD__ . " > " . $ct_data . "\n";
        $buffer->write("Received $ct_size byte data.\r\n");
    }

    static function ev_write($buffer, $id)
    {
        echo "[$id] " . __METHOD__ . "\n";
    }
}
new EpollSocketServer(2000);