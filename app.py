import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Put your key here
openai.api_key = "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"

# TODO: Test and modify variations of this prompt
# I want variations of the prompt that make it adhere to the script a bit less
# Initialize history with a system context prompt
INITIAL_HISTORY = [{
    "role": "system",
    "content": '''You are a helpful, compassionate, assistant and well listening companion. Try to be conversational. The user has a major stressor in their life and you should assist them in guiding them through the stressor.
                Help them work through their stressors by performing a Reflective Questioning Activity. Some guides on questions to ask are:
                What’s the situation? Feel free to explain it in as much detail as you’d like.
                What part of the situation is most troubling?
                What are you thinking to yourself?
                What thought is the most troubling?
                What do you feel when you think this?
                When you have these feelings, what actions do you take? What actions do you avoid?
                Ask the user to re-type a summary of the situation in the following format: Trigger: Thought: Feeling: Behavior
                Consider whether the trigger truly justifies this type of thinking. Explain below.
                If you were to explore an alternative line of thinking, how would you do it?
            '''
},
    {
        "role": "assistant",
        "content": "Think of a particular situation where you felt stressed or had a negative emotion, which you can try to reflect on as you go through this activity. It could be a current situation, one in the past, or one you anticipate in the future."
    }
]

history = INITIAL_HISTORY


# Temperature < 1 seemed to be very strict in following the guidelines
# Temperature range 0 - 2
# TODO: Test effects of different temperature, top_p, frequency_penalty, and presence_penalty
def get_completion(prompt, model="gpt-3.5-turbo"):
    # Append the users input to the context HISTORY
    history.append({"role": "user", "content": prompt})
    print(history)

    response = openai.ChatCompletion.create(
        model=model,
        messages=history,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.10,
        presence_penalty=0.10
    )
    print(response)
    history.append({"role": "assistant", "content": response.choices[0].message["content"]})
    return response.choices[0].message["content"]


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_completion(userText)
    # return str(bot.get_response(userText))
    return response


@app.route("/clear", methods=['POST'])
def clear_chat():
    global history 
    history = INITIAL_HISTORY
    return "True"


if __name__ == '__main__':
    app.run()
