import unittest
from unittest.mock import patch
import server

class MailboxTest(unittest.TestCase):
    def tearDown(self):
        server.mailboxes.clear()

    @patch('server.request')
    def test_lifecycle_and_consent(self, api):
        api.return_value = {'id': 'inbox', 'address': 'test@example.invalid', 'token': 'private-test-token'}
        created = server.create_mailbox()
        self.assertNotIn('token', created)
        api.return_value = {'messages': []}
        self.assertEqual(server.list_messages('inbox'), {'messages': []})
        api.assert_called_with('GET', '/mailboxes/inbox/messages', 'private-test-token')
        server.read_message('inbox', 'a/b')
        api.assert_called_with('GET', '/mailboxes/inbox/messages/a%2Fb', 'private-test-token')
        calls = api.call_count
        with self.assertRaises(ValueError):
            server.list_messages('unknown')
        with self.assertRaises(ValueError):
            server.delete_mailbox('inbox')
        self.assertEqual(api.call_count, calls)
        api.return_value = {'deleted': True}
        server.delete_mailbox('inbox', confirm=True)
        self.assertNotIn('inbox', server.mailboxes)

if __name__ == '__main__':
    unittest.main()
