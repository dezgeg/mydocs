Feature: Have permissions
    As a team player
    I want to share my documents with others
    But outsiders should not see my documents

    Scenario: I can allow anonymous users to see my document
        Given I am logged in as "UserA"
        And I have the document "Totally public" containing "Hello all"
        When I visit the change permissions URL for "Totally public"
        And I set the anonymous user permissions to "Access"
        And I press "Save"
        When I log out
        And I visit the URL for "Totally public"
        Then I should see "Hello all"

    Scenario: I can make my document readable to my friend
        Given I am logged in as "UserA"
        And I have the document "ToMyFriend" containing "Hello"
        And "UserB" has the permission "Read" to "ToMyFriend"

        When I log in as "UserB"
        And I visit the URL for "ToMyFriend"
        Then I should see "Hello"
        But I should not see "Save"

    Scenario: I can make my document modifiable by my friend
        Given I am logged in as "UserA"
        And I have the document "ToMyFriend" containing "Hello"
        And "UserB" has the permission "Modify" to "ToMyFriend"

        When I log in as "UserB"
        And I visit the URL for "ToMyFriend"
        Then I should see "Hello"
        And I should not be able to change "Name"
        And I should see "Save"
        When I fill in "Content" with "Hallo"
        And I press "Save"
        Then the document "ToMyFriend" should contain "Hallo"

    Scenario: I can allow others to change document permissions
        Given I am logged in as "UserA"
        And I have the document "ToMany" containing "Hello all"
        And "UserB" has the permission "ChangePerms" to "ToMany"

        When I log in as "UserB"
        And I visit the change permissions URL for "ToMany"
        And I set "Email" for the permission #1 to "UserC@test.com"
        And I set "Permission" for the permission #1 to "Modify"
        And I press "Save"

        When I log in as "UserC"
        And I visit the URL for "ToMany"
        Then I should see "Hello all"
