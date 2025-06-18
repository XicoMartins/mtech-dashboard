
# Dashboard de Produção - MTECH

Dashboard interativo desenvolvido em **Streamlit** para visualização e acompanhamento da produção MTECH.

---

## Funcionalidades:

* Status Operacional (Displays e Peças Prontas)
* Peças Faltantes - Solda MIG
* Estoque Intermediário - Dobra/Solda
* Filtros dinâmicos por peça
* Visualização gráfica com Plotly

---

## Como rodar localmente:

### Requisitos:

* Python 3.8 ou superior
* pip

### Instalação:

1. **Clone o repositório:**

```bash
git clone https://github.com/AdolphoBorgesSalvador/mtech-dashboard.git
cd mtech-dashboard
```

2. **Crie um ambiente virtual:**

```bash
# No Windows:
python -m venv .venv
.venv\Scripts\activate

# No Linux/Mac:
python3 -m venv .venv
source .venv/bin/activate
```

3. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

* Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

* Preencha os valores das variáveis conforme a necessidade.

---

##  Executando o projeto:

```bash
streamlit run app/main.py
```

> O dashboard abrirá no navegador na URL:
> [http://localhost:8501](http://localhost:8501)

---

## Estrutura de Pastas:

```
.
├── app/
│   ├── main.py
│   ├── layout.py
│   ├── dashboard.py
│   ├── data_loader.py
│   └── ...
├── image/
│   ├── logo.png
│   ├── industry.png
│   ├── industry-40.png
│   └── inventory-management.png
├── requirements.txt
├── .env.example
└── README.md
```


## Atualizando Dependências:

Se adicionar novas bibliotecas, gere um novo `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

MIT License

