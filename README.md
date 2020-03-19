# ITIS6010_Mobile_Security
# Automating UnSafe API's detection in Hybrid IoT companion apps

This project aims to automate unsafe API's detection in hybrid IoT companion mobile apps. It acquires a dataset of IOT companion mobile apps by web scrapping all related IoT companion mobile apk's using scrapy framework. Then, it analyzes whether the app is hybrid or not and aims to find unsafe APIs in them. On the basis of our unsafe API analysis, we try to expose these vulnerabilities by attacking them.

## Getting Started
To use our framework, Python version 3.5 or newer and Python 2.7 are required.

### Prerequisites

The scripts are intended to be used on a Linux operating system, but it may be possible to adapt them to other operating systems. Setup instructions are provided for Ubuntu-Based operating systems.

#### Setup (Ubuntu-Based OS)

Clone and cd into this repo using the following commands:

```
cd ~
git clone https://gitlab.com/pfrankl1/itis6010_mobile_security.git
```
The web scraper assumes that the working directory is called UnsafeAPIFramework. The following command will rename the git directory as necessary:
```
mv ~/itis6010_mobile_security/ ~/UnsafeAPIFramework/
```
From a Ubuntu-based operating system, the following commands will install the necessary dependencies:
```
cd ~
sudo apt-get update
sudo apt-get install -y python3.7 python3-pip python-pip apktool virtualenv python-dev python3-dev
python3 -m pip install pip setuptools wheel
python3 -m pip install virtualenvwrapper --user
pip2 install pandas
```
Some environment variables need to be set, and the following commands will persist them:
```
cd ~
echo -e "\nexport WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo -e "\nexport PROJECT_HOME=$HOME/Devel" >> ~/.bashrc
echo -e "\nexport VIRTUALENVWRAPPER_PYTHON=/usr/bin/python" >> ~/.bashrc
echo -e "\nsource ~/.local/bin/virtualenvwrapper.sh" >> ~/.bashrc

cd ~/UnsafeAPIFramework/apkturbo/apkturbo
CURR_DIR=$(pwd)
echo -e "\nexport PYTHONPATH=$CURR_DIR" >> ~/.bashrc
```
Afterwards, two directories need to be created and these commands will load the environment variables before creating them:
```
source ~/.bashrc
mkdir $WORKON_HOME $PROJECT_HOME
```

## Obtaining Applications to Analyze

### Prerequisites

It is necessary to restart bash before attempting to make a virtual environment for the first time. This can be done with the following command:
```
exec bash
```

#### Scraping

Scraping should be performed from within a virtual environment. The following commands will create the environment, install scrapy and perform the scraping. When scraping finishes, deactivate is used to exit the virtual environment. The variable PAGECOUNT is an integer interpreted as the number of pages to be scraped. So, in the terminal enter the commands in the order.
The step 3 - mkvirtualenv env if you are installing for the first time and `workon env` env doesn't exist.
```
PAGECOUNT=1
cd ~/UnsafeAPIFramework/apkturbo
mkvirtualenv env
pip install scrapy scrapy_splash
scrapy crawl monkapks
deactivate
```
If any APK files were scraped, the web scraper created a directory called APK_DIR in the user's home directory containing them. Before analysis, the APK_DIR directory should be moved to the same directory as the analysis scripts.
```
mv ~/APK_DIR/ ~/UnsafeAPIFramework/APK_DIR/
```
The web scraper also created a log directory called SCRAPY_LOG_DIR/ in the user's home directory for logs pertaining to the web scraper.

## Analysis

### Prerequisites

First, ensure that all scripts within the analysis directory can be executed by the user.
```
chmod +x ~/UnsafeAPIFramework/*.sh
```

#### Unpacking APKs

A script has been created to automate APK unpackage. The following command will execute the script:
```
~/UnsafeAPIFramework/unpack_APKs.sh
```

#### Identifying Hybrid Mobile Applications

A script has been created to automate hybrid mobile application detection. The following command will execute the script:
```
~/UnsafeAPIFramework/find_hybrid.sh
```
Results are stored in LOG_DIR/.

#### Identifying HTML files with Unsafe APIs

A script has been created to automate unsafe API detection in HTML files. The following command will execute the script:
```
~/UnsafeAPIFramework/parse_HTML.sh
```
Results are stored in LOG_DIR/.

#### Identifying JS files with Unsafe APIs

A script has been created to automate unsafe API detection in JS files. The following command will execute the script:
```
~/UnsafeAPIFramework/parse_JS.sh
```
Results are stored in LOG_DIR/.

## Running the tests

To run the tests on this system, user has to install the framework as detailed in the above steps and in the terminal, along with the command below

```
$ scrapy crawl turboapks -a PAGECOUNT=number of pages to scrape
```

And if you want to test each individual module, by feeding your own custom test data follow the steps from "Prerequisites" section above.


### end to end tests

You can choose to supply various types of apps, native as well as hybrid.
Also, you could choose to supply various .js and .html files, minified files, framework javascript files of Cordova, ionic, ReactNative etc.

When you want to test for unsafe APIs without APK, follow the steps below:

You can diretly jump to the step:

Identifying JS files with Unsafe APIs or
Identifying HTML files with Unsafe APIs

Example:
 - create a directory named "APK_DIR" inside "UnsafeAPIFramework" directory,
 - deposit an APK file inside that you want to test. You can pack an APK file using apktool with the files you want to custom test
 - Then follow the steps in the order below:

```

~/UnsafeAPIFramework/unpack_APKs.sh
~/UnsafeAPIFramework/find_hybrid.sh
~/UnsafeAPIFramework/parse_HTML.sh
~/UnsafeAPIFramework/parse_JS.sh
```

## Deployment

- Install a virtual box - https://www.virtualbox.org/wiki/Downloads
- Choose the package as per your Operating System.
- Download Ubuntu OS image from here http://www.releases.ubuntu.com/18.04/
- Then mount the image onto the Virtual box and follow the configuration steps as detailed in the Ubuntu and VirtualBox website.


## Built With

* [Python](http://www.dropwizard.io/1.0.2/docs/) - Programming language
* [Pip](https://pypi.org/project/pip/) - Dependency Management 
* [Scrapy](http://www.dropwizard.io/1.0.2/docs/) - The web scraping framework

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [GitLab](https://gitlab.com/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.com/pfrankl1/itis6010_mobile_security). 

## Authors

* **Himanshu Chourasia**  - [UNCC](https://github.com/HimanshuChourasia)
* **Paul Franklin**  - [UNCC](https://gitlab.com/pfrankl1)  
* **Arjun Kalidas** - [UNCC](https://gitlab.com/arjunkalidas)  
* **Karthik Raveendran** - [UNCC](https://gitlab.com/)  

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


