import openai

import config


openai.api_key = config.API_TOKEN


#@app.route("/", methods=("GET", "POST"))
def api_request(tasks: str):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Solve this tasks: " + tasks,
        temperature=0.0,
        max_tokens=500,
    )
    result = response.choices[0].text.strip()
    return result

