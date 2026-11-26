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

## TP2

**Q1. Pendant que vous travailliez sur la branche, main contenait-elle la règle 6 ? À quelle commande est-elle apparue sur main ? Pourquoi est-ce utile ?**

Non. La règle 6 n'est apparue sur main qu'après `git merge --no-ff feature/country-rule -m "Merge the country rule"`. Cela protège le rapport automatique exécuté depuis main pendant le développement de la nouvelle règle.

**Q2. Qu'apporterait une pull request sur GitHub qu'un git merge local n'apporte pas ?**

Une pull request ajoute la revue du code, des discussions, des validations automatiques, des contrôles d'accès et une trace explicite de la proposition avant sa fusion.

**Q3. Recopiez la ligne md5 de data/raw.dvc. Qu'identifie-t-elle, et que lui arriverait-il si vous changiez un seul caractère dans un CSV ?**

La ligne est `md5: 2b75ec746ea02fece82fb98df130590b.dir` pour data-v2 (elle était `md5: ed3c636d2a133a5327effed91f25d573.dir` pour data-v1). Elle identifie exactement le contenu et la structure du dossier suivi par DVC. Si un seul caractère change, DVC calcule de nouveaux hash; le md5 du fichier change et le md5 `.dir` du dossier change aussi.

**Q4. Quel fichier fait que Git ignore les CSV ?**

Le fichier [data/.gitignore](data/.gitignore), qui contient `/raw`.

**Q5. Comment sont nommés les fichiers de dvc-storage, et pourquoi est-ce utile ?**

Ils sont nommés avec leur empreinte de contenu: les deux premiers caractères forment un dossier et le reste de l'empreinte forme le nom du fichier. Plusieurs versions peuvent ainsi coexister, les fichiers identiques sont dédupliqués et les pointeurs DVC retrouvent la bonne copie.

**Q6. Pourquoi git diff data/raw.dvc suffit-il à Git, et pourquoi faut-il quand même commiter ?**

Le diff contient le nouveau md5 `.dir`, qui est la référence exacte vers le nouvel ensemble de données dans le cache distant. Il faut commiter ce pointeur pour l'associer à une version Git précise du code et de la configuration.

**Q7. Entre data-v1 et data-v2, le code a-t-il changé ? Écrivez les deux totaux.**

Le code n'a pas changé entre les deux tags; seuls les cinq commandes tardives ont été ajoutées. data-v1 donne **7655.90** et data-v2 donne **8835.40**.

**Q8. Qu'a changé git checkout data-v1 -- data/raw.dvc, puis dvc checkout ?**

`git checkout data-v1 -- data/raw.dvc` a remplacé uniquement le pointeur suivi par Git. `dvc checkout` a ensuite utilisé cet ancien pointeur pour remplacer les données sur disque par la version data-v1.

**Q9. Que se passe-t-il si vous oubliez dvc checkout, et pourquoi est-ce dangereux ?**

Le pointeur Git peut désigner data-v1 alors que les fichiers sur disque restent data-v2. Le pipeline produit un rapport avec les mauvaises données malgré un état Git ancien, ce qui rend le résultat trompeur et irréproductible.

**Q10. Qu'est-ce que git clone a donné au collègue, et qu'est-ce que dvc pull lui a donné ?**

`git clone` a donné au collègue le code, les pointeurs DVC, les tags, les commits et la configuration DVC. `dvc pull` a récupéré depuis le remote les fichiers réels correspondant au pointeur.

**Q11. Si vous aviez oublié dvc push à l'étape 4, qu'obtiendrait le collègue avec dvc pull, et quel total ?**

Le collègue ne pourrait pas télécharger les objets de data-v2 depuis le remote DVC. Avec `dvc pull`, il obtiendrait une erreur indiquant les données manquantes; il ne pourrait pas produire correctement le total 8835.40 de data-v2 depuis cette copie.

**Sortie de git log --oneline --graph --decorate**

```text
* 31fd9d4 (HEAD -> main) Describe the report as a DVC stage
* 58bf0eb (tag: data-v2) Data v2: late orders for 2026-10-05
* 53f8a98 Add the DVC remote
* 009d6aa (tag: data-v1) Track raw data with DVC
*   506260a Merge the country rule
|\  
| * 4a9942d (feature/country-rule) Reject orders from countries the shop does not sell to
|/
* 48bbda8 Finish TP1, add DVC to requirements
* 233ad5e (origin/main) Use MAX_REJECT_RATE in check_reject_rate
* b4f1a87 Add CI workflow
* cb9b4c3 Fix rule 3 and add day 2 and 3 data
* 8dedc96 Add day 2 and 3 data and report
* 92e55ad Add pipeline, data checks and unit tests
```
