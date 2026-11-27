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

## TP3

**Q1. Pourquoi charger toutes les colonnes en texte ?**

Le chargement brut évite qu'une valeur inattendue, comme une quantité `deux`, provoque une erreur ou une conversion silencieuse avant les contrôles. DuckDB garde ensuite toute la valeur telle quelle pour que les règles SQL puissent la classer.

**Q2. Qu'apprend-on du total naïf SQL ?**

Le langage ne garantit pas la fiabilité du résultat. Le SQL naïf donne 13950.6, comme le script Python naïf, parce qu'il calcule aussi les lignes invalides et les doublons; les transformations sans tests restent fausses.

**Q3. Quel avantage garde-t-on en conservant le brut ?**

Une règle erronée peut être corrigée et dbt peut être relancé sur les données originales, sans devoir redemander le fichier au fournisseur ni perdre les lignes mises en quarantaine.

**Q4. Que faudrait-il changer dans profiles.yml en entreprise, et où mettre le mot de passe ?**

Il faudrait remplacer `type: duckdb` et `path: warehouse.duckdb` par l'adaptateur, le compte, l'entrepôt et les paramètres du système cible, par exemple Snowflake. Le mot de passe doit être placé dans une variable d'environnement ou un gestionnaire de secrets, jamais dans le fichier YAML versionné.

**Q5. Pourquoi garder la commande 1013 dans stg_orders ?**

Le staging ne fait que typer et réparer les colonnes. Garder la ligne permet à la couche intermédiaire de la détecter comme `invalid_date` et de la conserver dans la quarantaine avec une trace.

**Q6. stg_orders est-il recalculé à chaque lecture ?**

Oui, une vue enregistre la requête SQL mais ne stocke pas les données. Chaque lecture rejoue le SQL depuis la source brute, ce qui convient au staging puisqu'une modification de la source ou du SQL est visible immédiatement.

**Q7. Par quoi dbt remplace-t-il {{ ref('stg_orders') }} ?**

Dans le modèle compilé, dbt remplace la référence par le nom relationnel concret `main.stg_orders`, après avoir établi la dépendance entre les modèles.

**Q8. Que fait row_number() pour les doublons ?**

`partition by order_id order by _row_number` numérote les lignes de chaque commande selon leur position dans le fichier. La première ligne reçoit 1 et reste acceptée; les suivantes reçoivent un numéro supérieur à 1 et sont marquées `duplicate_order_id`. `_row_number` permet donc de reproduire `keep="first"`.

**Q9. Où ajouter le chiffre d'affaires par produit ?**

Un analyste crée un modèle SQL `models/marts/revenue_by_product.sql`. Il n'a pas besoin de modifier le code Python.

**Q10. Quel test échoue si la règle 5 est supprimée ?**

Le test générique `unique_orders_clean_order_id` échoue. dbt construit quand même le test sur `int_orders_checked`, puis saute `revenue_by_country` et son test unique, ainsi que les enfants dépendants. Cela empêche toute publication d'un rapport contenant des doublons.

**Q11. Tableau des équivalents dbt**

| Contrôle du TP1 (Python) | Son équivalent dbt |
|---|---|
| `check_schema` | Sources déclarées et colonnes attendues par le modèle staging |
| Les règles 1 à 6 dans `clean_orders` | Modèle `int_orders_checked.sql` avec la règle `CASE` |
| `check_reject_rate` | `assert_reject_rate_below_20_percent.sql` |
| `rejected_orders.csv` | Table mart `orders_rejected` |
| `PIPELINE STOPPED`, rien n'est publié | `dbt build` échoue avec les modèles dépendants en `SKIP` |

**Q12. D'où viennent les données du test unitaire ?**

Elles viennent du bloc `given` écrit dans `int_orders_checked.yml`. Elles sont fabriquées directement dans le test, sans `load_raw.py` ni CSV, donc elles restent disponibles en CI.

**Q13. Quels modèles sont touchés si country arrive vide ?**

Le graphe montre que `stg_orders`, `int_orders_checked`, `orders_clean`, `orders_rejected` et `revenue_by_country` sont descendants ou dépendants de la source. Sans graphe, dans 200 scripts SQL, il faudrait rechercher manuellement les références à `country` et les dépendances, ce qui prendrait beaucoup plus longtemps.

**Q14. Tableau des jours 2 et 3**

| | Pipeline Python (TP1) | Pipeline dbt (TP3) |
|---|---|---|
| Jour 2 : contrôle arrêtant la chaîne | Taux de rejet supérieur à 20 % | `assert_reject_rate_below_20_percent` |
| Jour 3 : message d'erreur | Colonne `unit_price` manquante / renommée en `price` | `Table "src" does not have a column named "unit_price"` |
| Rapport de la veille conservé | Aucun nouveau rapport publié | Oui, `revenue_by_country` reste à 8835.40 |
| Code de sortie | 1 | 1 |

**Q15. orders_rejected est-il problématique au jour 2 ?**

Il n'est pas une copie fiable du jour 2, car dbt l'a placé en SKIP et a conservé la table du jour 1. Pour garder les rejets du jour 2 tout en bloquant le rapport, il faudrait construire une table de quarantaine avant le test de taux et la versionner ou écrire ses rejets dans un emplacement horodaté, par exemple `orders_rejected_2026-10-06`, indépendamment du mart du rapport directeur.

**Dernière ligne dbt build sur le jour 1**

```text
Done. PASS=14 WARN=0 ERROR=0 SKIP=0 NO-OP=0 REUSED=0 TOTAL=14
```
