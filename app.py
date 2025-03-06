from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {
        'cautions': None,
        'calories': None,
        'carbs': None,
        'sugar': None,
        'protein': None,
        'fats': None,
        'fiber': None,
        'dish': None,
        'error': None
    }
    
    if request.method == 'POST':
        result['dish'] = request.form.get('dish')
        print(f"Processing dish: {result['dish']}")
        
        url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"
        headers = {
            "x-rapidapi-key": "7e53339f08msh41410bf2932c95ep171b73jsn195caf675009",
            "x-rapidapi-host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
        }
        params = {
            "nutrition-type": "logging",
            "ingr": result['dish']
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"API Response: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            
            if 'error' in data:
                result['error'] = data['error']
            else:
                result['cautions'] = data.get('cautions', [])
                nutrients = data.get('totalNutrients', {})
                
                result['calories'] = nutrients.get('ENERC_KCAL', {}).get('quantity', 0)
                result['carbs'] = nutrients.get('CHOCDF', {}).get('quantity', 0)
                result['sugar'] = nutrients.get('SUGAR', {}).get('quantity', 0)
                result['protein'] = nutrients.get('PROCNT', {}).get('quantity', 0)
                result['fats'] = nutrients.get('FAT', {}).get('quantity', 0)
                result['fiber'] = nutrients.get('FIBTG', {}).get('quantity', 0)
                
        except requests.exceptions.RequestException as e:
            result['error'] = f"API request failed: {str(e)}"
        except ValueError as e:
            result['error'] = "Invalid response format from API"
        except Exception as e:
            result['error'] = f"An unexpected error occurred: {str(e)}"

    return render_template('index.html', **result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)