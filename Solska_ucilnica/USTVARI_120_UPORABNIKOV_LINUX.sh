#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
umask 077
if [[ -e "$HOME/testni_racuni.csv" ]]; then
  echo "Datoteka ~/testni_racuni.csv že obstaja. Premakni jo na varno; ne prepišem je." >&2
  exit 1
fi
sudo docker compose exec -T aplikacija python manage.py ustvari_testne_uporabnike --izvozi-gesla > "$HOME/testni_racuni.csv"
chmod 600 "$HOME/testni_racuni.csv"
echo "Končano. Gesla so shranjena samo v ~/testni_racuni.csv (ne v GitHubu)."
