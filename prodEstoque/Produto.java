public class Produto {
    private int codigo;
    private String descricao;
    private int quantidade;
    private String fabricante;

    public int getCodigo() { return codigo; }
    public void setCodigo(int codigo) { this.codigo = codigo; }
    
    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }
    
    public int getQuantidade() { return quantidade; }
    public void setQuantidade(int quantidade) { this.quantidade = quantidade; }
    
    public String getFabricante() { return fabricante; }
    public void setFabricante(String fabricante) { this.fabricante = fabricante; }

    public void darEntrada(int qtd) {
        this.quantidade += qtd; 
        System.out.println("Quantidade " + quantidade + " processada.");
    }

    public boolean darBaixa(int qtd) {
        System.out.println("Quantidade atual: " + quantidade);
        if (this.quantidade >= qtd) {
            System.out.println(". . .");
            this.quantidade -= qtd;
            System.out.println("Quantidade pós baixa: " + quantidade);
            return true;
        }
        return false; 
    }

    public void imprimir() {
        System.out.println("Código: " + this.codigo);
        System.out.println("Descrição: " + this.descricao);
        System.out.println("Quantidade em estoque: " + this.quantidade);
        System.out.println("Fabricante: " + this.fabricante);
    }
    
}
