from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from models import load_recipes, save_recipes, load_menu, save_menu, load_shopping_list, save_shopping_list
import logging
import builtins  # 追加: Python組み込み関数用

# Blueprintの作成
recipe_bp = Blueprint('recipe', __name__, template_folder='templates/recipe')
logger = logging.getLogger(__name__)

# テンプレートでenumerate関数を使えるようにする - 追加
@recipe_bp.app_template_global()
def enumerate(iterable, start=0):
    # builtinsモジュールから組み込みのenumerate関数を明示的に使用
    return [(i, item) for i, item in builtins.enumerate(iterable, start)]

# レシピ検索ページ
@recipe_bp.route('/', methods=['GET'])
@login_required
def index():
    error = None
    try:
        recipes = load_recipes()
        query = request.args.get('query', '')
        
        if query:
            filtered_recipes = []
            for recipe in recipes.get('recipes', []):
                try:
                    # タイトル検索
                    title_match = query.lower() in recipe.get('title', '').lower()
                    
                    # 材料検索 (構造をチェックしてからアクセス)
                    ingredient_match = False
                    # 旧形式: 'ingredients'キーがある場合
                    if 'ingredients' in recipe and isinstance(recipe['ingredients'], list):
                        ingredient_match = any(query.lower() in ing.lower() for ing in recipe['ingredients'])
                    # 新形式: 'main_ingredients', 'seasonings'キーがある場合
                    for ingredient_type in ['main_ingredients', 'seasonings']:
                        if ingredient_type in recipe and isinstance(recipe[ingredient_type], list):
                            # 名前のあるdict形式の材料
                            if all(isinstance(ing, dict) for ing in recipe[ingredient_type]):
                                ingredient_match = ingredient_match or any(
                                    query.lower() in ing.get('name', '').lower() 
                                    for ing in recipe[ingredient_type]
                                )
                            # 文字列形式の材料
                            elif all(isinstance(ing, str) for ing in recipe[ingredient_type]):
                                ingredient_match = ingredient_match or any(
                                    query.lower() in ing.lower() 
                                    for ing in recipe[ingredient_type]
                                )
                    
                    # タグ検索
                    tag_match = False
                    if 'tags' in recipe and isinstance(recipe['tags'], list):
                        tag_match = any(query.lower() in tag.lower() for tag in recipe['tags'])
                    
                    if title_match or ingredient_match or tag_match:
                        filtered_recipes.append(recipe)
                except Exception as e:
                    logger.error(f"レシピID {recipe.get('id', 'unknown')} の検索中にエラーが発生しました: {e}")
                    continue
            
            return render_template('index.html', recipes=filtered_recipes, query=query, error=error)
    
    except Exception as e:
        logger.error(f"レシピ検索中にエラーが発生しました: {e}")
        error = "レシピの検索中にエラーが発生しました"
        flash(error, "error")
        return render_template('index.html', recipes=[], query=query, error=error)
    
    return render_template('index.html', recipes=recipes.get('recipes', []), query='', error=error)

# レシピ詳細ページ
@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
@login_required
def detail(recipe_id):
    error = None
    try:
        recipes = load_recipes()
        recipe = next((r for r in recipes.get('recipes', []) if r['id'] == recipe_id), None)
        
        if not recipe:
            error = "レシピが見つかりませんでした"
            flash(error, "error")
            return redirect(url_for('recipe.index'))
    
    except Exception as e:
        logger.error(f"レシピ詳細の取得中にエラーが発生しました: {e}")
        error = "レシピの取得中にエラーが発生しました"
        flash(error, "error")
        return redirect(url_for('recipe.index'))
    
    return render_template('detail.html', recipe=recipe, error=error)

# レシピ追加ページ
@recipe_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    error = None
    
    if request.method == 'POST':
        try:
            title = request.form.get('title', '').strip()
            
            if not title:
                error = "レシピ名は必須です"
                flash(error, "error")
                return render_template('add.html', error=error)
            
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
                new_id = max((r.get('id', 0) for r in recipes['recipes']), default=0) + 1
            
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
            
            if save_recipes(recipes):
                logger.info(f"レシピを追加しました: {title} (ID: {new_id})")
                flash(f"レシピ「{title}」を追加しました", "success")
                return redirect(url_for('recipe.index'))
            else:
                error = "レシピの保存に失敗しました"
                flash(error, "error")
        
        except Exception as e:
            logger.error(f"レシピ追加中にエラーが発生しました: {e}")
            error = "レシピの追加中にエラーが発生しました"
            flash(error, "error")
    
    return render_template('add.html', error=error)

