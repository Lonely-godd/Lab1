import unittest
from unittest.mock import Mock

from Mediator import *


class TestCRM(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.supporter = Supporter()
        self.programmer = Programmer()
        self.crm = CRM(self.client, self.supporter, self.programmer)

    def test_report_issue(self):
        # Mock the notify method of the client
        self.client.notify = Mock()

        # Report an issue
        topic = "Test topic"
        description = "Test description"
        self.client.report_issue(topic, description)

        # Verify that the issue was sent to the supporter
        self.assertEqual(self.supporter.issue.topic, topic)
        self.assertEqual(self.supporter.issue.description, description)
        self.assertEqual(self.supporter.issue.status, IssueStatus.RESOLVED)
        # Verify that the issue was resolved and the client was notified
        self.assertEqual(self.client.notify.call_count, 1)
        called_issue = self.client.notify.call_args[0][0]
        self.assertEqual(called_issue.topic, topic)
        self.assertEqual(called_issue.description, description)
        self.assertEqual(called_issue.status, IssueStatus.RESOLVED)

    def test_escalate_issue(self):
        # Set up the initial issue and mock the resolve_issue method of the supporter
        issue = Issue("Test topic", "Test description", IssueStatus.RESOLVED)
        self.supporter.set_issue(issue)
        self.supporter.resolve_issue = Mock()

        # Escalate the issue
        self.supporter.escalate_issue()

        # Verify that the issue was escalated and resolve_issue was not called
        self.assertEqual(self.supporter.issue.status, IssueStatus.RESOLVED)
        self.assertEqual(self.supporter.resolve_issue.call_count, 0)

    def test_resolve_issue(self):
        # Set up the initial issue and mock the resolve_issue method of the supporter
        issue = Issue("Test topic", "Test description", IssueStatus.IN_PROGRESS)
        self.supporter.set_issue(issue)
        self.supporter.resolve_issue = Mock()

        # Resolve the issue
        self.supporter.resolve_issue()

        # Verify that the issue was resolved and resolve_issue was called
        self.assertEqual(self.supporter.issue.status, IssueStatus.RESOLVED)
        self.assertEqual(self.supporter.resolve_issue.call_count, 1)


if __name__ == '__main__':
    unittest.main()
