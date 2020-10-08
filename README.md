# LUIMA SBD

## Dependencies
* Python 3
* python-crfsuite
* flask
* chardet

```
sudo pip3 install python-crfsuite
sudo pip3 install Flask
sudo pip3 install chardet
```


## Run as a command line script

```
python3 luima_sbd.py -f ./data/example.txt
```

## Run as a service

```
python3 luima_sbd.py -p 5555
```

There is an example request to the service in *example_request.py*. If you
comment out the line with *url* variable and uncomment the line below you will
get sentence offsets instead of sentences.

## Integrate into Python code
Copy this project directory to your project and import *sbd_utils.py*. From
there you can call the *text2sentences(text, offsets=False)* function which
expects a text as an argument. Setting the optional *offsets* argument to
*True* indicates that you would like sentence offsets instead of the sentences.

## Attribution

We kindly ask you to cite the following paper in your work using the data set:


> Savelka, Jaromir, Vern R. Walker, Matthias Grabmair and Kevin D. Ashley. "Sentence Boundary Detection in Adjudicatory Decisions in the United States." TAL 58.2 (2017).
