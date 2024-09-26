# Jina CLIP Embedding Server

This is a basic embedding server built using FastAPI for processing text and image embeddings. The model used is `jinaai/jina-clip-v1` from the Hugging Face Transformers library.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Model](#model)
3. [Endpoints](#endpoints)
4. [Usage](#usage)

## Getting Started

To run this server, ensure you have [uv](https://docs.astral.sh/uv/#getting-started) installed. Then, run the following command:

```bash
uv run server.py
```

The server will be accessible at `http://0.0.0.0:7144`.

## Model

The model used is `jinaai/jina-clip-v1`, which is a pre-trained version of the CLIP (Contrastive Language-Image Pre-training) model. This model can generate embeddings for both text and images.

It outputs a 768 dimensional vector.

## Endpoints

### `/embed/` (POST)

- **Description**: This endpoint takes a JSON payload containing text sentences and/or image URLs, and returns their corresponding embeddings.

- **Request Payload**:
  ```json
  {
    "inputs": [
      {
        "type": "text",
        "data": "This is a text example."
      },
      {
        "type": "image",
        "data": "http://example.com/image1.jpg"
      }
    ]
  }
  ```

- **Response**:
  ```json
  {
    "embeddings": [
      [0.1, 0.2, ...],
      [0.5, 0.6, ...]
    ]
  }
  ```

## Usage

### Encoding Text

To encode text, send a POST request to `/embed/` with a payload containing the `text` field:

```bash
curl -X POST "http://0.0.0.0:7144/embed/" \
-H "Content-Type: application/json" \
-d '{
  "inputs": [
    {
      "type": "text",
      "data": "This is a text example."
    }
  ]
}'
```

### Encoding Images

To encode images, send a POST request to `/embed/` with a payload containing the `image` field:

```bash
curl -X POST "http://0.0.0.0:7144/embed/" \
-H "Content-Type: application/json" \
-d '{
  "inputs": [
    {
      "type": "image",
      "data": "http://example.com/image1.jpg"
    }
  ]
}'
```

### Encoding Both Text and Images

To encode both text and images, send a POST request to `/embed/` with a payload containing both the `text` and `image` fields:

```bash
curl -X POST "http://0.0.0.0:7144/embed/" \
-H "Content-Type: application/json" \
-d '{
  "inputs": [
    {
      "type": "text",
      "data": "This is a text example."
    },
    {
      "type": "image",
      "data": "http://example.com/image1.jpg"
    }
  ]
}'
```

## Notes

- The server handles both URLs and base64 encoded data URIs.
- If an error occurs while processing an image, the server will return a 400 Bad Request response with details about the error.

This server provides a simple way to integrate text and image embeddings into your applications using FastAPI and CLIP.