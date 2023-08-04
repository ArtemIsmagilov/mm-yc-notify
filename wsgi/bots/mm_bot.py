from mattermostdriver import Driver


class MMBot(Driver):
    def __init__(self, options=None):
        super().__init__(options)

    def update_user_status_custom(self, user_id, options=None):
        return self.client.put(
            '/users/' + user_id + '/status/custom',
            options=options
        )

    def check_correct_access_token(self):
        self.login()
        self.logout()
