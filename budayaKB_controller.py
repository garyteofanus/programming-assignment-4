from budayaKB_model import BudayaCollection
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, SubmitField, SelectField, FileField
from wtforms.validators import InputRequired, URL

# Set some required config for flask
app = Flask(__name__)
app.secret_key = "tp4"

# Initialize model object
databasefilename = ""
database = BudayaCollection()


class ImportForm(FlaskForm):
    """Form used for import function"""
    filename = FileField('File Name', validators=[FileRequired()], render_kw={'class': "file-input"})
    submit = SubmitField('Import Data', render_kw={'class': "button is-fullwidth is-hover is-primary "})


class EditForm(FlaskForm):
    """Form used for add and change function"""
    name = StringField('Name', validators=[InputRequired()], render_kw={'class': "input"})
    type = StringField('Type', validators=[InputRequired()], render_kw={'class': "input"})
    prov = StringField('Province', validators=[InputRequired()], render_kw={'class': "input"})
    url = StringField('Reference URL', validators=[InputRequired(), URL()], render_kw={'class': "input"})
    submit = SubmitField('Submit', render_kw={'class': "button is-fullwidth is-hover is-primary"})


class SearchForm(FlaskForm):
    """Form used for search function"""
    option = SelectField(choices=[('name', 'Name'), ('type', 'Type'), ('prov', 'Province')], validators=[InputRequired()], render_kw={'class': "input"})
    searched = StringField(validators=[InputRequired()], render_kw={'class': "input"})
    submit = SubmitField('Submit', render_kw={'class': "button is-hover is-primary"})


class DeleteForm(FlaskForm):
    """Form used for delete function"""
    deleted = StringField('Name', validators=[InputRequired()], render_kw={'class': "input"})
    submit = SubmitField('Delete', render_kw={'class': "button is-fullwidth is-hover is-danger", 'id': "confirmation"})


class StatisticsForm(FlaskForm):
    """Form used for statistics function"""
    shown = SelectField(choices=[('all', 'All'), ('type', 'Type'), ('prov', 'Province')], validators=[InputRequired()], render_kw={'class':'input'})
    submit = SubmitField('Show', render_kw={'class': 'button is-fullwidth is-hover is-primary'})


# Render out the default HTML, index.html
@app.route('/')
def index():
    return render_template("index.html")


# Implementation of import function
@app.route('/import.html', methods=['GET', 'POST'])
def import_data():
    import_form = ImportForm()
    if request.method == "GET":
        return render_template("import.html", form=import_form)
    elif request.method == "POST" and import_form.validate_on_submit():
        filename = import_form.filename.data
        database.importFromCSV(filename.filename)
        data = len(database.collection)
        return render_template("import.html", data=data, fname=filename.filename, form=import_form)


# Implementation of statistics
@app.route('/statistics.html', methods=['GET', 'POST'])
def statistics():
    statistics_form = StatisticsForm()
    if request.method == "GET":
        return render_template("statistics.html", form=statistics_form)
    elif request.method == "POST" and statistics_form.validate_on_submit():
        shown = statistics_form.shown.data
        total_type = len(database.statByType())
        total_prov = len(database.statByProv())
        if shown == "all":
            total = len(database.collection)
            return render_template("statistics.html", total=total, total_type=total_type, total_prov=total_prov, form=statistics_form)
        elif shown == 'type':
            stat_type = database.statByType()
            return render_template("statistics.html", type=stat_type,total_type=total_type, form=statistics_form)
        elif shown == 'prov':
            stat_prov = database.statByProv()
            return render_template("statistics.html", prov=stat_prov, total_prov=total_prov, form=statistics_form)


# Implementation of search function
@app.route('/search.html', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if request.method == "GET":
        return render_template('search.html', form=search_form)
    elif request.method == "POST" and search_form.validate_on_submit():
        option = search_form.option.data
        if option == "name":
            data = database.searchByName(search_form.searched.data)
            return render_template('search.html', form=search_form, data=data)
        elif option == "type":
            data = database.searchByType(search_form.searched.data)
            return render_template('search.html', form=search_form, data=data)
        elif option == "prov":
            data = database.searchByProv(search_form.searched.data)
            return render_template('search.html', form=search_form, data=data)


# Implementation of add function
@app.route('/add.html', methods=['GET', 'POST'])
def add():
    add_form = EditForm()
    if request.method == "GET":
        return render_template('add.html', form=add_form)
    elif request.method == "POST" and add_form.validate_on_submit():
        name = add_form.name.data
        type = add_form.type.data
        prov = add_form.prov.data
        url = add_form.url.data
        if database.add(name, type, prov, url) == 1:
            return render_template('add.html', name=name, form=add_form)
        else:
            return render_template('add.html', name=name, form=add_form, why="is found, cant make a duplicate object")


# Implementation of change function
@app.route('/change.html', methods=['GET', 'POST'])
def change():
    change_form = EditForm()
    if request.method == "GET":
        return render_template('change.html', form  =change_form)
    elif request.method == "POST" and change_form.validate_on_submit():
        name = change_form.name.data
        type = change_form.type.data
        prov = change_form.prov.data
        url = change_form.url.data
        if database.ubah(name, type, prov, url) == 1:
            return render_template('change.html', name=name, form=change_form)
        else:
            return render_template('change.html', name=name, form=change_form, why="is not found, cant change a null object")


# Implementation of delete function
@app.route('/delete.html', methods=['GET', 'POST'])
def delete():
    delete_form = DeleteForm()
    if request.method == "GET":
        return render_template('delete.html', form=delete_form)
    elif request.method == "POST" and delete_form.validate_on_submit():
        deleted = delete_form.deleted.data
        if database.delete(deleted) == 1:
            return render_template('delete.html', deleted=deleted, form=delete_form)
        else:
            return render_template('delete.html', deleted=deleted, why="is not found, can't delete a null object.", form=delete_form)


@app.route('/export.html', methods=['GET', 'POST'])
def export():
    if request.method == "GET":
        return render_template("export.html")
    if request.method == "POST":
        pass


# Run main app
if __name__ == "__main__":
    app.run(debug=True)
