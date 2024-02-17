class Category:
  def __init__(self, category):
    self.category = category
    self.ledger = []
    
  def deposit(self, amount, description = ''):
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description = ''):
    if self.check_funds(amount):
      self.ledger.append({"amount": -amount, "description": description})
      return True
    else:
      return False

  def get_balance(self):
    balance = 0
    for item in self.ledger:
      balance += item.get("amount")
      
    return balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, f"Transfer to {category.category}")
      category.deposit(amount, f"Transfer from {self.category}")
      return True
    else:
      return False

  def check_funds(self, amount):
    if amount > self.get_balance():
      return False
    else:
      return True

  def __str__(self):
    category_name = self.category.center(30, '*')
    
    items = []
    for item in self.ledger:
      formatted_amount = "%.2f" %item.get("amount")
      formatted_description = item.get("description")[:23]
      items.append(f"{formatted_description}{formatted_amount.rjust(30 - len(formatted_description))}")

    formatted_items = "\n".join(items)

    total = f"Total: {self.get_balance()}"

    return f"{category_name}\n{formatted_items}\n{total}"
    
def create_spend_chart(categories):
  spent_dict = {}

  for category in categories:
    spent = 0
    for item in category.ledger:
      if item.get("amount") < 0:
        spent += abs(item.get("amount"))
    spent_dict[category.category] = spent

  total = sum(spent_dict.values())

  percent_dict = {}

  for category, amount in spent_dict.items():
    percent_dict[category] = int(round(amount / total * 100))

  chart = "Percentage spent by category\n"

  for y in range(100, -10, -10):
    chart += f"{y}".rjust(3) + '| '

    for percent in percent_dict.values():
      if percent >= y:
        chart += 'o  '
      else: 
        chart += '   '
    chart += '\n'

  chart += ' ' * 4 + '-' * (len(percent_dict.keys())*3 + 1) + '\n'

  names = list(percent_dict.keys())
  max_name = len(max(names, key=len))

  for i in range(max_name):
    chart += ' ' * 5
    for name in names:
      if i < len(name):
        chart += name[i] + '  '
      else:
        chart += '   '
    if i < max_name - 1:
      chart += '\n'
      
  return chart