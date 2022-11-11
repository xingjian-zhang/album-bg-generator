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