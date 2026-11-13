# Tutorial do Data Quest

Site em Docusaurus com o passo a passo de implementação do Data Quest, o projeto de coleções em
Python.

```sh
npm install
npm start          # servidor local com recarga automática
npm run build      # site estático em build/
npm run serve      # serve o build/
```

As páginas ficam em `docs/`, uma pasta por parte. A ordem vem do `_category_.json` de cada pasta
e do `sidebar_position` de cada página.

As imagens de `static/img/` são SVG gerados por `scripts/imagens.py` a partir dos exemplos do
enunciado. O script só usa a biblioteca padrão e gera arquivos idênticos a cada execução:

```sh
python3 scripts/imagens.py
```
