# Whatsapp Chat Analysis 
> A simple data analysis which gives some useless stats about your chats and graphically represents your chatting patterns.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/built-with-resentment.svg)](https://forthebadge.com)

[![GitHub license](https://img.shields.io/badge/license-MIT-brightgreen?logo=github)](https://raw.githubusercontent.com/pra8eek/Whatsapp-Chat-Analysis/master/LICENSE)
[![PRs](https://img.shields.io/badge/PRs-Welcome-informational)](https://github.com/pra8eek/Whatsapp-Chat-Analysis/)
-[![Python3.6](https://img.shields.io/badge/python-3.6-success?logo=python)](https://www.python.org/downloads/release/python-360/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-important)](https://www.python.org/dev/peps/pep-0008/)
[![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/pra8eek/Whatsapp-Chat-Analysis/)  

## Why?
- I'm in quarantine and have literally nothing to do :sweat:
- Who wouldn't like some stats/graphs about their whatsapp conversations. Not just one to one, but group chats too!
- I wanted to learn about Github readmes, so here's how it goes.

## What you'll get
- A Stats Table <img src="/images/Table.png" alt="Yahan ek table aati, but tumhara net slow hai">
- A Weekly Analysis Graph <img src="/images/Weekly Analysis.png" alt="Yahan ek pyara sa chart aata, but tumhara net slow hai">
- An Hourly Analysis Graph <img src="/images/Hourly Analysis.png" alt="Yahan ek aur pyara sa chart aata, but tumhara net slow hai">

## Reading the graph
 Let's understand with the weekly analysis.
- In the individual graph, farther the graph is from center, more the number of messages sent on that day.
- For instance, Trap Nation (Green) has sent the max messages on Thursday while Paul Walker (Purple) has barely sent any.
- Sometimes, the number of participants can go quite high and it can be tough to see individual graphs, so there's another one, collective graph.
- The collective graph shows the messages sent by all participants on a given day of the week

Similarly for hourly analysis, you can see that the majority of chats have taken place during midnight!

## Installation
- Clone the repository using ```git clone https://github.com/pra8eek/Whatsapp-Chat-Analysis```
- Open the directory *Whatsapp-Chat-Analysis*
- Install the requirements with ```pip3 install -r requirements.txt```

### Getting chat.txt
**Heads Up: *The code only works if chats' time is in 12hour format i.e. am/pm format***
***Also, it requires DD/MM/YY format for date.***
***If either condition is not fulfilled, feel free to modify setup() and getArray() or [mail me](mailto:impra8eek@gmail.com)***
- Open up the chat in your Whatsapp
- Click on the three dots on the top-right corner
- Select on More > Export Chat > Without Media
- Put the documment in the same folder in which the code is present

**Now you can either execute in Jupyter or in Terminal. I'll tell you both.**

### Using Jupyter Notebook (Recommended)
- Open *Whatsapp Analyzer.ipynb* in Jupyter
- Enter the name of file in the first cell
- Execute all cells and Voila! You're done :beers:

### Using Terminal
- Open up your terminal and go to the project directory using ```cd /path/to/directory```
- (Optional) Preferrably rename your whatsapp chat to something simple, say chat.txt
- Replace chat.txt with the name of your input file```python3 WhatsappAnalyzer.py chat.txt``` and that's it. Cheers! :beers:


*And here are some other batches for no reason at all* :joy: :joy:

[![forthebadge](https://forthebadge.com/images/badges/no-ragrets.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/powered-by-netflix.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/winter-is-coming.svg)](https://forthebadge.com)
