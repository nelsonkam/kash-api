from orator.migrations import Migration


class CreateProductsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("product"):
            with self.schema.create('products') as table:
                table.big_increments('id')
                table.string("name").nullable()
                table.integer("price")
                table.text("description").nullable()
                table.string("currency_iso", 10).default("XOF")
                table.big_integer('shop_id').unsigned()
                table.foreign('shop_id').references('id').on('shops').on_delete("cascade")
                table.big_integer('category_id').unsigned().nullable()
                table.foreign('category_id').references('id').on('categories').on_delete("cascade")
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('products')
