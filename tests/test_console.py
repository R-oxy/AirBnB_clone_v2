#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import pep8
import unittest
import models
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """HBNBCommand testing setup.

        Temporarily rename any existing file.json.
        Reset FileStorage objects dictionary.
        Create an instance of the command interpreter.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        cls.HBNB = HBNBCommand()

    @classmethod
    def tearDownClass(cls):
        """HBNBCommand testing teardown.

        Restore original file.json.
        Delete the test HBNBCommand instance.
        """
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.HBNB
        if type(models.storage) == DBStorage:
            models.storage._DBStorage__session.close()

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_pep8(self):
        """Test Pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, "fix Pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(HBNBCommand.__doc__)
        self.assertIsNotNone(HBNBCommand.emptyline.__doc__)
        self.assertIsNotNone(HBNBCommand.do_quit.__doc__)
        self.assertIsNotNone(HBNBCommand.do_EOF.__doc__)
        self.assertIsNotNone(HBNBCommand.do_create.__doc__)
        self.assertIsNotNone(HBNBCommand.do_show.__doc__)
        self.assertIsNotNone(HBNBCommand.do_destroy.__doc__)
        self.assertIsNotNone(HBNBCommand.do_all.__doc__)
        self.assertIsNotNone(HBNBCommand.do_update.__doc__)
        self.assertIsNotNone(HBNBCommand.count.__doc__)
        self.assertIsNotNone(HBNBCommand.strip_clean.__doc__)
        self.assertIsNotNone(HBNBCommand.default.__doc__)

    def test_emptyline(self):
        """Test empty line input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_quit(self):
        """Test quit command input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("quit")
            self.assertEqual("", f.getvalue())

    def test_EOF(self):
        """Test that EOF quits."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.HBNB.onecmd("EOF"))

    def test_create_errors(self):
        """Test create command errors."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create asdfsfsd")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create(self):
        """Test create command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create User")
            us = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            st = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Place")
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create City")
            ct = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Review")
            rv = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create Amenity")
            am = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            self.assertIn(us, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(st, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            self.assertIn(pl, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all City")
            self.assertIn(ct, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Review")
            self.assertIn(rv, f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(am, f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_kwargs(self):
        """Test create command with kwargs."""
        with patch("sys.stdout", new=StringIO()) as f:
            call = ('create Place city_id="0001" name="My_house" '
                    'number_rooms=4 latitude=37.77 longitude=a')
            self.HBNB.onecmd(call)
            pl = f.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all Place")
            output = f.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'My house'", output)
            self.assertIn("'number_rooms': 4", output)
            self.assertIn("'latitude': 37.77", output)
            self.assertNotIn("'longitude'", output)

    def test_show(self):
        """Test show command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_show_valid(self):
        """Test show valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("create User")
            self.HBNB.onecmd("create Place")
            self.HBNB.onecmd("create City")
            self.HBNB.onecmd("create Review")
            self.HBNB.onecmd("create Amenity")
            self.HBNB.onecmd("show State")
            self.assertIn(
                "created: [{}] {}".format(State.__name__,
                                          eval(f.getvalue()).id), f.getvalue())
            self.HBNB.onecmd("show User")
            self.assertIn(
                "created: [{}] {}".format(User.__name__,
                                          eval(f.getvalue()).id), f.getvalue())
            self.HBNB.onecmd("show Place")
            self.assertIn(
                "created: [{}] {}".format(Place.__name__,
                                          eval(f.getvalue()).id), f.getvalue())
            self.HBNB.onecmd("show City")
            self.assertIn(
                "created: [{}] {}".format(City.__name__,
                                          eval(f.getvalue()).id), f.getvalue())
            self.HBNB.onecmd("show Review")
            self.assertIn(
                "created: [{}] {}".format(Review.__name__,
                                          eval(f.getvalue()).id), f.getvalue())
            self.HBNB.onecmd("show Amenity")
            self.assertIn(
                "created: [{}] {}".format(Amenity.__name__,
                                          eval(f.getvalue()).id), f.getvalue())

    def test_show_valid_id(self):
        """Test show valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("show State")
            output = f.getvalue()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("show State {}".format(output))
            self.assertIn(output, f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_destroy(self):
        """Test destroy command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_destroy_valid(self):
        """Test destroy valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("destroy State")
            self.assertNotIn(
                "{}".format(eval(f.getvalue()).id), f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_destroy_valid_id(self):
        """Test destroy valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            output = f.getvalue()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("destroy State {}".format(output))
            self.assertNotIn(output, f.getvalue())

    def test_all(self):
        """Test all command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all")
            self.assertIn(
                "[{}]".format(User.__name__), f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("all State")
            self.assertIn(
                "[{}]".format(State.__name__), f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_count(self):
        """Test count command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("count")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("count asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())

    def test_count_valid(self):
        """Test count valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("count State")
            self.assertEqual(
                "2\n", f.getvalue())

    def test_count_valid_plural(self):
        """Test count valid plural command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("count States")
            self.assertEqual(
                "2\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update(self):
        """Test update command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    def test_update_valid(self):
        """Test update valid command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("update State")
            self.assertEqual(
                "** instance id missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("update State 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_update_attrs(self):
        """Test update attributes."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("create State")
            self.HBNB.onecmd("update State 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd("update State 12345")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd('update State "California"')
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd('update State "California" Name="New York"')
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd('update State "California" name="New York"')
            self.assertEqual(
                "", f.getvalue().strip())
            self.HBNB.onecmd("show State California")
            self.assertIn(
                "[{}] {}".format(State.__name__,
                                 eval(f.getvalue()).id), f.getvalue())
            self.assertIn(
                "'name': 'New York'", f.getvalue())
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd('update State "California" n"New York"')
            self.assertEqual(
                "** value missing **\n", f.getvalue())

    def test_default(self):
        """Test default command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("asdfsdrfs.show()")
            self.assertEqual(
                "** command not found **\n", f.getvalue())

    def test_strip_clean(self):
        """Test strip clean function."""
        s = ("HBNBCommand.asdfsdrfs.show('1234')\nasdfsdasf")
        self.assertEqual(self.HBNB.strip_clean(s), "asdfsdrfs.show('1234')")

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_show_unique_id(self):
        """Test show command with unique id."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.HBNB.onecmd("show State")
            self.assertIn(
                "[{}]".format(State.__name__), f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_create_already_exist(self):
        """Test create command."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            output = f.getvalue()
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd('create State name="California"')
            self.assertNotEqual(output, f.getvalue())


if __name__ == "__main__":
    unittest.main()
