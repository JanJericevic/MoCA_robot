# MiR100 environment install steps

### Table of contents
- [Dependancies](#dependencies)
- [Packages overview](#overview)
- [Installation](#installation)
- [Frequent use cases](#frequent-use-cases)

### Dependencies

- **`ROS noetic:`** full desktop version is preferred. Can install other variant dependant on your use case. Make sure to install and initialize [rosdep](http://wiki.ros.org/noetic/Installation/Ubuntu#:~:text=source%20~%2F.zshrc-,dependencies%20for%20building%20packages,-Up%20to%20now).
- **`(optional) Docker:`** when using the external roscore for controlling and MiR100 internal roscore for monitoring the robot. See [docker instructions](#working-with-docker) for details. 

### Overview
- **`mir_robot:`** [DFKI](https://www.dfki.de/web) package containing the ROS driver and config files for MiR100 robot.
- **`mir_joy_teleop:`** joystick teleoperation package.
- **`mir_rest_api:`** MiR100 REST API. Allows direct requests or requests using a ROS service.

## Installation

### Create ROS workspace and source it

```
$ mkdir -p ~/MiR100/ws/src
$ cd ~/MiR100/ws/
$ catkin_make
$ source devel/setup.bash

# add workspace to .bashrc
$ echo "source ~/MiR100/ws/devel/setup.bash" >> ~/.bashrc
```
You can check if workspace is sourced correctly with:

```
$ echo $ROS_PACKAGE_PATH
/home/<youruser>/MiR100/ws/src:/opt/ros/noetic/share
```

### Install `mir_robot` package
We are using the source install. For other options see the package [github page](https://github.com/DFKI-NI/mir_robot#mir_robot).

```
# clone mir_robot into the catkin workspace
$ cd ~/MiR100/ws/src/
$ git clone -b noetic https://github.com/DFKI-NI/mir_robot.git

# update and install packages
$ sudo apt update \
&& sudo apt upgrade -y \
&& sudo apt install -y --no-install-recommends python3-catkin-lint python3-catkin-tools


# use rosdep to install all dependencies
$ rosdep update
$ rosdep install --from-paths ./ -i -y --rosdistro noetic 

# build all packages in the workspace
$ source /opt/ros/noetic/setup.bash
$ catkin_init_workspace
$ cd ~/MiR100/ws
$ catkin_make -DCMAKE_BUILD_TYPE=RelWithDebugInfo
```

### Install `mir_joy_teleop` package
TODO: package link

```
# package requires ROS joy package
$ sudo apt install ros-noetic-joy

# add mir_joy_teleop package to workspace and build workspace
$ cd ~/MiR100/ws
$ catkin_make
```

### Install `mir_rest_api` package
TODO: package link

```
# add mir_rest_api package to workspace and build workspace
$ cd ~/MiR100/ws
$ catkin_make
```

## Working with Docker:
The `mir_robot` package and in turn `mir_driver` use the external computer roscore to control the MiR100 robot. With the OS wide ROS install you can only simultaneously use either the external computer roscore for controlling the robot or connect to the internal MiR100 computer roscore for monitoring. Using docker containers you can do both.  

### Install Docker engine
Full install instructions are available at Dockers [official website](https://docs.docker.com/engine/install/ubuntu/).
Make sure old versions od Docker engine are [uninstalled](https://docs.docker.com/engine/install/ubuntu/#uninstall-docker-engine).

```
# Update the apt package index and install packages to allow apt to use a repository over HTTPS:
$ sudo apt-get update
$ sudo apt-get install ca-certificates curl gnupg

# Add Docker’s official GPG key
$ sudo install -m 0755 -d /etc/apt/keyrings
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
$ sudo chmod a+r /etc/apt/keyrings/docker.gpg

# set up the repository
$ echo \
  "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update the apt package index
$ sudo apt-get update

# install the latest version
$ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# verify the installation
$ sudo docker run hello-world
```

#### Optional post installation steps
All optional installation steps are available at Dockers [official website](https://docs.docker.com/engine/install/linux-postinstall/).  
Useful post installation step is to manage Docker as a non sudo user. This allow the omission of `sudo` in front of docker commands. When allowing this make sure to be aware of how this [impacts security of your system](https://docs.docker.com/engine/security/#docker-daemon-attack-surface).

```
# Create the docker group
# On some Linux distributions, the system automatically creates this group when installing Docker Engine using a package manager
$ sudo groupadd docker

# Add your user to the docker group
$ sudo usermod -aG docker $USER

# Log out and log back in so that your group membership is re-evaluated
# or un the following command to activate the changes to groups
$ newgrp docker

# Verify that you can run docker commands without sudo
$ docker run hello-world
```

### Building the image

If all you want is to connect to the MiR100 roscore for monitoring all you need is a ROS Docker image. We will build a custom ROS Docker image complete with the same ROS packages so you have a choice in running the project locally or using Docker containers.

Depending on your use case you will use the Docker image during development or you will only use it for deployment. For development see the [volume mounting]() section. For deployment see the [copying files]() section.

**TODO**
- dockerfile names
- dockerignore

#### Volume mounting

```
docker build -t mir-ros --build-arg MYUID=$(id -u) --build-arg MYGID=$(id -g) --build-arg MYUSER=$(id -nu) --build-arg MYGROUP=$(id -ng) .
```

#### Copying files

## Frequent use cases:
