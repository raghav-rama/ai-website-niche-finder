from flask_wtf import FlaskForm
from wtforms import StringField
from aboip1.views.inputs import Inputs


class InputForm(FlaskForm):
    from_row = StringField("From Row", default=Inputs.from_row)
    to_row = StringField("To Row", default=Inputs.to_row)
    batch_length = StringField("Batch Length", default=Inputs.batch_length)
    prompt_context = StringField("Prompt Context", default=Inputs.prompt_context)
    prompt_question = StringField("Prompt Question", default=Inputs.prompt_question)
