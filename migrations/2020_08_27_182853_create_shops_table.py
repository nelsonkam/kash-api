from orator.migrations import Migration


class CreateShopsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("shop"):
            with self.schema.create('shops') as table:
                table.increments('id')
                table.string("username").unique()
                table.string("name")
                table.string("whatsapp_number", 255)
                table.string("phone_number", 255)
                table.text("avatar_url").nullable()
                table.integer('user_id').unsigned()
                table.foreign('user_id').references('id').on('users').on_delete('cascade')
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('shops')
