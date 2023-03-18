# cjx-v1.1-build
This is cjx cli. It can be used to setup your JavaFX development environment using VS Code as your IDE. 

## Prerequisites

1. [Java 11 or higher](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)
2. [VS Code](https://code.visualstudio.com/download)
3. [VS Code Java Extension Pack](https://marketplace.visualstudio.com/items?itemName=vscjava.vscode-java-pack)
4. [JavaFX SDK](https://gluonhq.com/products/javafx/)

### JavaFX SDK

1. After downloading the JavaFX SDK, extract the zip file in a place where you can easily access (`C:/` is recommended)
2. Remember the path of the extracted folder, you will need it later


## CJX Installation

1. Download the latest release from [here](https://github.com/dagimg-dot/cjx-v1.1-build.git)
2. Extract the zip file
3. Open the **cjx** folder inside the extracted folder
4. Open a terminal here and type `cjx init` to initialize your CJX CLI. You should see the following output: **`CJX CLI initialized successfully`**
5. Type `cjx set-path` to set the path of the CJX CLI. You should see the following output: **`CJX CLI path successfully set to <Your current directory>`**
5. Copy the path of the cjx folder inside the extracted folder
6. Add the path you copied before to your PATH environment variable
7. Open a new terminal and type `cjx` to check if it is installed correctly. If it is installed correctly, you should see the following output: **`Invalid Command`** This is because you didn't give it any command. You can type `cjx help` to see all the commands available
8. Now you can use cjx to setup your JavaFX development environment

## Setup your JavaFX development environment

1. Open terminal from any directory you want.
2. type `cjx setup <JavaSDK Dirercory>`
3. The JavaFX SDK directory is the path of the extracted JavaFX SDK folder you downloaded earlier. You should see the following output: **`JavaFX SDK path set successfully to <JavaFX SDK Directory>`**
4. Now you can use cjx to create a new JavaFX project
5. Run `cjx doctor` to check if everything is setup correctly
6. If there is any error, go back and check if you have done everything correctly
## CJX Commands

### cjx init

This command initializes the CJX CLI. You should run this command only once inside the cjx folder.

### cjx set-path

This command sets the path of the CJX CLI. You should run this command only once inside the cjx folder.

### cjx setup `<JavaFX SDK Directory>`

This command sets the path of the JavaFX SDK. You should run this command only once.

### cjx create

This command creates a new JavaFX project. You can use this command to create a new JavaFX project.

#### Usage `cjx create simple <Project Name>`

### cjx doctor 

This command checks if everything is setup correctly. You can use this command to check if everything is setup correctly.


