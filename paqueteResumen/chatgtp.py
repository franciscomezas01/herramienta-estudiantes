import openai
# Define tu clave de API
api_key = "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"

# Inicializa el cliente de OpenAI con tu clave de API
openai.api_key = api_key

# Inicia una conversación con ChatGPT
response = openai.Completion.create(
    engine="davinci",
    prompt="Háblame sobre el clima en París.",
    max_tokens=50  # Define la longitud máxima de la respuesta
)

# Obtiene la respuesta generada por ChatGPT
message = response.choices[0].text

# Imprime la respuesta
print(message)
