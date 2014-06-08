from django.test import TestCase

from achilles.common import (BaseLibrary,
                             achilles_plugins,
                             achilles_renders)


class Library(BaseLibrary):
    pass


class AchillesRendersTests(TestCase):

    def test_achilles_renders(self):
        plugins = achilles_plugins()
        renders = achilles_renders()

        self.assertEqual(set(plugins.keys()), set(renders.keys()))


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
        self.assertRaises(KeyError, self.register.get, 'unknown_item')

    def test_register_unknown_item_global(self):
        self.assertRaises(KeyError, Library.get_global, 'test:unknown_item')

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
