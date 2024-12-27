from .repository import Repository

# from ..error.errors import DatabaseFetchError


class DatabaseRepository(Repository):
    def find_all(self):
        # return {"name": "John Doe", "email": "john@example.com"}
        return None
        # raise DatabaseFetchError("Failed to fetch data from database", 5001, "SELECT * FROM users")
