from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class GuestbookEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nick = db.Column(db.String(50))
    text = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/aboutme')
def about_me():
    return render_template('aboutme.html')


@app.route('/gallery')
def gallery():
    return render_template('gallery.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/guestbook', methods=['GET', 'POST'])
def guestbook():
    if request.method == 'POST':
        nick = request.form['nick']
        text = request.form['text']
        new_entry = GuestbookEntry(nick=nick, text=text)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('guestbook'))
    entries = GuestbookEntry.query.order_by(GuestbookEntry.date_added.desc()).all()
    return render_template('guestbook.html', entries=entries)


@app.route('/guestbook/edit/<int:entry_id>', methods=['POST'])
def edit_entry(entry_id):
    entry = GuestbookEntry.query.get_or_404(entry_id)
    entry.nick = request.form['nick']
    entry.text = request.form['text']
    entry.date_added = datetime.now()  # Opcjonalnie aktualizacja daty edycji
    db.session.commit()
    return redirect(url_for('guestbook'))


@app.route('/guestbook/delete/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    entry = GuestbookEntry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    return redirect(url_for('guestbook'))


if __name__ == '__main__':
    app.run(debug=True)
