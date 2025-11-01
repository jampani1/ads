<?php 
    $nome = "MariaDB";
    $sobrenome = "Data Base";

    echo '<br>';                    //aspas simples com comando html funciona normal
    echo "Bom dia 'amigos'";
    echo "<br>";
    echo '$nome $sobrenome';        //aspas simples não interpolam variáveis (não mostra conteúdo)
    echo "<br>";
    echo "$nome $sobrenome";        //aspas duplas interpolam variáveis (mostra conteúdo)
?>