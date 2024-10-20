# Unidad Territorial 
Desarrollar un sitio web intuitivo que facilite a las autoridades de las juntas de vecinos representar de manera eficiente a los residentes del barrio. Considerando la posibilidad de interacción de los usuarios para las gestiones de los residentes.

Esta herramienta tiene como objetivo promover el desarrollo y defender los intereses de la comunidad, mejorando la comunicación y la gestión de recursos por parte de las autorizades designadas.

## Stack

**Front-end:** JavaScript, Bootstrap, CSS  
**Back-end:** Django  
**Interacción Front-end y Back-end:** Django + JavaScript

---

## Clonar repositorio

Para la clonación e instalación del proyecto es necesario contar con Git instalado en el equipo.

Abrir la consola de Git Bash y copiar el siguiente código para hacer la clonación del repositorio:

```bash
git clone https://github.com/cvrlossj/UTProyecto.git
```

Luego, entrar a la carpeta del proyecto con el siguiente comando:
```bash
cd UTProyecto
```

Y abrir el editor de código (Visual Studio Code) con:
```bash
code .
```

## Instalación del entorno virtual

1. Una vez dentro del editor Visual Studio Code, presiona **Ctrl + Ñ** para abrir la terminal y asegúrate de estar en **PowerShell**
2. Crea un entorno virtual donde se instalarán todas las dependencias de forma local con el siguiente comando:

```bash
py -m venv venv
```

3. Luego, activa el entorno virtual con el siguiente comando:
 ```bash
venv\Scripts\activate
```

4. Instala las dependencias del proyecto de Django con:
 ```bash
pip install -r requirements.txt
```

Con esto, se instalarán todas las dependencias necesarias en el entorno virtual y estaremos listos para empezar.

## Migraciones y ejecución del servidor
Ejecuta los siguientes comandos de Django para realizar las migraciones y correr el servidor:

1. Realizar migraciones:
 ```bash
py manage.py makemigrations
```

2. Confirmar las migraciones:
 ```bash
py manage.py migrate
```

3. Correr el servidor:
 ```bash
py manage.py runserver
```

## Flujo de trabajo colaborativo
Para trabajar de forma colaborativa, seguiremos el flujo de trabajo que utiliza **Git** con **GitHub.**

* Las **ramas de desarrollo** para desplegar nuevas características serán en la rama develop.
* Una vez completadas y probadas, las características se pasarán a la rama principal **main.**

Cada vez que trabajes en una nueva característica (feature), crea una rama a partir de develop.
Una vez completada y fusionada la característica, puedes eliminar la rama localmente y continuar con otra tarea.

 ```bash
git branch -d nombre-de-la-rama-feature
```

## Otra información
* [Commits Convencionales](https://www.conventionalcommits.org/es/v1.0.0/)
* [Flujo de trabajo de Gitflow](https://www.atlassian.com/es/git/tutorials/comparing-workflows/gitflow-workflow#:~:text=%C2%BFQu%C3%A9%20es%20Gitflow%3F,vez%20y%20quien%20lo%20populariz%C3%B3.)
* [Patrón MVT: Modelo-Vista-Template](https://docs.hektorprofe.net/django/web-personal/patron-mvt-modelo-vista-template/)
