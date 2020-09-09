from orator.migrations import Migration


class MakeNameNullableOnUsers(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('users') as table:
            table.string('name').nullable().change()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('users') as table:
            self.db.statement('ALTER TABLE users ALTER COLUMN name SET NOT NULL;')
