//Maurício Jampani de Souza
//Exercicio 1 - calculadora
function soma(n1, n2) {
    return n1 + n2;
}
console.log(soma(5,8))

function subtracao(n1, n2) {
    return n1 - n2;
}
console.log(subtracao(5,8))

function multiplicacao(n1, n2) {
    return n1 * n2;
}
console.log(multiplicacao(5,8))

function divisao(n1, n2) {
    if (n2 !== 0) {
        return n1 / n2;
    } else {
        console.log("divisão impossivel");
    }
}
console.log(divisao(5,8))

function modulo(n1, n2) {
    return n1 % n2;
}
console.log(modulo(5,8))

function potencia(n1, n2) {
    return n1 ** n2;
}
console.log(potencia(5,8))

//Exercicio 2 - IMC
let peso = prompt("Qual seu peso?");
let altur = prompt("Qual sua altura? (em centímetros)");

function imc(peso, altur) {
    altur = altur / 100;
    return (peso / (altur * altur));
}
console.log("Seu IMC é: "+imc(peso, altur));

//Exercicio 3 - arrow function
let numero = prompt("Digite um número")
const dobro = (numero) => {
    return numero * 2;
}
console.log("O dobro do seu número é "+dobro(numero));

//Exercício 4 - array de cursos
const cursos = ["Análise e Desenvolvimento de Sistemas", "Mecanica", "Engenharia", "Sociologia", "Mecatronica"]
cursos.forEach(curso=>{
    console.log(curso);
})
console.log("O primeiro curso é "+cursos[0]);
console.log("O terceiro curso é "+cursos[2]);

console.log("Mais um curso individualmente "+cursos[4]); // nao sei se entendi a pergunta

//Exercicio 5 - array de nomes
const nomes = ["Joao", "Maria", "Fernando", "Sergio", "Tatiane"]
nomes.forEach(nome=> {
    console.log(nomes.join(", "));
})

//Exercicio 6 - filtrando numeros
const numeros = [5, 12, 8, 20, 3, 15, 7, 25]; 
const maiores = numeros.filter(numero=>numero>=12);
console.log(maiores)