from app import db, create_app



if __name__ == "__main__":
    db.init_app(create_app())
    db.cli.run()
