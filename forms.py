from wtforms import Form, StringField, SelectField

class BookSearchForm(Form):
    choices = [('ISBN', 'ISBN'),
               ('Title', 'Title'),
               ('Author', 'Author')]
    select = SelectField("", choices=choices)
    search = StringField('')

class UserSearchForm(Form):
    choices = [('TCNO', 'TC Number'),
               ('FIRSTNAME', 'First Name'),
               ('LASTNAME', 'Last Name'),
               ('NUMOFBOOKS', 'Number of Borrowed Books')]
    select = SelectField("", choices=choices)
    search = StringField('')

class BorrowSearchForm(Form):
    choices = [('ISBN', 'ISBN'),
               ('TCNO', 'TC Number')]
    select = SelectField("", choices=choices)
    search = StringField('')
