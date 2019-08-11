
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
        self.fetchall_called = 0
        self.fetchone_called = 0
        self.query = None
        self.values = None

    def execute(self, query, values=None):
        self.query = query
        self.values = values
        self.execute_called += 1

    def close(self):
        self.close_called += 1

    def fetchone(self):
        row = (
                'Apple', 52, 0.2, 14, 0.3, 0, 10, 2.4,
                '{"100g": 100, "1 medium": 182}', 'maxtrussell'
        )
        self.fetchone_called += 1
        return row

    def fetchall(self):
        row1 = (
                'Apple', 52, 0.2, 14, 0.3, 0, 10, 2.4,
                '{"100g": 100, "1 medium": 182}', 'maxtrussell'
        )
        row2 = (
                'Big Apple', 104, 0.4, 28, 0.6, 0, 20, 4.8,
                '{"100g": 100, "1 medium": 182}', 'maxtrussell'
        )
        self.fetchall_called += 1
        return [row1, row2]
