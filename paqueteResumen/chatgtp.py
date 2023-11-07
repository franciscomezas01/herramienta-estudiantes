import openai
# Define tu clave de API
api_key = "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"

# Inicializa el cliente de OpenAI con tu clave de API
openai.api_key = api_key

# Definir el mensaje inicial
mensaje_inicial = "Cuéntame una historia sobre gatos."

# Llamar a la API de ChatGPT para generar una respuesta
respuesta = openai.Completion.create(
    engine="text-davinci-002",
    prompt=mensaje_inicial,
    max_tokens=50  # Número máximo de tokens en la respuesta
)

# Imprimir la respuesta generada
print(respuesta.choices[0].text)