from decimal import Decimal
from babel.numbers import format_currency
from django.utils.translation import get_language
from moneyed.classes import Money as moneyed_Money, Currency, DEFAULT_CURRENCY,\
    CURRENCIES, DEFAULT_CURRENCY_CODE


class Money(moneyed_Money):
    def __unicode__(self):
        return format_currency(
            self.amount, self.currency.code, locale=get_language().replace('-', '_')
        )

    def __str__(self):
        return format_currency(
            self.amount, self.currency.code, locale=get_language().replace('-', '_')
        )

    def __pos__(self):
        return Money(
            amount=self.amount,
            currency=self.currency)

    def __neg__(self):
        return Money(
            amount=-self.amount,
            currency=self.currency)

    def __add__(self, other):
        if isinstance(other, (int, Decimal)):
            if other == 0:
                return Money(self.amount, self.currency)
        if not isinstance(other, Money):
            raise TypeError('Cannot add or subtract a ' +
                            'Money and non-Money instance.')
        if self.currency == other.currency:
            return Money(
                amount=self.amount + other.amount,
                currency=self.currency)

        raise TypeError('Cannot add or subtract two Money ' +
                        'instances with different currencies.')

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Money):
            raise TypeError('Cannot multiply two Money instances.')
        else:
            return Money(
                amount=(self.amount * Decimal(str(other))),
                currency=self.currency)

    def __div__(self, other):
        if isinstance(other, Money):
            if self.currency != other.currency:
                raise TypeError('Cannot divide two different currencies.')
            return self.amount / other.amount
        else:
            return Money(
                amount=self.amount / Decimal(str(other)),
                currency=self.currency)

    def __rmod__(self, other):
        """
        Calculate percentage of an amount.  The left-hand side of the
        operator must be a numeric value.

        Example:
        >>> money = Money(200, 'USD')
        >>> 5 % money
        USD 10.00
        """
        if isinstance(other, Money):
            raise TypeError('Invalid __rmod__ operation')
        else:
            return Money(
                amount=(Decimal(str(other)) * self.amount / 100),
                currency=self.currency)

    def quantize(self, *args, **kwargs):
        return Money(self.amount.quantize(*args, **kwargs), self.currency)

    __radd__ = __add__
    __rsub__ = __sub__
    __rmul__ = __mul__
    __rdiv__ = __div__

