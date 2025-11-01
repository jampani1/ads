<?php
    $num = 500;
    function escopo() {
        global $num;                //variável global é reconhecida em todo o código
        $num = $num + 5;          
        echo $num;
    }
    echo $num;
    echo "<br>";
    escopo();
?>