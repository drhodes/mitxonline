from factory import fuzzy, SubFactory
from factory.django import DjangoModelFactory
import faker
import random
from mitol.common.utils import now_in_utc

from ecommerce.factories import DiscountFactory
from flexiblepricing import models
from flexiblepricing.constants import FlexiblePriceStatus

from courses.factories import CourseFactory
from users.factories import UserFactory

FAKE = faker.Factory.create()


class CurrencyExchangeRateFactory(DjangoModelFactory):
    currency_code = FAKE.currency_code()
    exchange_rate = random.randrange(0, 100, 1) / 100

    class Meta:
        model = models.CurrencyExchangeRate


class CountryIncomeThresholdFactory(DjangoModelFactory):
    country_code = FAKE.country_code()
    income_threshold = random.randrange(1000, 750000, 1000)

    class Meta:
        model = models.CountryIncomeThreshold


class FlexiblePriceTierFactory(DjangoModelFactory):
    income_threshold_usd = random.randrange(0, 150000, 1000)
    courseware_object = SubFactory(CourseFactory)
    discount = SubFactory(DiscountFactory)

    class Meta:
        model = models.FlexiblePriceTier


class FlexiblePriceFactory(DjangoModelFactory):
    user = SubFactory(UserFactory)
    income_usd = random.randrange(0, 150000, 1000)
    original_currency = FAKE.currency_code()
    country_of_income = FAKE.country_code()
    date_exchange_rate = now_in_utc()
    date_documents_sent = now_in_utc()
    justification = FAKE.paragraph()
    country_of_residence = FAKE.country()
    status = FlexiblePriceStatus.ALL_STATUSES[
        random.randrange(0, len(FlexiblePriceStatus.ALL_STATUSES), 1)
    ]
    courseware_object = SubFactory(CourseFactory)
    tier = SubFactory(FlexiblePriceTierFactory)

    class Meta:
        model = models.FlexiblePrice
