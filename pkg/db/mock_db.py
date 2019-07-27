
class MockClient:
    def __init__(self):
        self.cursor_called = 0
        self.commit_called = 0
        self.mock_cursor = MockCursor()

    def cursor(self):
        self.cursor_called += 1
        return self.mock_cursor

    def commit(self):
        self.commit_called += 1

class MockCursor:
    def __init__(self):
        self.execute_called = 0
        self.close_called = 0
        self.query = None
        self.values = None

    def execute(self, query, values):
        self.query = query
        self.values = values
        self.execute_called += 1

    def close(self):
        self.close_called += 1
