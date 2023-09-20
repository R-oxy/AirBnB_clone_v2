#!/usr/bin/python3
"""Defines unittests for console.py."""

import unittest
import console  # Import your console module
from models.base_model import BaseModel
from models.user import User

HBNBCommand = console.HBNBCommand

class TestConsoleFunctionality(unittest.TestCase):
    """Class for testing the functionality of the console"""

    def setUp(self):
        """Set up any necessary resources for testing"""
        # Initialize your console and models here if needed
        self.console = HBNBCommand()
        self.base_model = BaseModel()
        self.user_model = User()

    def tearDown(self):
        """Clean up any resources after testing"""
        # Clean up any resources or perform post-test actions here
        pass

    def test_create_command(self):
        """Test the 'create' command functionality"""
        # Use 'create' command to create instances of objects
        # Check if they were created correctly by comparing attributes
        self.console.do_create("BaseModel name=\"test_name\" age=10")
        created_instance = None
        for obj in self.console.classes['BaseModel'].__objects.values():
            if obj.name == "test_name" and obj.age == 10:
                created_instance = obj
                break

        self.assertIsNotNone(created_instance, "Instance creation failed")
        self.assertEqual(created_instance.name, "test_name", "Name attribute does not match")
        self.assertEqual(created_instance.age, 10, "Age attribute does not match")

    def test_show_command(self):
        """Test the 'show' command functionality"""
        # Create a test instance
        self.console.do_create("BaseModel name=\"test_name\" age=10")
        
        # Use 'show' command to display the created instance
        result = self.console.onecmd("show BaseModel")
        
        # Implement assertions to check if the output matches expectations
        self.assertIn("test_name", result, "Show command failed")

    def test_destroy_command(self):
        """Test the 'destroy' command functionality"""
        # Create a test instance
        self.console.do_create("BaseModel name=\"test_name\" age=10")
        
        # Use 'destroy' command to delete the created instance
        result = self.console.onecmd("destroy BaseModel")
        
        # Implement assertions to check if the instance is deleted
        self.assertIsNone(self.console.classes['BaseModel'].__objects.get("test_name"), "Destroy command failed")

    def test_all_command(self):
        """Test the 'all' command functionality"""
        # Create multiple test instances
        self.console.do_create("BaseModel name=\"test_name1\" age=10")
        self.console.do_create("BaseModel name=\"test_name2\" age=20")
        
        # Use 'all' command to retrieve all instances of BaseModel
        result = self.console.onecmd("all BaseModel")
        
        # Implement assertions to check if the output contains the expected instances
        self.assertIn("test_name1", result, "All command failed")
        self.assertIn("test_name2", result, "All command failed")

    def test_update_command(self):
        """Test the 'update' command functionality"""
        # Create a test instance
        self.console.do_create("BaseModel name=\"test_name\" age=10")
        
        # Use 'update' command to modify attributes of the created instance
        result = self.console.onecmd("update BaseModel test_name name=\"new_name\" age=30")
        
        # Implement assertions to check if the instance is updated correctly
        updated_instance = self.console.classes['BaseModel'].__objects.get("test_name")
        self.assertIsNotNone(updated_instance, "Update command failed")
        self.assertEqual(updated_instance.name, "new_name", "Name attribute not updated correctly")
        self.assertEqual(updated_instance.age, 30, "Age attribute not updated correctly")

if __name__ == "__main__":
    unittest.main()
