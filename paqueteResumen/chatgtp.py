import openai
# Define tu clave de API
openai.api_key  = "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"

prompt = 'Cuéntame una historia sobre robots'

# Hacer la solicitud a la API
response = openai.Completion.create(
  engine="text-davinci-003",  # Puedes probar otros motores también
  prompt=prompt,
  max_tokens=150  # Puedes ajustar este valor según tus necesidades
)

# Obtener la respuesta generada por el modelo
generated_text = response.choices[0].text.strip()

# Imprimir la respuesta
print(generated_text)