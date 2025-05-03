from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import load_recipes, save_recipes, load_menu, save_menu, load_shopping_list, save_shopping_list

# Blueprintの作成
recipe_bp = Blueprint('recipe', __name__, template_folder='templates/recipe')

# レシピ検索ページ
@recipe_bp.route('/', methods=['GET'])
@login_required
def index():
    recipes = load_recipes()
    query = request.args.get('query', '')
    
    if query:
        filtered_recipes = []
        for recipe in recipes.get('recipes', []):
            # タイトル、材料、タグから検索
            if (query.lower() in recipe['title'].lower() or
                any(query.lower() in ing['name'].lower() for ingredient_type in ['main_ingredients', 'seasonings'] 
                    for ing in recipe.get(ingredient_type, [])) or
                any(query.lower() in tag.lower() for tag in recipe['tags'])):
                filtered_recipes.append(recipe)
        return render_template('index.html', recipes=filtered_recipes, query=query)
    
    return render_template('index.html', recipes=recipes.get('recipes', []), query='')

# レシピ詳細ページ
@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
@login_required
def detail(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes.get('recipes', []) if r['id'] == recipe_id), None)
    
    if not recipe:
        return redirect(url_for('recipe.index'))
    
    return render_template('detail.html', recipe=recipe)

# レシピ追加ページ
@recipe_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        url = request.form.get('url', '')
        summary = request.form.get('summary', '')
        tags = request.form.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]
        
        # 主材料の処理
        main_ingredients = []
        main_names = request.form.getlist('main_name[]')
        main_amounts = request.form.getlist('main_amount[]')
        for i in range(len(main_names)):
            if main_names[i].strip():
                main_ingredients.append({
                    'name': main_names[i].strip(),
                    'amount': main_amounts[i].strip() if i < len(main_amounts) else ''
                })
        
        # 調味料の処理
        seasonings = []
        seasoning_names = request.form.getlist('seasoning_name[]')
        seasoning_amounts = request.form.getlist('seasoning_amount[]')
        for i in range(len(seasoning_names)):
            if seasoning_names[i].strip():
                seasonings.append({
                    'name': seasoning_names[i].strip(),
                    'amount': seasoning_amounts[i].strip() if i < len(seasoning_amounts) else ''
                })
        
        # 手順の処理
        steps = []
        step_texts = request.form.getlist('step[]')
        for step in step_texts:
            if step.strip():
                steps.append(step.strip())
        
        # メモの処理
        notes = request.form.get('notes', '')
        
        recipes = load_recipes()
        new_id = 1
        if recipes.get('recipes'):
            new_id = max(r['id'] for r in recipes['recipes']) + 1
        
        new_recipe = {
            'id': new_id,
            'title': title,
            'url': url,
            'summary': summary,
            'main_ingredients': main_ingredients,
            'seasonings': seasonings,
            'steps': steps,
            'notes': notes,
            'tags': tags
        }
        
        recipes['recipes'].append(new_recipe)
        save_recipes(recipes)
        
        return redirect(url_for('recipe.index'))
    
    return render_template('add.html')

# レシピ削除
@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    recipes = load_recipes()
    # 指定されたIDのレシピを見つける
    recipe_index = None
    for i, recipe in enumerate(recipes.get('recipes', [])):
        if recipe['id'] == recipe_id:
            recipe_index = i
            break
    
    # レシピが見つかった場合は削除
    if recipe_index is not None:
        deleted_recipe = recipes['recipes'].pop(recipe_index)
        save_recipes(recipes)
        return redirect(url_for('recipe.index'))
    
    # レシピが見つからない場合はエラーメッセージを表示
    return render_template('detail.html', 
                          recipe=None, 
                          error="レシピが見つかりませんでした。")

# 材料を買い物リストに追加
@recipe_bp.route('/<int:recipe_id>/add_to_shopping_list', methods=['POST'])
@login_required
def add_to_shopping_list(recipe_id):
    recipes = load_recipes()
    recipe = next((r for r in recipes.get('recipes', []) if r['id'] == recipe_id), None)
    
    if not recipe:
        return redirect(url_for('recipe.index'))
    
    # 買い物リストにレシピの材料を追加
    shopping_list = load_shopping_list()
    
    # 主材料を追加
    for ingredient in recipe.get('main_ingredients', []):
        if ingredient['name'] not in shopping_list['食品']:
            shopping_list['食品'].append(ingredient['name'])
    
    # 調味料を追加（ユーザーの選択により追加するかどうか決定可能）
    add_seasonings = request.form.get('add_seasonings') == 'true'
    if add_seasonings:
        for seasoning in recipe.get('seasonings', []):
            if seasoning['name'] not in shopping_list['食品']:
                shopping_list['食品'].append(seasoning['name'])
    
    save_shopping_list(shopping_list)
    
    return redirect(url_for('recipe.detail', recipe_id=recipe_id))

# 一週間メニュープランナー
@recipe_bp.route('/weekly_menu', methods=['GET', 'POST'])
@login_required
def weekly_menu():
    recipes = load_recipes()
    menu = load_menu()
    
    if request.method == 'POST':
        # 新しい週間メニューの作成
        start_date = request.form.get('start_date')
        days = []
        
        for day in ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']:
            day_menu = {
                'day': day,
                'breakfast': int(request.form.get(f'{day}_breakfast')) if request.form.get(f'{day}_breakfast') else None,
                'lunch': int(request.form.get(f'{day}_lunch')) if request.form.get(f'{day}_lunch') else None,
                'dinner': int(request.form.get(f'{day}_dinner')) if request.form.get(f'{day}_dinner') else None
            }
            days.append(day_menu)
        
        new_week = {
            'id': len(menu.get('weeks', [])) + 1,
            'start_date': start_date,
            'days': days
        }
        
        menu['weeks'].append(new_week)
        save_menu(menu)
        
        return redirect(url_for('recipe.weekly_menu'))
    
    return render_template('menu_planner.html', recipes=recipes.get('recipes', []), weeks=menu.get('weeks', []))

# 一週間メニューから買い物リスト生成
@recipe_bp.route('/generate_shopping_list/<int:week_id>', methods=['POST'])
@login_required
def generate_shopping_list(week_id):
    recipes = load_recipes()
    menu = load_menu()
    
    week = next((w for w in menu.get('weeks', []) if w['id'] == week_id), None)
    
    if not week:
        return redirect(url_for('recipe.weekly_menu'))
    
    # 買い物リストの取得
    shopping_list = load_shopping_list()
    
    # 一週間分のレシピから材料を集める
    for day in week['days']:
        for meal_type in ['breakfast', 'lunch', 'dinner']:
            recipe_id = day.get(meal_type)
            if recipe_id:
                recipe = next((r for r in recipes.get('recipes', []) if r['id'] == recipe_id), None)
                if recipe:
                    # 主材料を追加
                    for ingredient in recipe.get('main_ingredients', []):
                        if ingredient['name'] not in shopping_list['食品']:
                            shopping_list['食品'].append(ingredient['name'])
    
    save_shopping_list(shopping_list)
    
    return redirect(url_for('recipe.weekly_menu'))
