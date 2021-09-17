from . import db_handler


# Override the settings!
pipeline = {
    "DB_HANDLER": db_handler.BaseHandler
}
