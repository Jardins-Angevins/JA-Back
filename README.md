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

## API

Ce service backend met à disposition une API avec 4 endpoints répondant en JSON :

<table>
	<thead>
		<tr>
			<th> Chemin </th>
			<th> Méthode </th>
			<th> Description </th>
			<th> Paramètres </th>
			<th> HTTP Response code </th>
			<th> Response fields </th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td rowspan="2"> /statistics </td>
			<td rowspan="2"> GET </td>
			<td rowspan="2"> Statistics of the application </td>
			<td rowspan="2"> ∅ </td>
			<td > 200 : Ok </td>
			<td> 
				Single object with :
				<ul>
					<li> pictureCount : int</li>
					<li> contributionCount : int </li>
					<li> downloadCount : string </li>
					<li> speciesCount : int </li>
					<li> plantsCount : int </li>
				</ul>
			</td>
		</tr>
		<tr>
			<td> 500 : Internal server error </td>
			<td> ∅ </td>
		</tr>
		<!-- - -->
		<tr>
			<td rowspan="4"> /map </td>
			<td rowspan="4"> GET </td>
			<td rowspan="4"> Returns  a list of point corresponding to scanned plants </td>
			<td rowspan="4"> 
				<ul>
					<li> <b>*</b> lat : float </li>
					<li> <b>*</b> long : float </li>
					<li> <b>*</b> dlat : float </li>
					<li> <b>*</b> dlong : float </li>
					<li> species : int </li>
					<li> year : int </li>
				</ul>
			</td>
			<td > 200 : Ok </td>
			<td> 
				Array of :
				<ul>
					<li> lat : float </li>
					<li> long : float </li>
					<li> speciesId : int </li>
					<li> timestamp : int </li>
				</ul>
			</td>
		</tr>
		<tr>
			<td> 500 : Internal server error </td>
			<td> ∅ </td>
		</tr>
		<tr>
			<td> 400 : Invalid request </td>
			<td> ∅ </td>
		</tr>
		<tr>
			<td> 416 : Too wide area </td>
			<td> ∅ </td>
		</tr>
		<!-- - -->
		<tr>
			<td rowspan="4"> /species </td>
			<td rowspan="4"> GET </td>
			<td rowspan="4"> Returns information about the given species id  </td>
			<td rowspan="4"> 
				<ul>
					<li> <b>*</b> id : int </li>
				</ul>
			</td>
			<td > 200 : Ok </td>
			<td> 
				Single object with :
				<ul>
					<li> name : string </li>
					<li> scientificName : string </li>
					<li> stats.water : int </li>
					<li> stats.light : int </li>
					<li> stats.toxicity : int </li>
					<li> refImage : string <i>Base64 image</i> </li>
					<li> desc : string </li>
				</ul>
			</td>
		</tr>
		<tr>
			<td> 500 : Internal server error </td>
			<td> ∅ </td>
		</tr>
		<tr>
			<td> 400 : Invalid request </td>
			<td> ∅ </td>
		</tr>
		<tr>
			<td> 404 : No matching species </td>
			<td> ∅ </td>
		</tr>
		<!-- - -->
		<tr>
			<td rowspan="3"> /query </td>
			<td rowspan="3"> POST </td>
			<td rowspan="3"> Adds the given entry to the database </td>
			<td rowspan="3"> 
				Parsed as json in the request body : 
				<ul>
					<li> <b>*</b> lat : float </li>
					<li> <b>*</b> long : float </li>
					<li> <b>*</b> img : string </li>
				</ul>
			</td>
			<td > 200 : Ok </td>
			<td> 
				Single object with :
				<ul>
					<li> speciesId : int </li>
				</ul>
			</td>
		</tr>
		<tr>
			<td> 400 : Invalid request </td>
			<td> ∅ </td>
		</tr>
		<tr>
			<td> 500 : Internal server error </td>
			<td> ∅ </td>
		</tr>
	</tbody>
</table>


### Commande utile
Pour lancer la création de fake data :
> ```bash
> docker-compose exec web python3 faker.py`
> ```

Pour lancer le projet
> ```back
> docker-compose build
> docker-compose up -d database
> sleep 3 #Attente de quelques seconde pour le lancement de cassandra
> docker-compose up -d web
> ```