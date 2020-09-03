from orator.migrations import Migration


class CreateBannersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("banner"):
            with self.schema.create('banners') as table:
                table.big_increments('id')
                table.text("link")
                table.text("image_url")
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('banners')
