# Local installation guide

## Create a virtuel environment

```
python3 -m venv .venv
. .venv/bin/activate
```
<br />

## Install dependencies

```
pip install -r requirements.txt
```

<br />

If the installation was successful, this command should open a vpype-viewer instance :
```
vpype begin grid -o 25 25 10 10 circle 0 0 100 end efill show
```