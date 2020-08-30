from orator.migrations import Migration


class AddSlugToProducts(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('products') as table:
            table.string("slug").unique().nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('products') as table:
            table.drop_column("slug")
