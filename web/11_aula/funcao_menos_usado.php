<?php
    $num = 500;
    function escopo() {
        $GLOBALS["num"] = $GLOBALS["num"] + 5;         //constante globals acessa variáveis em qualquer escopo
        echo $GLOBALS["num"];
    }
    echo $num;
    echo "<br>";
    escopo();
?>