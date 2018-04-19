# Agenda de Eventos
_Um exemplo de aplicação em Django_

## Instalação

Instale a versão 3.x do **Python** e o **Virtualenv**:
1. Clone este repositório : `git clone https://github.com/plainspooky/django-agenda_de_eventos.git`
1. Vá para o repositório : `cd django-agenda_de_eventos`
1. Crie um ambiente de desenvolvimento : `virtualenv --python $( which python3 ) py3`;
1. Vá para o ambiente : `source py3/bin/activate`;
1. Instale as dependências : `pip install -r requirements.txt`;
1. Crie a base de dados : `python manage.py migrate`
1. Suba o servidor : `python manage.py runserver`
1. Acesse o programa em  127.0.0.1:8000
