from orator.migrations import Migration


class CreatePhoneVerificationsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('phone_verifications') as table:
            table.increments('id')
            table.string('security_code')
            table.string('session_token')
            table.string('phone_number')
            table.boolean("is_verified").default(False)
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('phone_verifications')
