<?php
    $num = 500;
    function escopo() {
        $num = $num + 5;            //a variável não foi reconhecida nesse escopo 
        echo $num;
    }
    echo $num;
    escopo();
?>