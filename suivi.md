| Back log| Description | Status | Tested | Done |
|------|-------|--------|--------|------|
|[Job Search Feed](#job-search)| Feed a channel with job opportunite| in developpment| nope| nope|
|[Code Review](#code-review)|Offer possibility to get your code review by someelse| In progress| nope | nope |
|[Documentation](#documentation)| create a library with all documentation| in progress| nope | nope |
|[Interface 42 API](#42-api)| Looking easly for your friend in the campus| in progress| nope | nope |
|[Interface 42 API](#42-api)| Find personn who have done the project on the campus and in 42 network | in progress| nope | nope |
|[Interface 42 API](#42-api) |Allow you to create and look for evaluation slot| in progress | nope | nope|
|[News Feed](#news-feed)| Feed a new channel |to improve | done | nope|
|[Mistral](#mistral)| The Discord bot leverages Mistral in the background to comprehend and generate intelligent responses to user messages.|in progress | nope | nope|
|------|-------|--------|--------|------|

# Job Search  

***
Permettre d avoir les opportutnites en web scrapping linkedin.
Creer une recurrence pour la publications des jobs, verifications des donnees

# Code Review

***
Permettre au personne le souhaitant de faire evaluer leur code par leur pair. Il n y a pas de restriction au niveau du languages. On peut egalement penser que la mise en contact entre les personnes soit une possibilite.  
Une personne soumet son code sous forme de fichier ou via le message. Les donnees sont stockee et classee. Une personne qui souhaite evaluer des codes envoie une requete. L api envoie le code en format.txt. Une notification est envoye pour dire que le code est en cours de review par le login de la personne. Une notification est envoye quand le code a ete review.  

# Documentation

***
Creer une database des differentes documentations pour chaque projets. La documentation peut etre des lectures faites a Hive. Tous ce qui peuvent a une meilleure comprehension d un sujet.  
La doc peut etre aussi pour devellopper ses soft skills

Il faut definir le moyen de stockage, sqlite semble mon choix.  
Il faudra definir une systeme de tag sur les donnees.  
Il peut etre interressant de la construire comme une API.  
Que faire si la donnees n est pas un lien internet.(Est ce qu au final,  il faut une addresse vers la donnees et cette adresse peut un lien internet ou une PATH ?)  

L' user emet une requete de consultation sur un sujet. On effectue la recherche en comparant les mots clefs au tag mis en place sur les donnees.  
On repond par les donnees trouvees ou par un message.  

#### Exemples  
Dans le cas d' une documention concernant va_arg:  
> www.lien_vers_doucmentation || tags: ft_printf, va_arg  

ou
> /Chemin/vers/data || tags: ft_printf, va_arg

# 42 API

***

## Who is on campus
Creer un moyen rapide pour savoir qui est present sur le campus actuellement ou connectea un mac, ainsi que sa localisation

## Who can help me
Je suis bloque sur un projet. Creer un moyen rapide pour trouver les personnes qui ont fait le projet ou qui travaille sur le projet. Mettre en avant ceux present sur le campus puis les personnes dans le reseaux 42.

## Create and reserve evaluation slot
Permettre la creation et la reservation d evalution depuis discord

## Monitoring Student Evolution
Permettre d analyser l evolution des etudiants pour encourager le peer to peer
Quelqu un proche de black hole lui proposait de trouver de l aider. a linverse
trop de temps on encourage pour aller aider quelqu un.

# News Feed
Alimente un channel avec des actulaites relatif au technologies

***

# Mistral
***

Mistral 7B tourne de maniere local derriere le bot discord. Probleme de tiemout. Pas de ram pour generer des reponses rapidement. Solution creer des threads pour eviter le timeout et que le bot reste bloque. A tester egalement quand plusieurs personne utilise le bot ou avec une config plus rapide
Il faudra egalement creer notre model avec les parametres souhaiter.