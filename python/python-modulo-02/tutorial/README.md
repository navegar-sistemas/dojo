# Tutorial do Garden Guardian

Site em Docusaurus com o passo a passo dos cinco exercícios de tratamento de exceções em Python.

```sh
npm install
npm start          # servidor local com recarga automática
npm run build      # site estático em build/
npm run serve      # serve o build/
```

As páginas ficam em `docs/`, uma pasta por parte. A ordem vem do `_category_.json` de cada pasta
e do `sidebar_position` de cada página.

As imagens SVG de `static/img/` são geradas por `scripts/imagens.py`, que só usa a biblioteca
padrão:

```sh
python3 scripts/imagens.py
```
