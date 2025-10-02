<?php
    header('Content-Type: application/json;charset=UTF-8');
    header("Access-Control-Allow-Origin: *");
    header("Access-Control-Allow-Methods: POST");

	$input = trim($_POST["input"]);

	if (empty($input)) {
		echo json_encode([]);
		die();
	}
    
    $result = shell_exec('/usr/bin/python3 /var/ner_app/ner.py "' . $input . '"');

    echo $result;