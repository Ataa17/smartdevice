from django.shortcuts import render

# Create your views here.
def interface(request):
    context = {
        'temperature': 25,  # Replace with real data
        'red': True,         # Replace with real data
        'green': False,        # Replace with real data
        'blue': False,        # Replace with real data
        'distance': 100,    # Replace with real data
    }
    return render(request, 'interface/interface.html',context)