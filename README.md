# TechStaX Webhook Repo

Welcome to the TechStaX Webhook Repo! This repository is designed to handle GitHub webhooks and forward them for further processing.

## Features

- Processes incoming GitHub webhook events.
- Forwards the data to the target for further processing.
- Easy-to-integrate GitHub webhook endpoint for any application.

## Deployed URL

The webhook service is deployed and accessible at:

```
https://techstax.sahanisushilkumar.in
```

## Endpoint

### `/webhook`

- **Description:** The `/webhook` endpoint listens for incoming GitHub webhook events, processes the payload, and forwards the data to a target server for further action.
- **Method:** `POST`
- **Endpoint URL:** 
```
https://techstax.sahanisushilkumar.in/webhook
```

### Request Headers

- `Content-Type: application/json`
- `X-GitHub-Event`: Identifies the event type. It should be included in the GitHub webhook request.

### Response Example

If the request is successful, you will receive a JSON response similar to this:

```json
{
  "status": "success"
}
```

### Error Response Example

If there is an error during processing, you may receive a response like this:

```json
{
  "status": "error",
  "message": "Failed to process the GitHub webhook"
}
```

## How to Use

1. Configure a webhook in your GitHub repository settings with the URL: `https://techstax.sahanisushilkumar.in/webhook`.
2. Make sure to select events you want to trigger the webhook (e.g., push, pull request).
3. The webhook will forward the event data to the appropriate target.

## Running Locally

If you would like to run the service locally for development purposes, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/sushilkumarsahani41/TechStaX-webhook-repo.git
   cd TechStaX-webhook-repo
   ```

2. Set up a virtual environment:

   Install `virtualenv` if you don’t have it already:

   ```bash
   pip install virtualenv
   ```

   Create and activate the virtual environment:

   ```bash
   virtualenv venv
   source venv/bin/activate  # On Windows use: venv\Scriptsctivate
   ```

3. Install the necessary dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the server:

   ```bash
   python manage.py runserver
   ```

5. The server will be running at:

   ```
   http://127.0.0.1:8000/webhook
   ```