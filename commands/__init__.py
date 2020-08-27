import click
from flask import Blueprint, render_template, flash, url_for, redirect

from app import db

blueprint = Blueprint("scripts", __name__, url_prefix="/scripts")

@blueprint.cli.command("schema")
@click.argument("table")
def schema(table):
    DB = db._db
    conn = DB.get_schema_manager().list_table_columns(table)
    docstring = '"""Model Definition \n\n'
    for name, column in conn.items():
        length = '({})'.format(column._length) if column._length else ''
        docstring += '{}: {}{} default: {} nullable: {} \n'.format(
            name, column.get_type(), length, column.get_default(), not column.get_notnull())

    print(docstring + '"""')
