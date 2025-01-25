import pytest
from django.test import TestCase
from django.urls import reverse
from netbox.tests import TestCase as NetBoxTestCase

@pytest.fixture
def netbox_test_case():
    return NetBoxTestCase

@pytest.fixture
def test_case():
    return TestCase 