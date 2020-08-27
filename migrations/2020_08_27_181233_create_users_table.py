from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        if not self.schema.has_table("user"):
            with self.schema.create('users') as table:
                table.increments('id')
                table.string("username").unique().nullable()
                table.string("name")
                table.string("phone_number").unique()
                table.text("avatar_url").nullable()
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
