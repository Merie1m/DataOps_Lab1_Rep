# Compte rendu - TP1

Binome : Nom1 et Nom2

**Q1. Pourquoi écrit-on les bibliothèques dans requirements.txt au lieu de taper simplement pip install pandas ?**

Pour que le projet soit reproductible : n'importe qui recrée le même environnement avec pip install -r requirements.txt. Avec pip install pandas tapé à la main, rien n'est écrit ni partagé.

**Q2. La boutique vend dans cinq pays. Combien de lignes le rapport affiche-t-il ? Pourquoi ?**

8 lignes au lieu de 5, car Tunisia, tunisia, " Tunisia", Morocco et MOROCCO sont vus comme des pays différents.

**Q3. Problèmes dans le fichier (order_id et dimension)**

| order_id | Problème | Dimension |
|---|---|---|
| 1008 | customer_id vide | Complétude |
| 1010 | ligne en double | Unicité |
| 1004 | quantité négative | Validité |
| 1013 | date impossible (2026-13-45) | Validité |
| 1006, 1016, 1023 | casse et espaces dans country | Cohérence |
| 1019 | prix 4500 au lieu de 45 | Exactitude |

**Q4. Le total est-il trop haut ou trop bas ?**

Trop haut : le doublon 1010 et le prix de 1019 (+4455) le font monter, seule la quantité négative 1004 le baisse.

**Q5. Qu'a-t-on gagné en découpant le script en fonctions ?**

(1) On peut tester chaque étape séparément. (2) On peut modifier ou réutiliser une étape sans toucher aux autres et localiser plus vite une erreur.

**Q6. Quel est le bon total ? De combien l'ancien script se trompait-il ?**

Le bon total est 7655.90. L'ancien script (12771.10) était trop haut d'environ 67 %.

**Q7. Quelle commande a causé l'essentiel de l'erreur ? Quelle règle l'a attrapée ?**

La commande 1019 (prix 4500 au lieu de 45), attrapée par la règle 4 (invalid_unit_price).

**Q8. Pourquoi enregistre-t-on les lignes rejetées dans un fichier ?**

Pour les examiner, les corriger à la source et les retraiter, au lieu de perdre des données sans trace.

**Q9. Que s'est-il passé quand vous avez cassé la règle 3 ? Quel test a échoué ?**

Avec > -5, la quantité -2 n'était plus rejetée. Le test test_negative_quantity_is_rejected a échoué (1 failed, 4 passed). Après retour à > 0, 5 passed.

**Q10. Que vérifie un test unitaire, et que vérifie un contrôle de données ?**

Un test unitaire vérifie que mon code est juste, sur un petit tableau écrit à la main. Un contrôle de données vérifie que les données du jour sont acceptables, sur les vraies données.

**Q11. Tableau jours 2 et 3**

| | Ancien script | Votre pipeline |
|---|---|---|
| Jour 2 : message d'erreur ? | Non | Oui (PIPELINE STOPPED, rejet 100 %) |
| Jour 2 : total affiché | Un total énorme | Aucun, rien n'est publié |
| Jour 3 : message d'erreur ? | Oui (KeyError: 'unit_price') | Oui (Missing columns: ['unit_price']) |

**Q12. Qu'est-ce qui a changé dans le système source au jour 2 ? Au jour 3 ?**

Jour 2 : les prix sont multipliés par 100 (centimes au lieu d'euros). Jour 3 : la colonne unit_price est renommée price.

**Q13. Sans pipeline, quel jour est le plus dangereux ?**

Le jour 2 : le script ne plante pas et affiche un total faux sans que personne ne le remarque. Le jour 3 plante bruyamment.

**Q14. Qui ou quoi peut utiliser le code de sortie 1 ?**

Un orchestrateur, un serveur d'intégration continue ou un autre script, pour arrêter la chaîne et déclencher une alerte.
