Feature: Return user's full name
    Scenario: User exists
        Given the user exists on server
        When we request the user by id
        Then server returns 200
        And server returns JSON with full name of the user

    Scenario: User does not exist
        Given the user does not exist on server
        When we request the user by id
        Then server returns 404

    Scenario: Corrupted query
        When we send request with malformed query
        Then server returns 400
