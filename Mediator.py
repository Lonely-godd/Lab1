from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from random import choice
from typing import Optional

class Event(ABC):  # The Abstract class for message exchange
    pass

@dataclass
class Issue(Event):  # The specific message about the problem
    topic: str
    description: str
    status: IssueStatus

class IssueStatus(Enum):
    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    RESOLVED = 'resolved'

class Mediator(ABC):
    @abstractmethod
    def send(self, sender: Colleague, event: Event) -> None:
        pass

class Colleague(ABC):
    def __init__(self):
        self._mediator: Optional[Mediator] = None

    @property
    def mediator(self):
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

class Employee(Colleague):
    def __init__(self):
        super().__init__()
        self.issue: Optional[Issue] = None

class Client(Colleague):
    def report_issue(self, topic, description):
        issue = Issue(topic, description, IssueStatus.NEW)
        print(f'The client creates a request {issue}')
        self.mediator.send(self, issue)

    @staticmethod
    def notify(issue: Issue):
        print(f'The client will receive a response regarding the request {issue}')

class Supporter(Employee):
    def resolve_issue(self):
        print(f'The technical support staff resolved the issue independently {self.issue}')
        self.issue.status = IssueStatus.IN_PROGRESS
        self.mediator.send(self, self.issue)

    def escalate_issue(self):
        print(f'The technical support staff escalated the issue {self.issue}')
        self.issue.status = IssueStatus.RESOLVED
        self.mediator.send(self, self.issue)

    def set_issue(self, issue: Issue):
        self.issue = issue
        if choice([True, False]):
            self.resolve_issue()
        else:
            self.escalate_issue()

class Programmer(Employee):
    def resolve_issue(self):
        self.issue.status = IssueStatus.RESOLVED
        print(f'The programmer heroically declared a bug {self.issue} as a feature')
        self.mediator.send(self, self.issue)

    def set_issue(self, issue: Issue):
        self.issue = issue
        self.resolve_issue()

class CRM(Mediator):
    def __init__(self, client: Client, supporter: Supporter, programmer: Programmer):
        self.client = client
        self.client.mediator = self
        self.supporter = supporter
        self.supporter.mediator = self
        self.programmer = programmer
        self.programmer.mediator = self

    def send(self, sender: Colleague, event: Issue):
        if isinstance(sender, Client):
            self.supporter.set_issue(event)
        elif isinstance(sender, Supporter):
            if event.status == IssueStatus.IN_PROGRESS:
                self.programmer.set_issue(event)
            else:
                self.client.notify(event)
        elif isinstance(sender, Programmer):
            self.client.notify(event)

if __name__ == '__main__':
    client = Client()
    supporter = Supporter()
    programmer = Programmer()
    crm = CRM(client, supporter, programmer)
    topic = str(input("Enter your topic: "))
    description = str(input("Enter your description: "))
    client.report_issue(topic, description)
    print('--' * 10)
