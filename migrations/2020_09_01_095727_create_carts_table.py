from orator.migrations import Migration


class CreateCartsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('carts') as table:
            table.big_increments('id')
            table.string("uid", 40).unique()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('carts')
