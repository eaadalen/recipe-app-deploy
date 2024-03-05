from django.test import TestCase
from django.urls import reverse
from .models import Recipe
from .forms import RecipesSearchForm

class RecipeModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up a Recipe object once for all test methods in this class.
        cls.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients_list='Ingredient1,Ingredient2,Ingredient3',
            cooking_time=30,
            difficulty='Easy',
            date_created="2024-03-02",
            pic='no_picture.jpg'
        )
    
    def test_recipe_creation(self):
        # Test that a Recipe object is correctly created.
        self.assertTrue(isinstance(self.recipe, Recipe))
        self.assertEqual(self.recipe.__str__(), self.recipe.name)
    
    def test_recipe_name(self):
        # Check that the 'name' field's verbose name is as expected.
        recipe_name_label = self.recipe._meta.get_field('name').verbose_name
        self.assertEqual(recipe_name_label, 'name')

    def test_string_representation(self):
        # Test the string representation of a Recipe object (should be its name).
        self.assertEqual(str(self.recipe), self.recipe.name)
    
    def test_return_ingredients_as_list(self):
        # Ensure the ingredients are correctly split into a list.
        ingredients_list = self.recipe.return_ingredients_as_list()
        self.assertEqual(len(ingredients_list), 3)
    
    def test_calculate_difficulty(self):
        # Test the difficulty calculation for various scenarios.
        self.recipe.cooking_time = 5
        self.recipe.ingredients_list = 'Ingredient1,Ingredient2'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Easy')
        
        self.recipe.cooking_time = 15
        self.recipe.ingredients_list = 'Ingredient1,Ingredient2,Ingredient3,Ingredient4'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Hard')
        
    def test_save_method_override(self):
        # Check that the difficulty is correctly set when a Recipe is saved.
        self.recipe.cooking_time = 20
        self.recipe.ingredients_list = 'Ingredient1,Ingredient2,Ingredient3'
        self.recipe.save()
        self.assertEqual(self.recipe.difficulty, 'Intermediate')
    
    def test_default_image_path(self):
        # Verify the default image path is set as expected.
        self.assertEqual(self.recipe.pic, 'no_picture.jpg')

class RecipeViewsTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Set up data for the view tests.
        cls.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients_list='Ingredient1,Ingredient2,Ingredient3',
            cooking_time=30,
            difficulty='Easy',
            date_created="2024-03-02",
            pic='no_picture.jpg'
        )
    
    def test_home_page_status_code(self):
        # Test the home page is accessible and returns a HTTP 200 status.
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class SearchFormTest(TestCase):

    def test_cooking_time_validation(self):
        # Test with invalid cooking time
        form_data_invalid = {
            'min_cooking_time': -5,  # Invalid value
            'max_cooking_time': 'not a number'  # Invalid value
        }
        form_invalid = RecipesSearchForm(data=form_data_invalid)
        self.assertFalse(form_invalid.is_valid())
