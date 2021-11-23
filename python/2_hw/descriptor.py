# class Value:
#     """Working descriptor example"""
#     def __init__(self):
#         self.value = None
#
#     @staticmethod
#     def _calculate_value(commission, value):
#         return value * (1 - commission)
#
#     def __set__(self, obj, value):
#         self.value = self._calculate_value(obj.commission, value)
#
#     def __get__(self, obj, obj_type):
#         return self.value


class Account:
    # amount = Value()

    def __init__(self, commission):
        self.commission = commission
        self._amount = None

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value * (1 - self.commission)
        return self._amount


new_account = Account(0.1)
new_account.amount = 100

print(new_account.amount)
