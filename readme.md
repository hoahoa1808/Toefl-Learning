# Simple Quizlet for learning english

## Structure

- main.py : run in console
- grapic.py : create a graphic window 
- profile.yaml: temporary save (**shouldnt refine**)
- words.xlsx  : words data source is utilized for create quizes (**add words here**)

## Run:
- simple way:

```bash
python main.py #console mode
```
or
```python
python graphic.py #for graphic mode
```

## run EXE

- creat exe by pyinstaller:
  
```python
cd EVocabsQuizlet
pyinstaller --onefile .\graphic.py
```