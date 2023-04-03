# CJX - CLI for JavaFX

![GitHub release (latest by date)](https://img.shields.io/github/v/release/dagimg-dot/cjx-cli-tool)
![GitHub](https://img.shields.io/github/license/dagimg-dot/cjx-cli-tool)
![GitHub All Releases](https://img.shields.io/github/downloads/dagimg-dot/cjx-cli-tool/total)
![GitHub Repo stars](https://img.shields.io/github/stars/dagimg-dot/cjx-cli-tool?style=social)
<br> <br>
This is cjx cli. It can be used to setup your JavaFX development environment using VS Code as your IDE. 

<div align = 'center'><strong>Don't forget to star the project if you like it and find it useful ✌️</strong></div>

## Prerequisites

1. [Java 11 or higher](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)
2. [VS Code](https://code.visualstudio.com/download)
3. [VS Code Java Extension Pack](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)
4. [JavaFX SDK](https://gluonhq.com/products/javafx/)
5. [Git](https://git-scm.com/downloads)
6. [Scene Builder Extenstion for VS Code](https://marketplace.visualstudio.com/items?itemName=bilalekrem.scenebuilderextension)

### JavaFX SDK

1. After downloading the JavaFX SDK, extract the zip file in a place where you can easily access (`C:/` is recommended)
2. Remember the path of the extracted folder, you will need it later


## CJX Installation

1. Download the latest release from [here](https://github.com/dagimg-dot/cjx-cli-tool/releases)
    - Download the zip file in the assets section
2. Extract the zip file
3. Open the **cjx** folder inside the extracted folder
4. Open terminal (`command prompt is recommended` ) inside the `cjx` folder and type `cjx init` to initialize your CJX CLI. You should see the following output: **`CJX CLI initialized successfully`**
5. Type `cjx set-path` to set the path of the CJX CLI. You should see the following output: **`CJX CLI path successfully set to <Your current directory>`**
5. Copy the path of the cjx folder inside the extracted folder
6. Add the path you copied to your PATH environment variable
7. Open a new terminal and type `cjx` to check if it is installed correctly. If it is installed correctly, you should see the following output: **`CJX CLI`** and other paragraph that explains how to use the CLI. 
8. You can type `cjx -h` to see all the commands available.
9. Now you can use cjx to setup your JavaFX development environment

## Setup your JavaFX development environment

1. Open terminal from any directory you want.
2. type `cjx setup <JavaSDK Dirercory>`
3. The JavaFX SDK directory is the path of the extracted JavaFX SDK folder you downloaded earlier. You should see the following output: **`JavaFX SDK path set successfully to <JavaFX SDK Directory>`**
4. Now you can use cjx to create a new JavaFX project
5. Run `cjx doctor` to check if everything is setup correctly
6. If there is any error, go back and check if you have done everything correctly
## CJX Commands

### 1. cjx init

This command initializes the CJX CLI. You should run this command only once inside the cjx folder.

### 2. cjx set-path

This command sets the path of the CJX CLI. You should run this command only once inside the cjx folder.

### 3. cjx setup `<JavaFX SDK Directory>`

This command sets the path of the JavaFX SDK. You should run this command only once.

### 4. cjx create

This command creates a new JavaFX project. You can use this command to create a new JavaFX project.

#### 1. Simple Project

`cjx create simple <Project Name>`

#### 2. jfxml Project

`cjx create jfxml <Project Name>`

### 5. cjx clone `<Project URL>`

This command clones a JavaFX project from a git repository and set it up for offline development in your local machine and configures all the needed settings for VS Code.


### 6. cjx doctor 

This command checks if everything is setup correctly. You can use this command to check if everything is setup correctly.

## Updating CJX CLI

1. Open the cjxupdate folder inside the zip file you downloaded
2. Open command prompt inside the cjxupdate folder
3. Type `cjxupdate -c` to check for updates
4. If there is an update, you will see the following output: **`A new version is available`**
5. Type `cjxupdate -u` to update the CJX CLI
6. You can check the version of the CJX CLI by typing `cjx -v` after the update is complete

---
### Caution: If you are currently using v2.2 or less, you should update to v3.0 manually by downloading v3.0 from the releases page.
---

## Common Errors

### Error: `cjx is not recognized as an internal or external command`

If you face this problem when trying to run the command `cjx init` inside the folder you extracted the cjx zip file. Try to add the path of the cjx folder to your PATH environment variable. You can follow this [tutorial](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) to add the path to your PATH environment variable.

### Error: `cjx sdk path is not set`

If you face this problem when trying to run the command `cjx create simple <Project Name>` or `cjx create jfxml <Project Name>`. Try to run the command `cjx setup <JavaFX SDK Directory>` to set the path of the JavaFX SDK. You can find the JavaFX SDK directory in the Prerequisites section.


