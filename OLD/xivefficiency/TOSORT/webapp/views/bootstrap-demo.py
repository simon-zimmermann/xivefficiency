from enum import Enum
from flask import Blueprint, render_template, flash, redirect, url_for
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Regexp
from wtforms.fields import DateField, DateTimeField, DateTimeLocalField, TimeField, MonthField, ColorField, FloatField, IntegerField
from wtforms.fields import DecimalRangeField, IntegerRangeField, EmailField, URLField, TelField, FileField, RadioField, SelectField
from wtforms.fields import SelectMultipleField, TextAreaField, SearchField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import FieldList, FormField
from flask_bootstrap import SwitchField
# from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app

bp = Blueprint("bootstrap-demo", __name__, url_prefix="/bootstrap-demo")
# bp.secret_key = 'dev'

# bp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# bp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

# set default button sytle and size, will be overwritten by macro parameters
# bp.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
# bp.config['BOOTSTRAP_BTN_SIZE'] = 'sm'
#
# set default icon title of table actions
# bp.config['BOOTSTRAP_TABLE_VIEW_TITLE'] = 'Read'
# bp.config['BOOTSTRAP_TABLE_EDIT_TITLE'] = 'Update'
# bp.config['BOOTSTRAP_TABLE_DELETE_TITLE'] = 'Remove'
# bp.config['BOOTSTRAP_TABLE_NEW_TITLE'] = 'Create'

# bootstrap = Bootstrap5(bp)
# db = SQLAlchemy(bp)


class ExampleForm(FlaskForm):
    """An example form that contains all the supported bootstrap style form fields."""
    date = DateField(description="We'll never share your email with anyone else.")  # add help text with `description`
    datetime = DateTimeField(render_kw={'placeholder': 'this is a placeholder'})  # add HTML attribute with `render_kw`
    datetime_local = DateTimeLocalField()
    time = TimeField()
    month = MonthField()
    color = ColorField()
    floating = FloatField()
    integer = IntegerField()
    decimal_slider = DecimalRangeField()
    integer_slider = IntegerRangeField(render_kw={'min': '0', 'max': '4'})
    email = EmailField()
    url = URLField()
    telephone = TelField()
    image = FileField(render_kw={'class': 'my-class'}, validators=[Regexp(r'.+\.jpg$')])  # add your class
    option = RadioField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select = SelectField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    select_multiple = SelectMultipleField(
        choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('alien', 'Alien')])
    bio = TextAreaField()
    search = SearchField()  # will autocapitalize on mobile
    title = StringField()  # will not autocapitalize on mobile
    secret = PasswordField()
    remember = BooleanField('Remember me')
    submit = SubmitField()


class HelloForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 150)])
    remember = BooleanField('Remember me')
    submit = SubmitField()


class ButtonForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    confirm = SwitchField('Confirmation')
    submit = SubmitField()
    delete = SubmitField()
    cancel = SubmitField()


class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code')
    area_code = IntegerField('Area Code/Exchange')
    number = StringField('Number')


class IMForm(FlaskForm):
    protocol = SelectField(choices=[('aim', 'AIM'), ('msn', 'MSN')])
    username = StringField()


class ContactForm(FlaskForm):
    first_name = StringField()
    last_name = StringField()
    mobile_phone = FormField(TelephoneForm)
    office_phone = FormField(TelephoneForm)
    emails = FieldList(StringField("Email"), min_entries=3)
    im_accounts = FieldList(FormField(IMForm), min_entries=2)


class BootswatchForm(FlaskForm):
    """Form to test Bootswatch."""
    # DO NOT EDIT! Use list-bootswatch.py to generate the Radiofield below.
    theme_name = RadioField(
        default='default',
        choices=[
            ('default', 'none'),
            ('cerulean', 'Cerulean 5.3.1'),
            ('cosmo', 'Cosmo 5.3.1'),
            ('cyborg', 'Cyborg 5.3.1'),
            ('darkly', 'Darkly 5.3.1'),
            ('flatly', 'Flatly 5.3.1'),
            ('journal', 'Journal 5.3.1'),
            ('litera', 'Litera 5.3.1'),
            ('lumen', 'Lumen 5.3.1'),
            ('lux', 'Lux 5.3.1'),
            ('materia', 'Materia 5.3.1'),
            ('minty', 'Minty 5.3.1'),
            ('morph', 'Morph 5.3.1'),
            ('pulse', 'Pulse 5.3.1'),
            ('quartz', 'Quartz 5.3.1'),
            ('sandstone', 'Sandstone 5.3.1'),
            ('simplex', 'Simplex 5.3.1'),
            ('sketchy', 'Sketchy 5.3.1'),
            ('slate', 'Slate 5.3.1'),
            ('solar', 'Solar 5.3.1'),
            ('spacelab', 'Spacelab 5.3.1'),
            ('superhero', 'Superhero 5.3.1'),
            ('united', 'United 5.3.1'),
            ('vapor', 'Vapor 5.3.1'),
            ('yeti', 'Yeti 5.3.1'),
            ('zephyr', 'Zephyr 5.3.1'),
        ]
    )
    submit = SubmitField()


class MyCategory(Enum):
    CAT1 = 'Category 1'
    CAT2 = 'Category 2'


class Message:
    def __init__(self, id, text, author, category, draft, create_time):
        self.id = id
        self.text = text
        self.author = author
        self.category = category
        self.draft = draft
        self.create_time = create_time


