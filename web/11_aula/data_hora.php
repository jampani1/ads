<html>
    <body>
        <?php
            $data = date("d/m/Y", time());      //retorna a data atual do servidor
            $hora = date("H:i", time());        //retorna a hora atual do servidor
        ?> 
        <p align="center">
            <strong>A data e a hora atual deste servidor é: 
                <?php echo $data; ?> 
                <?php echo $hora; ?>
            </strong>
        </p>       
    </body>
</html>

