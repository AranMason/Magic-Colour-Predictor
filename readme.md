# Try for yourself
Webpage: [mtg.aran.nz](https://mtg.aran.nz)
# Downloading MTG Data

Goal here is to adapt the VGG16 to detect what colour of card an image might belong to using the whole of MTG's history

We use the Scryfall Library. I have written a scrapping tool, which uses information from Scryfalls Bulk Data which can be found [here](https://scryfall.com/docs/api/bulk-data). There is a 0.1s delay between fetches to accomidate Scryfalls rate limiting requests

## Ignored Card Types
We ignore the following due to either poor cropped art provided by the Scryfall API or to simplify approach to colour classification. I am currently debating removing colourless from being classified.
- Multi-colour
- Planeswalker
- Schemes
- Tokens
- Promos
- Emblems


## Requirements

The following Python modules are used

- Keras (Version 2.1.6)
- TensorFlow
- Pillow
- sklearn
- numpy

## Hosting

To host the application, is in a AWS EC2 Instance using the following:
- Nginx
- Flask
- Gunicorn