messages = [
    Message(id=1, text='Test message 1', author='Author 1', category=MyCategory.CAT1, draft=False, create_time=1633021440),
    Message(id=2, text='Test message 2', author='Author 2', category=MyCategory.CAT2, draft=True, create_time=1633021500),
    Message(id=3, text='Test message 3', author='Author 3', category=MyCategory.CAT1, draft=False, create_time=1633021550),
    Message(id=4, text='Test message 4', author='Author 4', category=MyCategory.CAT2, draft=False, create_time=1633021600),
    Message(id=5, text='Test message 5', author='Author 5', category=MyCategory.CAT1, draft=True, create_time=1633021650),
]

# with bp.bp_context():
#    db.drop_all()
#    db.create_all()
#    for i in range(20):
#        url = 'mailto:x@t.me'
#        if i % 7 == 0:
#            url = 'www.t.me'
#        elif i % 7 == 1:
#            url = 'https://t.me'
#        elif i % 7 == 2:
#            url = 'http://t.me'
#        elif i % 7 == 3:
#            url = 'http://t'
#        elif i % 7 == 4:
#            url = 'http://'
#        elif i % 7 == 5:
#            url = 'x@t.me'
#        m = Message(
#            text=f'Message {i+1} {url}',
#            author=f'Author {i+1}',
#            create_time=4321*(i+1)
#            )
#        if i % 2:
#            m.category = MyCategory.CAT2
#        if i % 4:
#            m.draft = True
#        db.session.add(m)
#    db.session.commit()


@bp.route('/')
def index():
    return render_template('bootstrap-demo/index.html')


@bp.route('/form', methods=['GET', 'POST'])
def test_form():
    form = HelloForm()
    if form.validate_on_submit():
        flash('Form validated!')
        return redirect(url_for('bootstrap-demo.index'))
    return render_template(
        'bootstrap-demo/form.html',
        form=form,
        telephone_form=TelephoneForm(),
        contact_form=ContactForm(),
        im_form=IMForm(),
        button_form=ButtonForm(),
        example_form=ExampleForm()
    )


@bp.route('/nav', methods=['GET', 'POST'])
def test_nav():
    return render_template('bootstrap-demo/nav.html')


@bp.route('/bootswatch', methods=['GET', 'POST'])
def test_bootswatch():
    form = BootswatchForm()
    if form.validate_on_submit():
        if form.theme_name.data == 'default':
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = None
        else:
            app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = form.theme_name.data
        flash(f'Render style has been set to {form.theme_name.data}.')
    else:
        if app.config['BOOTSTRAP_BOOTSWATCH_THEME'] is not None:
            form.theme_name.data = bp.config['BOOTSTRAP_BOOTSWATCH_THEME']
    return render_template('bootstrap-demo/bootswatch.html', form=form)


@bp.route('/pagination', methods=['GET', 'POST'])
def test_pagination():
    # page = request.args.get('page', 1, type=int)
    # pagination = Message.query.paginate(page=page, per_page=10)
    # messages = pagination.items
    return render_template('bootstrap-demo/pagination.html', pagination=None, messages=messages)


@bp.route('/flash', methods=['GET', 'POST'])
def test_flash():
    flash('A simple default alert—check it out!')
    flash('A simple primary alert—check it out!', 'primary')
    flash('A simple secondary alert—check it out!', 'secondary')
    flash('A simple success alert—check it out!', 'success')
    flash('A simple danger alert—check it out!', 'danger')
    flash('A simple warning alert—check it out!', 'warning')
    flash('A simple info alert—check it out!', 'info')
    flash('A simple light alert—check it out!', 'light')
    flash('A simple dark alert—check it out!', 'dark')
    flash(Markup('A simple success alert with <a href="#" class="alert-link">an example link</a>. Give it a click if you like.'), 'success')
    return render_template('bootstrap-demo/flash.html')


@bp.route('/table')
def test_table():
    # page = request.args.get('page', 1, type=int)
    # pagination = Message.query.paginate(page=page, per_page=10)
    # messages = pagination.items
    titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'),
              ('category', 'Category'), ('draft', 'Draft'), ('create_time', 'Create Time')]
    data = []
    for msg in messages:
        data.append({'id': msg.id, 'text': msg.text, 'author': msg.author,
                   'category': msg.category, 'draft': msg.draft, 'create_time': msg.create_time})
    return render_template('bootstrap-demo/table.html', messages=messages, titles=titles, Message=Message, data=data)


@bp.route('/table/<int:message_id>/view')
def view_message(message_id):
    message = Message.query.get(message_id)
    if message:
        return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
    return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'


@bp.route('/table/<int:message_id>/edit')
def edit_message(message_id):
    message = messages[message_id]
    if message:
        message.draft = not message.draft
        # db.session.commit()
        return f'Message {message_id} has been editted by toggling draft status. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be edited. Return to <a href="/table">table</a>.'


@bp.route('/table/<int:message_id>/delete', methods=['POST'])
def delete_message(message_id):
    message = messages[message_id]
    if message:
        # db.session.delete(message)
        # db.session.commit()
        return f'Message {message_id} has been deleted. Return to <a href="/table">table</a>.'
    return f'Message {message_id} did not exist and could therefore not be deleted. Return to <a href="/table">table</a>.'


@bp.route('/table/<int:message_id>/like')
def like_message(message_id):
    return f'Liked the message {message_id}. Return to <a href="/table">table</a>.'


@bp.route('/table/new-message')
def new_message():
    return 'Here is the new message page. Return to <a href="/table">table</a>.'


@bp.route('/icon')
def test_icon():
    return render_template('bootstrap-demo/icon.html')


@bp.route('/icons')
def test_icons():
    return render_template('bootstrap-demo/icons.html')
