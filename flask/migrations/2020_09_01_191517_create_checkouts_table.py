from orator.migrations import Migration


class CreateCheckoutsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('checkouts') as table:
            table.big_increments('id')
            table.big_integer("customer_id").unsigned()
            table.big_integer("cart_id").unsigned()
            table.foreign("customer_id").references("id").on("customers").on_delete("cascade")
            table.foreign("cart_id").references("id").on("carts").on_delete("cascade")
            table.string("country")
            table.string("city")
            table.text("address")
            table.string("uid", 40).unique()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('checkouts')
