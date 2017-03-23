Feature: Showing off behave

    Scenario: Check admin account
        Given user with login "admin"

        Then user role is "admin"

    Scenario: Check enable property can be changed
        Given user with login "john"
        When user enable changing
        Then user enable changed

    Scenario: User create and read
        Given random user create
        Given new user

        Then user must be the same
