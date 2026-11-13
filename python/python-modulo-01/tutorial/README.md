# Tutorial do Code Cultivation

Site em Docusaurus com o passo a passo de implementação dos sete exercícios do Code Cultivation
(python-modulo-01).

```sh
npm install
npm start          # servidor local com recarga automática
npm run build      # site estático em build/
npm run serve      # serve o build/
```

As páginas ficam em `docs/`, uma pasta por parte. A ordem vem do `_category_.json` de cada pasta
e do `sidebar_position` de cada página.

As imagens de `static/img/` são SVG gerados por `scripts/imagens.py`, que só usa a biblioteca
padrão do Python e calcula as alturas com as mesmas contas dos exercícios:

```sh
python3 scripts/imagens.py
```
