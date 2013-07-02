from django.core.validators import MinValueValidator, MaxValueValidator

__all__ = ('MoneyMinValueValidator', 'MoneyMaxValueValidator',)


class MoneyMinValueValidator(MinValueValidator):
    def compare(self, cleaned, limit_value):
        value = cleaned.amount
        return super(MoneyMinValueValidator, self).compare(value, limit_value)


class MoneyMaxValueValidator(MaxValueValidator):
    def compare(self, cleaned, limit_value):
        value = cleaned.amount
        return super(MoneyMaxValueValidator, self).compare(value, limit_value)
