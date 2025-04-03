# Projeto Operacional

Um sistema de gestão operacional desenvolvido com Django para controle de produtos, escolas, pedidos e gerenciamento.

## Requisitos

- Python 3.8+
- Django 5.1.7
- Outras dependências listadas em `requirements.txt`

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/mma21947/Projeto-Operacional.git
cd Projeto-Operacional
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
# No Windows
venv\Scripts\activate
# No Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
DJANGO_SECRET_KEY=sua_chave_secreta_aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## Estrutura do Projeto

O projeto está organizado nos seguintes apps:

- `core`: Funcionalidades centrais e compartilhadas
- `produtos`: Gerenciamento de produtos
- `escolas`: Gerenciamento de escolas
- `pedidos`: Gerenciamento de pedidos
- `gestao`: Funcionalidades de gestão e administração

## Licença

Este projeto é de uso privado e não está disponível para redistribuição sem autorização. 