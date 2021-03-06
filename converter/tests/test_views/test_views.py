from django.test import TestCase
from django.test import Client
import datetime
from unittest.mock import patch
from typing import Sequence, List, Mapping, Any
from converter.tests.utility import *

from converter.models import Currency


class TestViews(TestCase):
	def test_index_view(self) -> None:
		currency1 = create_currency()
		currencies = Currency.objects.all()

		client = Client()
		response = client.get('')

		self._check_index_view_context(response.context, currencies, currency1)
		self._check_index_view_template(response.templates)
		Currency.objects.all().delete()

	def _check_index_view_context(self, 
								  context: Mapping[str, Any], 
								  currencies: QuerySet, 
								  currency: Currency) -> None:
		self.assertEqual(len(context['currencies']), 
						 len(currencies))
		self.assertEqual(context['amount'], 1)
		self.assertEqual(context['from_currency'], 
						 currency)
		self.assertEqual(context['to_currency'], 
						 currency)
		self.assertEqual(context['rate'], 1)
		self.assertEqual(context['date_valid'], currency.date_valid)
		self.assertEqual(context['conversion_result'], 1)

	def _check_index_view_template(self, 
								   templates: Sequence[Templates]) -> None:
		template_list = self._get_template_names(templates)
		self.assertTrue('converter/index.html' in template_list)

	def _get_template_names(self, 
						   template_list: Sequence[Template]) -> List[str]:
		template_names = []
		for template in template_list:
			template_names.append(template.name)
		return template_names

	def test_convert_view(self) -> None:
		currency1 = create_currency()
		currency2 = create_currency(name='Currency 2',
								    code='DEF',
								    rate=54.54321)
		client = Client()
		response = client.get('/convert/?amount=2&from=ABC&to=DEF')

		self._check_convert_view_response(response)
		Currency.objects.all().delete()

	def _check_convert_view_response(self, response: Response) -> None:
		decoded = response.json()
		self.assertEqual(decoded['result'], '0.44454')
		self.assertEqual(decoded['rate_info']['amount'], '2')
		self.assertEqual(decoded['rate_info']['from_currency_name'], 'Currency 1')
		self.assertEqual(decoded['rate_info']['to_currency_name'], 'Currency 2')
		self.assertEqual(decoded['rate_info']['amount'], '2')
		self.assertEqual(decoded['rate_info']['rate'], '0.22227')

	def test_admin_currencies_list_view(self) -> None:
		client = Client()
		response = client.get('/admin/converter/currency/')
		self.assertEqual(response.status_code, 302)

	@patch('converter.utility.currency.update_currency_data')
	def test_update_currencies_view(self, 
								    mock_update_currency_data: MagicMock) -> None:
		currency1 = create_currency(name='Currency 1',
								    code='ABC',
								    per=1,
								    rate=12.12345,
								    date_valid=date_valid)
		existing = Currency.objects.all()

		client = Client()
		response = client.get('/update-currencies/')

		mock_update_currency_data.assert_called_with(existing)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, '/admin/converter/currency/')

		existing.delete()