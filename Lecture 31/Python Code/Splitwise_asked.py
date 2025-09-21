'''
Implement an algo similar to slipwise with below feature
System would take expenses <userWhoPaidAmount, AmountPaid, listOfUsersAmoungWithThisAmountWillBeShared>
Provided a user list all the transactions telling which user ows how much amount
This has to be a running code and code was tested with 2-3 testcases as well.

'''

from abc import ABC, abstractmethod
from collections import defaultdict

# ---------------- Split Strategy ----------------
class SplitStrategy(ABC):
    @abstractmethod
    def split(self, payer: str, amount: float, users: list[str]) -> dict[str, float]:
        pass


class EqualSplitStrategy(SplitStrategy):
    def split(self, payer: str, amount: float, users: list[str]) -> dict[str, float]:
        if not users:
            raise ValueError("At least one user must share the expense")
        share = amount / len(users)
        return {user: share for user in users if user != payer}


# ---------------- Expense ----------------
class Expense:
    def __init__(self, payer: str, amount: float, users: list[str], strategy: SplitStrategy):
        self.payer = payer
        self.amount = amount
        self.users = users
        self.strategy = strategy

    def get_splits(self) -> dict[str, float]:
        return self.strategy.split(self.payer, self.amount, self.users)


# ---------------- Expense Builder ----------------
class ExpenseBuilder:
    def __init__(self):
        self.payer = None
        self.amount = 0
        self.users = []
        self.strategy = None

    def with_payer(self, payer: str):
        self.payer = payer
        return self

    def with_amount(self, amount: float):
        self.amount = amount
        return self

    def with_users(self, users: list[str]):
        self.users = users
        return self

    def with_strategy(self, strategy: SplitStrategy):
        self.strategy = strategy
        return self

    def build(self) -> Expense:
        if not self.payer or not self.amount or not self.users or not self.strategy:
            raise ValueError("Missing required fields for Expense")
        return Expense(self.payer, self.amount, self.users, self.strategy)


# ---------------- Splitwise Manager ----------------
class SplitwiseManager:
    def __init__(self):
        self.balances = defaultdict(lambda: defaultdict(float))

    def add_expense(self, expense: Expense):
        payer = expense.payer
        splits = expense.get_splits()

        for user, owed in splits.items():
            self.balances[user][payer] += owed
            # Simplify debts
            if self.balances[payer][user] > 0:
                net = self.balances[user][payer] - self.balances[payer][user]
                if net >= 0:
                    self.balances[user][payer] = net
                    del self.balances[payer][user]
                else:
                    self.balances[payer][user] = -net
                    del self.balances[user][payer]

    def show_all_balances(self):
        print("\n=== All Balances ===")
        for user, owes in self.balances.items():
            for other, amount in owes.items():
                if amount > 0:
                    print(f"{user} owes {other}: Rs {amount:.2f}")

    def show_user_balance(self, user: str):
        print(f"\n=== Balances for {user} ===")
        found = False
        if user in self.balances:
            for other, amount in self.balances[user].items():
                if amount > 0:
                    print(f"Owes {other}: Rs {amount:.2f}")
                    found = True

        for other, owes in self.balances.items():
            if user in owes and owes[user] > 0:
                print(f"{other} owes {user}: Rs {owes[user]:.2f}")
                found = True

        if not found:
            print("No transactions for this user")


# ---------------- Demo ----------------
if __name__ == "__main__":
    manager = SplitwiseManager()

    # A paid 300 for A, B, C
    exp1 = ExpenseBuilder().with_payer("A").with_amount(300).with_users(["A", "B", "C"]).with_strategy(EqualSplitStrategy()).build()
    manager.add_expense(exp1)

    # B paid 300 for A, B, C
    exp2 = ExpenseBuilder().with_payer("B").with_amount(300).with_users(["A", "B", "C"]).with_strategy(EqualSplitStrategy()).build()
    manager.add_expense(exp2)

    # C paid 300 for A and C
    exp3 = ExpenseBuilder().with_payer("C").with_amount(300).with_users(["A", "C"]).with_strategy(EqualSplitStrategy()).build()
    manager.add_expense(exp3)

    manager.show_all_balances()
    manager.show_user_balance("A")
    manager.show_user_balance("B")
    manager.show_user_balance("C")
