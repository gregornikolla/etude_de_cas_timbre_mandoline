# etude_de_cas_timbre_mandoline
Étude de cas pour le cours de PHY-1005

# Analyse Spectrale d'Enregistrements de Mandoline

Ce dépôt contient un script Python permettant d'enregistrer un son joué sur une mandoline à l'aide d'un microphone Rode NT-USB, de visualiser l'onde sonore ainsi que son spectre de fréquences, et d'analyser les amplitudes relatives des harmoniques.

## Objectif

Le but est d'illustrer expérimentalement la différence de timbre produite par deux cordes différentes jouant la même note (Sol, 196 Hz) sur une mandoline. Le script permet de comparer les composantes fréquentielles du signal audio afin d’en extraire des marqueurs objectifs du timbre.

## Fonctionnalités principales

- Enregistrement du signal sonore (`record`)
- Validation des paramètres d’enregistrement
- Calcul et affichage de la transformée de Fourier
- Tri des fréquences dominantes par groupes (pics)
- Calcul des amplitudes relatives des 10 premières harmoniques
- Moyenne sur plusieurs essais pour une analyse plus robuste
- Visualisation des résultats sur des graphiques clairs

## Dépendances

Ce script utilise les bibliothèques suivantes :

- `numpy`
- `matplotlib`
- `scipy`
- `sounddevice`

Installe-les avec pip si nécessaire :

```bash
pip install numpy matplotlib scipy sounddevice
