---
layout: post
title: Choosing type of interface in a new project
---
### My previous experience
During my studies and scientific work, I have not faced the task of creating a user-friendly and functional graphic interface. Homework is usually set to create an effective algorithm. And, of course, we do them primarily based on the basic requirements for obtaining credit. We send our solutions and pass the exams, and the written code is unlikely to be used ever - so the most I have wrote for my programs is the command line interface (getting arguments and processing flags).

In scientific work research and searching a new solution for the problem also predominates under creating useful interface. So when I faced with need to choose the best interface for the task I am solving, I went through this area. We сonsidered the following types:

- Command line interfaces
	- Argparser
	- Curses
- Graphic interfaces
	- PyQT
	- Web interface

With help of my mentor I have prepared a list of pros and cons of each type of interface regarding our task.

### Command line interfaces
* Argparser

```python
import argparse

parser = argparse.ArgumentParser(
        description='This is an exaple argparser')
    parser.add_argument('dir',
                        metavar='directory',
                        type=str,
                        nargs=1,
                        help='Path to a directory with file(s)')
    parser.add_argument('filename',
                        metavar='filename(s)',
                        type=str,
                        nargs=+,
                        help='Filenames (space-separated)')
    parser.add_argument('-out', '--outfile',
                        type=str,
                        help='Filename to save the output (optional)')
```
I use it now, during the developement, for which it is quite convenient. But on the last stage of my internship I could provide useful ans user-friendly tools and interface, so I took a look on other types.

* Curses
![Exaple of curses interface](http://www.muylinux.com/wp-content/uploads/2010/01/alsamixer.png){:width="60%" style="margin-bottom: 7px;"}
	- (+) curses will be more convenient to run on a remote servers without X11
	- (+) it will be easier to implement
	- (-) perhaps it will be convenient only for advanced users
	- (-) you will need to use some graphical interface if you want to visualise the data, but probably this is not so critical

There are also alternatives for python curses, for example I found [Urwid](http://urwid.org)

### Graphic interfaces
* PyQT
	- (+) cross-platform
	- (+) easy to use
	- (-) need to install pyqt package
	- (-) may be slow over remote connections
* Web interface
	- (+) more cross-platform as you can use it even with the tablet
	- (+) no need to install extra packages
	- (+) I could add interactive charts (I've used [Highcharts](https://www.highcharts.com), but there are many open-source libraries, for example [D3: Data-Driven Documents](https://d3js.org)
	- (-) it can be more difficult to implement, but there are many frameworks, for example I've tried the examples from Flask http://flask.pocoo.org
	- (-) a running web application must be accessed some way, typically over ssh forwarding, which is some hassle

Web interface seems to be more attractive to me, however, its implementation can take a long time. Since I would like to devote more time to developing an algorithm, we decided to choose the curses/urwid interface. At the same time I'll leave the possibility to change the interface if necessary, so if there is enough time, I would try to create a web interface. 

I hope my resume will help to get an initial idea of what interface is best for you, but do not forget that the choice depends on the task that you decide and the time available to you.