# レシピ削除
@recipe_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    error = None
    
    try:
        recipes = load_recipes()
        recipe_index = None
        
        for i, recipe in enumerate(recipes.get('recipes', [])):
            if recipe.get('id') == recipe_id:
                recipe_index = i
                break
        
        if recipe_index is not None:
            deleted_recipe = recipes['recipes'].pop(recipe_index)
            
            if save_recipes(recipes):
                logger.info(f"レシピを削除しました: {deleted_recipe.get('title')} (ID: {recipe_id})")
                flash(f"レシピ「{deleted_recipe.get('title')}」を削除しました", "success")
                return redirect(url_for('recipe.index'))
            else:
                error = "レシピの削除に失敗しました"
                flash(error, "error")
        else:
            error = "レシピが見つかりませんでした"
            flash(error, "error")
    
    except Exception as e:
        logger.error(f"レシピ削除中にエラーが発生しました: {e}")
        error = "レシピの削除中にエラーが発生しました"
        flash(error, "error")
    
    return render_template('detail.html', recipe=None, error=error)

# 材料を買い物リストに追加
@recipe_bp.route('/<int:recipe_id>/add_to_shopping_list', methods=['POST'])
@login_required
def add_to_shopping_list(recipe_id):
    error = None
    
    try:
        recipes = load_recipes()
        recipe = next((r for r in recipes.get('recipes', []) if r.get('id') == recipe_id), None)
        
        if not recipe:
            error = "レシピが見つかりませんでした"
            flash(error, "error")
            return redirect(url_for('recipe.index'))
        
        shopping_list = load_shopping_list()
        items_added = 0
        
        # 主材料を追加
        for ingredient in recipe.get('main_ingredients', []):
            # dictの場合
            if isinstance(ingredient, dict) and ingredient.get('name'):
                if ingredient['name'] not in shopping_list['食品']:
                    shopping_list['食品'].append(ingredient['name'])
                    items_added += 1
            # 文字列の場合 (古い形式)
            elif isinstance(ingredient, str) and ingredient:
                if ingredient not in shopping_list['食品']:
                    shopping_list['食品'].append(ingredient)
                    items_added += 1
        
        # 旧形式の材料を処理
        if 'ingredients' in recipe and isinstance(recipe['ingredients'], list):
            for ingredient in recipe['ingredients']:
                if ingredient and ingredient not in shopping_list['食品']:
                    shopping_list['食品'].append(ingredient)
                    items_added += 1
        
        # 調味料を追加（ユーザーの選択により追加するかどうか決定可能）
        add_seasonings = request.form.get('add_seasonings') == 'true'
        
        if add_seasonings:
            for seasoning in recipe.get('seasonings', []):
                # dictの場合
                if isinstance(seasoning, dict) and seasoning.get('name'):
                    if seasoning['name'] not in shopping_list['食品']:
                        shopping_list['食品'].append(seasoning['name'])
                        items_added += 1
                # 文字列の場合
                elif isinstance(seasoning, str) and seasoning:
                    if seasoning not in shopping_list['食品']:
                        shopping_list['食品'].append(seasoning)
                        items_added += 1
        
        if save_shopping_list(shopping_list):
            logger.info(f"レシピの材料を買い物リストに追加しました: {recipe.get('title')} (ID: {recipe_id}) - {items_added}個のアイテム")
            flash(f"「{recipe.get('title')}」の材料を買い物リストに追加しました", "success")
        else:
            error = "買い物リストの保存に失敗しました"
            flash(error, "error")
    
    except Exception as e:
        logger.error(f"買い物リストへの追加中にエラーが発生しました: {e}")
        error = "買い物リストへの追加中にエラーが発生しました"
        flash(error, "error")
    
    return redirect(url_for('recipe.detail', recipe_id=recipe_id))

