from orator.migrations import Migration


class CreateCustomersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('customers') as table:
            table.big_increments('id')
            table.string('name')
            table.string('email').nullable().unique()
            table.string('phone_number').nullable().unique()
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('customers')
