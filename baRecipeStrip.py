# -*- coding: utf-8 -*-
"""
baRecipeStrip.py - Strips Bon Appetit Recipes from given URL


Created on Wed Apr 24 12:54:00 2019

@author: micke
"""

import requests, pyperclip
from datetime import datetime
from bs4 import BeautifulSoup as bs

def BARecipeStrip(URL=None):
    if URL == None:
        # Get address from clipboard.
        URL = pyperclip.paste()
        
    recipeHTML = requests.get(URL)
    
    try:
        recipeHTML.raise_for_status()
    except Exception as exc:
        print('There was a problem: %s' % (exc))
    
    recipeSoup = bs(recipeHTML.text, 'lxml')
    
    ingredient = recipeSoup.select('.ingredient div')
    step = recipeSoup.select('.step p')
    contribName = recipeSoup.select('.contributor-name')
    comment = recipeSoup.select('h2')
    servings = recipeSoup.select('.post-dek-meta span span')
    title = recipeSoup.select('h1 .top-anchor')
    date = recipeSoup.select('.MonthYear')
    
    newRecipe = recipe(title, contribName, comment, servings, step, ingredient, date)



    recipeFile = open(newRecipe.title + '.txt', 'wb')

    recipeFile.write(newRecipe.title.encode('utf-8'))
    recipeFile.write(('\n\nPublished: ' + newRecipe.date).encode('utf-8'))
    recipeFile.write(('\n\nStripped from the web: ' + newRecipe.stripDate).encode('utf-8'))
    recipeFile.write(('\n\n' + newRecipe.comment).encode('utf-8'))
    recipeFile.write(('\n\n' + newRecipe.serving).encode('utf-8'))
    recipeFile.write(('\n\nIngredients:\n\n' + newRecipe.ingredients).encode('utf-8'))
    recipeFile.write(('\n\nRecipe:\n\n' + newRecipe.recipe).encode('utf-8'))
    recipeFile.write(('\n\nBy: ' + newRecipe.author).encode('utf-8'))
    recipeFile.close()


class recipe:
    
    def __init__(self, title, author, comment, servings, steps, ingredient, date):
        self.title = title[0].getText()
        self.author = author[0].getText()
        self.comment = comment[0].getText()
        self.serving = servings[0].getText()
        self.recipe = '\n\n'.join(self.recipeIn(steps))
        self.ingredients = '\n\n'.join(self.ingredientsIn(ingredient))
        self.date = date[0].getText()
        self.stripDate = datetime.now().strftime('%d %B %Y')
    
    def recipeIn(self, stepElems):
        recipeList = []
        for i in stepElems:
            recipeList.append(i.getText())
        return recipeList
    
    def ingredientsIn(self, ingredientElems):
        ingredientList = []
        for i in ingredientElems:
            ingredientList.append(i.getText())
        return ingredientList

BARecipeStrip()
