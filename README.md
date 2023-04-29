# Text Summarization App

Text Summarization App is a Japanese text summarization application using Django and Transformers.
The summarization method is sentence-extractive summarization.

## Requirements

* Python 3.10
* Django 3.2.18
* Transformers 4.26.1


## Installation

```bash
$ git clone https://github.com/noriho137/text-summarization.git
$ cd text-summarization/
$ python -m venv {venv_name}
$ source {venv_name}/bin/activate
({venv_name}) $ pip install -r requirements.txt
```


## Download pretrained model and tokenizer

This application use BERT model pretrained by Japanese text.
To get pretrained BERT model and tokenizer, execute following command.

```bash
({venv_name}) $ python save_pretrained_model.py
```

Then, directory `pretrained/` will be created and save pretrained model and tokenizer.


## Generate Django secret key

Generate Django secret key by `secrets.token_urlsafe`.

```bash
({venv_name})$ python -c "import secrets; print(secrets.token_urlsafe(38))"
```


## Set up environment variables

Make ```.env``` file at project root directory and define environment variables like following:

```bash
# Django settings
export DJANGO_SECRET_KEY={Django secret key generated above}
export DJANGO_DEBUG=True

# Pretrained model
export PRETRAINED_MODEL=./pretrained/model
export PRETRAINED_TOKENIZER=./pretrained/tokenizer
export MAX_LENGTH=512
export NUMBER_OF_SENTENCES=3
```


## How to run

```bash
({venv_name})$ python manage.py runserver
```

Browse to http://127.0.0.1:8000/ .
