<div align="center" style="text-align: center;">

# Jardins Angevins
## Back

</div>

## Technologies

Pour la section Back du projet nous avons mit en place une full stack orienté python avec :

 Nom           | Version       | Utilisation                    |  Icone         
---------------|---------------|--------------------------------|---------------
 Flask         | 2.2.2         | Serveur HTTP                   | <img alt="Flask icon" src="https://flask.palletsprojects.com/en/2.2.x/_static/flask-icon.png" height="25"/>
 Cassandra     | 4.1           | Base de données                | <img alt="Cassandra icon" src="https://cassandra.apache.org/assets/img/favicon.ico" height="25"/>
 Docker        | 20.10.5       | Conteneurisation & déploiement | <img alt="Docker icon" src="https://cdn.icon-icons.com/icons2/2107/PNG/512/file_type_docker_icon_130643.png" width="50" />
 DockerCompose | 1.25.0        | Conteneurisation & déploiement | <img alt="Dockercompose logo" src="https://cdn.icon-icons.com/icons2/2107/PNG/512/file_type_docker_icon_130643.png" width="50" />
 Keras         | 2.11.0        | Analyse d'images               | <img alt="KerasLogo" src="https://s3.amazonaws.com/keras.io/img/keras-logo-2018-large-1200.png" width="50" />


### Commande utile
Pour lancer la création de fake data :
> ```bash
> docker-compose exec web python3 faker.py
> ```

Pour lancer le projet
> ```back
> docker-compose up -d database
> state=1;while [[ "$state" != 0 ]]; do docker-compose exec database cqlsh -e 'describe cluster' > /dev/null ; state=$? ; done;
> docker-compose up -d web
> ```
> _La troisième commande permet d'attendre que cassandra soit complètement prêt, sinon le conteneur web se lance dès que le conteneur database est lancer et non prêt_

Pour build le projet
> ```back
> cd scrapping && python3 image_tela_botanica.py && cd ..
> docker-compose build
> ```

Pour lancer les tets, _on suppose le projet déjà lancer_
> ```back
> docker-compose exec web python3 faker.py
> docker-compose exec web python3 -m unittest $(find tests -name Test*.py)
> ```