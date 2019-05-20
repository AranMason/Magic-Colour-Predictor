# Downloading MTG Data

Goal here is to adapt the VGG16 to detect what colour of card an image might belong to using the whole of MTG's history

We use the Scryfall Library. I have written a scrapping tool, which uses information from Scryfalls Bulk Data which can be found [here](https://scryfall.com/docs/api/bulk-data). There is a 0.1s delay between fetches to accomidate Scryfalls rate limiting requests

We ignore multi-colour cards, planeswalkers, schemes, tokens, promos and emblems. This is due to either poor cropped art provided by Scryfall and to simplify approach to colour classification.

## Requirements

The following Python modules are used

- Keras (Version 2.1.6)
- TensorFlow
- Pillow
- sklearn