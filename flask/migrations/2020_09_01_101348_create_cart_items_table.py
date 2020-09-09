from orator.migrations import Migration


class CreateCartItemsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('cart_items') as table:
            table.big_increments('id')
            table.integer("quantity")
            table.big_integer("cart_id").references("id").on("carts").on_delete("cascade")
            table.big_integer("product_id").references("id").on("products").on_delete("cascade")
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('cart_items')
