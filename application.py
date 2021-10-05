from app import create_app
import os

application = create_app()
if __name__ == "__main__":
    application.run()
