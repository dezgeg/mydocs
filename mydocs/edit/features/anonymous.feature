Feature: Let anonymous users to see my documents
    As a document sharing guy
    I want to share my documents with random people

    Scenario: I can allow anonymous users to see my document
        Given I am logged in as "UserA"
        And I have the document "Totally public" containing "Hello all"
        When I visit the change permissions URL for "Totally public"
        And I set the anonymous user permissions to "Access"
        And I press "Save"
        When I log out
        And I visit the URL for "Totally public"
        Then I should see "Hello all"

    Scenario: Anonymous users' permissions apply to logged in users too
        Given I am logged in as "UserA"
        And I have the document "FreeForAll" containing "Hello"

        When I visit the change permissions URL for "FreeForAll"
        And I set the anonymous user permissions to "Modify"
        And I set "Email" for the permission #1 to "UserB@test.com"
        And I set "Permission" for the permission #1 to "Access"
        And I press "Save"

        When I log in as "UserB"
        And I visit the URL for "FreeForAll"
        When I change the content to "Hallo"
        And I press "Save"
        Then the document "FreeForAll" should contain "Hallo"
