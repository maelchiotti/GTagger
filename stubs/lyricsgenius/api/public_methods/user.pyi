from _typeshed import Incomplete

class UserMethods:
    def user(self, user_id, text_format: Incomplete | None = ...): ...
    def user_accomplishments(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ...): ...
    def user_following(self, user_id, per_page: Incomplete | None = ..., page: Incomplete | None = ...): ...
    def user_followers(self, user_id, per_page: Incomplete | None = ..., page: Incomplete | None = ...): ...
    def user_contributions(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., sort: Incomplete | None = ..., text_format: Incomplete | None = ..., type_: Incomplete | None = ...): ...
    def user_annotations(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., sort: str = ..., text_format: Incomplete | None = ...): ...
    def user_articles(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., sort: str = ..., text_format: Incomplete | None = ...): ...
    def user_pyongs(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def user_questions_and_answers(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def user_suggestions(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., text_format: Incomplete | None = ...): ...
    def user_transcriptions(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., sort: str = ..., text_format: Incomplete | None = ...): ...
    def user_unreviewed(self, user_id, per_page: Incomplete | None = ..., next_cursor: Incomplete | None = ..., sort: str = ..., text_format: Incomplete | None = ...): ...