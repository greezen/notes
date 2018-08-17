<?php
/**
 * 多进程和单进程求素数的性能比较
 * User: greezen
 * Date: 2018/7/21
 * Time: 22:26
 */

ini_set('memory_limit', -1);
// 判断一个数是否为素数
function isPrime($n) {
    if ($n <= 3) {
        return $n > 1;
    } else if ($n % 2 === 0 || $n % 3 === 0) {
        return false;
    } else {
        for ($i = 5; $i * $i <= $n; $i += 6) {
            if ($n % $i === 0 || $n % ($i + 2) === 0) {
                return false;
            }
        }
        return true;
    }
}

// 多进程回调函数
function callback(swoole_process $worker)
{
    $recv = json_decode($worker->read(), true);
    $process_index = $recv['process_index']; // 进程编号
    $total_number = $recv['total_number']; // 要判断质数总数量
    $process_num = $recv['process_num']; // 总的进程数

    $numbers = range(1, $total_number); //总的数据表
    $limit = ceil($total_number / $process_num); // 每个进程处理的数据数
    $start = ($process_index - 1) * $limit;
    $end = ($limit * $process_index) <= $total_number ?:$total_number;

    for ($i = $start; $i < $end; $i++) { 
        if (isPrime($numbers[$i])) {
            //echo PHP_EOL . $numbers[$i];
        }
    }
    //echo PHP_EOL.$process_index.'==='.$worker->pid.'==='.$total_number;
 
    $worker->exit(0);
}


if ($argc < 2) {
    die('php multiple_process.php 100 [5]' . PHP_EOL);
}

if ($argc >= 3 && $argv[2] > 0) { // 多进程模式
    $total_number = $argv[1];
    $process_num = $argv[2]; // 进程数
    $workers = [];        // 进程保存
    $redirect_stdout = false;    // 重定向输出  ; 这个参数用途等会我们看效果
    $num = 0;
    for($i = 1; $i <= $process_num; $i++){
        $process = new swoole_process('callback', $redirect_stdout);
        $pid = $process->start();
     
        // 管道写入内容
        $data = [
            'process_index' => $i,
            'process_num' => $process_num,
            'total_number' => $total_number
        ];
        $process->write(json_encode($data));
        // 将每一个进程的句柄存起来
        $workers[$pid] = $process;
    }

    while(1){
        $ret = swoole_process::wait();
        if ($ret){// $ret 是个数组 code是进程退出状态码，
            $pid = $ret['pid'];
            echo PHP_EOL."Worker Exit, PID=" . $pid . PHP_EOL;
        }else{
            break;
        }
    }


} else { // 单进程模式
    for ($i = 0; $i < $argv[1]; $i++) { 
        if (isPrime($i)) {
            //echo $i . PHP_EOL;
        }
    }
}


