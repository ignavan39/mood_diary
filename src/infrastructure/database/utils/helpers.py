from sqlalchemy.exc import IntegrityError


def is_duplication_error(e: IntegrityError):
    error_msg = str(e.orig).lower() if e.orig else str(e).lower()
    return "unique constraint" in error_msg or "duplicate key" in error_msg
