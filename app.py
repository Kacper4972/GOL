from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, bcrypt, SavedSimulation
from game import GameOfLife
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- WIDOKI AUTORYZACJI ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Użytkownik już istnieje', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Rejestracja zakończona sukcesem! Możesz się zalogować.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        
        flash('Błędne dane logowania', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- OBSŁUGA GRY W ŻYCIE ---
@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/get_grid')
@login_required
def get_grid():
    if current_user.game_state:
        return jsonify(eval(current_user.game_state))  # Odczyt z bazy
    else:
        return jsonify(GameOfLife().get_grid())  # Nowa plansza

@app.route('/next_generation', methods=['POST'])
@login_required
def next_generation():
    game = GameOfLife()
    
    if current_user.game_state:
        game.grid = eval(current_user.game_state)  # Załaduj planszę z bazy
    
    game.next_generation()
    current_user.game_state = str(game.get_grid())  # Zapisz do bazy
    db.session.commit()

    return jsonify(game.get_grid())

from flask import g
from flask_login import current_user

@app.context_processor
def inject_user():
    return dict(current_user=current_user)


import json
from flask import request

@app.route('/update_grid', methods=['POST'])
@login_required
def update_grid():
    data = request.get_json()
    current_user.game_state = json.dumps(data['grid'])  # Zapisujemy nowy stan planszy do bazy
    db.session.commit()
    return jsonify(success=True)

@app.route('/random_grid', methods=['POST'])
@login_required
def random_grid():
    game = GameOfLife()
    current_user.game_state = json.dumps(game.get_grid())  # Losujemy nową planszę i zapisujemy do bazy
    db.session.commit()
    return jsonify(success=True)

@app.route('/save_simulation', methods=['POST'])
@login_required
def save_simulation():
    data = request.get_json()
    sim_name = data.get("name")
    
    if not sim_name:
        return jsonify({"error": "Nazwa symulacji jest wymagana"}), 400

    if not current_user.game_state:
        return jsonify({"error": "Brak aktywnej symulacji do zapisania"}), 400
    
    new_simulation = SavedSimulation(
        user_id=current_user.id,
        name=sim_name,
        grid_state=current_user.game_state  # Przechowujemy w formacie JSON
    )
    
    db.session.add(new_simulation)
    db.session.commit()
    return jsonify({"success": True})

@app.route('/saved_simulations')
@login_required
def saved_simulations():
    simulations = SavedSimulation.query.filter_by(user_id=current_user.id).all()
    return render_template('saved_simulations.html', simulations=simulations)

@app.route('/load_simulation/<int:sim_id>')
@login_required
def load_simulation(sim_id):
    simulation = SavedSimulation.query.get_or_404(sim_id)
    
    if simulation.user_id != current_user.id:
        return redirect(url_for('saved_simulations'))

    # Wczytujemy planszę i zapisujemy do game_state
    current_user.game_state = simulation.grid_state
    db.session.commit()
    
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Tworzy tabele w bazie danych
    app.run(debug=True)
