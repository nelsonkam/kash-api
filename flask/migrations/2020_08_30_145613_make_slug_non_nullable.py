from orator.migrations import Migration


class MakeSlugNonNullable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            self.db.statement('ALTER TABLE products ALTER COLUMN slug SET NOT NULL;')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            table.string('slug').nullable().change()
