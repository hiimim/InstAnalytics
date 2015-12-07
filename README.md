# InstAnalytics

## About

Each day, this Python script scraps the web version of Instagram, to get the number of posts, followers, following + likes and comments per photo from any **public** account. The data is then stored in a JSON file (`data/InstAnalytics.json`) so you can get track its growth.

As I made it to run on my Raspberry Pi, it uses PhantomJS, a lightweight headless browser (which is perfect for a RPi, especially in terms of resources consumption).

For more info, check out my [blog post](http://nbyim.com/monitor-instagram-accounts-without-using-api).

## Requirements

Before you can run **InstAnalytics.py**, you will need to install a few Python dependencies.

Note: Python 2.7.9 and later (on the python2 series), and Python 3.4 and later include pip by default, so you may have pip already. Otherwise, you can install [easy_install](https://pythonhosted.org/setuptools/easy_install.html) `sudo apt-get install python-setuptools` to install [pip](https://pypi.python.org/pypi/pip) `sudo easy_install pip`.

- [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4), for parsing html: `pip install BeautifulSoup4`
- [Selenium](http://www.seleniumhq.org/), for browser automation: `pip install Selenium`

PhantomJS:
- On Windows, download the binary from the [official website](http://phantomjs.org) and put it in the same folder than **InstAnalytics.py**.
- On OS X Yosemite, the binary provided by the PhantomJS crew doesn't work (*selenium.common.exceptions.WebDriverException: Message: 'Can not connect to GhostDriver'*). You can either compile it by yourself or download the binary provided by the awesome [eugene1g](https://github.com/eugene1g/phantomjs/releases). Then put it in the `/usr/local` folder.
- It's the same for Raspbian : compile it and put it in the `/usr/bin` folder or download the binary provided by the awesome [spfaffly](https://github.com/spfaffly/phantomjs-linux-armv6l).

If you want to built your own binaries, here is the [build instructions](http://phantomjs.org/build.html) for PhantomJS.

If you plan to change the browser to Firefox or Chrome, edit the line `browser = webdriver.PhantomJS(desired_capabilities=dcap)` to `browser = webdriver.Firefox()` or `browser = webdriver.Chrome()`. To use Firefox you don't need anything more. For Chrome, first get the [webdriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) then put it in the same folder than **InstAnalytics.py** if you are on Windows, or in the `/usr/local` folder if you are on OS X.

## Configuration

Before you run **InstAnalytics.py**, edit the `users = ['yotta_life']` list to add as much as you want public Instagram accounts. It's that simple!

## JSON output example

```JSON
[
  {
    "username": "yotta_life", 
    "date": "2015-11-23", 
    "data": {
      "following": 164, 
      "followers": 351000, 
      "pLikesT": 966048, 
      "posts": 419, 
      "photos": [
        {
          "pId": "-aOwFCMU6P", 
          "pLikes": 1763, 
          "pComments": 24
        },
          ...
        {
          "pId": "-Z_AthsU8T", 
          "pLikes": 2096, 
          "pComments": 27
        }
      ]
    }
  }
]
