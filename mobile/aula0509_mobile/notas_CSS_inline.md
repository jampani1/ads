Aparentemente nessa aula vamos aprender sobre formatação inline (CSS junto do componente):

```jsx
<View style = {{
      width: 300,
      height: 70,
      backgroundColor: 'lightgray',
      padding: 5,
      margin: 5
    }}>
      <Text
      style = {{
        color: 'blue',
        fontSize: 25,
        fontWeight: 'bold',
        textAlign: 'center'
      }}
      >Bem vindo ao react-native</Text>
    </View>
  ```

```jsx 
<TextInput
    style = {{
      width: 300,
      height: 30,
      borderColor: 'black',
      borderWidth: 1,
      borderRadius: 5,
      fontSize: 20,
      margin: 20
    }}
    />
```

# Exemplo 'completo'
Mostrando divesos tipos de formatação inline para componentes como View, Text, TextInput, Button e Image

```jsx 
<View
    style = {{
      margin: 20,
      padding: 5,
      backgroundColor: '#f1f1f1',
      borderRadius: 5,
      alignItems: 'center'

    }}>
      <Text
      style = {{
        color: '#3333AA',
        fontSize: 20
      }}>App</Text>
      <Image
      source = {{
        uri: 'https://i.pinimg.com/474x/bf/66/cd/bf66cdcb62398ee924ee192647bcc7a1.jpg'
      }}
      style = {{
        width: 300,
        height: 150,
        borderRadius: 5,
        marginBottom: 20,
        marginTop: 20
      }}/>
      <TextInput
      placeholder = "teste aqui"
      placeholderTextColor = "gray"
      style = {{
        width: 250,
        height: 50,
        borderWidth: 1,
        borderRadius: 5,
        marginTop: 10,
        padding: 10,
        fontSize: 18,
        backgroundColor: 'yellow'
        
      }}/>
      <View
      style = {{
        margin: 20,
        padding: 5,
        backgroundColor: 'purple',
        marginBottom: 300
      }}>
      <Button
      title = 'bo tao'
      onPress = {() => alert('Clicou né')} />
      </View>
    </View>
  ```