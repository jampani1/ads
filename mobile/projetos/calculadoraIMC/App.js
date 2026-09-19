import { useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native';

function classificar(imc) {
  if (imc < 18.5) return 'Abaixo do peso';
  if (imc < 25) return 'Peso normal';
  if (imc < 30) return 'Sobrepeso';
  if (imc < 35) return 'Obesidade grau 1';
  if (imc < 40) return 'Obesidade grau 2';
  return 'Obesidade grau 3';
}

export default function App() {
  const [peso, setPeso] = useState('');
  const [altura, setAltura] = useState('');
  const [resultado, setResultado] = useState(null);

  function calcularIMC() {
    const pesoNum = parseFloat(peso.replace(',', '.'));
    const alturaNum = parseFloat(altura.replace(',', '.'));

    if (!pesoNum || !alturaNum) {
      alert('Preencha peso e altura corretamente.');
      return;
    }

    const imc = pesoNum / (alturaNum * alturaNum);
    setResultado({
      valor: imc.toFixed(2),
      classificacao: classificar(imc),
    });
  }

  return (
    <View style={styles.container}>
      <StatusBar style="auto" />

      <View style={styles.cabecalho}>
        <Text style={styles.titulo}>Calculadora de IMC</Text>
      </View>

      <View style={styles.conteudo}>
        <Text style={styles.rotulo}>Peso (kg)</Text>
        <TextInput
          style={styles.input}
          placeholder="Ex: 70"
          keyboardType="numeric"
          value={peso}
          onChangeText={setPeso}
        />

        <Text style={styles.rotulo}>Altura (m)</Text>
        <TextInput
          style={styles.input}
          placeholder="Ex: 1.75"
          keyboardType="numeric"
          value={altura}
          onChangeText={setAltura}
        />

        <TouchableOpacity style={styles.botao} onPress={calcularIMC}>
          <Text style={styles.textoBotao}>CALCULAR IMC</Text>
        </TouchableOpacity>

        {resultado && (
          <View style={styles.resultado}>
            <Text style={styles.textoResultado}>IMC: {resultado.valor}</Text>
            <Text style={styles.textoResultado}>
              Classificação: {resultado.classificacao}
            </Text>
          </View>
        )}
      </View>

      <View style={styles.rodape}>
        <Text style={styles.textoRodape}>Aplicação desenvolvida em React Native</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f2f6ff',
    justifyContent: 'space-between',
    paddingTop: 60,
    paddingBottom: 20,
  },
  cabecalho: {
    alignItems: 'center',
    marginBottom: 20,
  },
  titulo: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#1d3557',
    textAlign: 'center',
  },
  conteudo: {
    paddingHorizontal: 24,
  },
  rotulo: {
    fontSize: 14,
    color: '#1d3557',
    marginBottom: 4,
    marginTop: 12,
  },
  input: {
    borderWidth: 1,
    borderColor: '#a8b8d8',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 10,
    fontSize: 16,
    backgroundColor: '#fff',
  },
  botao: {
    backgroundColor: '#1d3557',
    borderRadius: 8,
    paddingVertical: 14,
    marginTop: 24,
    alignItems: 'center',
  },
  textoBotao: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 16,
  },
  resultado: {
    marginTop: 24,
    padding: 16,
    backgroundColor: '#e0e9ff',
    borderRadius: 8,
    alignItems: 'center',
  },
  textoResultado: {
    fontSize: 16,
    color: '#1d3557',
    fontWeight: '600',
  },
  rodape: {
    alignItems: 'center',
  },
  textoRodape: {
    fontSize: 12,
    color: '#6c7a94',
  },
});
