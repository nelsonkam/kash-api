from orator.migrations import Migration


class AddShippingOptionToCheckouts(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('checkouts') as table:
            table.json('shipping_option').nullable()

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('checkouts') as table:
            table.drop_column('shipping_option')
