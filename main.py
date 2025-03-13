import uvicorn
from lux.server import app
from lux.utils.settings import settings


def main():
    host = settings.get("server.host", "localhost")
    port = settings.get("server.port", 3105)
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
