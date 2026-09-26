import React, { useState } from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
  Alert,
  StatusBar,
  Keyboard
} from 'react-native';

export default function App() {
  const [num1, setNum1] = useState('');
  const [num2, setNum2] = useState('');

  const calcular = (operacao) => {
    Keyboard.dismiss();

    const n1 = parseFloat(num1.replace(',', '.'));
    const n2 = parseFloat(num2.replace(',', '.'));

    if (isNaN(n1) || isNaN(n2)) {
      Alert.alert('Erro', 'Por favor, insira valores numéricos válidos em ambos os campos.');
      return;
    }

    let resultado = 0;
    let simbolo = '';

    switch (operacao) {
      case 'somar':
        resultado = n1 + n2;
        simbolo = '+';
        break;
      case 'subtrair':
        resultado = n1 - n2;
        simbolo = '-';
        break;
      case 'multiplicar':
        resultado = n1 * n2;
        simbolo = '×';
        break;
      case 'dividir':
        if (n2 === 0) {
          Alert.alert('Erro', 'Não é possível realizar divisão por zero.');
          return;
        }
        resultado = n1 / n2;
        simbolo = '÷';
        break;
      default:
        return;
    }

    Alert.alert(
      'Resultado',
      `${n1} ${simbolo} ${n2} = ${resultado}`
    );
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1E40AF" />

      {/* 2. Cabeçalho */}
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Calculadora Simples</Text>
      </View>

      <View style={styles.content}>
        {/* 3. Área de conteúdo */}
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            placeholder="Digite o primeiro número"
            placeholderTextColor="#9CA3AF"
            keyboardType="numeric"
            value={num1}
            onChangeText={setNum1}
          />
          <TextInput
            style={styles.input}
            placeholder="Digite o segundo número"
            placeholderTextColor="#9CA3AF"
            keyboardType="numeric"
            value={num2}
            onChangeText={setNum2}
          />
        </View>

        {/* 4. Botões de operações */}
        <View style={styles.buttonsContainer}>
          <TouchableOpacity
            style={[styles.button, styles.btnSomar]}
            activeOpacity={0.8}
            onPress={() => calcular('somar')}
          >
            <Text style={styles.buttonText}>SOMAR</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.btnSubtrair]}
            activeOpacity={0.8}
            onPress={() => calcular('subtrair')}
          >
            <Text style={styles.buttonText}>SUBTRAIR</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.btnMultiplicar]}
            activeOpacity={0.8}
            onPress={() => calcular('multiplicar')}
          >
            <Text style={styles.buttonText}>MULTIPLICAR</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={[styles.button, styles.btnDividir]}
            activeOpacity={0.8}
            onPress={() => calcular('dividir')}
          >
            <Text style={styles.buttonText}>DIVIDIR</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>Aplicação desenvolvida em React Native</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
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
    paddingTop: 28,
  },
  inputContainer: {
    marginBottom: 5,
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
    marginBottom: 14,
  },
  buttonsContainer: {
    gap: 6,
  },
  button: {
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
  btnSomar: {
    backgroundColor: '#059669', // Verde
  },
  btnSubtrair: {
    backgroundColor: '#1D4ED8', // Azul
  },
  btnMultiplicar: {
    backgroundColor: '#D97706', // Laranja
  },
  btnDividir: {
    backgroundColor: '#DC2626', // Vermelho
  },
  footer: {
    paddingVertical: 10,
    alignItems: 'center',
  },
  footerText: {
    color: '#6B7280',
    fontSize: 10,
  },
});
