# queries to add nodes to graph database
queries_to_add_nodes = [
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Ingredient"') YIELD row
        CREATE (:Ingredient {ingredientId: row.ingredient_id, ingredientName: row.main_ingredient})
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Meal"') YIELD row
        CREATE (:Meal {mealId: row.meal_id, mealName: row.name, description: row.description})
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Recipe"') YIELD row
        CREATE (:Recipe {recipeId: row.recipeid, author: row.author});
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Category"') YIELD row
        CREATE (:Category {categoryId: row.category_id, categoryName: row.category})
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Cuisines"') YIELD row
        CREATE (:Cuisines {cuisinesId: row.cuisines_id, cuisinesName: row.cuisines})
    '''
]

# Queries to add relationships between nodes
queries_to_add_relationships = [
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "CategoryToMeal"') YIELD row
        MATCH (c:Category {categoryId: row.category_id})
        MATCH (m:Meal {mealId: row.meal_id})
        MERGE (m) - [:BELONGS_TO] -> (c);
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "CuisineToMeal"') YIELD row
        MATCH (cu:Cuisines {cuisinesId: row.cuisines_id})
        MATCH (m:Meal {mealId: row.meal_id})
        MERGE (m) - [:HAS_CUISINE] -> (cu);    
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "RecipeIngredient"') YIELD row
        MATCH (i:Ingredient {ingredientId: row.ingredient_id})
        MATCH (r:Recipe {recipeId: row.recipe_id})
        MERGE (r) - [:HAS_INGREDIENT] -> (i);
    ''',
    '''
        WITH $jdbc_url AS url
        CALL apoc.load.jdbc(url, 'SELECT * FROM "Recipe"') YIELD row
        MATCH (r:Recipe {recipeId: row.recipeid})
        MATCH (m:Meal {mealId: row.meal_id})
        MERGE (m) - [:BELONGS_TO_RECIPE] -> (r);
    '''
]

def index_queries():
    index_queries = [
        ("Cuisines", "cuisinesId"),
        ("Category", "categoryId"),
        ("Ingredient", "ingredientId"),
        ("Meal", "mealId"),
        ("Recipe", "recipeId")
    ]

    # Generate unique index names and create them
    for label, property in index_queries:
        yield f"""
            CREATE INDEX node_range_index_name IF NOT EXISTS
            FOR (n:{label}) ON (n.{property})
        """