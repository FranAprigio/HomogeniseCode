# How to run Homogenise


## Via Docker
Docker is the preferred way to run the application.

### Requirements
You'll need some tools to run it via Docker.
- Docker (Either Docker CLI or Docker Desktop)
- Docker Composer

### Installing The tools
Before you run Homogenise, you'll need to install the tools cited in the Requirements section.
The steps vary on Windows or Linux.

#### Linux
##### Docker
There are various methods to install Docker on your Linux, and the best way is to follow the guide available on the following repo:

https://github.com/docker/docker-install

> [!WARNING]
> 
>It's recommended to install via the rootless path due 
> It can become an attack surface because running Docker with ``sudo`` will run the code inside the container as root.


##### Docker Composer
For Docker compose on Linux, you should use the following guide available on the docker website:

https://docs.docker.com/compose/install/

#### Windows

##### Docker
For Docker on Windows, you can download the Docker desktop on Linux, making it more manageable.

Please follow the guide available on the Docker Website:

https://docs.docker.com/desktop/install/windows-install/



##### Docker Composer
Docker Composer comes bundled with Docker Desktop, so manually installing this plugin is unnecessary.

### Running The Application
#### Linux
##### Introduction
You are almost there to run the application, but before we break it down,
The Docker Composer created to run the application creates two containers,
One is the application Homogenise itself, and the other is a Postgres version 13 database.
Both containers are needed for the app to work correctly.

The process will take two steps to start the application.
- Cloning the Repository
- Running the ```start.sh``` script

##### Cloning the repository
It's the more accessible part of the process.
However, you need the application source code to create and run the Docker image as the application container.

To clone, you need to do the following thing on a terminal:
properly
``` git clone https://github.com/FranAprigio/HomogeniseCode.git ```

After that, you need to change to the directory created by the clone:

``` cd HomogeniseCode```

##### Running the ```start.sh```:

You can run the application using a supplied script to bootstrap the image creation and containers.

For that, all you need is to do two steps:
- Change the script to have the executable flag
- Run the Script

###### Change the script to have the executable flag
This step is relatively easy to do. All you need to do is to issue the following command:

``` sudo chmod +x start.sh```

###### Run the Script
Finally, to start the application, all you need is to run the command:

``` ./start.sh ```

> [!NOTE]
> 
>If you are Running Docker without being rootless, you'll need to add a sudo on command call, like this:
> ``` sudo ./start.sh```
> 
>Or the script will not work correctly.

###### What does the script do?
The script will create a Docker network if it still needs to be designed and run a Docker compose to run the file with the same name, thus running the application.

#### Windows
TBD

## Manually
Manually running the Homogenise Application on your machine differs from the preferred method, but it is possible.
