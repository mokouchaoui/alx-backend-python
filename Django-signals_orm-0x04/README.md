# Messaging App

This is a Django-based messaging application that allows users to participate in conversations and send messages to each other. The application includes features such as user authentication, message serialization, and custom permissions.

## Features

- **User Authentication**: Users can register, log in, and manage their accounts.
- **Conversations**: Users can create and participate in conversations.
- **Messages**: Users can send and receive messages within conversations.
- **Permissions**: Custom permissions to ensure only participants can access conversations and only senders can edit messages.
- **Middleware**: Custom middleware for logging requests, restricting access by time, and limiting offensive language.
- **Caching**: Caching for optimizing performance.

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd messaging_app
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables:
    ```sh
    cp .env.example .env
    ```

5. Apply the migrations:
    ```sh
    python manage.py migrate
    ```

6. Create a superuser:
    ```sh
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```sh
    python manage.py runserver
    ```

## Usage

- Access the admin panel at [http://127.0.0.1:8000/admin/](http://_vscodecontentref_/21) to manage users and conversations.
- Use the API endpoints to interact with the messaging system.

## API Endpoints

- `POST /api/token/`: Obtain a JWT token.
- `POST /api/token/refresh/`: Refresh the JWT token.
- `POST /api/token/verify/`: Verify the JWT token.
- `GET /api/conversations/`: List all conversations for the authenticated user.
- `POST /api/conversations/`: Create a new conversation.
- `GET /api/conversations/{conversation_id}/messages/`: List all messages in a conversation.
- `POST /api/conversations/{conversation_id}/messages/`: Send a new message in a conversation.

## Running Tests

To run the tests, use the following command:
```sh
python manage.py test

