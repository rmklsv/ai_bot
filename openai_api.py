import openai

import config


openai.api_key = config.API_TOKEN


def api_request(tasks: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Solve this tasks: " + tasks,
        temperature=0.0,
        max_tokens=500,
    )
    result = response.choices[0].text.strip()
    return result

def speech_to_text(audio_path: str) -> str:
    audio_file = open(audio_path, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    result = transcript.choises[0].text.strip()
    return result

