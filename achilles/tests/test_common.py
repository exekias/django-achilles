from django.test import TestCase
from django.test import RequestFactory

from achilles.common import (BaseLibrary,
                             achilles_data,
                             achilles_plugins,
                             achilles_renders)


class Library(BaseLibrary):
    pass


class AchillesDataTests(TestCase):

    @classmethod
    def setupClass(cls):
        cls.request_factory = RequestFactory()

    def setUp(self):
        self.request = self.request_factory.get('/path')

    def test_achilles_data_not_found(self):
        self.assertRaises(KeyError, achilles_data, self.request, 'foobar')

    def test_achilles_data_default(self):
        result = achilles_data(self.request, 'foobar', 'Default value')
        self.assertEqual(result, 'Default value')

    def test_achilles_data_get(self):
        my_data = {'a': 3, 'b': 4}
        result = achilles_data(self.request, 'mydata', my_data)
        self.assertEqual(result, my_data)

        result2 = achilles_data(self.request, 'mydata', my_data)
        self.assertEqual(result2, my_data)


class AchillesRendersTests(TestCase):

    def test_achilles_renders(self):
        plugins = achilles_plugins()
        renders = achilles_renders()

        self.assertListEqual(plugins.keys(), renders.keys())


class LibraryTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.register = Library('test')

    def test_register_function1(self):
        @self.register.register
        def test():
            pass

        self.assertIs(self.register.get('test'), test)

    def test_register_function2(self):
        @self.register.register()
        def test():
            pass

        self.assertIs(self.register.get('test'), test)

    def test_register_unknown_item(self):
        self.assertRaises(KeyError, Library.get_global, 'unknown_item')

    def test_register_get_global(self):
        @self.register.register
        def test():
            pass

        self.assertIs(Library.get_global('test:test'), test)

    def test_register_namespaces(self):
        register = Library('namespace')

        @register.register
        def test():
            pass

        self.assertIs(Library.get_global('namespace:test'), test)

    def test_register_duplicated_namespaces(self):
        Library('repeated')
        self.assertRaises(ValueError, Library, 'repeated')

    def test_register_unknown_namespace(self):
        self.assertRaises(KeyError, Library.get_global, 'unknown:namespace')
