# Exercício

Análise de dados de logs. Prof. Leonardo Afonso Amorim.

**Requerimentos**

- Python >= 9.0
- [poetry](https://python-poetry.org/docs/#installation)

**Setup**

```bash
poetry install
```

Dentro do diretório data, descompactar os arquivos

**Run**

Python

```bash
poetry run python python.py
```

Pandas

```bash
poetry run python pandas.py
```

## Enunciado

Faça uma análise de dados de logs a fim de responder as seguintes perguntas:

1. Qual é o número distintos de hosts no mês de julho e agosto?
2. Qual é o número de consultas que retornam erro do tipo 404 no mês de julho e agosto?
3. Retorne as 5 primeiras URLs com mais erros 404
4. Retorne a quantidade de bytes acumulados ou processados neste servidor web no mês de julho e agosto

O Exercício deve ser implementando em duas versões, uma utilizando os métodos nativos do python, outra, utilizando a
biblioteca Pandas para manipulação do Dataframe.
