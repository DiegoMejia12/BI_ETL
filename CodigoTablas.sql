create table artists(
	nombre_artista varchar(100),
	id_artista varchar(100),
	tipo varchar(100),
	uri varchar(100),
	popularidad varchar(100),
	cantidad_followers varchar(100),
	origin varchar(100),
	fecha_consulta TIMESTAMP,
	PRIMARY KEY (id_artista)
);

create table tracks(
	
	nombre_track varchar,
	tipo_track varchar,
	album varchar,
	track_number varchar,
	id_track varchar,
	nombre_artista varchar,
	id_artista varchar,
	fecha_lanzamiento varchar,
	generos varchar,
	uri varchar,
	origin varchar,
	fecha_consulta TIMESTAMP,
	PRIMARY KEY (id_track),
	FOREIGN KEY (id_artista) references artists(id_artista)
);