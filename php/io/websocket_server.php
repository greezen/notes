<?php
// 实例化server
$server = new swoole_websocket_server("0.0.0.0", 9501);
$server->set([
    'worker_num' => 4,
    'task_worker_num' => 4
]);

// 广播
function brodcast($_server, $data)
{
    $client_list = $_server->getClientList();
    foreach($client_list as $client){
        $_server->push($client, $data);
    }
}

// 定时报告聊天室人数
$server->on('WorkerStart', function($_server, $work_id){
    if ($work_id == 0) {
        $_server->tick(5000, function() use ($_server){
            $client_list = $_server->getClientList();
            if (!empty($client_list)) {
                $count = count($client_list);
                if ($count > 0) {
                    $msg = '当前聊天室人数:' . $count . '人';
                    brodcast($_server, $msg);
                }
            }
        });
    }
});

// 监听链接握手成功事件
$server->on('open', function (swoole_websocket_server $_server, swoole_http_request $request) {
    $con_info = $_server->connection_info($request->fd);
    $msg = '欢迎新童鞋! '. $con_info['remote_ip'] . '<br><hr>';
    brodcast($_server, $msg);
    $_server->task(['msg' => $msg]);
    
});

// 监听有新消息事件
$server->on('message', function (swoole_websocket_server $_server, $frame) {
    echo "received ".strlen($frame->data)." bytes\n";
    $ip = $_server->connection_info($frame->fd)['remote_ip'];
    $msg = '<strong>' . $ip . '说: </strong>'. $frame->data . '<br><hr>';
    brodcast($_server, $msg);
    $_server->task(['msg' => $msg]);
});

// 监听断开链接事件
$server->on('close', function ($_server, $fd) {
    $con_info = $_server->connection_info($fd);
    $msg = $con_info['remote_ip'] . '离开了!<br><hr>';
    brodcast($_server, $msg);
});

// task执行完后的回调
$server->on('finish', function ($_server, $task_id, $result) {
    var_dump($task_id, $result);
});

// 异步任务
$server->on('task', function (swoole_websocket_server $_server, $task_id, $from_id, $data) {
    file_put_contents('./msg.log', $data['msg'] . PHP_EOL, FILE_APPEND);
    $_server->finish('ok');
});

$server->start();
