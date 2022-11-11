# Album Desktop Background Generator

## API

```
.
├── black_bg.jpg
├── build
├── data
   ├── image
   ├── info
```

`image`: A directory of png format album images (600x600 px)
`info`: A directory of json format album information, example:

```json
{
  "genre": "R&B/Soul",
  "album": "Starboy",
  "name": "Starboy (feat. Daft Punk)",
  "album artist": "The Weeknd",
  "date": 2016
}
```

An album should have two asset files:
```
data/image/<album>.png
data/info/<album>.json
```

## Demo
![](examples/Dessous%20de%20plage%20-%20EP.png)
![](examples/Overnight%20-%20Single.png)
![](examples/Sometimes%20I%20Might%20Be%20Introvert.png)
![](examples/Use%20Your%20Illusion%20I.png)
![](examples/Zion.png)

## Sample data
https://drive.google.com/file/d/1Eu7-gL5muRrGUstlC92RK13A6Vkwrw-R/view?usp=sharing