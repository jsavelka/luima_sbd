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

There is an example request to the service in *example_request.py*.

## Integrate into Python code
Simply copy the *sbd_utils.py* to your project and import it.