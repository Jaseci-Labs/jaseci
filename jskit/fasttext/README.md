# Demo AIV service with fasttext: Tourist VA

## Capabilities

Guyana Tourism Virtual Assistant provides answers to frequently asked questions when traveling to Guyana.

Hi, I'm your Guyana Tourism Virtual Assistant.

You can ask me things like:
- Do I need a passport or visa to enter Guyana?
- Do I need a visa to enter Guyana?
- Where can I get more information once I arrive at the airport?
- Are there any fees or taxes I will have to pay when I leave?
- What items are considered 'personal effects' by Guyana Customs?
- What do I have to declare?
- How long does it take to reach Guyana from USA, Canada, Germany and UK?
- Which are the major airlines that connect USA, Canada, Germany and UK to Guyana?

## Build

`docker build -t fasttext-classifier .`

## Endpoint Interface

The endpoint accepts a map that contains
- An `op` (`predict`)
- A list of `sentences` to classify

It returns a map where each sentence is a key and its value is a list of maps with the keys `intent`, `probability`, and `sentence`.

Request:

```json
{
  "op": "predict",
  "sentences": [
    "hello",
    "Do I need a passport or visa to enter Guyana?",
    "..."
  ]
}
```

Response:

```json
{
    "Do I need a passport or visa to enter Guyana?": [
        {
            "intent": "travel-documents",
            "probability": 0.9999077320098877,
            "sentence": "Do I need a passport or visa to enter Guyana?"
        }
    ],
    "hello": [
        {
            "intent": "hello",
            "probability": 0.9987579584121704,
            "sentence": "hello"
        }
    ]
}
```

In the response, the first map in the list for each sentence key represents the best prediction.
