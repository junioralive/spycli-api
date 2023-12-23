# SPYCLI-API 

This application is the backend for [spy-cli](https://github.com/junioralive/spycli-database) provides an interface for searching, fetching, and scraping movie data. It includes endpoints for searching movies from a JSON source, scraping content from web pages, and processing movie and series data.

You can also try [spycli-noserver](https://github.com/junioralive/spycli-noserver)

## Features

- Search movies from [spycli-database](https://github.com/junioralive/spycli) JSON dataset.
- Scrape content for requested content.
- Process and parse movie and series data.
- Asynchronous scraping using Pyppeteer.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/junioralive/spycli-api.git
   ```
2. Navigate to the cloned directory:
   ```sh
   cd your-repository
   ```
3. Install required packages:
   ```sh
   pip install -r requirements.txt
   ```

### Running the Application

Run the application using the following command:

```sh
python spycli-server.py
```

The server will start on `http://localhost:5000` or http://{your ip}:5000

## Usage

### Search Movies

- Endpoint: `/search`
- Method: `GET`
- Query Parameters:
  - `query`: The search text for the movie.

### Fetch Episode Information

- Endpoint: `/fetch`
- Method: `GET`
- Query Parameters:
  - `url`: The URL to fetch all available links.

### Scrape Content

- Endpoint: `/scrape`
- Method: `GET`
- Query Parameters:
  - `url`: The URL to scrape streaming link.

## Contributing

Contributions are welcome! For queries, please open an issue first to discuss.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Contact

Discord - junioralive
