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

    Scenario: Not supported Content-Type
        When we send request with not supported Content-Type
        Then server returns 415

    Scenario Outline: Bad id
        Given there are users on server
        When we send request with <id>
        Then server returns <code> 
        Examples: out of range
            | id   | code |
            | 0    | 404  |
            | -1   | 404  |
        Examples: not integer
            | id   | code |
            | 1.1  | 400  |
            | 1e-6 | 400  |
            | two  | 400  |


    Scenario: Not supported HTTP method
        # TODO
