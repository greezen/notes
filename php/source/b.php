<?php
$m1 = memory_get_usage();
$arr = [];

for ($i=0; $i < 200000; $i++) { 
	$arr[$i] = 1;
}

$m2 = memory_get_usage();

echo $m2-$m1 . "\n";