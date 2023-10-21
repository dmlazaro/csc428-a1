import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Put your key here
openai.api_key = "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"

current_q = 0

questions = [
    "What’s the situation? Feel free to explain it in as much detail as you’d like.",
    "What part of the situation is most troubling?",
    "What are you thinking to yourself?",
    "What thought is the most troubling?",
    "What do you feel when you think this?",
    "When you have these feelings, what actions do you take? What actions do you avoid?",
    "Re-type the summary of the situation in the following format:\n\tTrigger:\n\tThought:\n\tFeeling:\n\tBehavior:",
    "Consider whether the trigger truly justifies this type of thinking. Write your thoughts.",
    "If you were to explore an alternative line of thinking, how would you do it?",
]

# TODO: Test and modify variations of this prompt
# I want variations of the prompt that make it adhere to the script a bit less
# Initialize history with a system context prompt
history = [{
    "role": "system",
    "content": '''You are a helpful assistant and well listening companion. The user has a major stressor in their life and you should assist them in guiding them through the stressor. The user will be answering:
                “Think of a particular situation where you felt stressed or had a negative emotion, which you can try to reflect on as you go through this activity. It could be a current situation, one in the past, or one you anticipate in the future.”
                
                Help them work through their stressors by performing a Reflective Questioning Activity. Some guides on questions to ask are:

                What’s the situation? Feel free to explain it in as much detail as you’d like.
                What part of the situation is most troubling?
                What are you thinking to yourself?
                What thought is the most troubling?
                What do you feel when you think this?
                When you have these feelings, what actions do you take? What actions do you avoid?
                Re-type the summary of the situation in the following format: Trigger: Thought: Feeling: Behavior
                Consider whether the trigger truly justifies this type of thinking. Explain below.
                If you were to explore an alternative line of thinking, how would you do it?
            '''
}]


# Temperature < 1 seemed to be very strict in following the guidelines
# Temperature range 0 - 2
# TODO: Test effects of different temperature, top_p, frequency_penalty, and presence_penalty
def get_completion(prompt, model="gpt-3.5-turbo"):
    # Append the users input to the context history
    history.append({"role": "user", "content": prompt})
    messages = history
    print(messages)

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.50,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.50,
        presence_penalty=0.25
    )
    print(response)
    history.append({"role": "assistant", "content": response.choices[0].message["content"]})
    return response.choices[0].message["content"]


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route("/next")
def next_question():
    global current_q
    current_q += 1
    if (current_q > 8):
        return get_completion("Tell the user that they have completed the Reflective Questioning Activity"
                              "Summarize the interaction, including any important insights, and then wish them well.")
    return get_completion(f"Ask the USER the following question (DO NOT ANSWER IT YOURSELF):\n\"{questions[current_q]}\"")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = get_completion(userText)
    # return str(bot.get_response(userText))
    return response


if __name__ == '__main__':
    app.run()
