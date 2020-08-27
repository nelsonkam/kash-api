from orator.migrations import Migration


class CreateCategoriesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("category"):
            with self.schema.create('categories') as table:
                table.increments('id')
                table.string("name").unique()
                table.text("slug").unique()
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('categories')
