from django.shortcuts import render
from django.views.generic import ListView, DetailView   #to display lists
from .models import Recipe                #to access Recipe model
#to protect class-based view
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RecipesSearchForm
from .models import Recipe
import pandas as pd
from .utils import get_chart, get_recipename_from_id

# Create your views here.
def home(request):
   return render(request, '../templates/recipes/recipes_home.html')

def records(request):
   #create an instance of SalesSearchForm that you defined in sales/forms.py
   form = RecipesSearchForm(request.POST or None)
   recipes_df=None     #initialize dataframe to None
   chart = None

   #check if the button is clicked
   if request.method =='POST':
       recipe_title = request.POST.get('recipe_title')
       chart_type = request.POST.get('chart_type')

       qs = Recipe.objects.all()
       qs = Recipe.objects.filter(name__contains=recipe_title)
       if qs:      #if data found
           #convert the queryset values to pandas dataframe
           recipes_df=pd.DataFrame(qs.values()) 
           print(recipes_df)
           
           chart=get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
           recipes_df=recipes_df.to_html()

       print (qs.values())
       print (qs.values_list())

       obj = Recipe.objects.get(id=2)
       print (obj)

   #pack up data to be sent to template in the context dictionary
   context={
           'form': form,
           'recipes_df': recipes_df,
           'chart': chart
   }

   return render(request, '../templates/recipes/records.html', context)

# Create your views here.
class RecipeListView(LoginRequiredMixin, ListView):           #class-based view
   model = Recipe                         #specify model
   template_name = '../templates/recipes/recipe_list.html'    #specify template 

class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "../templates/recipes/recipe_details.html"