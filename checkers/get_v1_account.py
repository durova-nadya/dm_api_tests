from datetime import datetime
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from assertpy import assert_that, soft_assertions
from clients.http.dm_api_account.models.user_details_envelope import UserRole


class GetV1Account:

    @classmethod
    def check_response_values(cls, response):
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to("AlisaLuu")
            assert_that(response.resource.online).is_instance_of(datetime)
            assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
        assert_that(
            response, all_of(
                has_property('resource', has_property('login', starts_with("Alisa"))),
                has_property('resource', has_property('registration', instance_of(datetime))),
                has_property(
                    'resource', has_properties(
                        {
                            'rating': has_properties(
                                {
                                    "enabled": equal_to(True),
                                    "quality": equal_to(0),
                                    "quantity": equal_to(0)
                                }
                            )
                        }
                    )
                )
            )
        )