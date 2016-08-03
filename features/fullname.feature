Feature: Return user's full name
    Scenario: User exists
        Given the user exists on server
        When we request the user by id
        Then server returns HTTP status code 200
        And server returns JSON with full name of the user

    Scenario: User does not exist
        Given the user does not exist on server
        When we request the user by id
        Then server returns HTTP status code 404

    Scenario: Corrupted query
        When we send request with malformed query
        Then server returns HTTP status code 400

    Scenario: Not supported Accept
        When we send request with not supported Accept header
        Then server returns HTTP status code 415

    Scenario Outline: Bad id
        Given there are users on server
        When we send request with <id>
        Then server returns HTTP status code <code> 
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
        When we use not suppported HTTP method
        Then server returns HTTP status code 501

    Scenario: User without surname
        Given the user does not have surname
        When we request the user by id
        Then server returns HTTP status code 200
        And server returns JSON with empty surname of the user

    Scenario: No-no user
        Given there is not user on server
        When we request the user by id
        Then server returns HTTP status code 404
