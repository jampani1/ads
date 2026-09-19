import { Text, View, TextInput, Button, TouchableOpacity, Pressable, Image } from 'react-native';

export default function meuApp(){

  const nome = "João"
  const idade = 30
  const num1 = 10
  const num2 = 10

  function clicar() {
    alert("E-mail enviado")
  }

  return (
    <View>

      <View>
        <Text>Desenvolvimento mobile - react-native</Text>
        <Text>primeira View</Text>
      </View>

      <View>
        <Text>~ ~ ´ ´ ` ` - - _ _ </Text>
        <Text>segunda View</Text>
      </View>

      <View>
        <Text>Nome </Text>
        <TextInput
          placeholder = 'Digite seu nome'
        />
      </View>

      <View>
      <Text>E-mail </Text>
        <TextInput
          placeholder = 'Digite seu e-mail'
        />
      </View>

      <View>
        <Button
          title = 'Enviar'
          onPress={clicar}
        />
        <Button
          title = 'Limpar'
          onPress={""}
        />
      </View>

      <View>
        <TouchableOpacity onPress={clicar}>
          <Text>Enviar dados 1 - touchableopacity</Text>
        </TouchableOpacity>
      </View>

      <View>
        <Pressable onPress={clicar}>
          <Text>Enviar dados 2 - pressable </Text>
        </Pressable>
      </View>

      <View>        
        <Image
          source={{
            uri:'https://reactnative.dev/img/tiny_logo.png'
          }}
          style={{
            height: 100,
            width: 200
          }}
        />
      </View>
    </View>
  )
}