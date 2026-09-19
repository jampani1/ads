Agora, um exemplo de formatação via StyleSheet (um componente novo que permite editarmos os estilos "à parte")

PRECISAMOS importar StyleSheet no inicio do projeto, e mexemos nele FORA do return do App


# Exemplo com Text

```jsx 
export default function App () {
  return (
    <Text
    style = {styles.titulo}>
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum ac neque. </Text>
  )
}

const styles = StyleSheet.create({
  titulo: {
    color: 'blue',
    fontSize: 15,
    fontWeight: 'bold',
    textAlign: 'center'
  }
})
```