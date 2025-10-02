<?php
$command = "/usr/bin/python3 /var/ner_app/ner.py 'сгущёное молоко' 2>&1"; // ls command will fail, and error will be redirected
$output = shell_exec($command);
echo "<pre>$output</pre>";