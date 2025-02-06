# BTC_prediction_lstm

Prédiction du prix du BTC avec un LSTM

- `btc.csv` : contient les données
- `lstm.py` : contient le code pour récupérer les données, les formater, et le LSTM (Long Short-Term Memory) à entraîner et utiliser pour la prédiction
- `PFE_HPDA` : donne du contexte à mon projet (projet de fin d'études)

## Objectif

Mon but premier était de faire du scalping (trading sur les cryptomonnaies à très court terme, de l'ordre de quelques minutes) en utilisant l'effet de levier (contrats à terme - futures).


Mettons que le BTC monte de 0.12% en l'espace d'une minute, ce qui est réaliste, et que l'on parie une somme de 100 euros avec un effet de levier de 100. Cela donne une somme totale réelle de 100 * 100 = 10,000 euros. Si le BTC monte de 0.1%, les dividendes reçues sont 0.1% * 10,000 = 100 euros, soit la somme initialement investie. Ainsi, on gagne la somme investie en l'espace de quelques minutes. À cela, il faut soustraire les frais de taker (commission de la plateforme de trading). Chez MEXC.com, ils étaient de 0.01% par ordre. Soit 0.01% * 10,000 = 10 euro, fois deux car il y a deux ordres (achat et vente). Donc, la somme réelle obtenue est 100 - 20 = 80 euros.


On peut faire un long (achat au plus bas puis revente au plus haut) ou un short (vente au plus haut puis achat au plus bas), ce qui signifie que l'on peut faire du profit sur la baisse ou l'élévation du BTC.


Le risque avec l'effet de levier est la limite de contre. Si l'on a acheté au plus bas pour revendre au plus haut, avec effet de levier, et que la valeur baisse, même faiblement, on perd notre somme investie (100 euros) si la valeur franchit une valeur limite calculée. La somme initiale investie est 100 euros, si la somme réellement investie perd 100 euros, alors la vente est automatiquement déclenchée par la plateforme. De cette manière, la plateforme ne perd aucun argent. 100 euros constituent 0.1% de 10,000 euros, donc si le BTC perd 0.1%, l'acte de vente est déclenché. Ainsi, la valeur limite de vente est :

- Prix du BTC à l'achat - 0.1% * prix du BTC à l'achat si le trade est un long
- Prix du BTC à l'achat + 0.1% * prix du BTC à l'achat si le trade est un short


Le gain est  :  

variation en pourcents du BTC * (mise initiale investie*effet de levier) - frais de taker par ordre en pourcents * 2 

soit  ( variation en pourcents du BTC  - frais de taker par ordre en pourcents * 2)  * (mise initiale investie * effet de levier)

 soit en réalité : 

 ( 0.12 - 0.02) * ( 100 * 100) = 100 

Pour une variation de 0.12%, le gain est celui de la somme initiale investie, soit 100 euros.

Ce n'est pas un jeu à somme nulle, car il faut compter les frais de taker, et la différence entre le gain progressif et la valeur limite à contre qui elle se fait d'un coup.

En utilisant un modèle d'IA, on peut prédire la valeur du BTC, et on peut établir une courbe de risque pour le scalping. Le scalping est risqué, et on peut limiter les risques à un certain seuil en modifiant la somme initiale investie, le temps entre l'achat et la vente, et la confiance établie dans la prédiction.



Les modèles comme les LSTM sont obsolètes depuis longtemps et les modèles d'IA basés sur l'architecture Transformers ont montré leur efficacité depuis longtemps. Sur https://paperswithcode.com/task/time-series-forecasting, on peut voir les modèles de Time-series forecasting open-source les plus performants à l'heure actuelle (SOTA).

Selon moi, en particulier pour le scalping, les modèles basés sur l'apprentissage de motifs dans les courbes seraient idéals pour la prédiction de valeurs. En apprenant sur les graphiques, et en regardant la courbe du BTC en temps réel, l'IA peut fournir une prédiction basée sur son apprentissage des motifs ultérieurs, en fournissant une probabilité de hausse ou baisse basée sur le motif de la courbe actuelle et en regardant si la valeur avait baissé ou monté dans les motifs ultérieurs qui lui ressemblaient.

À cela, coupler un modèle d'IA d'évaluation de risque, en jouant sur les paramètres de la somme investie, du temps écoulé entre l'ordre d'achat et de l'ordre de vente, ou de la confiance sur le modèle de prédiction, et on peut investir en conditions réelles.

## Projet Bokeh

Le dossier `bokeh` est un projet plus élaboré où est utilisée la librairie Bokeh pour faire de l'affichage en temps réel (actualisation chaque seconde) du BTC, avec une courbe de prédiction. Les données (prix, volume, date) sont récupérées via l'API MEXC, et les prédictions sont faites via TimeGPT de Nixtla.io (extrêmement précis, même pour les prédictions à court terme), dorénavant payant. En plus de l'affichage, des investissements peuvent être faits automatiquement, en utilisant l'API MEXC ou la librairie Selenium qui permet d'exécuter des actions sur un navigateur automatiquement, ou manuellement.
