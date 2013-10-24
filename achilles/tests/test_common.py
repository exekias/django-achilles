from django.test import TestCase
from achilles.common import BaseLibrary


class Library(BaseLibrary):
    pass


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
