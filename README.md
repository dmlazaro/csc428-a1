# CSC428 Chatbot

A simple chatbot implementing the RQA concept for A1 of CSC428

To use this chatbot, you must enter an OpenAI API key in `app.py`

## Run Project

Project is written as a simple flask server. To run, set up python virtual env:

```bash
python3 -m venv ./venv
source ./venv/bin/activate
```

With your virtual environment initialized, pip install all packages in `requirements.txt`:
```bash
pip install -r ./requirements.txt
```

Run the webserver
```bash
python3 app.py
```

Navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)
