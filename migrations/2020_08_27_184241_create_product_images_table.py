from orator.migrations import Migration


class CreateProductImagesTable(Migration):
    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("product_image"):
            with self.schema.create("product_images") as table:
                table.increments("id")
                table.text("url")
                table.integer("product_id").unsigned()
                table.foreign("product_id").references("id").on("products").on_delete(
                    "cascade"
                )
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop("product_images")