# 一週間メニュープランナー
@recipe_bp.route('/weekly_menu', methods=['GET', 'POST'])
@login_required
def weekly_menu():
    error = None
    
    try:
        recipes = load_recipes()
        menu = load_menu()
        
        if request.method == 'POST':
            start_date = request.form.get('start_date', '')
            
            if not start_date:
                error = "開始日を入力してください"
                flash(error, "error")
                return render_template('menu_planner.html', recipes=recipes.get('recipes', []), weeks=menu.get('weeks', []), error=error)
            
            days = []
            
            for day in ['月曜日', '火曜日', '水曜日', '木曜日', '金曜日', '土曜日', '日曜日']:
                breakfast = request.form.get(f'{day}_breakfast')
                lunch = request.form.get(f'{day}_lunch')
                dinner = request.form.get(f'{day}_dinner')
                
                day_menu = {
                    'day': day,
                    'breakfast': int(breakfast) if breakfast and breakfast.isdigit() else None,
                    'lunch': int(lunch) if lunch and lunch.isdigit() else None,
                    'dinner': int(dinner) if dinner and dinner.isdigit() else None
                }
                days.append(day_menu)
            
            new_id = len(menu.get('weeks', [])) + 1
            
            new_week = {
                'id': new_id,
                'start_date': start_date,
                'days': days
            }
            
            menu['weeks'].append(new_week)
            
            if save_menu(menu):
                logger.info(f"新しい週間メニューを作成しました: {start_date}から (ID: {new_id})")
                flash(f"{start_date}からの週間メニューを作成しました", "success")
                return redirect(url_for('recipe.weekly_menu'))
            else:
                error = "週間メニューの保存に失敗しました"
                flash(error, "error")
    
    except Exception as e:
        logger.error(f"週間メニュー処理中にエラーが発生しました: {e}")
        error = "週間メニューの処理中にエラーが発生しました"
        flash(error, "error")
        recipes = load_recipes()
        menu = load_menu()
    
    return render_template('menu_planner.html', recipes=recipes.get('recipes', []), weeks=menu.get('weeks', []), error=error)

# 一週間メニューから買い物リスト生成
@recipe_bp.route('/generate_shopping_list/<int:week_id>', methods=['POST'])
@login_required
def generate_shopping_list(week_id):
    error = None
    
    try:
        recipes = load_recipes()
        menu = load_menu()
        
        week = next((w for w in menu.get('weeks', []) if w.get('id') == week_id), None)
        
        if not week:
            error = "指定された週間メニューが見つかりませんでした"
            flash(error, "error")
            return redirect(url_for('recipe.weekly_menu'))
        
        shopping_list = load_shopping_list()
        items_added = 0
        
        for day in week.get('days', []):
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                recipe_id = day.get(meal_type)
                
                if recipe_id:
                    recipe = next((r for r in recipes.get('recipes', []) if r.get('id') == recipe_id), None)
                    
                    if recipe:
                        # 主材料を追加
                        for ingredient in recipe.get('main_ingredients', []):
                            # dictの場合
                            if isinstance(ingredient, dict) and ingredient.get('name'):
                                if ingredient['name'] not in shopping_list['食品']:
                                    shopping_list['食品'].append(ingredient['name'])
                                    items_added += 1
                            # 文字列の場合 (古い形式)
                            elif isinstance(ingredient, str) and ingredient:
                                if ingredient not in shopping_list['食品']:
                                    shopping_list['食品'].append(ingredient)
                                    items_added += 1
                        
                        # 旧形式の材料を処理
                        if 'ingredients' in recipe and isinstance(recipe['ingredients'], list):
                            for ingredient in recipe['ingredients']:
                                if ingredient and ingredient not in shopping_list['食品']:
                                    shopping_list['食品'].append(ingredient)
                                    items_added += 1
        
        if save_shopping_list(shopping_list):
            logger.info(f"週間メニューから買い物リストを生成しました: {items_added}個のアイテムを追加")
            flash(f"週間メニューの材料を買い物リストに追加しました ({items_added}個のアイテム)", "success")
        else:
            error = "買い物リストの保存に失敗しました"
            flash(error, "error")
    
    except Exception as e:
        logger.error(f"買い物リスト生成中にエラーが発生しました: {e}")
        error = "買い物リストの生成中にエラーが発生しました"
        flash(error, "error")
    
    return redirect(url_for('recipe.weekly_menu'))

# レシピ詳細をJSONで取得するAPI（JavaScriptからの呼び出し用）
@recipe_bp.route('/api/recipe/<int:recipe_id>', methods=['GET'])
@login_required
def get_recipe_json(recipe_id):
    try:
        recipes = load_recipes()
        recipe = next((r for r in recipes.get('recipes', []) if r.get('id') == recipe_id), None)
        
        if not recipe:
            return jsonify({'error': 'Recipe not found'}), 404
        
        return jsonify(recipe)
    
    except Exception as e:
        logger.error(f"レシピAPIでエラーが発生しました: {e}")
        return jsonify({'error': 'Internal server error'}), 500
