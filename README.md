# DALL-E 2 Scraper

This is a crawler and scraper Python program that extracts generations
done with DALL-E 2.

# Usage

## Conda environment

Create or use a `conda` environment using the `environment.yml` file:

```bash
# create
conda env create -f environment.yml

# use
conda activate dalle2-scraper
```

## Environment variables

Create (and fill) the `.env` file based on the `.envdefault` file at the
root of the repository. Then, execute the extraction script:

```bash
python extract.py
```

To see how that data looks, see the "How does it work?" section below.

# Testing

Run PyTest.

```sh
python -m pytest
```

## Testing with a file watcher (`entr`)

```sh
ls test/*.py extractor/**/*.py | entr python -m pytest
```

## How does it work?

This scraper uses the official Reddit and OpenAI APIs. Reddit has an
API that allows to get submissions from subreddits. The "/r/dalle2"
subreddit has a lot of DALL-E 2 generations since people submit them
to that subreddit. Using `PRAW` you can crawl all the
`labs.openai.com...` links from the comment forest. These links follow
this schema: `https://labs.openai.com/s/{generation-id}`. Then, you
can use the `generation-id` to get all the publicly available
information from the OpenAI API. For example, for the generation with
the following ID `0bKAonFhT9qJ82W3uL65NAxj`, we can follow [this
link](https://labs.openai.com/api/labs/public/generations/generation-0bKAonFhT9qJ82W3uL65NAxj)
to get the following JSON response:

```json
{
  "id": "generation-0bKAonFhT9qJ82W3uL65NAxj",
  "object": "generation",
  "created": 1655571037,
  "generation_type": "ImageGeneration",
  "generation": {
    "image_path": "https://openai-labs-public-images-prod.azureedge.net/user-HMnIRUw6QrXKtTyRbxa4Km8e/generations/generation-0bKAonFhT9qJ82W3uL65NAxj/image.webp"
  },
  "task_id": "task-szI42NxRvS8JLHbZVZgD5wVl",
  "prompt_id": "prompt-Uy3iV8DOhzWOGHDHhUlGUcMF",
  "is_public": true,
  "prompt": {
    "id": "prompt-Uy3iV8DOhzWOGHDHhUlGUcMF",
    "object": "prompt",
    "created": 1655571022,
    "prompt_type": "CaptionPrompt",
    "prompt": {
      "caption": "Jurassic Pork, digital art"
    },
    "parent_generation_id": null
  },
  "user": {
    "object": "user",
    "id": "user-HMnIRUw6QrXKtTyRbxa4Km8e",
    "created": 1655371148,
    "name": null,
    "picture": "https://s.gravatar.com/avatar/1d2a5abb3d04fdd63c726cc6bce1e072?s=480&r=pg&d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fdp.png"
  }
}
```

You can check more samples inside the `samples` folder. We can, then,
store the response into a database for further processing.
