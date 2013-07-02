from django import forms
from moneyed import Money, CURRENCIES, DEFAULT_CURRENCY_CODE
from decimal import Decimal
import operator

__all__ = ('InputMoneyWidget', 'CurrencySelectWidget', 'MoneyNoCurrencyInputWidget')

CURRENCY_CHOICES = [(c.code, c.name) for i, c in CURRENCIES.items() if c.code != DEFAULT_CURRENCY_CODE]
CURRENCY_CHOICES.sort(key=operator.itemgetter(1))

class CurrencySelectWidget(forms.Select):
    def __init__(self, attrs=None, choices=CURRENCY_CHOICES):
        super(CurrencySelectWidget, self).__init__(attrs, choices)
    
class InputMoneyWidget(forms.TextInput):
    
    def __init__(self, attrs=None, currency_widget=None):
        self.currency_widget = currency_widget or CurrencySelectWidget()
        super(InputMoneyWidget, self).__init__(attrs)
    
    def render(self, name, value, attrs=None):
        amount = ''
        currency = ''
        if isinstance(value, Money):
            amount = value.amount
            currency = value.currency.code
        if isinstance(value, tuple):
            amount = value[0]
            currency = value[1]
        if isinstance(value, int) or isinstance(value, Decimal):
            amount = value
        result = super(InputMoneyWidget, self).render(name, amount)
        result += self.currency_widget.render(name+'_currency', currency)
        return result
    
    def value_from_datadict(self, data, files, name):
        return (data.get(name, None), data.get(name+'_currency', None))


class MoneyNoCurrencyInputWidget(InputMoneyWidget):
    """
    Custom Django Money widget which doesn't require user to enter a currency
    and uses a default currency passed to the constructor.
    """
    def __init__(self, attrs=None, currency_widget=None,
                 currency=DEFAULT_CURRENCY_CODE):
        kwargs = {'attrs': attrs, 'currency_widget': currency_widget}
        super(NoCurrencyMoneyInputWidget, self).__init__(**kwargs)
        self.currency = currency

    def render(self, name, value, attrs=None):
        amount = ''
        if isinstance(value, Money):
            amount = value.amount
        if isinstance(value, tuple):
            amount = value[0]
        if isinstance(value, int) or isinstance(value, Decimal):
            amount = value
        result = TextInput.render(self, name, amount)
        return result

    def value_from_datadict(self, data, files, name):
        value = data.get(name, None)
        currency = self.currency
        return (value, currency)
