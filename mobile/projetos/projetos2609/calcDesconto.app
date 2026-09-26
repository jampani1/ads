import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  Alert,
  StatusBar,
  Keyboard,
  Platform
} from 'react-native';

export default function App() {
  const [valorProduto, setValorProduto] = useState('');

  const exibirAlerta = (titulo, mensagem) => {
    if (Platform.OS === 'web') {
      window.alert(`${titulo}\n\n${mensagem}`);
    } else {
      Alert.alert(titulo, mensagem);
    }
  };

  const calcularDesconto = () => {
    Keyboard.dismiss();

    const valor = parseFloat(valorProduto.replace(',', '.'));

    if (isNaN(valor) || valor <= 0) {
      exibirAlerta('Erro', 'Por favor, insira um valor válido para o produto.');
      return;
    }

    let percentual = 0;
    if (valor >= 100) {
      percentual = 0.10;
    } else {
      percentual = 0.05;
    }

    const valorDesconto = valor * percentual;
    const valorFinal = valor - valorDesconto;

    exibirAlerta(
      'Resultado',
      `Valor do produto: R$ ${valor.toFixed(2)}\n` +
      `Desconto (${percentual * 100}%): R$ ${valorDesconto.toFixed(2)}\n` +
      `Valor final: R$ ${valorFinal.toFixed(2)}`
    );
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1E40AF" />

      <View style={styles.header}>
        <Text style={styles.headerTitle}>Calculadora de Desconto</Text>
      </View>

      <View style={styles.content}>
        <TextInput
          style={styles.input}
          placeholder="Digite o valor do produto"
          placeholderTextColor="#9CA3AF"
          keyboardType="numeric"
          value={valorProduto}
          onChangeText={setValorProduto}
        />

        <TouchableOpacity
          style={styles.button}
          activeOpacity={0.8}
          onPress={calcularDesconto}
        >
          <Text style={styles.buttonText}>CALCULAR DESCONTO</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>Desenvolvido para fins educacionais</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
    paddingTop: StatusBar.currentHeight || 0,
  },
  header: {
    backgroundColor: '#1E40AF',
    paddingVertical: 18,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.1,
    shadowOffset: { width: 0, height: 2 },
    shadowRadius: 4,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 30,
  },
  input: {
    backgroundColor: '#FFFFFF',
    borderWidth: 1,
    borderColor: '#D1D5DB',
    borderRadius: 8,
    paddingHorizontal: 16,
    paddingVertical: 12,
    fontSize: 16,
    color: '#1F2937',
    marginBottom: 20,
  },
  button: {
    backgroundColor: '#1D4ED8',
    paddingVertical: 14,
    borderRadius: 8,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 15,
    letterSpacing: 0.5,
  },
  footer: {
    paddingVertical: 16,
    alignItems: 'center',
  },
  footerText: {
    color: '#6B7280',
    fontSize: 13,
  },
});
