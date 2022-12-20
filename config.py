config = {
    "max_tokens": "128",
    "voice":"1", # 0 for male, 1 for female
    "logging_level":"INFO",
    "model": "text-davinci-003", # check the OpenAI documentation for a full list of models here https://beta.openai.com/docs/models/gpt-3
    "temperature": "0.9"
}


max_tokens = int(config["max_tokens"])
voice = int(config["voice"])
logging_level = config["logging_level"]
model = config["model"]
temperature = float(config["temperature"])