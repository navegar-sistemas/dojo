# Tutorial do A-Maze-ing

Site em Docusaurus com o passo a passo de implementação do A-Maze-ing.

```sh
npm install
npm start          # servidor local com recarga automática
npm run build      # site estático em build/
npm run serve      # serve o build/
```

As páginas ficam em `docs/`, uma pasta por parte. A ordem vem do `_category_.json` de cada pasta
e do `sidebar_position` de cada página.

As imagens de `static/img/` são SVG gerados pelos scripts de `scripts/` a partir de labirintos
reais. Cada script recebe a raiz de uma implementação pronta do A-Maze-ing, de onde importa o
`mazegen`:

```sh
for script in scripts/imagens_*.py; do
  ../project-validate/.venv/bin/python -B "$script" ../project-validate
done
```
