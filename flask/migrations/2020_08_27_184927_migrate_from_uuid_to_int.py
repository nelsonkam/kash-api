from orator.migrations import Migration


class MigrateFromUuidToInt(Migration):

    def up(self):
        """
        Run the migrations.
        """
        tables = [
            "user",
            "shop",
            "product",
            "product_image",
            "category",
            "banner"
        ]
        pkeys = {
            'user': 'user_pkey',
            'shop': 'shop_pkey1',
            'product': 'product_pkey',
            'product_image': 'product_image_pkey',
            'category': 'category_pkey',
            'banner': 'banner_pkey'
        }
        new_names = {
            'user': 'users',
            'shop': 'shops',
            'product': 'products',
            'product_image': 'product_images',
            'category': 'categories',
            'banner': 'banners'
        }
        self.db.statement('DROP TABLE likes CASCADE')
        self.db.statement('DROP TABLE followings CASCADE')
        if self.schema.has_table("user"):
            for name in tables:
                with self.schema.table(name) as table:
                    self.db.statement(f'ALTER TABLE "{name}" DROP CONSTRAINT {pkeys[name]} CASCADE')

                with self.schema.table(name) as table:
                    table.big_increments("new_id")

            with self.schema.table("product_image") as table:
                table.big_integer("product_new_id").unsigned().default(0)

            with self.schema.table("product") as table:
                table.big_integer("shop_new_id").unsigned().default(0)
                table.big_integer("category_new_id").unsigned().nullable()

            with self.schema.table("shop") as table:
                table.big_integer("user_new_id").unsigned().default(0)

            self.db.statement(f"UPDATE product_image SET product_new_id = product.new_id FROM product WHERE product_image.product_id = product.id")
            self.db.statement(f"UPDATE product SET shop_new_id = shop.new_id FROM shop WHERE product.shop_id = shop.id")
            self.db.statement(f"UPDATE product SET category_new_id = category.new_id FROM category WHERE product.category_id = category.id")
            self.db.statement(f'UPDATE shop SET user_new_id = "user".new_id FROM "user" WHERE shop.user_id = "user".id')

            with self.schema.table("product_image") as table:
                table.drop_column("product_id")
                table.rename_column("product_new_id", "product_id")

            with self.schema.table("product") as table:
                table.drop_column("shop_id")
                table.rename_column("shop_new_id", "shop_id")
                table.drop_column("category_id")
                table.rename_column("category_new_id", "category_id")

            with self.schema.table("shop") as table:
                table.drop_column("user_id")
                table.rename_column("user_new_id", "user_id")

            for name in tables:
                with self.schema.table(name) as table:
                    table.drop_column("id")
                self.db.statement(f'ALTER TABLE "{name}" RENAME COLUMN "new_id" TO "id"')
                self.schema.rename(name, new_names[name])

            with self.schema.table("shops") as table:
                table.foreign('user_id').references('id').on('users').on_delete('cascade')

            with self.schema.table("products") as table:
                table.foreign('shop_id').references('id').on('shops').on_delete("cascade")
                table.foreign('category_id').references('id').on('categories').on_delete("cascade")

            with self.schema.table("product_images") as table:
                table.foreign("product_id").references("id").on("products").on_delete(
                    "cascade"
                )




    def down(self):
        """
        Revert the migrations.
        """
        pass
