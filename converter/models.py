from __future__ import annotations
from decimal import Decimal
import datetime
from typing import Optional, Union

from django.db.models import QuerySet
from django.db import models
from django.utils.timezone import now
from .utility.general import qs_find


class Currency(models.Model):
	precision = 5
	base_code = 'BGN'
	
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=3)
	symbol = models.CharField(max_length=5, 
							  default='')
	per = models.IntegerField(default=1)
	rate = models.DecimalField(max_digits=10, 
							   decimal_places=precision)
	date_valid = models.DateField(default=now)

	def __str__(self):
		return f'[{self.code}] {self.name} | '\
			   f'За единица валута: {self.per} | '\
			   f'Курс към лев: {self.rate}'

	def get_rate_to(self, 
				    code: str, 
			        list_: Optional[QuerySet]=None, 
			        precision=precision) -> Decimal:
		currency = None
		if list_ is None:
			currency = Currency.objects.only('per', 'rate') \
							   		   .get(code=code)
		else:
			currency = qs_find(list_, ('code', code))
		result = self._convert(1, to=currency)
		return round(result, precision)

	def convert_to(self, 
				   code: str, 
			       amount: Union[str, float, int], 
			       precision=precision) -> Decimal:
		currency = Currency.objects.only('per', 'rate') \
							       .get(code=code)
		result = self._convert(amount, to=currency)
		return round(result, precision)

	def _convert(self, 
				 amount: Union[str, float, int], 
			     to: Currency) -> Decimal:
		base = self._to_base(Decimal(amount))
		rate = self._get_rate(to)
		result = base / rate \
				 if to.rate > 1 \
				 else base * rate
		return result

	def _to_base(self, 
			     amount: Union[str, float, int]) -> Decimal:
		rate = self.rate \
			   if self.per == 1 \
			   else self.rate / self.per
		result = rate * amount \
			     if self.rate > 1 \
			     else rate / amount
		return result

	def _get_rate(self, currency: Currency) -> Decimal:
		result = currency.rate \
			     if currency.per == 1 \
			     else currency.rate / \
					  currency.per
		return result

	class Meta:
		verbose_name_plural = "currencies"
		ordering =['code']